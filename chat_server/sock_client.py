"""Socks chat client

"""
import socket, select, string, sys

banner ="""
                 _        
                | |       
  ___  ___   ___| | _____ 
 / __|/ _ \ / __| |/ / __|
 \__ \ (_) | (__|   <\__ \

 |___/\___/ \___|_|\_\___/
                                           
Welcome to the socks chat
"""
class ChatClient(object):
    host = ''
    port = ''

    def __init__(self, host='localhost', port=1050):
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        
        try:
            self.sock.connect((host, port))
        except:
            print(' * Unable to connect')
            sys.exit()

        print('Connected to remote host')
        print(banner)
        self.prompt()
        
        while True:
            socks = [sys.stdin, self.sock] 
            ready_read, ready_write, in_error = \
                                    select.select(socks, [], [])

            for ready_sock in ready_read:
                if ready_sock == self.sock:
                    data = self.sock.recv(4096)
                    if not data:
                        self.sock.close()
                        print('\nDisconnected')
                        sys.exit()
                    else:
                        sys.stdout.write(data.decode("utf-8") )
                        self.prompt()
                else: # User input
                    message = sys.stdin.readline()
                    self.sock.send(str.encode(message))
                    self.prompt()
    
    def prompt(self):
        """Take user input?"""
        sys.stdout.write('<Me> ')
        sys.stdout.flush() # why flush?

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print('args missing: host and port')
        print('defaults localhost 1050')
        ChatClient()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        ChatClient(host, port)
    
