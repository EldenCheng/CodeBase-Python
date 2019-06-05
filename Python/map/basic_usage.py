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
