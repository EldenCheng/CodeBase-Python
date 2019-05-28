import unittest

from Python.unittest.Get_Started import TestStringMethods


def suite():
    suite = unittest.TestSuite()
    #suite.addTest(TestStringMethods('test_default_widget_size'))
    #suite.addTest(TestStringMethods('test_widget_resize'))
    suite.addTest(TestStringMethods("test_upper"))
    suite.addTest(TestStringMethods("test_isupper"))
    return suite

if __name__ == '__main__':
    #suite().run()
    runner = unittest.TextTestRunner()
    runner.run(suite())
