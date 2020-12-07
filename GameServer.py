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
        self.keyLOCK = False

        # this runs start(), which halts anything below.
        super().__init__(server, port)

    def console(self, msg):
        # to make things cleaner, GameServer output are sent to clients.
        new_msg = (f"[SERVER-{self.PORT}]:", msg)
        print(new_msg)
        self.send_to_all_clients(new_msg)

    def returnPort(self):
        return self.PORT

    def returnKey(self):
        # now we don't want the key returned anymore, so prevent use of this func.
        if not self.keyLOCK:
            self.keyLOCK = True
            return self.KEY
        else:
            return "!NOKEY"

    def returnPlayers(self):
        return self.PLAYER_COUNT

    def returnMaxPlayers(self):
        return self.MAX_PLAYERS


# might the infrastructure dif on this one?
# have join and leave functions?
# send_to_game functions?
#