import requests


# Get
r = requests.get('https://api.github.com/events')

print(r)
# 查看服务器response的内容, 默认编码是uni-code
print(r.text)

# POST
r = requests.post('http://httpbin.org/post', data={'key': 'value'})

# 其它类型
r = requests.put('http://httpbin.org/put', data = {'key':'value'})
r = requests.delete('http://httpbin.org/delete')
r = requests.head('http://httpbin.org/get')
r = requests.options('http://httpbin.org/get')

# 传递参数
parameters = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=parameters)
print(r.url)



