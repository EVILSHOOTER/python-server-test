import socket, time, pickle

HEADERSIZE = 10

SERVER = ''
# '' # for Linode
#socket.gethostname() # for local
PORT = 1337

# object with IPv4 and TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bound to tuple (IP and port) - your server
s.bind((SERVER, PORT)) # requires a port-forwarded computer
# prepare queue for incoming connections
s.listen(5)

while True:
    # allow anybody connecting
    clientsocket, address = s.accept()
    print(f"Connected with {address}")

    #msg = "welcom 2 server!"
    d = {1: "testing", 2: "message"}
    msg = pickle.dumps(d)
    print(msg)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    clientsocket.send(msg)


    '''
    # test send with time
    while True:
        time.sleep(3)
        msg = f"The time is: {time.time()}"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
    '''
    # send info to client
    #clientsocket.send(bytes("zis is da massage", "utf-8"))
    #clientsocket.close()
