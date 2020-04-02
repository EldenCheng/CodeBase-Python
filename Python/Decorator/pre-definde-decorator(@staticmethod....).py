"""
Python中是没有公有成员与私有成员的, 但是，有时候又需要保护一些类的字段而需要写get / set方法,

那我们可以写一个简单的方法return一个字段,然后在这个方法上@property decorator, 在添加了@property decorator之后, 这个方法对应的

setter, getter与deleter就会被自动创建, 如果对应的方法都创建了的话,在类的实例获取 / 设置对应字段的值时,

Python会自动调用写好的get方法或者set方法来实际而不是直接返回字段值
"""


class PropertyTest:

    from_outside = None
    _field = 0

    def __init__(self, value):
        self.field = value
        pass

    @property
    def field(self):
        return self._field  # 要注意实际存放数据的变量名要与property的方法名不一样, 不然会导致死循环出错

    @field.setter
    def field(self, value):  # 注意无论getter, setter还是deleter的方法名都要要与@property的方法名一致
        if isinstance(value, int):
            self._field = self._field + value
        else:
            raise TypeError

    @field.getter
    def field(self):
        if self._field < 10:
            return self._field + 10
        else:
            return self._field

    @field.deleter
    def field(self):
        self._field = 0

    '''
    python中的@classmetho的作用是不用实例化类都可以调用这个方法, 而且还有一个cls指针是指向当前类的
    所以类方法的用途大概有如下:
    1. 在类初始化之前有些初始化参数需要先处理
    2. 某些设计模式需要
    3. 由于classmethod是在类的实例外面运行的, 所以可以避开一些类实例的某些逻辑
    '''

    @classmethod
    def create_method(cls, value):
        if isinstance(value, int):
            # 这句话写入后, 所有属于这个类的实例中对应的字段都会是被修改,实际作用就是约等于Jave的类静态变量
            cls.from_outside = "It is set from a classmethod"
            # 由cls是类的指针,所以cls()就等于是PropertyTest(), 这句的作用是实例化PropertyTest并返回
            return cls(value)
        else:
            raise TypeError

    @staticmethod
    def print_words():
        print("This is a static method!")


if __name__ == '__main__':

    p1 = PropertyTest.create_method(1)
    p2 = PropertyTest(0)

    print(p1.from_outside)
    print(p1.field)
    print(p2.from_outside)
    print(p2.field)
    p1.field = 50  # 触发setter
    print(p1.field)
    del p1.field  # 触发deleter
    print(p1.field)
    print(PropertyTest.from_outside)
    PropertyTest.print_words()










