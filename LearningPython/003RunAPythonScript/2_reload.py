"""
要注意的是reload方法仅仅会reload显式写在方法参数中的模块, 被reload模块中的引用模块不会被reload
"""
import time

from importlib import reload

import Python.String.reload_example

if __name__ == "__main__":
    print(Python.String.reload_example.import_time)

    print(Python.String.reload_example.self_time)

    time.sleep(1)

    reload(Python.String.reload_example)

    print(Python.String.reload_example.import_time)  # 这个属性的值是reload_example import其它模块的, reload后不会变化

    print(Python.String.reload_example.self_time)    # 这个属性的值是reload_example自己的, reload后会变化
