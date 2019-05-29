import ftplib
import os


if __name__ == "__main__":
    remote_folder = "Framework"
    USER = "wesoft"
    PASSWORD = "password"
    conn = ftplib.FTP()
    conn.connect("192.168.9.36", port=21, timeout=120)  # host_address不包含协议
    conn.login(USER, PASSWORD)
    welcome = conn.getwelcome()  # 获得欢迎信息表明已经连接到FTP服务器上
    current_folder = conn.pwd()  # 获得当前目录名称
    print(current_folder)
    try:
        folder = conn.cwd(remote_folder)  # 改变当前目录
    except ftplib.error_perm as ftp_error:
        print(ftp_error)

    conn.dir()  # 这个是List命令的包装, 可以接收跟List命令一样的参数, 但默认只在控制台打印, 无返回

    # 由于这个方法最后一个参数如果是一个function的话, 这个func会被认为是callback func
    # 所以如果需要获得返回的内容, 可以传入一个function(lambda)来记录/处理输出内容

    subfolder = "2019-05-14_095621"
    conn.dir(lambda line: print("True") if subfolder == line.split(" ")[-1] and line.split(" ")[0].startswith('d') else print("False"))
    dir_list = list()
    conn.dir(dir_list.append)
    print(len(dir_list))

    files = conn.nlst()  # 获取目录下的文件, 但实际返回的是包括目录名与文件名的一个列表
    print(files)
    if "Base_tests.py" in files:
        try:
            result1 = conn.nlst("Base_tests.py")  # 如果尝试列出一个文件,会返回[文件名]
            result2 = conn.nlst("2019-05-14_095621")  # 如果尝试列出一个空目录, 会返回一个空列表[]
            result3 = conn.nlst("2019-05-09_150934")  # 如果尝试列出一个包含目录与文件的目录, 每个目录名与文件就会成为列表中的一个元素
            result4 = conn.nlst("None")  # 如果尝试列出一个不存在的目录, 会报错
        except ftplib.error_perm as ftp_error:
            print(ftp_error)

    # 要注意的是不是所有FTP服务器都支持mlsd协议
    files2 = conn.mlsd()  # 如果不指定, 默认会查找当前目录, 检查器只会检查type
    files3 = conn.mlsd(facts=["type", "size", "perm"])  # 可以指定多种检查器, 注意的是目录没有size, 只有文件才有, perm不是所有服务器都支持返回

    print(list(files2))  # 生成器不能直接访问到元素, 可以先转换成list
    print(list(files3))

    files4 = conn.mlsd(".", ["type"])  # 当前可以支持指定路径
    #  因为返回的ftp mlsd对象是一个生成器, 所以可以直接用循环来访问所有元素
    for name, facts in files4:
        if facts["type"] == "dir" and name == "remote_ftp":
            print("isdir: " + name)
            remotefoldername_exists = 1
            break

