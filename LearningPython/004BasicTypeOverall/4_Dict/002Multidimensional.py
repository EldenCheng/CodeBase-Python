'''
字典也可以多重嵌套的
'''

rec = {"name": {"first": "elden", "last": "elden"}, "job": ["dev","mgr"], "age": 40.5}

# 通过下标访问
print("通过下标访问:", rec["name"]["first"])
print("通过下标访问:", rec["job"][0])

# 元素也可以使用它们自己特有的方法

rec["name"]["first"] = rec["name"]["first"].upper()
rec["job"].append("hr")
print("元素也可以使用它们自己特有的方法:", rec["name"]["first"])
print("元素也可以使用它们自己特有的方法:", rec["job"])