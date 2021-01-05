
if __name__ == '__main_':
    file = open("d:/杭州.txt", "r", encoding="gb2312")
    content = file.read()
    file.close()
    utf8 = content.encode("utf-8").decode("utf-8")
    file = open("d:/杭州_utf8.txt", "w", encoding="utf-8")
    file.write(utf8)
    file.close()