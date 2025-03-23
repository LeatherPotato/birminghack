import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import time

CLIENTS = set()
game_alive = True

async def game(websocket):
    while game_alive:
        try:
            print("hi this is looping...")
            await websocket.send("yar?")
            print("not getting shit...")
            response = await websocket.recv()
        except ConnectionClosed:
            break

        print(response)


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            await game(websocket)
        except ConnectionClosed:
            break
            print("removing client")
            CLIENTS.remove(websocket)
        print(message)


async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send("YARRR ME MAITEE")


async def main():
    async with serve(handler, "", 8765) as server:
        await server.serve_forever()


asyncio.run(main())
