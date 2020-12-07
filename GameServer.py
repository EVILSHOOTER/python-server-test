import socket, threading, pickle
import random, string
from BaseServer import Server

class GameServer(Server):
    def __init__(self, server, port):
        self.STATUS = "running"

        newKey = ""
        for i in range(6):
            newKey += random.choice(string.digits + string.ascii_uppercase)
        #print(newKey)

        self.KEY = newKey
        self.keyLOCK = False

        # this runs start(), which halts anything below.
        super().__init__(server, port)

    def returnPort(self):
        return self.PORT

    def returnKey(self):
        # now we don't want the key returned anymore, so prevent use of this func.
        if not self.keyLOCK:
            self.keyLOCK = True
            return self.KEY
        else:
            return "!NOKEY"


# might the infrastructure dif on this one?
# have join and leave functions?
# send_to_game functions?