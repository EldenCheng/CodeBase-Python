import calendar
from calendar import Calendar

# 返回一周内各天的名称
c1 = Calendar() #不指定参数的话默认星期一(0 is Monday)
print("返回一周内各天的名称: ", list(c1.iterweekdays()))

c2 = Calendar(firstweekday=calendar.SATURDAY) #指定今天是星期六
print("返回指定周几后一周内各天的名称: ", list(c2.iterweekdays()))

# 返回指定年,月的所有天数,会自动加上月前与月后的天数来令到每周都不会缺少日期(比如10.31是周三,会补上11.1,11.2与11.3来补全这一周)
# 返回的迭代器是以datetime.date为元素
print("返回指定年,月的所有天数(datetime.date): ", list(c2.itermonthdates(2018,10)))

# 返回指定年,月的所有天数,不会自动加上月前与月后的天数来令到每周都不会缺少日期,缺少的天数为设为0
# 返回的迭代器是以int为元素
print("返回指定年,月的所有天数(int): ", list(c2.itermonthdays(2018, 10)))

# 返回指定年,月的所有天数,不会自动加上月前与月后的天数来令到每周都不会缺少日期,缺少的天数为设为0
# 返回的迭代器是以元组为元素, 元组里是(几号,星期x)这样
print("返回指定年,月的所有天数(tuple): ", list(c2.itermonthdays2(2018, 10)))

# 以周为单位返回指定年,月的所有天数,会自动加上月前与月后的天数来令到每周都不会缺少日期(比如10.31是周三,会补上11.1,11.2与11.3来补全这一周)
# 返回的列表是每七个datetime.date列表为元素
print("返回指定年,月的所有天数(tuple): ", c2.monthdatescalendar(2018, 10))



