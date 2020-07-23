"""
经过实验可知, 实际上exec方法中的global参数是用于将当前运行环境中的变量带入exec运行环境中去的
而如果不显式指定global, exec方法会默认使用globals()来获取所有当前环境中的变量
所以这里的所谓global参数内的指定的变量也是要遵守变量作用域的, 不是写入里面就自动变成exec运行块里的global变量
"""
"""
而local参数的作用是把exec运行块里产生的对象, return的变量带出来, 一般来说如果不显式指定的话会默认使用locals()
即把exec运行块中产生的对象自动加载到当前环境中
"""

if __name__ == '__main__':
    l1 = {}
    l2 = {}
    l3 = {}
    global driver
    driver = "Outside"
    # 这里globals就会把l1, l2, l3, driver都带入到exec运行真里
    # 而l1将会把import的结果带出来(), 即把Test53 module带了出来
    # 当然, 这里如果不指定l1, 实际上Test 53 module会被locals()隐式带出来
    # 后面的code可以直接用, 现在使用了l1带出来的话, 后面的code就只能通过l1去访问Test53 module了
    exec("from Python.Exec.import_module import Test53", globals(), l1)

    # exec("g = {'Test53': l1['Test53']}", l2)
    # driver = "Outside dirver"
    # 这里指定了g作为global参数而不是使用默认的globals(), 所以如果不把刚刚import的Test53 module显式引入
    # exec运行块将会找不到Test 53 module
    # 当然return_value也会被l2带出到当前环境
    g = {'Test53': l1['Test53'],
         'driver': driver}
    exec("returen_value = Test{0}().test_start(driver)".format("53"), g, l2)
    print(l1)
    # print(l2)
    # exec运行块多于一行的可以使用\n换行
    # 如果不指定任何参数, 就会自动带出带入当前环境的变量, 对象等等
    exec("print(l2)\n"
         "x = 3 + 2")
    print(x)


