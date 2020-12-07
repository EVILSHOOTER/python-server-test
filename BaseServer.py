import socket, threading, pickle

import abc #force handle messages to be made.

class Server:

    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port

        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"
        self.CREATESERVER_MSG = "!CREATESERVER"
        self.JOINSERVER_MSG = "!JOINSERVER"
        self.JOININGGAME_MSG = "!JOININGGAME"

        self.all_connections = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.SERVER, self.PORT))

        #self.start()
        t = threading.Thread(target=self.start, args=()) # nice.
        t.start()

    def send_to_client(self, connection, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        connection.send(send_len)
        connection.send(message)

    # any other specific messages. overriden by children.
    def handleClientMessages(self, connection, address, msg):
        #raise NotImplementedError("Must be overriden")
        print("base server!!")

    # handles individual connections
    def handle_client(self, connection, address):
        print(f"[SERVER-{self.PORT}]: new connection = {address}")

        counter = 0 # just test purposes. count of all msgs senT back.
        connected = True
        while connected:
            #try: # capture client disconnecting prematurely.
                # first message = length of message
                msg_len = connection.recv(self.HEADER_SIZE).decode(self.FORMAT)
                # second message = data
                if msg_len:
                    msg_len = int(msg_len)
                    msg = connection.recv(msg_len)
                    msg = pickle.loads(msg)
                    print(f"[{address}]: {msg}")

                    if msg == self.DISCONNECT_MSG:
                        connected = False
                        self.send_to_client(connection, self.DISCONNECT_MSG)
                        print(f"[{address}] has disconnected")
                    # handle any other messages.
                    self.handleClientMessages(connection, address, msg)

                    counter += 1
                    self.send_to_client(connection, f"msg received ({counter})")
            #except:
            #    connected = False
            #    print(f"[SERVER]: Client message error. Connection cut with {address} -")

        connection.close()

    def send_to_all_clients(self, msg): # e.g. useful for ticks.
        for con in self.all_connections:
            # if connection exists, send. if not, delete it.
            if con.fileno() == -1:
                self.all_connections.remove(con)
            else:
                if msg != None: # useful just to clean up all_connections
                    self.send_to_client(con, msg)

    # handles new connections
    def start(self):
        print(f"[SERVER-{self.PORT}]: Hello world!")
        self.sock.listen()
        print(f"[SERVER-{self.PORT}]: listening on {self.SERVER}.")
        while True:
            connection, address = self.sock.accept()
            self.all_connections.append(connection)
            thread = threading.Thread(target=self.handle_client
                                      , args=(connection, address))
            thread.start()
            print(f"[SERVER-{self.PORT}]: active connections = {threading.active_count()-1}")
            self.send_to_all_clients(None) # clean-up all_connections

#s = Server(socket.gethostname(), 6969)
# above is more or less the base server script, but in OOP form.