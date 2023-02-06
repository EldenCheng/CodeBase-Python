if __name__ == '__main__':

    '''
    新增字符串函数
    虽然字符串函数没有其他新特性那么强大，但字符串作为开发中使用最频繁的数据类型，这里也需要提一下他的改变。
    新版本中添加了移除前缀removeprefix()和后缀removesuffix()的两个字符串函数
    '''
    test_string = "./script/ios/regression/lumalou/test_123456.py"
    test_string_remove_prefix = test_string.removeprefix("./")
    print("移除字符串前缀: ", test_string_remove_prefix)
    test_string_remove_suffix = test_string.removesuffix(".py")
    print("移除字符串后缀: ", test_string_remove_suffix)
