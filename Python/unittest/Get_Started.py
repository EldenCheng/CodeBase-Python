import unittest


# Test Case是由一个继承TestCase类的新类组成,一个Test Case里面包含数个检查点
class TestStringMethods(unittest.TestCase):

    # Test case里面使用一些带test_xxx为名字的方法,只有以test_xxx命名的方法才会被test runner发现与执行
    # 这些方法负责实际测试具体的检查点(测试点)
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_zfail(self):
        self.fail("Force fail")

    def test_print(self):
        print("Force fail")


if __name__ == '__main__':
    unittest.main()
