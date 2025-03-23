import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import json
import random


active_games = {}


class Game:
    def __init__(self, p1_socket, p1_attributes):
        self.p1_socket = p1_socket
        self.p1_attributes = p1_attributes

    def register_player_2(self, p2_socket, p2_attributes):
        self.p2_socket = p2_socket
        self.p2_attributes = p2_attributes


async def create_lobby(websocket, attributes):
    code = random.randint(1000, 9999)
    while str(code) in active_games.keys():
        code = random.randint(1000, 9999)
    active_games[str(code)] = Game(websocket, attributes)
    await websocket.send(json.dumps({"code": code}))


async def join_lobby(websocket, data):
    code = data["code"]
    attributes = data["attributes"]
    active_games[str(code)].register_player_2(websocket, attributes)
    await websocket.send({"opponent_attributes": active_games[str(code)].p1_attributes})
    await active_games[str(code)].p1_socket.send({"opponent_attributes": active_games[str(code)].p1_attributes})


async def handler(websocket):
    while True:
        try:
            data = await websocket.recv()
            data = json.dump(data)
            match data["request_type"]:
                case "CREATE_LOBBY":
                    await create_lobby(websocket, data["data"])

                case "JOIN_LOBBY":
                    await join_lobby(websocket, data["data"])

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
