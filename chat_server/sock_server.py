"""Chat server.

A simple chat server
"""
import socket, select, os, sys
if os.name != 'nt':
    import fcntl
    import struct
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
    host = ''
    clients = {}

    def __init__(self, host='', port=1050):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10) # 10 connections
        self.connections.append(self.sock)
        print('Chat server accepting connections:',
              get_local_ip(), 'port:', str(port))
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

        message =  (b'\r * ' + str.encode(self.clients[peer_name])
                   + b' enters chat\n')
        print(str(message))
        self.broadcast_message(client, message)
        
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
                print(str(message))
                self.broadcast_message(sender, message)
                sender.shutdown(socket.SHUT_RDWR)
                sender.close()
                self.connections.remove(sender)
        except:
            message = str.encode('\r * %s leaves chat\n' %h)
            print(str(message))
            self.broadcast_message(sender, message)
            sender.shutdown(socket.SHUT_RDWR)
            sender.close()
            self.connections.remove(sender)

def get_local_ip(ifname='wlp3s0'):
    """Return local ip address.

    http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/1947766#1947766
    """
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.') and os.name != 'nt':
        interfaces = ['eth0','eth1','eth2','wlan0','wlp3s0',
                      'wlan1','wifi0','ath0','ath1','ppp0']
        for ifname in interfaces:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ip =  socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915, # SIOCGIFADDR
                    struct.pack('256s', bytes(ifname[:15], 'utf-8'))
                )[20:24])
                break
            except IOError:
                pass
    return ip
            
if __name__ == '__main__':
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
