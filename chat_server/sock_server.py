"""Chat server.

A simple chat server
"""
import socket, select, os, sys
#from time import gmtime, strftime

from sock_names import NAMES

def log(message):
    """Log messages to logfile."""
    with open(os.path.join(os.getcwd(), 'chat.log'), 'a+') as f:
        # TODO: add timestamp
        f.write('\n' + str(message))
        
class ChatServer(object):
    """Chat server.

    Keyword arguments:
    - sock -- the server socket
    """
    connections = []
    buffer_size = 4096
    port = 1050
    clients = {}

    def __init__(self, port=1050):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(10) # 10 connections

        self.connections.append(self.sock)
        print('Chat server accepting connections at:', str(port))

        while True:
            ready_read, ready_write, in_error = \
                        select.select(self.connections, [], [])
            for s in ready_read:
                if s == self.sock:
                    self.accept_connection()
                else:
                    self.forward_message(s)
                
    
    def broadcast_message(self, sender, message):
        """Broadcast message to all connections.
        
        Keyword arguments:
        - sock -- to no send message to the sender
        - message -- text to broadcast, include user
        """
        log(message)
        for connection in self.connections:
            if connection != self.sock and connection != sender:
                try:
                    connection.send(message)
                except:
                    self.connections.remove(connection)

    def accept_connection(self):
        """Set up new connection.
    
        If readable socket is the server socket, there
        is a new connection to be made, add it to the 
        self.connections list.
        """
        client, address = self.sock.accept()
        peer_name = str(client.getpeername()[1])
        self.connections.append(client)
        if NAMES:
            self.clients[peer_name] = NAMES[0]
            NAMES.pop(0)
        else:
            self.clients[peer_name] = peer_name

        self.broadcast_message(client, b'\r * ' 
                           + str.encode(self.clients[peer_name])
                           + b' enters chat\n')
        
    def forward_message(self, sender):
        """Broadcast message to chat room.
        
        Attributes:
        - h -- the senders handle
        
        Keyword arguments:
        - sender -- the message author, to whom don't forward
        """
        h = self.clients[str(sender.getpeername()[1])]
        try:
            data = sender.recv(self.buffer_size)
            if data:
                message = str.encode('\r<' + h + '> ') + data
                self.broadcast_message(sender, message)
            else:
                message = str.encode('\r * %s leaves chat\n'%h) 
                self.broadcast_message(sender, message)
                sender.shutdown(socket.SHUT_RDWR)
                sender.close()
                self.connections.remove(sender)
        except:
            message = str.encode('\r * %s leaves chat\n' %h)
            self.broadcast_message(sender, message)
            sender.shutdown(socket.SHUT_RDWR)
            sender.close()
            self.connections.remove(sender)


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
    ChatServer()
