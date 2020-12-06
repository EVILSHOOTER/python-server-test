# here is an insanely ugly way of me keeping my old unused code
# for incase I need it later.


'''
ok so problem. if client sends 2 messages as a stream, there is no discernible
split between the 2 messages. it's all just continuous data.
all you have to go by is message length WHICH IS FINE but,
now I'm trying to concatenate the last cut-out stream of data
with the current stream to form the next message.
and this means I have to concatenate bytes together, which is REALLY strange
and I might give up on that to just use variable buffer sizes instead.
that idea uses less code too, but idk how much less reliable it is.

last edit: 06/12/2020
'''
# handles individual connections
def handle_client(connection, address):
    print(f"[SERVER]: new connection = {address}")

    connected = True
    while connected:
        # newer method using pickle. streaming.
        full_msg = b""
        new_msg = True
        msg_len = 0
        last_msg = b""
        while True:
            msg = connection.recv(16)
            if new_msg:
                msg = last_msg + msg
                print(last_msg)
                print(f"new msg received. length: {msg[:HEADER_SIZE]}")
                msg_len = int(msg[:HEADER_SIZE])
                print("message length: ", msg_len)
                new_msg = False

            full_msg += msg
            print("piece: ", msg, "msg length", len(full_msg) - HEADER_SIZE)

            if len(full_msg) - HEADER_SIZE >= msg_len:
                newest_msg = full_msg[HEADER_SIZE:msg_len + HEADER_SIZE]
                last_msg = full_msg[HEADER_SIZE + len(newest_msg):]

                print(newest_msg)
                print(last_msg)
                print(pickle.loads(newest_msg))

                new_msg = True

                # break
                '''
                print(f"FINAL MESSAGE: {full_msg[HEADER_SIZE:]}")

                d = pickle.loads(full_msg[HEADER_SIZE:])
                print(f"actual object: {d}")

                new_msg = True
                full_msg = b""
                '''

        '''
        try:

            # older method. no streaming.
            msg_len = connection.recv(HEADER_SIZE).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = connection.recv(msg_len).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    connected = False

                print(f"[{address}]: {msg}")
                connection.send(("msg received").encode(FORMAT)) # back to client



        except:
            connected = False
            print(f"[SERVER]: Client message error. Connection cut with {address} -")
        '''
    connection.close()

'''
the client code

last edit: 06/12/2020
'''
def send(msg):
    '''
    # older method without pickle.
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_SIZE - len(send_len))

    sock.send(send_len)
    sock.send(message)
    '''
    '''
    msgB = pickle.dumps(msg)
    msgB = bytes(f'{len(msgB):<{HEADER_SIZE}}', FORMAT) + msgB
    print(f"you sent: {msgB}")
    sock.send(msgB)
    '''
    # second message - the data
    message = pickle.dumps(msg)
    # first message - the length
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_SIZE - len(send_len))

    sock.send(send_len)
    sock.send(message)

    #print(sock.recv(2048).decode(FORMAT))
    # make a client receive message function that streams cuz this is lazy.
