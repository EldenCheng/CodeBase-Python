"""
固件（Fixture）是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们。

我们可以利用固件做任何事情，其中最常见的可能就是数据库的初始连接和最后关闭操作。

Pytest 使用 pytest.fixture() 定义固件，下面是最简单的固件，只返回北京邮编
"""
import os

"""
固件可以直接定义在各测试脚本中，就像上面的例子。
更多时候，我们希望一个固件可以在更大程度上复用，这就需要对固件进行集中管理。Pytest 使用文件 conftest.py 集中管理固件

在复杂的项目中，可以在不同的目录层级定义 conftest.py，其作用域为其所在的目录和子目录

不要自己显式调用 conftest.py，pytest 会自动调用，可以把 conftest 当做插件来理解

另外, 有些pytest中的钩子函数的逻辑也需要在conftest.py中定义, 下面列出一些比较常用的(带pytest开头的都是)
"""

import pytest

"""
Register argparse-style options and ini-style config values, called once at the beginning of a test run.
主要用于支持一些自定义的pytest命令行参数
需要在最顶层的conftest.py中定义
"""
def pytest_addoption(parser):
    # 为pytest的命令行添加一个输入参数--device
    parser.addoption(
        '--device',
        type=str,
        help='device to test on, such as ios, android, <device>'
    )

"""
Called after the Session object has been created and before performing collection and entering the run test loop.
测试开场时一些全局初始化时用
"""
def pytest_sessionstart(session):
    pass

"""
Called after whole test run finished, right before returning the exit status to the system.
测试收尾用, 比如下面我就用来调用命令行来自动生成allure report
"""
def pytest_sessionfinish(session, exitstatus):
    cmd = r"allure generate -c -o .\report --single-file .\allure-data"
    os.system(cmd)



@pytest.fixture()
def postcode():
    return '010'
