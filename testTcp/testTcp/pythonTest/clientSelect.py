from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
import time
import os
import math
import random
import sys
import datetime
import select

IP_ADDRESS_SERVER: str = "172.19.75.177"    # SERVER address
PORT_CLIENT = 6666                          # port num for socket
MAX_LINE = 1024                             # buffer read/write size
CLIENT_TIMEOUT = 3                          # (s)

SOCKET_CLIENT = (IP_ADDRESS_SERVER, PORT_CLIENT)
ERROR_KEYBOARDINT = -1
ERROR_WRONGMESSAGE = -2

MESSAGE_TEST = "client test string"


def socket_connect(argvs):
    socket_new = socket(AF_INET, SOCK_STREAM, 0)

    if len(argvs) > 1:    # execute by command line?
        server_addr = argvs[1]
        port = argvs[2]
        tup_socket = (server_addr, int(port))  # tuple
        socket_new.connect(tup_socket)
    else:
        socket_new.connect(SOCKET_CLIENT)

    return socket_new


def socket_input():
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


def socket_sendandwait(socket_id, data_send, *args):
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

    # set timeout value
    client_timeout = CLIENT_TIMEOUT
    # blocked in select func
    readable, writeable, exceptional = select.select(r_set, w_set, x_set, client_timeout)
    print("select updated")
    if not (readable or writeable or exceptional):
        print("Client timeout", file=sys.stderr)
        sys.exit(1)
    for fd in readable:
        if fd in rset:
            recv = socket_id.recv(MAX_LINE).decode()  # decode receive message b'xxx'
            print("get message form server:{}\n".format(recv))
        else:
            print("get message failed\n")


if __name__ == '__main__':
    clientSock = socket_connect(sys.argv)
    rset = [clientSock.fileno()]    # config read sets and write sets according to requirement
    # wset = [clientSock.fileno()]
    '''eof test script'''


    # clientSockTest = socket_connect(sys.argv)
    # rset.append(clientSockTest.fileno())
    # clientSock.send(("test_msg").encode())
    # clientSock.shutdown(SHUT_WR)    # shutdown client socket
    # socket_sendAndWait(clientSockTest, rset, [], [])

    ''''''

    while True:
        msg, status = socket_input()
        if status == 0:
            clientSock.send(msg.encode("utf-8"))
            socket_sendandwait(clientSock, rset, [], [])
        else:
            break

    clientSock.close()
    print("Client socket closed")
