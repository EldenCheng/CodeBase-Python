import logging

import pytest

# 1. 在比较新版本的pytest中, 建议使用fixture来实现test case的初始化与结尾处理

@pytest.fixture(scope='function', autouse=True)
def init_testcase():
    logging.info("初始化Test Case")

    yield # pytest中, 用Python中的yield关键字来分隔测试完成后要执行的部分
    logging.info("Test Case的结尾处理")

# 2.编写所需的测试用例
# 此类方法表示一个函数
def test_login():
    logging.info("登录步骤")
    # pytest所用的断言是Python自身断言assert关键字
    assert "abcd" in "abcdefg"


def test_register():
    logging.info("注册步骤")
    assert False

# 又或者可以

# 3.执行测试用例
if __name__ == '__main__':
    # 注意格式，main参数是一个列表
    pytest.main(["-s", "get_start_test.py"])