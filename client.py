import socket
import select
from Udp import Udp

file = open('./html/client.html', 'wb')

while(1):

    data = input('enter: source_protocol\n').split(' ')

    sourceProtocol = data[0]#'udp'
    sourceHost ='127.0.0.1'
    sourcePort = 80
    destProtocol ='tcp'

    client_ip = "127.0.0.1"
    proxy_ip = "127.0.0.1"

    client_send_port = 6789
    client_rec_port = 2222

    # http start

    if sourceProtocol == 'udp':
        url = input('enter dest url\n')
        msg = 'GET / HTTP/1.1 Host: '+url #quera.ir/accounts/login/'
        udp = Udp()
        udp.udp_send(msg, (proxy_ip, client_send_port), (proxy_ip, client_rec_port), 0.5)
        print('request sent. waiting for response...\n')
        data = udp.udp_rec((proxy_ip, client_rec_port), client_send_port)

        print(data[0])
        file.write(data[0].encode('UTF-8'))
        print('done\n')
    # http end

    if sourceProtocol == 'tcp':
        type, server, target = input('enter type server target\n').split(' ')
        # type = 'A'
        # server = '204.74.108.1'
        # target = 'google.com'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        MESSAGE = type + ' ' + server + ' '+target + '#'

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((proxy_ip, TCP_PORT))

        s.send(bytes(MESSAGE,'utf8'))
        print('message sent. waiting...')
        data = s.recv(BUFFER_SIZE).decode('utf-16')
        print(data)
        s.close()
        print('done')
