"""
无论是import ... 还是from ... import ... 当一个模块被引入时,它包含的script就会被执行
from ... import ... 与import不同之外在于from ... import ... 实际上是将被引用的模块代码复制到当前位置中
所以使用from ... import ...的话要注意被引用模块中的变量被当前script中的同名变量所覆盖
如果两个模块中有同名的类名, 变量名的话, 应该使用import ... 而不是from ... import ...
"""
from imp import reload
import time

if __name__ == "__main__":

    import Python.String.Import_From_Example

    print(Python.String.Import_From_Example.title)  # 由于import只是指明了模块所在的路径, 所有如果要访问模块中的内容的话需要完整路径

    time.sleep(1)

    print(Python.String.Import_From_Example.current_time)

    time.sleep(1)

    print(Python.String.Import_From_Example.current_time)

    reload(Python.String.Import_From_Example)  # 重新加载一次, 以获得更新后的某些属性值

    print(Python.String.Import_From_Example.current_time)

    from Python.String.Import_From_Example import title, current_time, g_value

    print(title)  # 由于from .. import .. 相当于复制了所有代码到当前的script中, 所以在模块中定义的变量也可以直接使用

    time.sleep(1)

    print(current_time)

    time.sleep(1)

    reload(Python.String.Import_From_Example)  # reload方法在from .. import ..下是没用的, 因为属性值已经复制到当前script中了

    print(current_time)

    title = "Updated Title"  # 可以直接改属性值

    print(title)

    reload(Python.String.Import_From_Example)

    print(Python.String.Import_From_Example.title)  # 在本地script改了属性值不会影响模块里的属性值, 但要注意global 变量

    print(g_value)

    g_value = "I tried to update a global value!"

    print(g_value)

    reload(Python.String.Import_From_Example)

    print(Python.String.Import_From_Example.g_value)

    Python.String.Import_From_Example.g_value = "I try to update a global value in import"

    Python.String.Import_From_Example.title = "I try to update a local value in import"

    print(Python.String.Import_From_Example.g_value)  # import来的value也可以修改, 但不清楚这个修改会不会影响其它import相同模块的script

    print(Python.String.Import_From_Example.title)

    reload(Python.String.Import_From_Example)

    print(Python.String.Import_From_Example.g_value)  # Reload过后无论是否global value, 都会回复之前的值

    print(Python.String.Import_From_Example.title)



