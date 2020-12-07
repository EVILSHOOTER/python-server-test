import socket, threading, pickle

SERVER = socket.gethostname()
PORT = 0 # this will change for individual game servers

LOBBY_PORT = 2000
PORT = LOBBY_PORT

HEADER_SIZE = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!GETOUT"
CREATESERVER_MSG = "!CREATESERVER"
JOINSERVER_MSG = "!JOINSERVER"
ENTERGAME_MSG = "!ENTERGAME"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

def send_to_server(msg):
    # second message - the data
    message = pickle.dumps(msg)
    # first message - the length
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_SIZE - len(send_len))

    sock.send(send_len)
    sock.send(message)


def handleServerMessages(msg):
    if JOINSERVER_MSG in msg: # end of server creation process.
        key = msg[len(JOINSERVER_MSG)+1:] # key received.
        print("you got the key:", key)
        send_join_server_request(key)
    elif ENTERGAME_MSG in msg: # end of server join process
        game_port = msg[len(ENTERGAME_MSG)+1:]
        print("your server port is ", game_port)
        attemptToJoinGame(game_port)

def expectMessage():
    expecting_messages = True
    while expecting_messages:
        # first message = length of message
        msg_len = sock.recv(HEADER_SIZE).decode(FORMAT)
        # second message = data
        if msg_len:
            msg_len = int(msg_len)
            msg = sock.recv(msg_len)
            msg = pickle.loads(msg)
            print(f"[SERVER]: {msg}") # test.

            # if statements here for all the actions u want!
            if msg == DISCONNECT_MSG:
                expecting_messages = False
                print("you've been disconnected.")
            # any other specific messages, send to another function.
            handleServerMessages(msg)

# use threading and make while loop to always await server messages
thread = threading.Thread(target=expectMessage)
thread.start()

def disconnect():
    send_to_server(DISCONNECT_MSG)


# game server functions.
def send_create_server_request():
    # ask ServerManager to create server. have it return key to you.
    print("asking server to create me a server...")
    send_to_server(CREATESERVER_MSG)
    # the key is returned and joinServer() runs.

def send_join_server_request(key):
    # ask ServerManager to join server with given key. it returns to you that u joined
    print("asking server to join...")
    # to server: !JOINSERVER *key*
    send_to_server(f"{JOINSERVER_MSG} {key}")
    # to client: !SERVERPORT *port*
    # client: disconnect from ServerManager. try: connect to port.
    # also client: if message received: fail, full or non-existent, return to GameManager.

    # when in-game, set a variable for IN_GAME to true, so disconnect to lobby safely l8r.

def attemptToJoinGame(game_port):
    disconnect()

    global PORT
    global sock
    PORT = int(game_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("attempt to join game server",game_port)
    sock.connect((SERVER, PORT))
    thread = threading.Thread(target=expectMessage)
    thread.start()

    while True: # test
        send_to_server(input())

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

option = choiceMaker(["Create a server", "Join a server"])

if option == 1:
    print("creating server...")
    send_create_server_request()
elif option == 2:
    print("joining server... ")
    send_join_server_request(input("enter the key for that server: "))
else:
    print("invalid option")

#disconnect()
#
