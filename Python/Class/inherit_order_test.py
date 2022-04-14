"""
有时候我们会建立一个继承了多个超类的类, 但如果不同的超类里, 有同名的方法, 而子类又没有重写这个方法时
到底使用子类调用这个方法时, 是使用哪一个超类的方法呢, 这里就涉及一个Python的方法(模块)解释顺序(Method Resolution Order)
的问题了;
根据Python的作者对相关问题的回答, Python的MRO的原则是是按照参数列表中的从左到右的顺序的, 比如下面的例子中
子类定义时定义超类的顺序是Second, Third 所以如果调用一个子类的方法时, 会从下列顺序查找:
        1. 先从子类本身的方法列表中查找
        2. 如果子类本身没有定义这个方法, 则从第一个超类(排在超类列表的左边)定义的方法查找
        3. 第一个超类中没有找到这个方法, 则从第二个, 第三个, 第N个超类定义的方法查找
        4. 如果子类的超类也没有找到, 就从超类的超类(爷爷类)中, 按上述的顺序查找
        5. 都没有找到, 就从所有类的父类Object中查找
        6. 还没有找到, 就报找不到
"""


class First:
    def __init__(self):
        print("Init First")

    def differnt1(self):
        print("First")

    def same(self):
        print("First")


class Second(First):
    def __init__(self):
        print("Init Second")

    def differnt2(self):
        print("Second")

    def same(self):
        print("Second")


class Third(First):
    def __init__(self):
        print("Init Third")

    def differnt3(self):
        print("Third")

    def same(self):
        print("Third")


class Four(Second, Third):
    def differnt4(self):
        print("Four")


class Mix(Second, Third):
    def __init__(self, number):
        if number == 1:
            super(Mix, self).__init__()
        elif number == 2:
            super(Second, self).__init__()
        elif number == 3:
            super(Third, self).__init__()


if __name__ == '__main__':
    f = Four()
    '''
    调用same方法时, 由于Four类本身没有same方法, 所以会按照MRO顺序先从Second中查找
    '''
    f.same()

    '''
    调用different4方法时, 由于Four类本身有different4方法, 所以会按照MRO顺序先从本身的方法中查找
    '''
    f.differnt4()

    """
    当我们调用超类的__init__方法时, 默认也是遵从MRO顺序的, 所以如果用通常形式指定, 实际上调用顺序是:
        1. 最左边的超类的__init__方法, 比如Second有的话, 就是Second的
        2. 如果左边没有, 就第二个, 第三个, 或者第N个, 
    """
    """
    但实际上使用的时候, 我们可以把super(Mix, self)里的Mix替换掉, 如果替换掉的话, 经过测试就是不再查找被替换
    的超类之前的__init__方法, 比如把Mix替换成Second, 因为根据MRO, 查找顺序是Mix, Second, Third, First,
    所以把Mix替换成Second之后, 查找会从Third开始, 而不再查找Mix, Second类中的__init__方法
    """
    '''
    比如下面例子中, 如果直接调用super(Mix, self).__init__(), 会调用Second的__init__方法
    而如果把Second的__init__方法注释掉, 就会变成调用Third的__init__方法
    '''
    mix2 = Mix(1)
    '''
    比如下面两个例子, 如果super中分另把Mix替换成Second和Third, 则实际查找__init__方法时会忽略MRO中
    指定的类与之前的类
    '''
    mix3 = Mix(2)
    mix1 = Mix(3)
    '''
    但实际上, 子类中指定使用哪一个__init__方法, 不影响它继承其它超类的方法
    比如下面的例子使用了Third的__init__方法, 但对应的子类仍然可以调用Second类的独有方法
    注, mix1使用的是First类的__init__方法, mix2使用的是Second类的__init__方法
    '''
    mix1.differnt3()
    mix2.differnt3()
    mix1.same()
    mix2.same()



