import re

if __name__ == '__main__':
    search_string = 'text/plain; charset="utf-8"; format="fixed"'
    search_string2 = 'text/html; charset=utf-8'

    result1 = re.search(r'charset="\S+"', search_string)
    result2 = re.search(r'(?<=charset=").*?(?=")', search_string)  # 使用前置条件(?<=) / 后置条件(?=)筛选出需要的字符串
    result3 = re.search(r'(?<=charset=)\S+', search_string2)
    result1.group(0)

    print(result1)
    print(result2)
    print(result3)

