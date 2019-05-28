import sys

#sys.modules是一个字典,包含了当前可导入模块的路径信息,key是模块名称,value是对应模块的路径
print("当前可导入模块的名称: ", sys.modules.keys())
print("os模块的属性: ", sys.modules["os"])

#内置模块可以在sys.builtin_module_names处查询
print("内置模块的名称: ", sys.builtin_module_names)

#导入模块时,Python会有一个模块路径列表,这个路径列表就存储在sys.path中
#当然我们也可以添加,修改,删除sys.path中的记录以达到将我们想要的路径加入/移出模块路径列表中的目的

print("模块路径列表: ", sys.path)

sys.path.append("d:/testing")
print("更新后的模块路径列表: ", sys.path)

print("当前运行的py文件名(包括完整路径), 基本等同于__file__: ", sys.argv[0])

