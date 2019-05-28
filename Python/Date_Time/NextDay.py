import time

SEC_OF_DAY = 86400

assert_time = "00:00"

# To exchange the structed time back to time stamp for counting
def time_exchange(ex_time):
    ex_time = time.strptime(ex_time, "%Y/%m/%d_%H:%M:%S")
    ex_time = time.mktime(ex_time)
    return ex_time


# Set the begin time to 11:00am of today
b_time = time_exchange(time.strftime("%Y/%m/%d", time.localtime()) + "_11" + time.strftime("%M%S", time.localtime()))
# Set the end time to 3:01pm of today
e_time = time_exchange(time.strftime("%Y/%m/%d", time.localtime()) + "_1501" + time.strftime("%S", time.localtime()))
current_day = time_exchange(time.strftime("%Y/%m/%d", time.localtime()) + "_000000")
current_day_time = time_exchange(time.strftime("%Y/%m/%d_%H:%M:%S", time.localtime()))
next_day = time_exchange(time.strftime("%Y/%m/%d", time.localtime(current_day + SEC_OF_DAY)) + "_00:00:00")

next_day_with_assert_time = time_exchange(time.strftime("%Y/%m/%d", time.localtime(current_day + SEC_OF_DAY)) + "_" + assert_time+ ":00")

print(next_day - current_day)

