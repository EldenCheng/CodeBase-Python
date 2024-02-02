
if __name__ == '__main__':
    '''
    Python 3.6 在PEP 526 中引入了用于注释变量的语法 ，我们在大多数示例中使用它。
    如果赋予一个错误的类型, 编译器会有warning, 不过仍然能运行不会报错误
    '''
    num: int
    num = 10
    num = "An error"
    print("最终变量的值是: ", num)

