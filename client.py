import socket
import select
from Udp import Udp

file = open('client.html', 'wb')

sourceProtocol = 'udp'
sourceHost = '127.0.0.1'
sourcePort = 80
destProtocol = 'tcp'

client_ip = "127.0.0.1"
proxy_ip = "127.0.0.1"

client_send_port = 6789
client_rec_port = 2222

# http start

if sourceProtocol == 'udp':
    msg = 'GET / HTTP/1.1 Host: quera.ir/'
    udp = Udp()
    udp.udp_send(msg, (proxy_ip, client_send_port), (proxy_ip, client_rec_port), 0.5)
    data = udp.udp_rec((proxy_ip, client_send_port), (proxy_ip, client_rec_port))

    print(data)
    file.write(data.encode('UTF-8'))

# http end

if sourceProtocol == 'tcp':
    type = 'A'
    server = '204.74.108.1'
    target = 'google.com'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    MESSAGE = type + ' ' + server + ' '+target + '#'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((proxy_ip, TCP_PORT))

    s.send(bytes(MESSAGE,'utf8'))
    data = s.recv(BUFFER_SIZE)
    print(str(data))
    s.close()
