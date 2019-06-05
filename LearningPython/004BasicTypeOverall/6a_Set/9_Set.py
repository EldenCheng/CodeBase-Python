"""
集合是Python 3新增加的一个数据类型, 实际表现类似无键的字典
集合是无序的, 所以不能使用下标去直接访问元素
但它的主要特点是支持集合的数字运算
"""


def add_one(number):
    return number + 1

if __name__ == "__main__":

    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    set3 = {1, 2, 3, 4, 5, 6, 7, 8}
    print("交集: ", set1 & set2)
    print("并集: ", set1 | set2)
    print("差异集: ", set1 - set2)
    print("子集: ", set1 < set3)
    print("超集: ", set3 > set1)
    print("元素是否存在: ", 1 in set3)

    # 以上的运算可以使用set的内置方法完成
    print("交集: ", set1.intersection(set2))
    print("并集: ", set1.union(set2))
    print("差异集: ", set1.difference(set2))
    print("子集: ", set1.issubset(set3))
    print("超集: ", set3.issuperset(set1))

    tuple1 = (10, 11)
    list1 = [12, 13]

    print("集合与元组的并集: ", set3.union(tuple1))  # 这里一定要使用集体的内置方法, 因为操作符 | 不支持不同类型的数据进行操作
    print("集合与列表的并集: ", set3.union(list1))

    # 另外如果使用一个字符串通过set()方法生成一个集合, 将会得到一个单字母的集合
    set3 = set("Testing")
    list1 = list("Testing")
    print("使用字符串生成集合: ", set3)  # 注意集合是无序的, 有可能生成的元素不一定按原来字符串的顺序
    print("使用字符串生成列表: ", list1)  # 注意列表是有序的, 生成的元素一定按原来字符串的顺序(其实字符串本身也可以看作是一个有序的列表了)

    try:
        print(set3[0])  # 不能使用下标访问元素
    except Exception as msg:
        print(msg)

    # 由于集合是不可变的, 所以不能使用列表, 字典与集合作为一个集合的元素
    # 集合的元素可以是数, 字符串, 指针(函数,对象), 表达式与元组
    try:
        set3 = set()
        set3.add({'key': 'value'})
    except Exception as msg:
        print(msg)

        set3.add(add_one)
        print("添加函数指针到集合: ", set3)

        set3.add(lambda x: x + 1)  # 实际上是等于添加表达式的结果到集合
        print("添加表达式到集合: ", set3)

    # 因为集合内部是使用Hash表存储的, 所以同一个值在一个集合里只能有一个
    # 当两个集合产生并集的时候, 相同的元素就只会保留一个
    # 或者往一个人集合添加一个已存在的元素值时, 实际上不会增加
    set5 = {1, 2, 3, 4, 5} | {3, 4, 5, 6, 7}
    print("具有相同元素的集合并集时相同的元素只保留一个: ", set5)
    set5.add(1)  # 并不会报错, 但也不会多出另一个元素1
    print("添加一个已存在的值同集合: ", set5)

    # 另外还有一些针对集合元素的操作
    set4 = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    set4.add(10)
    print("添加元素进入集合: ", set4)
    set4.remove(10)
    print("从集合删除元素: ", set4)
    set4.discard(10)  # 查找并删除元素, 如果存在这个元素, 元素会被删除, 如果不存在则不进行任何操作
    print("从集合查找并删除元素(元素不存在): ", set4)
    set4.discard(1)
    print("从集合查找并删除元素(元素存在): ", set4)
    print("从集合提取元素(先进先出)", set4.pop())
    print("从集合提取元素后", set4)
