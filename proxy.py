# Again we import the necessary socket python module
import socket
import dns
import dns.resolver
import http.client
import requests as req
import select
from Udp import Udp

file = open('./html/proxy.html', 'wb')

dns_cache = []
http_cache = []

tmp = 1

def dns_query(type, server, domain):
    k = 0
    msg = ''
    res = dns.resolver.Resolver()
    res.nameservers = ['8.8.8.8']

    for record in dns_cache:
        if record[0] == type and record[1] == server and record[2] == domain:
            print('query found in cache')
            return record[3]
    while k < 15:
        #print(k)
        try:
            if tmp == 1:
                answer = res.query(domain, type)#, source=server)
            else:
                answer = dns.resolver.query(domain, type)#, source=server)
            for data in answer:
                if type == 'A':
                    print(data.address)
                    msg += data.address + '\n'
                if type == 'CNAME':
                    print(data.target)
                    msg += str(data.target) + '\n'
            k = 16
        except dns.exception.Timeout:
            k += 1

    qm = dns.message.make_query(domain, type)
    qa = dns.query.udp(qm, server, timeout=4)
    if(qa.flags & dns.flags.AA == 1024):
        print('answer is authoritative')
        msg += 'answer is authoritative'
    else:
        print('answer is not authoritative')
        msg += 'answer is not authoritative'

    if len(dns_cache) == 100:
        dns_cache.pop(0)
    dns_cache.append((type, server, domain, msg))
    return msg

def http_query(host):

    for record in http_cache:
        if record[0] == host:
            print('http answer found in cache')
            return record[1]
    resp = req.request(method='GET', url='http://www.'+ host, allow_redirects=False)
    code = resp.status_code
    if code == 400 or code == 404:

        if len(http_cache) == 100:
            http_cache.pop(0)
        http_cache.append((host, 'error 400'))
        return 'error 400'
    while code == 301 or code == 302 or code == 307:
        print(str(code) +' redirecting...\n')
        new_url = resp.headers['Location']
        resp = req.request(method='GET', url=new_url, allow_redirects=False)
        code = resp.status_code

        if code == 400 or code == 404:

            if len(http_cache) == 100:
                http_cache.pop(0)
            http_cache.append((host, 'error 400'))
            return 'error 400'
    if len(http_cache) == 100:
        http_cache.pop(0)

    http_cache.append((host, resp.text))
    return resp.text

sourceProtocol = 'udp'
sourceHost = '127.0.0.1'
sourcePort = 80
destProtocol = 'tcp'

client_ip = "127.0.0.1"
proxy_ip = '127.0.0.1'
proxy_rec_port = 6789
proxy_send_port = 2222
while(1):
    sourceProtocol = input('enter source protocol\n')
    if sourceProtocol == 'udp':
        udp = Udp()
        data, client_ip = udp.udp_rec((proxy_ip, proxy_rec_port), proxy_send_port)
        print(data, client_ip)
        data_str = str(data)
        param = data_str.split(' ')
        msg = http_query(param[4])

        #msg = http_query(param[4])
        #print(msg)
        #file.write(msg)
        udp.udp_send(msg, (client_ip, proxy_send_port), (proxy_ip, proxy_rec_port), 0.5)

    if sourceProtocol == 'tcp':
        print('listening for tcp connection...')
        TCP_PORT = 5005
        BUFFER_SIZE = 20  # Normally 1024, but we want fast response
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((client_ip, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        #print ('Connection address:', addr)
        finish = 0
        final_params = []
        final_data = ''
        while finish != 1:

            data = str(conn.recv(BUFFER_SIZE))
            if not data: break
            end = len(data)-1

            if data[len(data)-2] == '#':
                finish = 1
                end -= 1
            final_data += data[2:end]

        final_params = final_data.split(' ')
        print('msg received')
        msg = dns_query(final_params[0], final_params[1], final_params[2])
        conn.send(msg.encode('utf-16'))
        #print(final_params)
        conn.close()
