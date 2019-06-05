"""
map()是Python的内置方法, 主要参数有两个, 第一个参数是一个方法的指针f, 第二个是可迭代的列表或者元组
它的作用是会逐一将列表或者元组里的元素作为f的参数调用f,然后把结果输出为一个列表

一般来说map()方法的用途很多都是将某一个列表里的所有元素转换成某种形态, 或者特殊排序之类
"""


def add_one(number):
    return number + 1


def suffix(file_name: str):
    return file_name.split(".")[1].upper()


if __name__ == "__main__":
    inputs = (1, 2, 3, 4, 5, 6, 7)

    result = map(add_one, inputs)

    print(result)  # inputs元组里的所有元素都会加1, 但要注意的是result与inputs元组还是相互独立的
    print(list(result))  # 由于result是map对象, 而map对象是一个迭代器, 是不能直接访问元素的, 所以可以将它转换成列表

    result = map(add_one, inputs)
    print(result.__next__())  # 又或者用迭代器方法__next()__逐一读取

    files = ("a.com", "b.bat", "c.jpg")
    suffixs = list(map(suffix, files))
    print(suffixs)

    # 如果方法f需要有多个参数, 实际上可以传对应多个迭代器
    l2 = map(lambda x, y: x ** y, [1, 2, 3], [1, 2, 3])
    print(list(l2))

    # 当然与传参进方法是一样, 参数过少或者过多都会出错
    try:
        l3 = map(lambda x, y: (x ** y, x + y), [1, 2, 3])
        print(list(l3))
    except Exception as msg:
        print(msg)

    try:
        l3 = map(lambda x, y: (x ** y, x + y), [1, 2, 3], [1, 2, 3], [1, 2, 3])
        print(list(l3))
    except Exception as msg:
        print(msg)

    # 但如果传入的迭代器元素个数不一致的话, 以最短的那一个为基准
    l4 = map(lambda x, y: (x ** y, x + y), [1, 2, 3], [1, 2])
    print(list(l4))

    # 如果传入的迭代器元素类型不一样的话, 而又没有在方法中作专门的处理的话, 会报错
    try:
        l4 = map(lambda x, y: (x ** y, x + y), [1, 2, 3], [1, 2, '3'])
        for i in l4:
            print(i)
    except Exception as msg:
        print(msg)

    l5 = map(lambda x, y: (x ** int(y), x + int(y)), [1, 2, 3], [1, 2, '3'])
    print(list(l5))
