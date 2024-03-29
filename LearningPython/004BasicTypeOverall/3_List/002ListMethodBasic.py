"""
列表除了是序列之外也是一种特立的数据类型，所以可以使用序列的方法之外，实际上也有它自己特有的方法
"""

l1 = [1, "test", (3, 4)]
l2 = [8, 6, 5, 7]

# 追加元素
l1.append(9)
print("追加元素:", l1)

# 取出元素(取出后同在列表中删除该元素)
print("取出元素:", l1.pop(3))
print("取出元素后:", l1)

# 移除指定的元素项
l.remove(1)  # 从列表中移除值为1的元素
print("移除元素项:", l1)

# 插入元素到指定位置
l1.insert(0,1)  # 在位置0插入值为1的元素
print("插入元素到指定位置:", l1)

# 列表排序
l2.sort()
print("列表排序:", l2)

# 列表反转
l2.reverse()
print("列表反转:", l2)
