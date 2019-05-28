'''
本书的作者对使用type来判定变量的类型持否定态度，认为这样会牺牲了Python的变量灵活性
type方法用来获得变量，实例的类型对象名称

'''

import time
import _io

tm = time.localtime()

num = 10
s = "A string"
b = True
t = (1,2,3,4)
l = [5,6,7,8]
set = {9,10,11}
d ={"A": 12, "B": 13}
f = open("test.txt", "w")

# 使用type方法查看对象类型
print("使用type方法查看数字对象类型:", type(num))
print("使用type方法查看字符串对象类型:", type(s))
print("使用type方法查看逻辑对象类型:", type(b))
print("使用type方法查看元组对象类型:", type(t))
print("使用type方法查看列表对象类型:", type(l))
print("使用type方法查看集合对象类型:", type(set))
print("使用type方法查看字典对象类型:", type(d))
print("使用type方法查看文件对象类型:", type(f))

# 使用类型名判断对象类型是否特定类型
if type(l) == int:
    print("使用类型名判断对象类型是否特定类型:", "yes")
else:
    print("使用类型名判断对象类型是否特定类型:", "no")

if type(l) == list:
    print("使用类型名判断对象类型是否特定类型:", "yes")

# 使用类名称判断对象实例是否属于特定类
if isinstance(f, _io.TextIOWrapper):
    print("使用类名称判断对象实例是否属于特定类:", "yes")
