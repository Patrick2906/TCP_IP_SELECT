'''
    @Create time:   2022/2/15 9:58
    @Autohr:        Patrick.Yang
    @File:          serverTest_errorCase.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-

    ***   test Manual   ***
    in this error case target server should not be started
    ***********************
'''
from Client_socketScript.clientSelect import *
import unittest


class ClientTestErrorCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("set up class...")

    @classmethod
    def tearDownClass(self):
        print("tear down class...")

    def setUp(self):
        print("set up...")
        pass

    def tearDown(self):
        self.testSocket.socket_close()
        print("tear down...")
        pass

    def testCase01_connect_serverNotStart(self):
        self.testSocket = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)
        with self.assertRaises(OSError):
            self.testSocket.socket_connect()

    def testCase02_connect_serverNotAvailable(self):
        InvalidIP = "198.166.22.1"
        InvalidPort = 8001
        self.testSocket = ClientSocket(InvalidIP, InvalidPort)  # switch to another socket which is not available
        with self.assertRaises(OSError):
            self.testSocket.socket_connect()

    def testCase03_connect_wrongSocket(self):
        InvalidIP = IP_ADDRESS_SERVER
        InvalidPort = 8001
        self.testSocket = ClientSocket(InvalidIP, InvalidPort)  # switch to another socket which is not available
        with self.assertRaises(OSError):
            self.testSocket.socket_connect()

if __name__ == "__main__":
    unittest.main()


