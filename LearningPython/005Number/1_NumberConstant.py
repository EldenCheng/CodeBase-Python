"""
1. Python中，数字可以是整数（包括二进制整数，八进制整数，十六进制整数），浮点数，复数
2. Python中，数字的长度只受内存大小的限制，即实际上没有了诸如32位int是-2147xxx - 2147xxx这样的限制了
3. Python中，数字实际上一创建了就会在内存中分配位置，并且创建后就不能修改的，所以实际上这些数字都是一个常量
   但如果将数字赋值到变量时，修改变量的值，后台会根据情况在另一个内存位置新创建另一个数字常量然后再将新数字常量赋值到
   变量，或者先摧毁原有内存位置旧的数字常量，再创建新的数字常量
4. 为解决浮点数精度不够的情况，Python特地为小数与分数引入了两个专门的小数类与分数类来处理小数与分数
   这两个类与纯浮点数的不同在于小数与分数是有固定精度的，这会令这两个类型比直接浮点数更精确
"""
# 十进制整数
print("负整数", -12359)
print("正整数", 12359)
print("大整数", 999999999999)

# 八进制整数，要在数字前面加数字0然后加字母o
print("负八进制整数", -0o1235)
print("正八进制整数", 0o1235)
print("大八进制整数", 0o777777777777)

# 二进制整数，要在数字前面加数字0然后加字母b
print("负二进制整数", -0b101010101)
print("正二进制整数", 0b1010101010)
print("大二进制整数", 0b1111111111111111111111111111111111)

# 十六进制整数，要在数字前面加数字0然后加字母x
print("负十六进制整数", -0xabc)
print("正十六进制整数", 0xabc)
print("大十六进制整数", 0xabcdefabcdef)

# 十进制，二进制，八进制，十六进制整数之间的转换
print("十进制转二进制", bin(99))
print("十进制转八进制", oct(99))
print("十进制转八进制", hex(99))
print("二进制转十进制", int("0b1100011", 2))  # 注意int方法接收的参数是str
print("八进制转十进制", int("0o143", 8))
print("十六进制转十进制", int("0x63", 16))
print("又或者，十六进制转十进制", int("63", 16))
print("使用str方法，默认输出的字符串会变成十进制数", str(0x63))

# 浮点数
# 好像只支持十进制浮点数
print("普通浮点数", 1.2359)
print("科学记数法浮点数1", 1.2359E10)
print("科学记数法浮点数2", 1.2359E-10)
print("科学记数法浮点数3", 1.2359e-10)

# print("十六进制浮点数", 0x1.2359e10) #这个会出错，不能这样写

# 复数
print("复数整数", 3+4j)
print("复数浮点数", 3.5+4.1j)
print("纯复数", 4j)
print("使用内置方法complex(real, imag)来创建复数", complex(3, 4))

# 小数类型
from decimal import Decimal
print("浮点数有时候结果不够精确: ", 0.1+0.1+0.1-0.3)
print("小数类型比浮点数精确: ", Decimal("0.1")+Decimal("0.1")+Decimal("0.1")-Decimal("0.3"))
print("创建后的小数的数据类型是：", type(Decimal("0.1")))

# 设置小数位数
import decimal
print("设置小数位数前：", decimal.Decimal('1')/decimal.Decimal('7'))
decimal.getcontext().prec = 4
print("设置小数位数后：", decimal.Decimal('1')/decimal.Decimal('7'))

# 小数可以参加正常的数值运算
x = Decimal("0.1")
y = Decimal("0.3")
print("小数的加", x+y)
print("小数的乘", x-y)
print("小数的乘方", y**2)

# 分数类型
from fractions import Fraction
print("使用x/y的形式创建分数:", Fraction(1, 2))
print("使用小数的形式创建分数:", Fraction(0.5))

# 分数也可以参加正常的数值运算
x = Fraction(1, 2)
y = Fraction(1, 7)
print("分数数的加", x+y)
print("分数数的乘", x-y)
print("分数数的乘方", y**2)






