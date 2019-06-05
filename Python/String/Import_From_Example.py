"""
这是用于import_from的例子所导入的文件
"""

import time

global g_value

print("This statement is executed when import!")

title = "This is a title"

current_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

g_value = "I'm a global value"

