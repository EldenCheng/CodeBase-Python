import time
import datetime

"""
无论time与Date中，都有一个strftime方法，作用是格式化输出日期与时间
%Y  Year with century as a decimal number.
%m  Month as a decimal number [01,12].
%d  Day of the month as a decimal number [01,31].
%H  Hour (24-hour clock) as a decimal number [00,23].
%I  Hour (12-hour clock) as a decimal number [00,12].
%M  Minute as a decimal number [00,59].
%S  Second as a decimal number [00,61].
%p  either AM or PM. [AM,PM]
%f  Millisecond as a decimal number [000000,999999]. but this may not support in most of the platform

%z  Time zone offset from UTC.

%a  Locale's abbreviated weekday name.
%A  Locale's full weekday name.
%w  Weekday as a decimal number, 0 is Sunday and 6 is Saturday.

%b  Locale's abbreviated month name.
%B  Locale's full month name.

%c  Locale's appropriate date and time representation.
%I  Hour (12-hour clock) as a decimal number [01,12].
%p  Locale's equivalent of either AM or PM
"""

if __name__ == '__main__':

    print(time.strftime("%Y-%m-%d", time.localtime()))
    print(time.strftime("%H:%M:%S", time.localtime()))
    # 由于很多平台中的strftime不支持格式化字符%f, 所以如果我们要显示Millisecond
    # 而又在Python 3.6之后, 可以在要显示Millisecond的地方使用time.time_ns()%1000
    print(time.strftime(f"%H:%M:%S.{time.time_ns() % 1000}", time.localtime()))

    # 当前日期加n日
    print(datetime.datetime.now())
    nextWeek = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    next_hour12 = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%I:%M %p')
    next_hour24 = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%H:%M')
    print(nextWeek)
    print(next_hour12)
    print(next_hour24)
