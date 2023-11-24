import csv

#  Read the file
csvfile1 = open('Test.csv', 'r')        # 采用b的方式处理可以省去很多问题

if __name__ == '__main__':
    # 获得的对象是一个迭代器, 迭代器中每一个元素就是一个字典
    # 迭代器不能直接使用下标访问元素
    dict_reader = csv.DictReader(csvfile1, fieldnames=None)

    # 但可以使用Next访问
    first_row = next(dict_reader)
    print("first_row: ", first_row)

    # 也可以使用for访问(就像一种特殊的链接表，只知道后一个，不知道前一个)
    # 注意迭代器不能重复访问同一元素, 只能按顺序一个一个访问
    for row in dict_reader:
        print("every row: ", row)

    csvfile1.close()

    # 可以先转化为List
    # 这样就可以使用下标来访问特定的元素
    # 同时可以多次访问而不用担心访问后元素会被删除
    csvfile1 = open('Test.csv', 'r')
    dict_reader = csv.DictReader(csvfile1, fieldnames=None)
    csv_dict_list = list(dict_reader)
    csvfile1.close()

    print(csv_dict_list[0]['ID'], csv_dict_list[3]['PW'])
    for row in csv_dict_list:
        print("every row: ", row)

    print(csv_dict_list)  # 列表不会被清空

