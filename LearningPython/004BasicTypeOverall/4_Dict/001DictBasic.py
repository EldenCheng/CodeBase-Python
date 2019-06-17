"""
Python中的字典不是序列，而是一种映射(mapping)
字典没有顺序，只能通过键来访问值
Python中的字典也是可变的，键对应的值可以被修改，字典本身的长度也可以变化
字典的键可以是数字，字符和对象，不能是列表，集合与字典，字典的值则可以是任意类型
"""

f = open("test.txt", "w")
t = (1,2,3,4)
l = [1,2,3,4]
s = {1,2,3,4}

d = {"food": "Egg", "num": 4, "proudct": ["GD","GZ"]}
d2 = {1: "One", 2: "Two"}
try:
    d3 = {d: d2, d2: d}
except Exception as msg:
    print("字典的键不能用字典，否则会出错: ", str(msg))

try:
    d4 = {l:d}
except Exception as msg:
    print("字典的键不能用集合，否则会出错: ", str(msg))
try:
    d5 = {s: d}
except Exception as msg:
    print("字典的键不能用列表，否则会出错: ", str(msg))

d6 = {f: d}

# 通过键访问字典的值
print("通过键访问字典的值:", d["food"])
print("通过键访问字典的值2:", d2[1])
print("通过键访问字典的值3:", d6[f])


# 下面会报错
try:
    print("通过下标访问字典的值:", d[0])
except Exception as msg:
    klass = msg.__class__
    arg = klass.args
    print("通过下标访问字典的值会出错:%s,%s" % (msg.__str__(), str(klass)))

# 可以修改字典中的值
d["num"] +=1
print("可以修改字典中的值:", d)

# 向字典中添加新的键和值
d["level"] = "High" # 直接写新的键与新的值，会自动添加到字典中
print("向字典中添加新的键和值:", d)

# 使用del方法来删除字典的键与对应的值
del d["level"]
print("使用del方法来删除字典的键与对应的值:", d)


