# Again we import the necessary socket python module
import socket
import http.client
import requests as req
import select
import re
# Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.

def udp_send(data , send , rec):
    i=0
    so = serverSock

    so2= ans

    so.sendto(bytes(data, 'utf8'), send)
    while (i < 15):
        ready = select.select([so2], [], [], 0.3)
        if ready[0]:
            data =so.recv(4096)
            print(data)
            break
        else:
            print("timeout")
            i += 1
            so.sendto(bytes(data, 'utf8'), send)
            #print(resp.headers)
    so.close()
    so2.close()
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

# declare our serverSocket upon which
# we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# One difference is that we will have to bind our declared IP address
# and port number to our newly declared serverSock
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

ans = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data, address = serverSock.recvfrom(1024)
    print("Message: ", data)
    data_str = str(data)
    arr = data_str.split(" ")
    print(arr[0])
    i = 0
    while(i<10000):
        i+=1
    ans.sendto(bytes("ack", 'utf8'), (address[0], 2222))
    print("ok")
    print(arr[4])
    resp = req.request(method='GET', url="http://www."+arr[4])
    print(resp.text)

    udp_send(resp.text, (address[0], 2222), (UDP_IP_ADDRESS, UDP_PORT_NO))
    #ans.sendto(bytes(resp.text, 'utf8'), (address[0], 2222))



    # conn = http.client.HTTPSConnection(arr[4])
    # conn.request("GET", "/aut/fa/")
    # r1 = conn.getresponse()
    # print(r1.status, r1.reason)
    # data1 = r1.read()
    # print(data1)