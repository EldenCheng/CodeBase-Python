
# Print String
print("Try to print with a string %s" %  "Test String")

print("Try to print with a string list %s & %s" %  ("Test String1","Test String2"))

String = "This is a string"
print("Try to print a string Var: %s" % String)

#Print int

print("This is an int: %d" % 10)

# Print int with a specify width, can be used in every format print
# %[(name)][flags][width].[precision]typecode
# flags可以有+,-,' '或0。+表示右对齐。-表示左对齐。
# ' '为一个空格，表示在正数的左侧填充一个空格，从而与负数对齐。0表示使用0填充。

print("This is an specify width int: %04d" % 10)

#Print float

print("This is a float: %f" % 1.85)

print("This is a float which limited the digital: %.2f" % 1.85)

#Print bin

# print("This is an bin number: %b, it will auto change from dec number" % 10) # fail

#Print oct
print("This is an ocr number: %o, it will auto change from dec number" % 10)

#Print hex
print("This is an hex number: %x, it will auto change from dec number" % 10)

#Print raw data

print("This is a string raw data: %r" % "C:\windows")

print("This is an int raw data: %r" % 10)

print("This is an float raw data: %r" % 1.85)

#使用f string来格式化字符串
#f string就是在字符串前面加f 或者 F，然后在字符串在使用花括号{}，花括号里可以使用变量，常量，表达式等
#生成字符串时会自动替换成对应的内容
one =1
two =2
s = f"This is {one}, and {two}"
print(s)
