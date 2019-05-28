'''
#在一个目录下面添加一个__init__.py文件，就算空白也可以，之后就可以使用from folder.file name import classname这样的方式导入
#要从项目的根目录开始算，如下
'''
from Python.String.ImportExample import Example

Example()
'''
#上面这个情况是__init__.py文件内容为空的情况，实际上我们可以在__init__.py里面填写一些Script
#常用的就是在__.init__.py文件时把文件名引入一下，那么在主文件的时候就只需要from folder import classname了
# 如例子的__init__.py文件里加上：

#from Python.Import_Library.ImprotExample import ToImport

#那么在使用包的Script就可以节省一级，如下
'''
from Python.Import_Library import ToImport

'''另外, 如果导入模块时, 模块里面有一些可以直接运行的语句时, 这些语句会直接运行'''

from Python.Import_Library import Use_exec_to_import_dyamic_library


