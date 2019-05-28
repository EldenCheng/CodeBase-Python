

s = "   Hello World   "

#去除左空格

print(s.lstrip())

#去除右空格

print(s.rstrip())

#去除两边空格
print(s.strip())

#去除所有空格
s = ''.join(s.split())

print(s)