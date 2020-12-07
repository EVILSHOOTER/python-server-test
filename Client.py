import socket, threading, pickle, time

SERVER = socket.gethostname()
PORT = 2000 # this is the main lobby port.

HEADER_SIZE = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!GETOUT"
CREATESERVER_MSG = "!CREATESERVER"
JOINSERVER_MSG = "!JOINSERVER"
ENTERGAME_MSG = "!ENTERGAME"
GAMEQUESTION_MSG = "!ISGAME"

IN_GAME = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

# server - client stuff.
def send_to_server(msg):
    # second message - the data
    message = pickle.dumps(msg)
    # first message - the length
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_SIZE - len(send_len))

    sock.send(send_len)
    sock.send(message)

def expectMessage():
    expecting_messages = True
    while expecting_messages:
        # first message = length of message
        msg_len = sock.recv(HEADER_SIZE).decode(FORMAT)
        # second message = data
        if msg_len:
            msg_len = int(msg_len)
            msg = sock.recv(msg_len)
            #print(msg_len)
            #print(msg)
            msg = pickle.loads(msg)
            print(f"[SERVER]: {msg}") # test.

            # if statements here for all the actions u want!
            if DISCONNECT_MSG in msg:
                expecting_messages = False
                console("you've been disconnected.")
            # any other specific messages, send to another function.
            handleServerMessages(msg)

thread = threading.Thread(target=expectMessage) # start waiting for messages.
thread.start()

def disconnect():
    send_to_server(DISCONNECT_MSG)

def console(msg):
    print("[CLIENT]:", msg)

# game server functions.
def handleServerMessages(msg):
    if "[SERVER" in msg: # ignore reposts.
        return

    if JOINSERVER_MSG in msg: # end of server creation process.
        key = msg[len(JOINSERVER_MSG)+1:] # key received.
        console(f"you got the key: {key}")
        send_join_server_request(key)
    elif ENTERGAME_MSG in msg: # end of server join process
        game_port = msg[len(ENTERGAME_MSG)+1:]
        console(f"your server port is {game_port}")
        # v basically is starting the client afresh with a new connection really.
        threading.Thread(target=exchangeServer, args=(game_port,)).start()
    elif GAMEQUESTION_MSG in msg: # this is a game server.
        global IN_GAME
        IN_GAME = True
        console("you're in a game.")

def send_create_server_request():
    console("server creation asked. you should join it automatically.")
    send_to_server(CREATESERVER_MSG)
    # ask ServerManager to create server. have it return key to you.
    # the key is returned and joinServer() runs.

def send_join_server_request(key):
    console("attempt to join server. if nothing happens, server doesn't exist.")
    send_to_server(f"{JOINSERVER_MSG} {key}")
    # ask ServerManager to join server with given key. it returns to you the port.
    # you autojoin with that port.

def exchangeServer(new_port):
    disconnect()
    time.sleep(.1)  # let all messages return first.

    global IN_GAME
    IN_GAME = False

    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    console(f"attempt to join different server: {new_port}")
    connect_state = "connecting"
    try:
        sock.connect((SERVER, int(new_port)))
        connect_state = "connected"
    except: # cannot connect
        console(f"FAILED connecting to server: {new_port}")
        connect_state = "failed"

    if connect_state == "connected":
        # pass state.
        console("connected.")
        thread = threading.Thread(target=expectMessage)
        thread.start()

        time.sleep(.1) # let the thread start
        send_to_server(GAMEQUESTION_MSG) # is this a game?

    else: # return to lobby
        exchangeServer(PORT) # would this work if it's disconnecting from nothing?


# - your own code after here! -
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
        send_create_server_request()
    elif option == 2:
        print("joining server... ")
        send_join_server_request(input("enter the key for that server: "))
    else:
        print("invalid option - leaving lobby.")
        disconnect()

    time.sleep(3)

def game():
    text = input("type whatever u want: ")
    # if u type !backtolobby, it runs exchangeServer(2000)?
    if text == "!leave":
        exchangeServer(2000)
    else:
        send_to_server(text)

    time.sleep(3)

while True:
    try: #if server connection doesn't work, end loop
        send_to_server("test message")
    except:
        break
    if IN_GAME:
        game()
    else:
        lobby()


# honestly not proud of the use of time.sleep to wait for thread to die and messages to send.