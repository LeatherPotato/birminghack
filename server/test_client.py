from websockets.sync.client import connect


def hello():
    with connect("ws://172.22.236.99:8765") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")


hello()
