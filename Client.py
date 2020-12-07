import socket, threading, pickle

SERVER = socket.gethostname()
PORT = 2000

HEADER_SIZE = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!GETOUT"
CREATESERVER_MSG = "!CREATESERVER"
JOINSERVER_MSG = "!JOINSERVER"
JOININGGAME_MSG = "!JOININGGAME"

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


def joinGame(key):
    #send_to_server()
    # ask server if full.
    #
    pass

def handleServerMessages(msg):
    if JOINSERVER_MSG in msg:
        key = msg[len(JOINSERVER_MSG)+1:]
        print("you got the key:", key)
        # perform join function.

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
            print(f"[SERVER]: {msg}")

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

def createServer():
    # ask ServerManager to create server. have it return key to you.
    send_to_server(CREATESERVER_MSG)
    # perform joinServer()
    pass

def joinServer(key):
    # ask ServerManager to join server with given key. it returns to you that u joined
    send_to_server(f"{JOINSERVER_MSG} {key}")
    pass

if option == 1:
    print("creating server...")
    createServer()
elif option == 2:
    print("joining server... ")
    joinServer(input("enter the key for that server: "))
else:
    print("invalid option")

disconnect()
