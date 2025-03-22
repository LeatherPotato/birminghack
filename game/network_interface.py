class NetworkInterface:
    def __init__(self):
        ...
        #init some stuff here or smth 

    def create_lobby(self):
        # creates new lobby
        code = 0
        return code

    def join_existing_lobby(self, code):
        # for a player to join another's lobby'
        ...

    def opponent_joined_lobby(self, opponent):
        # is called when an opponent joins the player's lobby'
        ...

    def send_rap(self):
        # is called when the player enters their rap
        # will return damage dealt to opponent and status effects to update opponent gamestate
        ...

    def recieved_rap(self):
        # called when an opponent rap is recieved
        # will return rap and the damage taken from the rap and any status effects
        ...

    def player_defeated(self):
        # called when the player is defeated 
        ...
    
    def opponent_defeated(self):
        # is called when the opponent is defeated
        ...
