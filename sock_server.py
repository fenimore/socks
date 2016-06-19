import socket, select

# Add broadcast message to all connected clients

# Do not send the message to master socket and the client

def broadcast(sock, message):
    """Broadcast message to all connections.

    Keyword arguments:
        - sock -- to no send message to the sender
        - message -- text to broadcast, include user
    """
    
    for suck in CONNECTIONS:
        if suck != base_socket and socket != sock:
            try:
                suck.send(message)
            except:
                suck.close()
                CONNECTIONS.remove(suck)

if __name__ == "__main__":
    """Keep track of sockets
    
    Start port
    and loop and read available sockets (through select)
    in the readable sockets, there'll be two options:
    (1) a new connection (2) a new message
    either add new connection to list (and broadcast welcome)
    or broadcast the message in the recieving buffer
    If nothing is in the buffer, the user has disconnected
    close socket, and remove from list
    """

    CONNECTIONS = []
    BUFFER = 4096
    PORT = 1050

    base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    base_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    base_socket.bind(("0.0.0.0", PORT))
    base_socket.listen(10) # ten connections

    CONNECTIONS.append(base_socket)

    print('Chat server on port:', str(PORT))


    
    while True:
        # https://docs.python.org/3/howto/sockets.html
        ready_read, ready_write, in_error = select.select(CONNECTIONS,
                                                          [], [])
        for sock in ready_read:
            if sock == base_socket:
                (client, address) = sock.accept() # or base_socket
                CONNECTIONS.append(client)
                print('Client connected:', address)
                broadcast(sock, '(%s, %s) enters chat' % address)
            else:
                try:
                    data = sock.recv(BUFFER)
                    if data:
                        broadcast(sock, '<'
                                  + str(sock.getpeername())
                                  + '>' + data)
                except:
                    broadcast(sock, '<' + str(sock.getpeername())
                              + '> has left the chat')
                    sock.close()
                    CONNECTIONS.remove(sock)

        base_socket.close()
                
