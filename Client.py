import socket, threading, pickle, time

class Client:
    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port # this is the main lobby port.

        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"
        self.CREATESERVER_MSG = "!CREATESERVER"
        self.JOINSERVER_MSG = "!JOINSERVER"
        self.ENTERGAME_MSG = "!ENTERGAME"
        self.GAMEQUESTION_MSG = "!ISGAME"

        self.IN_GAME = False
        self.connected = False
        self.sock = None

        self.exchangeServer(self.PORT)  # basically a start() function

    # server - client stuff.
    def send_to_server(self, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        self.sock.send(send_len)
        self.sock.send(message)

    def expectMessage(self):
        self.connected = True
        while self.connected:
            # first message = length of message
            msg_len = self.sock.recv(self.HEADER_SIZE).decode(self.FORMAT)
            # second message = data
            if msg_len:
                msg_len = int(msg_len)
                msg = self.sock.recv(msg_len)
                #print(msg_len)
                #print(msg)
                msg = pickle.loads(msg)
                print(f"[SERVER]: {msg}") # test.

                # if statements here for all the actions u want!
                if self.DISCONNECT_MSG in msg:
                    self.connected = False
                    self.console("you've been disconnected.")
                # any other specific messages, send to another function.
                self.handleServerMessages(msg)

    def disconnect(self):
        self.send_to_server(self.DISCONNECT_MSG)

    def console(self, msg):
        print("[CLIENT]:", msg)

    # game server functions.
    def handleServerMessages(self, msg):
        if "[SERVER" in msg: # ignore reposts.
            return

        if self.JOINSERVER_MSG in msg: # end of server creation process.
            key = msg[len(self.JOINSERVER_MSG)+1:] # key received.
            self.console(f"you got the key: {key}")
            self.send_join_server_request(key)
        elif self.ENTERGAME_MSG in msg: # end of server join process
            game_port = msg[len(self.ENTERGAME_MSG)+1:]
            self.console(f"your server port is {game_port}")
            # v basically is starting the client afresh with a new connection really.
            threading.Thread(target=self.exchangeServer, args=(game_port,)).start()
        elif self.GAMEQUESTION_MSG in msg: # this is a game server.
            self.IN_GAME = True
            self.console("you're in a game.")

    def send_create_server_request(self):
        self.console("server creation asked. you should join it automatically.")
        self.send_to_server(self.CREATESERVER_MSG)
        # ask ServerManager to create server. have it return key to you.
        # the key is returned and joinServer() runs.

    def send_join_server_request(self, key):
        self.console("attempt to join server. if nothing happens, server doesn't exist.")
        self.send_to_server(f"{self.JOINSERVER_MSG} {key}")
        # ask ServerManager to join server with given key. it returns to you the port.
        # you autojoin with that port.

    def exchangeServer(self, new_port):
        if self.connected:
            self.disconnect()
            # ima keep for now, cuz of weird python message bug when u print after thread
            while self.connected:
                time.sleep(.01)  # wait for the disconnect message from server.


        self.IN_GAME = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.console(f"attempt to join server: {new_port}")
        connect_state = "connecting"
        try:
            self.sock.connect((self.SERVER, int(new_port)))
            connect_state = "connected"
        except: # cannot connect
            self.console(f"FAILED connecting to server: {new_port}")
            connect_state = "failed"

        if connect_state == "connected":
            # pass state.
            self.console("connected.")
            thread = threading.Thread(target=self.expectMessage)
            thread.start()

            time.sleep(0.5)

            self.send_to_server(self.GAMEQUESTION_MSG) # is this a game?

        else: # return to lobby
            self.exchangeServer(self.PORT) # would this work if it's disconnecting from nothing?


# - your own code after here! -
client = Client(socket.gethostname(), 2000)

# i'm doing a basic menu to showcase entering and leaving the server via ServerManager
def choiceMaker(options):
    print(f"You have {len(options)} options:")
    i = 0
    for o in options:
        i += 1
        print(f"\t{i}. {o}")
    option = input("enter your option: ")
    try:
        option = int(option)
    except:
        option = 0
    return option

def lobby():
    option = choiceMaker(["Create a server", "Join a server"])

    if option == 1:
        print("creating server...")
        client.send_create_server_request()
    elif option == 2:
        print("joining server... ")
        client.send_join_server_request(input("enter the key for that server: "))
    else:
        print("invalid option - leaving lobby.")
        client.disconnect()

    time.sleep(3)

def game():
    text = input("type whatever u want: ")
    # if u type !backtolobby, it runs exchangeServer(2000)?
    if text == "!leave":
        client.exchangeServer(client.PORT)
    else:
        client.send_to_server(text)

    time.sleep(3)

while client.connected:
    if client.IN_GAME:
        game()
    else:
        lobby()

# honestly not proud of the use of time.sleep to wait for thread to die and messages to send.