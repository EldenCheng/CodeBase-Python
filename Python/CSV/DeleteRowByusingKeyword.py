csvfile1 = open('ResultsTC1.csv', 'r')        # 采用b的方式处理可以省去很多问题
csvfile2 = open('ResultsTC1.jtl', 'w')


# Python中如果想删除有相对关键字的行时，使用标准CSV库会比较麻烦，
# 但CSV本身就是一种文本文件，所以用处理文本文件的方法来实现比较快

# 按行读取整个CSV
lines = csvfile1.readlines()

# 逐行写回去，如果该行有对应关键字则不写
# 这里试过用csv.writer.writerows()方法，不知为什么会逐个字符写入当一行而不是一下整行
for line in lines:
    if line.find("BeanShell Sampler") != -1:
        pass
    else:
        csvfile2.write(line)