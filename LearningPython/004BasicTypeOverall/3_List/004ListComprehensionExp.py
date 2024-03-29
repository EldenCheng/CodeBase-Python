"""
在列表的操作中，Python还包括一个更高级的操作，被称为列表解析表达式
这个操作可以用来获取列表中的某个元素，或者用来创建一个列表
实际上这个操作是依靠Python中的序列的下标都可以接受表达式和语句来实现的
所以列表，集合，字典都可以使用下面的解析表达式，它们之间甚至可以通过解析表达式互换
"""

l1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# 方便地从每个元素中获取特定位置的元素
col = [row[1] for row in l1]  # 这个表达式的意义是：遍历二维列表，从每一个一级元素中获得二级的第二个元素，然后组成一个新的列表
print("方便地从每个元素中获取特定位置的元素:", col)

# 还可以对获取到的元素进行一定运算或者使用条件语句判断进行一定筛选
col = [row[1] + 1 for row in l1]  # 对获取到的元素+1
print("对获取到的元素进行运算:", col)

col = [row[1] for row in l1 if row[1] % 2 == 0]  # 使用条件判断对获得的元素进行筛选
print("使用条件判断对获得的元素进行筛选:", col)

# 按顺序汇总各项
total = [sum(row) for row in l1]
print("按顺序汇总各项:", total)

# 使用解析表达式从列表生成字典
d = {i: sum(l1[i]) for i in range(3)}
print("使用解析表达式从列表生成字典:", d)

