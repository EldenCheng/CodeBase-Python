"""
Python支持正则表达式
"""

import re

s1 = "/user/home/lumberjack"

match = re.match("/(.*)/(.*)/(.*)", s1)

print(match.groups())
