import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import json
import random
from calculate_damage import calc_damage


active_games = {}


class Game:
    def __init__(self, p1_socket, p1_attributes):
        self.p1_socket = p1_socket
        self.p1_attributes = p1_attributes
        self.p1_rap = []
        self.p2_rap = []
        self.p1_damage = 0
        self.p2_damage = 0
        self.raps_submitted=0

    def register_player_2(self, p2_socket, p2_attributes):
        self.p2_socket = p2_socket
        self.p2_attributes = p2_attributes


async def create_lobby(websocket, attributes):
    code = random.randint(1000, 9999)
    while str(code) in active_games.keys():
        code = random.randint(1000, 9999)
    active_games[str(code)] = Game(websocket, attributes)
    print(json.dumps({"code": code}))
    print(active_games)
    await websocket.send(json.dumps({"code": code}))


async def join_lobby(websocket, data):
    code = data["code"]
    attributes = data["attributes"]
    active_games[str(code)].register_player_2(websocket, attributes)
    await websocket.send({"opponent_attributes": active_games[str(code)].p1_attributes})
    await active_games[str(code)].p1_socket.send({"opponent_attributes": active_games[str(code)].p2_attributes})


async def submit_rap(websocket, data):
    code = data["code"]
    player = int(data["player"])
    if player==1:
        damage = calc_damage(data["rap"], active_games[str(code)].p2_attributes["strength"], active_games[str(code)].p2_attributes["weakness"], active_games[str(code)].p2_attributes["defence"], active_games[str(code)].p1_attributes["lethality"])
        active_games[str(code)].p2_attributes["health"] -= damage
    elif player==2:
        damage = calc_damage(data["rap"], active_games[str(code)].p1_attributes["strength"], active_games[str(code)].p1_attributes["weakness"], active_games[str(code)].p1_attributes["defence"], active_games[str(code)].p2_attributes["lethality"])
        active_games[str(code)].p1_attributes["health"] -= damage
         

    active_games[str(code)].raps_submitted+=1

    if active_games[str(code)].raps_submitted%2==0:
        await active_games[str(code)].p1_socket.send({"opponent_rap": active_games[str(code)].p2_rap, "opponent_damage": active_games[str(code)].p2_damage, "your_damage": active_games[str(code)].p1_damage})
        await active_games[str(code)].p2_socket.send({"opponent_rap": active_games[str(code)].p1_rap, "opponent_damage": active_games[str(code)].p1_damage, "your_damage": active_games[str(code)].p2_damage})


async def handler(websocket):
    while True:
        try:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)
            match data["request_type"]:
                case "CREATE_LOBBY":
                    print("creating lobby")
                    await create_lobby(websocket, data["data"])
                    break

                case "JOIN_LOBBY":
                    print("joining lobby")
                    await join_lobby(websocket, data["data"])
                    break

                case "SUBMIT_RAP":
                    print("submitting rap")
                    await submit_rap(websocket, data["data"])

        except ConnectionClosed:
            break


async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send("YARRR ME MAITEE")


async def main():
    async with serve(handler, "", 8765) as server:
        await server.serve_forever()


asyncio.run(main())
