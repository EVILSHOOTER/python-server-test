import socket, threading, pickle, time

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
            #threading.Thread(target=handleServerMessages, args=(msg,)).start() # no halts.

# use threading and make while loop to always await server messages
thread = threading.Thread(target=expectMessage)
thread.start()

def disconnect():
    send_to_server(DISCONNECT_MSG)

def console(msg):
    print("[CLIENT]:", msg)

# game server functions.
def handleServerMessages(msg):
    if JOINSERVER_MSG in msg: # end of server creation process.
        key = msg[len(JOINSERVER_MSG)+1:] # key received.
        console(f"you got the key: {key}")
        send_join_server_request(key)
    elif ENTERGAME_MSG in msg: # end of server join process
        game_port = msg[len(ENTERGAME_MSG)+1:]
        console(f"your server port is {game_port}")
        #attemptToJoinGame(game_port) # thread this? because it basically starts anew.
        threading.Thread(target=attemptToJoinGame, args=(game_port,)).start()

def send_create_server_request():
    send_to_server(CREATESERVER_MSG)
    # ask ServerManager to create server. have it return key to you.
    # the key is returned and joinServer() runs.

def send_join_server_request(key):
    send_to_server(f"{JOINSERVER_MSG} {key}")
    # ask ServerManager to join server with given key. it returns to you the port.
    # you autojoin with that port.

def attemptToJoinGame(game_port):
    disconnect()
    time.sleep(1)  # let all messages return first.

    global PORT
    global sock
    PORT = int(game_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    console(f"attempt to join different server: {game_port}")
    sock.connect((SERVER, PORT))
    console("connected.")
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
    disconnect()

#disconnect()
