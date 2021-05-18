import pytest


# 2.编写所需的测试用例
# 此类方法表示一个函数
def test_login():
    print("登录步骤")
    # pytest所用的断言是Python自身断言assert关键字
    assert "abcd" in "abcdefg"


def test_register():
    print("注册步骤")
    assert False


# 3.setup和teardown
# def setup_function():
#     print("打开浏览器/打开APP")
#
# def teardown_function():
#     print("关闭浏览器/关闭APP")

# 3.执行测试用例
if __name__ == '__main__':
    # 注意过格式，main参数是一个列表
    pytest.main(["-s", "get_start_test.py"])