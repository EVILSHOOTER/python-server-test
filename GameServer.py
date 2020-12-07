import socket, threading, pickle
import random, string
from BaseServer import Server

class GameServer(Server):
    def __init__(self, server, port):
        self.STATUS = "running"
        self.PLAYER_COUNT = 0
        self.MAX_PLAYERS = 2

        newKey = ""
        for i in range(6):
            newKey += random.choice(string.digits + string.ascii_uppercase)
        #print(newKey)
        self.KEY = newKey

        # this runs start(), which halts anything below.
        super().__init__(server, port)

    #
    def handleClientMessages(self, connection, address, msg):
        if self.GAMEQUESTION_MSG in msg:
            self.send_to_client(connection, self.GAMEQUESTION_MSG)

    def console(self, msg):
        new_msg = (f"[SERVER-{self.PORT}]: {msg}")
        # inspiration for future: send tuples for objects. e.g. (f"[SERVER-{self.PORT}]:", msg)
        #print(new_msg)
        # to make things cleaner, GameServer output are sent to clients.
        self.send_to_all_clients(new_msg)

    # return functions.
    def returnPort(self):
        return self.PORT

    def returnKey(self):
        # used to be one time use, but realised that only the server can use this
        return self.KEY

    def returnPlayers(self):
        return self.PLAYER_COUNT

    def returnMaxPlayers(self):
        return self.MAX_PLAYERS


# might the infrastructure dif on this one?
# have join and leave functions?
# send_to_game functions?
# if game is full, act as spectator? kick player out?