import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except ConnectionClosedOK:
            break
        print(message)


async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send("YARRR ME MAITEE")


async def main():
    async with serve(echo, "", 8765) as server:
        await server.serve_forever()


asyncio.run(main())
