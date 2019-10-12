import socket
import threading
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

def heartbeat(server_address):
    connection.sendto(b'con-h 0x00', server_address)
    heartbeat_timer = threading.Timer(3, heartbeat, [server_address])
    heartbeat_timer.start()

# Create a UDP socket
connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 0
heartbeat_timer = None

server_address = ('localhost', 10000)

try:
    connection.sendto(('com-0 %s' % (socket.gethostbyname(socket.gethostname()))).encode(), server_address)
    data, _ = connection.recvfrom(4096)
    print(data)
    connection.sendto(b'com-0 accept', server_address)

    if config['client']['keep_alive'] == 'yes':
        heartbeat(server_address)

    while True:
        # message = input('Type your message!')
        # connection.sendto(('msg-%i=%s' % (counter, message)).encode(), server_address)

        data, _ = connection.recvfrom(4096)
        counter += 2

        if data.startswith(b'res-'):
            print(data)
        elif data.startswith(b'con-res'):
            print('Connection was reset')
            connection.sendto(b'con-res 0xFF', server_address)

        print(data)

finally:
    print('closing socket')
    connection.close()
