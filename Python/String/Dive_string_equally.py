"""
按指定长度等分字符串
"""

import re


def cut_text(text, length):
    """
    按长度等分字符串
    :param text: 需要被等分的字符串
    :param length: 每隔多长做等分
    :return: 等分后的字符串列表
    """
    textarr = re.findall('.{'+str(length)+'}', text)
    textarr.append(text[(len(textarr)*length):])
    return textarr


if __name__ == '__main__':
    s = "6175746F"
    after = cut_text(s, 2)
    for a in after:
        print(a)
