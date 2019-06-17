"""
Python中有某些符号有特殊含义，也有一些流传下来的转义字符
"""

# \n, \t， 换行与tab
s1 = "\tHi\nLeo"
print(s1)

# \0 空格(这里是数字0，不是字母o)
s2 = "A\0B\0C"
print(s2)

# 使用r 前缀可以去掉转义机制，转义字符会原样输出
s3 = r"\tHi\nLeo\0Liu"
print(s3)
