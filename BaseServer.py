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
        self.ENTERGAME_MSG = "!ENTERGAME"

        self.all_connections = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.SERVER, self.PORT))

        #self.start()
        t = threading.Thread(target=self.start, args=()) # nice.
        t.start()

    def console(self, msg): # easier output. overridable too.
        print(f"[SERVER-{self.PORT}]:", msg)

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
        pass

    # handles individual connections
    def handle_client(self, connection, address):
        self.console(f"new connection = {address}")

        counter = 0 # just for test purposes. counts individual total of client msgs.
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
                    self.console(f"[{address}] said: {msg}")

                    if msg == self.DISCONNECT_MSG:
                        connected = False
                        self.send_to_client(connection, self.DISCONNECT_MSG)
                        self.console(f"[{address}] has disconnected")
                    # handle any other messages.
                    self.handleClientMessages(connection, address, msg)

                    counter += 1
                    self.send_to_client(connection, f"msg received ({counter})")
            #except:
            #    connected = False
            #    print(f"[SERVER]: Client message error. Connection cut with {address} -")
            #    self.console(f"Client message error. Connection cut with {address}")

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
        self.sock.listen()
        self.console(f"Hello world! Listening on {self.SERVER}.")
        while True:
            connection, address = self.sock.accept()
            self.all_connections.append(connection)
            thread = threading.Thread(target=self.handle_client
                                      , args=(connection, address))
            thread.start()
            # -2 on active thread count because: main thread, start() thread. was -1 tho.
            self.console(f"active connections = {threading.active_count()-2}")
            self.send_to_all_clients(None) # clean-up all_connections

#s = Server(socket.gethostname(), 6969)
# above is more or less the base server script, but in OOP form.
#