import math
"""
Python支持C所支持的多数数学方法包括：
1. 数学数量，如
   math.pi, math.e
2. 三角函数
   math.sin
3. 方根
   math.sqrt
4. 取整的的不同方法
   a. math.floor: 向下求整
   b. math.trunc: 直接只取整数部分
也直接内置了一部分数学方法：
1. 幂
   pow
2. 绝对值
   abs
3. 最大/最小值，和
   min, max, sum
4. 取整的不同方法
   a. int: 只取整数部分
   b. round: 四舍五入
"""
# math.floor与math.trunc的不同:
print("math.floor在正数中使用: ", math.floor(2.567))
print("math.floor在负数中使用: ", math.floor(-2.567))

print("math.trunc在正数中使用: ", math.trunc(2.567))
print("math.trunc在负数中使用: ", math.trunc(-2.567))

# 最大/最小值与和需要传入一个序列tuple作为参数
t = (1,2,3,4,5)
print("最大值：", max(t))
print("最小值：", min(t))
print(print("和：", sum(t)))

# 四舍五入round的使用
print("默认的round方法是取到整数:", round(2.567))
print("round方法可以指定小数位:", round(2.567,2))