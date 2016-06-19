"""Socks chat client

"""
import socket, select, string, sys

def prompt():
    """Take user input?"""
    sys.stdout.write('<Me> ')
    sys.stdout.flush()

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print('args missing: host and port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(2)

    try:
        server_socket.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host')
    prompt()

    while 1:
        socks = [sys.stdin, server_socket] # listen from server & input
        ready_read, ready_write, in_error = select.select(socks, [], [])

        for sock in ready_read:
            if sock == server_socket:
                data = sock.recv(4096)
                if data:
                    sys.stdout.write(data)
                    prompt()
                else:
                    print('\nDisconnected')
                    sys.exit()
            else: # User input
                message = sys.stdin.readline()
                server_socket.send(message)
                prompt()
            
