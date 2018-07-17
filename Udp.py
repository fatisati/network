# Again we import the necessary socket python module
import socket
import http.client
import requests as req
import select

maxChar = 500  # max character send size
mrs = 4040
parity_en = 1

class Udp:

    def udp_send(self, data, sendAddr, recAddr, timeout):

        finish = 0
        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rec.setblocking(0)
        rec.bind(recAddr)

        fragment = 0
        offset = 0
        #msg = ''
        sequence_no = 0

        while finish != 1:
            print('sending packet with offset: '+ str(offset))
            end = len(data)
            if len(data) > maxChar:

                fragment = 1
                if offset + maxChar < len(data):
                    end = offset + maxChar
                else:
                    fragment = 0

            msg = data[offset: end]
            msg += str(sequence_no)
            if fragment == 0:
                msg += 'f'
            msg += str(self.parity(msg))
            send.sendto(self.str_to_bytes(msg), sendAddr)
            #print(msg)
            k = 0

            while k < 15:
                ready = select.select([rec], [], [], timeout)
                if ready[0]:
                    ack = self.bytes_to_str(rec.recv(mrs))
                    #ack = ack[2]
                    if str(sequence_no) == ack:
                        break

                else:
                    print("timeout sending "+str(sequence_no))
                    k += 1
                    send.sendto(self.str_to_bytes(msg), sendAddr)

            if fragment == 0:
                finish = 1
            else:
                offset += maxChar
                sequence_no += 1
                sequence_no %= 2

        send.close()
        rec.close()

    def udp_rec(self, recAddr, sendPort):

        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rec.setblocking(0)
        rec.bind(recAddr)

        sequence_no = 0
        finish = 0
        final_data = ''
        #addr = ''
        while finish != 1:
            ready = select.select([rec], [], [])

            if ready[0]:
                data, sendAddr = rec.recvfrom(mrs)  # buffer size is 1024 bytes
                sendAddr = sendAddr[0]
                data = self.bytes_to_str(data)
                #print(data)
                if data[-2] == 'f': #data[-2] is parity then
                    ack = data[-3]
                    finish = 1
                else:
                    ack = data[-2]

                parity = self.parity(data[:-1])
                if ack == str(sequence_no) and str(parity) == data[-1]:
                    send.sendto(self.str_to_bytes(ack), (sendAddr, sendPort))
                    sequence_no += 1
                    sequence_no %= 2

                    if finish == 0:
                        final_data += data[:-2] # sequence number & parity
                    else:
                        final_data += data[:-3] # +f


                else:
                    if str(parity) != data[-1]:
                        print('parity error')

                    print('waiting for'+str(sequence_no)+' but what i get '+ack)
                    finish = 0
        send.close()
        rec.close()
        return final_data, sendAddr

    def parity(self, msg):
        if parity_en == 0:
            return 0
        ans = 0
        for c in msg:
            ans += ord(c)
            ans %= 2
        return ans

    def str_to_bytes(self, msg):
        return msg.encode('utf-16')

    def bytes_to_str(self, bts):
        return bts.decode('utf-16')