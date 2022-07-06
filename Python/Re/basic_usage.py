import re

if __name__ == '__main__':
    search_string = 'text/plain; charset="utf-8"; format="fixed"'
    search_string2 = 'text/html; charset=utf-8'
    search_string3 = "Cats are smarter than dogs"

    '''
    re.search 扫描整个字符串并返回第一个成功的匹配。如果一个成功匹配都没有, 则返回None
    '''
    result1 = re.search(r'charset="\S+"', search_string)  #
    result2 = re.search(r'(?<=charset=").*?(?=")', search_string)  # 使用前置条件(?<=) / 后置条件(?=)筛选出需要的字符串
    result3 = re.search(r'(?<=charset=)\S+', search_string2)
    no_result = re.search(r'(?<=charset!=").*?(?=")', search_string)
    result4 = re.search(r'(.*) are (.*?) .*', search_string3)
    # print(result1)
    # print(result2)
    # print(result3)
    # print(no_result)

    '''
    可以使用result.group({num})来获取匹配到的字符串, 以
    '''
    print(result3.group(0))  # 整个正则匹配到的字符串放在group(0)
    print(result3.group())   # 等于group(0)
    print(result3.groups())  # 没有子查询, 所以没有groups
    print(result4.group(0))  # 整个正则匹配到的字符串放在group(0)
    print(result4.group(1))  # 子查询匹配字符串1(有疑问, 待研究)
    print(result4.group(2))  # 子查询匹配字符串1(有疑问, 待研究)
    print(result4.group())   # 等于group(0)
    print(result4.groups())  # 子查询匹配字符串1, 2组成的元组(有疑问, 待研究)


