import json


if __name__ == "__main__":
    '''
    将数据编译成json, 实际上就是把python的字典的内容变成格式化的json字符串
    
    Python变量类型转换成json后的对应变量类型如下
    
    dict ->	                object
    list,tuple ->	        array
    str, unicode ->	        string
    int, long, float -> 	number
    True ->             	true
    False ->            	false
    None ->             	null
    '''
    data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
    # 将字典编译成json格式
    jsons = json.dumps(data)
    print(jsons)
    # 也可以将字典编译成json格式后写入文件中
    with open("test.json", "w", encoding='utf-8') as f:
        # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
        f.write(json.dumps(data, indent=4))

    '''
    从json中读取数据
    
    '''

    import json

    jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
    # 可以直接从json格式的字符串中读取并写入一个字典
    text = json.loads(jsonData)
    print(text)

    # 也可以从文件中读取
    with open("test.json", "r", encoding='utf-8') as f:
        test = json.loads(f.read())
    print(test)

