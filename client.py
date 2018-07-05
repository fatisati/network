import socket
import select
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = "GET / HTTP/1.1 Host: aut.ac.ir "

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.settimeout(0.5)
ackSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ackSock.setblocking(0)
ackSock.bind((UDP_IP_ADDRESS, 2222))

clientSock.sendto(bytes(Message, 'utf8'), (UDP_IP_ADDRESS, UDP_PORT_NO))

i = 0
ackSock.setblocking(0)
while(i<15):
    ready = select.select([ackSock], [], [], 0.3)
    if ready[0]:
        data = ackSock.recv(4096)
        print(data)
        break
    else:
        print("timeout")
        i+=1
        clientSock.sendto(bytes(Message, 'utf8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
ready = select.select([ackSock], [], [], 1)
if ready[0]:
    data, address = ackSock.recvfrom(4096)
    clientSock.sendto(bytes("ack", 'utf8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    print(data)
