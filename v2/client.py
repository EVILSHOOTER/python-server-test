import socket, threading, pickle

SERVER = socket.gethostname()
PORT = 1337

HEADER_SIZE = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!GETOUT"

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

    # ALWAYS expect a message back, or else all the messages will queue up!
    #expectMessage()

expecting_messages = False
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
            # maybe add if statement checking what action this is, etc.
            if msg == DISCONNECT_MSG:
                expecting_messages = False


# use threading and make while loop to always await server messages
thread = threading.Thread(target=expectMessage)
thread.start()

def disconnect():
    send_to_server(DISCONNECT_MSG)

send_to_server(input())
disconnect()
