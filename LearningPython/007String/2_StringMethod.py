
if __name__ == "__main__":

    # replace方法
    # 由于字符串属于不可改变类型，所以replace之后的字符串已经是一个新变量了，所以要记得重新赋值
    s1 = "1234567890"
    s1 = s1.replace("0","9")
    print("replace方法:", s1)

    # find方法如果能找到就返回下标，从0开始计算，找不到就返回-1
    print("find方法返回下标:", s1.find("1"))

    # 将字符串转化为列表
    # 由于字符串本身属于不可改变类型，但又有时真的需要对某些元素作出更改，这时可以先把字符串转化为列表(list)，就可以修改
    # 其中的元素

    l1 = list(s1)
    print("将字符串转化为列表：", l1)

    # 将列表转化为字符串
    # 我们使用一字符串方法将一个列表合成一个字符串
    s2 = "".join(l1)
    print("将列表转化为字符串: ", s2)

    # join方法
    # join方法是使用分隔符把目标的迭代器(元组，列表，集合)的元素连接起来后生成一个字符串
    # join方法是split方法的反方法
    l2 = ("2018","07","03",)
    s3 = "-".join(l2)
    print("join方法把列表的元素合成一个字符串: ", s3)

    # split方法
    # split方法是把一个字符串按照分隔符来拆分成一个列表
    l3 = s3.split("-")
    print("split方法把一个字符串拆分成一个列表: ", l3)
