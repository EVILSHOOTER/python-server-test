import socket, threading, pickle
from BaseServer import Server
from GameServer import GameServer

class ServerManager(Server):
    def __init__(self, server, port):
        self.SERVERS = {}
        self.SERVER_COUNTER = 0
        self.s = None # for server creation...

        #this runs start(), which halts anything below.
        super().__init__(server, port)

    def createServer(self, connection, address):
        self.console(f"[{address}] wants to create a server")
        # create server object. get its key. server should have a STATUS var tbh.
        self.SERVER_COUNTER += 1
        s = GameServer(self.SERVER, self.PORT+self.SERVER_COUNTER) # this halts. how not?
        k = s.returnKey()
        # self.SERVERS.append(s)
        self.SERVERS[k] = s
        # return key to client.
        self.send_to_client(connection, f"{self.JOINSERVER_MSG} {k}")
        # client gets key, and performs join function by themselves automatically.

    def joinServer(self, connection, address, msg):
        key = msg[len(self.JOINSERVER_MSG) + 1:]
        self.console(f"[{address}] wants to join ({key})")

        if key in self.SERVERS:
            game_port = self.SERVERS[key].returnPort()
            self.console(f"SERVER FOUND FOR PLAYER: {game_port}")
            # hand player the port. now they try to go there themselves.
            self.send_to_client(connection, f"{self.ENTERGAME_MSG} {game_port}")
        else:
            self.console(f"server NOT found for player: {key}")

    # any other specific messages. this overrides the parent one.
    def handleClientMessages(self, connection, address, msg):
        #print("serverManager client message handling. ")
        if self.CREATESERVER_MSG in msg:
            self.createServer(connection, address)
        elif self.JOINSERVER_MSG in msg:
            self.joinServer(connection, address, msg)

# - your code after here! -
s = ServerManager(socket.gethostname(), 2000)
#