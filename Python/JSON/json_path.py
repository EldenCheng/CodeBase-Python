"""
如果需要在一个大型的json文件中快速地获取想要的value,那么json path就是一个非常好的工具

python自带的json库是不支持json path, 这里需要下载另外的库来支持
可以使用pip install jsonpath2来安装一个简单的jsonpath2库来实现

json path中的语法如下:

$	跟节点
@	现行节点
. or []	取子节点
..  递归(深度优先)搜索子孙节点
*	匹配所有元素节点
[]	迭代器标示(可以在里面做简单的迭代操作，如数组下标，根据内容选值等)
[,]	支持迭代器中做多选
[start:end:step] json array切片操作
?()	支持过滤操作
()	支持表达式计算
"""

import json
from jsonpath2.path import Path

if __name__ == "__main__":

    with open("test.json", "r", encoding='utf-8') as f:
        test = json.loads(f.read())

    print(test)
    p = Path.parse_str('$..a')  # 设置解释器
    matchdata = list(p.match(test))  # 使用解释器分析json字符串, 得到的结果是一个map类型, 所以需要使用list()来让它转换为一个列表
    # 列表的内容是解释产生的Match_Data对象列表, 而具体的符合条件的值是存放在Match_Data对象中的, 需要访问对象的属性current_value获取
    # 另外由于这个例子只有一个符合的值所以只访问第一个, 但实际上json解释的结果可能有多个值, 这时应该会有多个Match_Data对象
    result = matchdata[0].current_value

    # 如果嫌上面分开写麻烦的话,可以使用map()与lambda 表达式组合的方法来获得结果的列表
    result2 = list(map(lambda match_data: match_data.current_value, p.match(test)))
    print(result)
    print(result2)

    """
    jsonpath2库还有一些方法可以作为解释器用于解释json
    
    entries(): List[Tuple[str, Any]]
    keys(): List[str]
    values(): List[Any]
    length(): int
    charAt(index: int): str
    substring(indexStart: int, indexEnd: Optional[int]): str
    """

    pf = Path.parse_str('$..[keys()]')  # 查找所有层级的keys(注意这个方法应该不是jsonpath内置的)
    result3 = list(map(lambda match_data: match_data.current_value, pf.match(test)))
    print(result3)




