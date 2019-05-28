'''
字典不是序列，所以序列能使用的方法字典是不一定能使用的
'''

d = {"food": "Egg", "num": 4, "proudct": ["GD","GZ"]}

# 求长度
print(len(d))

# 返回键的合集，由于返回的是一个dict_key对象，所以要选将它转换为列表或者集合，才能访问具体内容
keys_list = list(d.keys())
keys_set = set(d.keys())
print("字典键值列表:", keys_list)
print("字典键值集合:", keys_set)


# 返回值的合集，由于返回的是一个dict_values对象，所以要选将它转换为列表或者集合，才能访问具体内容
values = d.values()
values_list = list(values)
try:
    valuse_set = set(values)
except Exception as msg:
    print("如果字典的值里包含列表，则不能转换为集合:", str(msg))
print("字典值列表:", values_list)

# 使用sorted方法对字典的键进行排序
d2 = {1: "a", 3: "c", 2: "b"}
print("使用sorted方法对字典的值进行排序:", sorted(d2))

# 使用get方法来获取值
# get方法可以指定一个缺省值，如果找不到对应的key，就会返回缺省值而不是返回None
key = d2.get(4, "d")
print("使用get方法来获取值:", key)


