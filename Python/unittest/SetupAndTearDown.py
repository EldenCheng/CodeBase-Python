import unittest


# Test Case是由一个继承TestCase类的新类组成,一个Test Case里面包含数个检查点
class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUp Class method run")

    def setUp(self):
        print("setUp method run!")

    def test_upper(self):
        print("Test 1")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        print("Test 2")
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        print("Test 3")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def tearDown(self):
        print("tearDown method run!")

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class method run!")


if __name__ == '__main__':
    unittest.main()