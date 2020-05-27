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
strs = "123"
print(int("123") + int(strs))

# 字符串转换为浮点数
print(float("123") + float(strs))

# 字符串转换为ascii格式bytes
print(bytes(strs, encoding='ascii'))

# 字符串转换为utf-8格式bytes
print(bytes(strs, encoding='utf-8'))

# 将bytes转换成ascii/utf-8字符串

bytes_char = bytes('1234', encoding='ascii')

strs_ascii = bytes_char.decode(encoding='ascii')

strs_utf8 = bytes_char.decode(encoding='utf-8')

print(strs_ascii)
print(strs_utf8)

