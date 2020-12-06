import socket, threading, pickle

SERVER = socket.gethostname()
PORT = 1337

HEADER_SIZE = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!GETOUT"

all_connections = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER, PORT))

def send_to_client(connection, msg):
    # second message - the data
    message = pickle.dumps(msg)
    # first message - the length
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_SIZE - len(send_len))

    connection.send(send_len)
    connection.send(message)

# handles individual connections
def handle_client(connection, address):
    print(f"[SERVER]: new connection = {address}")

    counter = 0 # just test purposes. count of all msgs senT back.
    connected = True
    while connected:
        try: # capture client disconnecting prematurely.
            # first message = length of message
            msg_len = connection.recv(HEADER_SIZE).decode(FORMAT)
            # second message = data
            if msg_len:
                msg_len = int(msg_len)
                msg = connection.recv(msg_len)
                msg = pickle.loads(msg)
                if msg == DISCONNECT_MSG:
                    connected = False
                    send_to_client(connection, DISCONNECT_MSG)
                    print(f"[{address}] has disconnected")
                print(f"[{address}]: {msg}")

                counter += 1
                send_to_client(connection, f"msg received ({counter})")
        except:
            connected = False
            print(f"[SERVER]: Client message error. Connection cut with {address} -")

    connection.close()

def send_to_all_clients(msg): # e.g. useful for ticks.
    for con in all_connections:
        # if connection exists, send. if not, delete it.
        if con.fileno() == -1:
            all_connections.remove(con)
        else:
            if msg != None: # useful just to clean up all_connections
                send_to_client(con, msg)

# handles new connections
def start():
    print("[SERVER]: Hello world!")
    sock.listen()
    print(f"[SERVER]: listening on {SERVER}")
    while True:
        connection, address = sock.accept()
        all_connections.append(connection)
        thread = threading.Thread(target=handle_client
                                  , args=(connection, address))
        thread.start()
        print(f"[SERVER]: active connections = {threading.active_count()-1}")
        send_to_all_clients(None) # clean-up all_connections

start()