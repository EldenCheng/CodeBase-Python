#-*-coding=utf-8-*-

'''
时间戳与字符串的互相转换
'''

import time

localtime1=time.localtime()
#time.sleep(5)
localtime2=time.localtime(time.time())

#print(type(localtime1),localtime1)
#print(type(localtime2),localtime2)
print(localtime1)
print(localtime2)

gmtime=time.gmtime(time.time())
#print(type(gmtime),gmtime)
print(gmtime)

strtime = time.strftime("%Y/%m/%d_%H%M%S", time.localtime())

print(strtime)

strtime1='20160518010101'
strtime2='20160518020101'

#字符串变成时间数据结构
localtime1=time.strptime(strtime1,'%Y%m%d%H%M%S')
localtime2=time.strptime(strtime2,'%Y%m%d%H%M%S')

print(localtime1)
print(localtime2)


#从时间数据结构转换成时间戳
time1= time.mktime(localtime1)
time2= time.mktime(localtime2)

print(time1)
print(time2)

#时间戳可以直接相减，得到以秒为单位的差额
print(time2-time1)