'''
    @Create time:   2022/2/15 9:58
    @Autohr:        Patrick.Yang
    @File:          serverTest_basic.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-

    ***   test Manual   ***
    in this basic case target server just normally start up.
    ***********************
'''
from Client_socketScript.clientSelect import *
import unittest


class ClientTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("set up class...")
        self.testSocket = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)

    @classmethod
    def tearDownClass(self):
        print("tear down class...")


    def setUp(self):
        self.testSocket = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)
        # self.testSocket.socket_connect()
        print("set up...")
        pass

    def tearDown(self):
        self.testSocket.socket_close()
        # self.testSocket.socket_close()
        print("tear down...")
        pass

    def testCase01_messageSend(self):
        self.testSocket.socket_connect()
        rset = [self.testSocket.id] # only config read set

        TEST_STRING_1 = "selectTestString"  # normal string
        TEST_STRING_2 = "test string 123 321__"  # alphabet and number mixed
        TEST_STRING_3 = " 5_@@#$%(())_d "  # symbol

        dataSend = TEST_STRING_1
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = self.testSocket.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

        dataSend = TEST_STRING_2
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = self.testSocket.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

        dataSend = TEST_STRING_3
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = self.testSocket.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

    def testCase02_close(self):
        rset = [self.testSocket.id] # only config read set
        self.testSocket.socket_connect()

        TEST_STRING = "selectTestString"
        dataSend = TEST_STRING
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = self.testSocket.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "Could not receive message!")
        self.testSocket.socket_close()

        with self.assertRaises(OSError):
            self.testSocket.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])

    def testCase03_serverTimeout(self):
        rset = [self.testSocket.id] # only config read set
        self.testSocket.socket_connect()
        time.sleep(11)  # sleep more than 10s(server timeout)
        dataRecv = self.testSocket.socket.recv(2046).decode()
        self.assertEqual(dataRecv, '', "Not fulfill timeout condition!")

    def messageAnalyze(self, msgInput):
        msgOut = msgInput[::-1]
        return msgOut



if __name__ == "__main__":
    unittest.main()
