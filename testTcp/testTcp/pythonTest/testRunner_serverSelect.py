'''
    @Create time:   2022/2/15 14:53
    @Autohr:        Patrick.Yang
    @File:          testRunner_serverSelect.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import unittest
import time
from serverTest_errorCase import ClientTestErrorCase
from serverTest_reliability import ClientTestReliability
from serverTest_basic import ClientTestBase

def runAll():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(ClientTestErrorCase))
    suite.addTest(loader.loadTestsFromTestCase(ClientTestBase))
    suite.addTest(loader.loadTestsFromTestCase(ClientTestReliability))

    runner = unittest.TextTestRunner(verbosity=2)

    try:
        print
        "#############   runner start   ###############"
        result = runner.run(suite)
        print(result)
    except KeyboardInterrupt:
        print("Test aborted")


if __name__ == "__main__":
    runAll()