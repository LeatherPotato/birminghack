from websockets.sync.client import connect
import json
import asyncio


class Network:
    def __init__(self, websocket):
        # self.SERVER = "ws://172.22.236.99:8765"
        self.websocket = websocket

    def request_sender(self, req_type, data):
        print("sending request...")
        try:
            print("sending request 2...")
            self.websocket.send(json.dumps({"request_type": req_type, "data": data}))
            print("sending request 3...")
            response = self.websocket.recv()
            print("sending request 4...")
            print(response)
            return json.loads(response)
        except Exception as e:
            print(e)

    def create_lobby(self, playerInfo):
        print("started creating lobby")
        response = self.request_sender("CREATE_LOBBY", playerInfo)
        print("got response from request builder")
        return response.get("code")
    

    def join_lobby(self, playerInfo, code):
        response = self.request_sender("JOIN_LOBBY", {"code": code, "player_info": playerInfo})
        
        if response["response_type"] == "ERROR":
            return -1
        else:
            return response["opponent_info"]
        
    
    def submit_rap(self, code, player, rap):
        response = self.request_sender("SUBMIT_RAP", {"code": code, "player": player, "rap": rap})
        return response
     