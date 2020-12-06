import socket, pickle

HEADERSIZE = 10

SERVER = socket.gethostname()
# '139.162.219.137' # for Linode
#socket.gethostname() # for local
PORT = 1337

# object with IPv4 and TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to host + port. gethostname is just this pc.
s.connect((SERVER, PORT))

while True:
    full_msg = b""
    new_msg = True
    msg_len = 0
    while True:
        # receive data from socket.
        msg = s.recv(16) # 1 byte = 1 char in utf-8
        if new_msg:
            print(f"new msg received. length: {msg[:HEADERSIZE]}")
            msg_len = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg
        print("piece: ", msg, "len: ", len(full_msg)-HEADERSIZE)

        if len(full_msg)-HEADERSIZE == msg_len:
            print(f"FINAL MESSAGE: {full_msg[HEADERSIZE:]}")

            d = pickle.loads(full_msg[HEADERSIZE:])
            print(f"actual object: {d}")

            new_msg = True
            full_msg = b""


#s.send((bytes("zis is da client's massage bak", "utf-8")))
