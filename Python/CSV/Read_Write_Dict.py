import csv

#Read the file
csvfile1 = open('Test.csv', 'r')        # 采用b的方式处理可以省去很多问题
csvfile2 = open('Test1.csv', 'w')

# 获得的对象是字典，可以通过关键字访问而不能通过下标访问
dictreader = csv.DictReader(csvfile1, fieldnames=None)

csv = []

# 不能直接使用下标访问一个迭代器(就像一种特殊的链接表，只知道后一个，不知道前一个)
#
#for row in dictreader:
#    print(row)

# 使用Next访问

header = next(dictreader)

print(header)

# 一样可以先转化为List
csv = list(dictreader)

print(csv[0]['ID'], csv[3]['PW'])
