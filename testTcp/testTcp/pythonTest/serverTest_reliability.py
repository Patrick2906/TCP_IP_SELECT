'''
    @Create time:   2022/2/15 9:58
    @Autohr:        Patrick.Yang
    @File:          serverTest_reliability.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-

    ***   test Manual   ***
    in this basic case target server just normally start up.
    ***********************
'''
from Client_socketScript.clientSelect import *
import unittest


class ClientTestReliability(unittest.TestCase):
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
        print("tear down...")
        pass

    def testCase01_multiClients(self):
        test_socket1 = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)
        test_socket2 = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)
        test_socket3 = ClientSocket(IP_ADDRESS_SERVER, PORT_CLIENT)

        test_socket1.socket_connect()
        test_socket2.socket_connect()
        test_socket3.socket_connect()

        rset = [] # only config read set
        rset.append(test_socket1.id)
        rset.append(test_socket2.id)
        rset.append(test_socket3.id)

        TEST_STRING_1 = "selectTestString"  # normal string
        TEST_STRING_2 = "test string 123 321__"  # alphabet and number mixed
        TEST_STRING_3 = " 5_@@#$%(())_d "  # symbol

        dataSend = TEST_STRING_1
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = test_socket1.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

        dataSend = TEST_STRING_2
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = test_socket2.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

        dataSend = TEST_STRING_3
        dataCheck = self.messageAnalyze(dataSend)
        dataRecv = test_socket3.socket_sendandwait(dataSend.encode("utf-8"), rset, [], [])
        self.assertEqual(dataRecv, dataCheck, "message receive not correct")

        test_socket1.socket_close()
        test_socket2.socket_close()
        test_socket3.socket_close()

    def messageAnalyze(self, msgInput):
        msgOut = msgInput[::-1]
        return msgOut



if __name__ == "__main__":
    unittest.main()

