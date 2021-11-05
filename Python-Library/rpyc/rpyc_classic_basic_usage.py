import rpyc

if __name__ == '__main__':
    # 连接服务器, 标准服务的默认端口为18812
    conn = rpyc.classic.connect("localhost")

    # 调用Server端的模块, 注意的是只有在Server的模块path里的模块才可以被调用(应该就是通过Server程序做代理运行Server端的模块)
    rsys = conn.modules.sys
    print(rsys.argv)

    #


