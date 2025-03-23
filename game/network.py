from websockets.sync.client import connect
import json


class Network:
    def __init__(self):
        self.SERVER = "ws://172.22.236.99:8765"

    def _request_sender(self, req_type, data):
        try:
            with connect(self.SERVER) as websocket:
                websocket.send(json.dumps({"request_type": req_type, "data": data}))
                response = websocket.recv()
            return json.load(response)
        except:
            return {"response_type": "ERROR", "data": {"error_type": "unable to connect to server"}}

    def create_lobby(self, playerInfo):
        response = self._request_sender(self, "CREATE_LOBBY", playerInfo)

        if response["response_type"] == "ERROR":
            return -1
        else:
            return response["data"]["room_code"]
        
    def join_lobby(self, playerInfo, code):
        respone = self._request_sender(self, "JOIN_LOBBY", {"code": code, "player_info": playerInfo})
        
        if response["response_type"] == "ERROR":
            return -1
        else:
            return response["data"]["opponent_info"]

    def _opponent_joined_lobby():
        ...

net = Network()


