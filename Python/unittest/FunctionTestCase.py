'''
有时候做测试的时候有可能需要直接使用一些方法来做测试
这时候就可以使用unittest的Function Test Case
它的作用就是使用一些已经写好方法来生成一个test case
'''

import unittest


def to_print():
    print("Testing")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    #将一个不是unit test test case里的方法变为test case
    testcase1 = unittest.FunctionTestCase(to_print())
    suite.addTest(testcase1)
    runner = unittest.TextTestRunner()
    runner.run(suite)
