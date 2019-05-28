
# 日历模块
import calendar



# calendar() 获取指定年份的日历字符串
result = calendar.calendar(1990)
print("获取指定年份的日历:\n", result)


# month()获取指定月份的日历字符串
result = calendar.month(1990,7)
print("\n获取指定月份的日历:\n",result)

# monthcalendar()获取指定月份的信息列表
result = calendar.monthcalendar(1990,7)
print("\n获取指定月份:\n", result)


# isleap()  检测年份是否是润年  如果不是100的整数倍，能被4整除就是润年，如果是100的整数倍，能被400整除就是润年
result = calendar.isleap(1990)
print("\n检测年份是否是润年: ", result)

# leapdays()  检测指定年限内润年的数量
result = calendar.leapdays(1988,2020)
print("检测指定年限内润年的数量: ", result)

# monthrange()  获取指定月份的信息
result = calendar.monthrange(1990,7)
print("\n获取指定月份的信息:\n", result)

# weekday ()根据指定的年月日计算星期几
result = calendar.weekday(1990,7,22)
print("\n根据指定的年月日计算星期几:", result)

# timegm() 将时间元组转化为时间戳
tps = (1990,6,10,20,35,0,0,0)
result = calendar.timegm(tps)
print("将时间元组转化为时间戳:", result)
