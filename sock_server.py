"""Chat server.

A simple chat server
"""
import socket, select

from sock_names import NAMES

def broadcast_data(server, sock, message):
    """Broadcast message to all connections.

    Keyword arguments:
        - sock -- to no send message to the sender
        - message -- text to broadcast, include user
    """
    print('Broadcast', message)
    for connection in CONNECTIONS:
        if connection != server and connection != sock:
            try:
                connection.send(message)
            except:
                print('\nclosing\n')
                #sock.shutdown(socket.SHUT_RDWR)
                #print(connection.getpeername())
                CONNECTIONS.remove(connection)

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

    client_dict = {}
    while True:
        # https://docs.python.org/3/howto/sockets.html
        ready_read, ready_write, in_error = select.select(CONNECTIONS,[], [])
        for sock in ready_read:
            if sock == base_socket:
                (client, address) = base_socket.accept() # or base_socket
                CONNECTIONS.append(client)
                #print('Client connected:', address)
                client_dict[str(client.getpeername()[1])] = NAMES[0]
                NAMES.pop(0)
                broadcast_data(base_socket, client, b'\r<' + str.encode(client_dict[str(client.getpeername()[1])]) + b'> enters chat\n')
            else:
                try:
                    data = sock.recv(BUFFER)
                    if data:
                        user = '\r<' + client_dict[str(sock.getpeername()[1])] + '> '
                        byte_handle = str.encode(user)
                        broadcast_data(base_socket, sock, byte_handle + data) 
                except:
                    broadcast_data(base_socket, sock, "Client (%s, %s) is offline" % address)
                    print("Client (%s, %s) is offline" % address)
                    sock.shutdown(socket.SHUT_RDWR)
                    CONNECTIONS.remove(sock)
                    #continue
            if sock not in CONNECTIONS:
                print('termination time')
                sock.close()
    base_socket.close()
                
