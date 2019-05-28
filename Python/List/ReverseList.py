

l = [1,2,3,4,5,6,7,8]

#使用reverse方法直接反转全部
l.reverse()

print("使用reverse方法直接反转原list的元素", l)

#使用读取list元素，然后放到相反位置的方式反转，这个操作有个好处是可以顺便复制list而不是在原list上反转
l2 = [1,2,3,4,5,6,7,8]
l3 = l2[::-1]

print("原list", l2)
print("新list", l3)

l4 = [1,2,3,4,5,6,7,8]
l5 = l2[::2]

print("原list", l4)
print("新list", l5)
