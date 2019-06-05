"""
布尔值实际上使用True代表非0, False代表0
而实际上Python内部定义来说, 实际True的值是1, False的值是0
"""

if __name__ == "__main__":
    list1 = []
    list2 = [1, 2, 3]
    list3 = list()
    print("非空的列表在布尔判断中就是True: ", bool(list2))
    print("空的列表在布尔判断中就是False: ", bool(list1))
    print("空的列表在布尔判断中就是False: ", bool(list3))

    # 当然布尔值是支持逻辑运算的
    print(1 < 2)
    print(0 == 1)

    print(True + 1)  # 由于True的内部值是个int 1, 所以能做运算就不出奇了
