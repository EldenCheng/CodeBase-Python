# 数字转换为字符串
intNum = 123

print(str(intNum))

# 将字符转变为编码，会自动使用unicode

print(ord('c'), ord('我'), ord('ぬ'))

# 将编码转变为字符

print(chr(intNum), chr(99), chr(25105), chr(12396))

# 将常见的unicode编码格式转变为字符

uni = '\u4e2d\u6587'

print(uni)

# 将字符转换成对应编码
a = "Unicode转换"

print(a.encode('utf-8'))

print(a.encode('gb2312'))

# 将字符转换为其它编码
# 由于Python内部使用unicoe，所以UTF-8转其它不用decode

gb2312 = a.encode('gb2312')

utf = gb2312.decode('gb2312').encode('utf-8')

print(utf)

# 将编码转换回字符
print(gb2312.decode('gb2312'))

# 字符串转换为十进制数字
str = "123"
print(int("123") + int(str))

# 字符串转换为浮点数
print(float("123") + float(str))
