"""
字符串在Python里实际上是一个字符的序列，所以可以使用序列的操作
"""

s = "A String"

# 求长度

print("长度:", len(s))

# 使用索引返回元素

element = s[0]

print("第一个字符是:", element)

# 使用反向索引返回元素

element = s[-1]

print("最后一个字符是:", element)

# 使用分片操作返回一个子字符串

element = s[2:]

print("子字符串是:", element)

# 合并

s2 = " test"

s = s + s2

print("字符串合并:", s)

# 简单复制

s2 = s2 * 4

print("字符串复制:", s2)

