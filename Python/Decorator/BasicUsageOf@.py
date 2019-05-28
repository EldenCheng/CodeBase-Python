from threading import Thread
import time

'''
@修饰符的基本用法1:

直接在修饰器内部直接调用被修饰的方法,这种用法实际上无什么意义吧

等价于:
def funB(txt)
    print(txt)

funB=funA(funB(txt))

注意,在运行到@funA修饰符的时候,修饰器里的内容就会自动运行了

'''
print("Part 1 Start")

def funA(arg):
    print('Code in decorator is executed at once')
    arg("Call inside the decorator with new args")
    return arg  #这个是隐式包含了的

@funA
def funB(txt):
    print(txt)


funB("Call outside the decorator!")

'''
@修饰符的基本用法2:

在修饰器内部使用wrapper(这个名称可以随便改)

这里wrapper(*args)的参数列表所获得的就是funD中的参数

等价于:
def funD(txt1, txt2)
    return txt1 + txt2 

funD=funC(funD)(txt1, txt2)

其中, wrapper里,args[0]的值就是参数txt1, args[1]的值就是参数txt2

注意,而由于wrapperr的存在,修饰器里的内容是包含在一个方法里的,所以在运行到@funC修饰符时,wrapper的内容被定义但未被调用
当下面调用funD("Hello", " world!")时,wrapper的内容才会被调用

其实这种用法还未想到有什么用途
'''

print("Part 2 Start")

def funC(arg):

    def wrapper(*args):
        print(args[0] + args[1] + "!") #使用funD的参数
        print(arg(args[0], " world with wrapper in decorator")) #在修饰器内容调用原方法
    return wrapper


@funC
def funD(txt1,txt2):
    return txt1 + txt2


funD("Hello","world!")

'''
用于异步运行,这时候用修饰器的好处就是可以很清楚地在代码中告知下面的方法将会是怎样的运行状态
'''

print("Part 3 Start")


def async(arg):
    def wrapper(*args, **kwargs):
        thr = Thread(target = arg, args = args, kwargs = kwargs) #创建异步线程,将要运行的方法放入
        thr.start()                                              #开启线程
    return wrapper


@async
def funF(txt1, txt2, txt3):
    for i in range(5):
        print(txt1 + txt2 + str(i) + txt3)
        time.sleep(0.5)

for t in range(3):
    funF("Thread " + str(t), " The "," times")



