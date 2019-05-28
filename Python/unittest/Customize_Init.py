import unittest


class TC1(unittest.TestCase):
    driver = ""
    paramaters = ""

    def __init__(self, testname, paramaters = "testing paramaters"):

        super(TC1, self).__init__(testname)
        print("init")
        print("driver in init: ", self.driver)
        self.paramaters = paramaters
        print(self.paramaters)

    @classmethod
    def setUpClass(cls):
        print("paramaters in setUpClass: ", cls.paramaters)
        cls.driver = "Set up driver testing " + cls.paramaters


    def setUp(self):
        print("setUp")

    def test_Excute1(self):
        print("Execute1")
        print("driver in execute 1: ", self.driver)

    def test_Excute2(self):
        print("Execute2")
        print("driver in execute 2: ", self.driver)


if __name__ == '__main__':
    unittest.main()