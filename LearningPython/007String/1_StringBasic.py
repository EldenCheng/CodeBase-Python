"""
字符串是一个序列, 所以它可以支持所有序列方法
但字符串本身是一个不可变常量, 所以对字符串的修改操作都是生成另一个新的字符串对象
"""

if __name__ == "__main__":

    s1 = ''  # 空字符串

    print(bool(s1))  # 空字符串与空列表一样,逻辑上是False

    s2 = "I say 'Hello world'"  # 引号套用

    s3 = "I say \"Hello world\""  # 使用转义字符

    s4 = """三重引号字符串"""  # 一般用于多行注释

    s5 = r"c:\windows"  # 字符串raw模式, 会自动尝试将Python不支持的字符转义为支持的字符

    print(s5)

    s6 = b"A"  # 使用二进制存储字符串

    print(s6)

    s7 = "I say " + "'Hello world'"  # 字符串合并

    print(s7)

    s8 = "Hello" * 3  # 字符串重复

    print(s8)

    print(s8[0])  # 使用下标访问字符

    print(s8[0:5])  # 字符串分片
