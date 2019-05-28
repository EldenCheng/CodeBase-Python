from collections import namedtuple
import csv

#Read the file
csvfile1 = open('Test.csv', 'r')
csvfile2 = open('Test1.csv', 'w')
reader = csv.reader(csvfile1)

print(reader)


#for row in reader:
#    print(row)

# Python的for循环本质上就是通过不断调用next()函数实现的
# 所以在使用下面两种方法之前已经使用for循环做过遍历操作，就得不到任何结果

# 两种方式可以读取csv的值
# 第一种使用内置的Next函数逐行读取
header = next(reader)
row1 = next(reader)
print(header)
print(row1)

# 第二种将iterator直接转换为list
readerlist = list(reader)
print(readerlist)

'''
# 获得CSV文件的一些属性
reader = csv.reader(csvfile1)
print(reader.line_num)
dialect = reader.dialect

# 分隔符
print(dialect.delimiter)

# 结尾符，这里是默认的“\r\n”
print(dialect.lineterminator)

# 指定写入时使用的分隔符
writer = csv.writer(csvfile2, delimiter=':', quoting=csv.QUOTE_NONE)

writer.writerow(readerlist[0])
writer.writerow(readerlist[1])

#csvfile3 = open('Test1.csv', 'r')
reader2 = csv.reader(csvfile2, delimiter=':', quoting=csv.QUOTE_NONE)
print(reader2)
#for row in reader2:
#    print(row)

'''
