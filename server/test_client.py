from websockets.sync.client import connect

uri = "ws://localhost:8765"
with connect(uri) as websocket:
    name = input("What's your name? ")

    websocket.send(name)
    print(f">>> {name}")

    greeting = websocket.recv()
    print(f"<<< {greeting}")

    while True:
        s = input()
        if s == "q":
            websocket.send(s)
            break

    greeting = websocket.recv()
    print(f"<<< {greeting}")


