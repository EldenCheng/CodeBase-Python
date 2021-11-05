import rpyc

if __name__ == '__main__':

    # 调用服务器端的方法，格式为：conn.root.xxx。xxx代表服务器端的方法名
    # sum是服务端的那个以"exposed_"开头的方法
    # RPYC没有认证机制，任何客户端都可以直接访问服务器端的暴露的方法
    conn = rpyc.connect('localhost', 9999)
    result = conn.root.sum(1234, 5678)
    conn.close()
    print('>>>',result)