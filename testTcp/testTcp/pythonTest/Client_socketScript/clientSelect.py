'''
    @Create time:   2022/2/15 9:58
    @Autohr:        Patrick.Yang
    @File:          serverTest_reliability.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
import time
import os
import math
import random
import sys
import datetime
import select

IP_ADDRESS_SERVER: str = "172.17.55.200"    # SERVER address
PORT_CLIENT = 6666                          # port num for socket
MAX_LINE = 1024                             # buffer read/write size
CLIENT_TIMEOUT = 3                          # (s)

SOCKET_CLIENT = (IP_ADDRESS_SERVER, PORT_CLIENT)
ERROR_KEYBOARDINT = -1
ERROR_WRONGMESSAGE = -2

MESSAGE_TEST = "client test string"


class ClientSocket():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM, 0)   # ipv4 stream
        self.id = self.socket.fileno()

    def socket_connect(self):
        try:
            self.socket.connect((self.ip, self.port))
        except OSError as err:
            print(err, file=sys.stderr)
            print("Failed to connect to server")
            raise OSError
        else:
            print("Connected to server")

    def socket_sendandwait(self, data_send, *args):
        # do not handle timeout
        r_set = []
        w_set = []
        x_set = []
        if args[0]:
            r_set = args[0]
            print("has rset")
        if args[1]:
            w_set = args[2]
            print("has wset")
        if args[2]:
            x_set = args[2]
            print("has xset")

        self.socket.send(data_send)
        # set timeout value
        client_timeout = CLIENT_TIMEOUT
        # blocked in select func
        readable, writeable, exceptional = select.select(r_set, w_set, x_set, client_timeout)
        print("select updated")
        if not (readable or writeable or exceptional):
            print("Client timeout", file=sys.stderr)
            sys.exit(1)

        recv = ""
        for fd in readable:
            if fd in r_set:
                recv = self.socket.recv(MAX_LINE).decode()  # decode receive message b'xxx'
                print("Get message form server:{}\n".format(recv))
            else:
                print("Get message failed\n")
        return recv

    def socket_close(self):
        self.socket.close()
        print("Client socket closed")

def message_input():
    error_code = 0   # set error code < 0
    get_msg = ''
    try:
        get_msg = input(">>:").strip()  # strip space in begin and end
    except KeyboardInterrupt:
        print("keyboard interruption happened, closing connection")
        error_code = ERROR_KEYBOARDINT
        return get_msg, error_code    # return while interrupt signal happened
    if get_msg == '':
        print("not valid message")
        error_code = ERROR_WRONGMESSAGE

    return get_msg, error_code


if __name__ == '__main__':
    clientSock = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)
    clientSock.socket_connect()


    '''EOF test script'''

    # clientSockTest = socket_connect(sys.argv)
    # rset.append(clientSockTest.fileno())
    # clientSock.send(("test_msg").encode())
    # clientSock.shutdown(SHUT_WR)    # shutdown client socket
    # socket_sendAndWait(clientSockTest, rset, [], [])

    ''''''

    while True:
        rset = [clientSock.id]  # config read sets and write sets according to requirement
        # wset = [clientSock.fileno()]
        msg, status = message_input()
        if status == 0:
            clientSock.socket_sendandwait(msg.encode("utf-8"), rset, [], [])
        else:
            break

    clientSock.socket.close()

