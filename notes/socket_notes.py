import socket

internal_ip = '192.168.0.'
my_ext = '254'



# Create an Af_INET stream socket (TCP
def create_socket():
    """Create an AF_INET STREAM socket (TCP)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print(msg[0])
        quit()

    print('socket created')
    return s

def get_ip_address(host):
    """Retrieve ip address from url
    
    Keyword arguement:
    host - a ip address or url such as www.wikipedia.org
    """
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Could not resolve')
        quit()
    return ip

def port_scan(ip):
    for x in range(75, 85):
        s = create_socket()
        try:
            s.connect((ip, x))
            print('Connection Made: ', str(x))
        except:
            print('No connection: ', str(x))

def gateway_scan(base_ip, port=22):
    """Check the local ip address for other devices
    
    Use this method to find your raspberry pi on 
    a busy network

    Keyword arguments:
    base_ip - your local ip address, ending in .
              something like 192.68.0. (string)
    port - option, 22 is ssh port
    """
    for x in range(240, 260):
        s = create_socket()
        try:
            potentional_gateway = base_ip + str(x)
            s.connect((potentional_gateway, port))
            print('This door checks out: ', str(x))
        except:
            print('This doors no good: ', str(x))

def send_data(sock):
    # send data:
    return data
            
def do_GET(ip, sock, port):
    sock.connect((ip, port))
    print('Socket Connected to '+ ip)
    message = "GET / HTTP/1.1/r/n/r/n"
    try:
        sock.sendall(message)
    except socket.error:
        # fail
        quit()
    reply = sock.recv(4096)
    # do something
    return reply

def do_POST(ip, sock):
    return something


                
if __name__ == "__main__":
    remote_host = input('Remote host: ')
    if not remote_host.startswith('www'):
        remote_host = 'www.wikpedia.org'

    remote_ip = get_ip_address(remote_host)
    print('Ip address of ' + remote_host + ' is ' + remote_ip)
    port_scan(remote_ip)
    gateway_scan(internal_ip)
    
