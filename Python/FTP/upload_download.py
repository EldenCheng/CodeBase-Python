import ftplib
import time
import os


if __name__ == "__main__":
    remote_folder = "Framework"
    USER = "wesoft"
    PASSWORD = "password"
    conn = ftplib.FTP()
    conn.connect("192.168.9.36", port=21, timeout=120)  # host_address不包含协议
    conn.login(USER, PASSWORD)
    if len(conn.getwelcome()) != 0:
        upload_file = time.strftime("%Y-%m-%d_%H%M%S", time.localtime()) + ".txt"
        with open(upload_file, "w", encoding='utf-8') as f:
            # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
            f.write(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
            f.close()
        conn.cwd("Framework")
        subfolder = "Report"

        # 以二进制模式上传文件
        with open(upload_file, "rb") as f:
            conn.storbinary('STOR ' + upload_file, f, blocksize=1024)
            conn.storbinary('STOR ' + './' + subfolder + '/' + upload_file, f, blocksize=1024)
            f.close()

        # 以二进制模式下载文件
        remote_file = 'Base_tests.py'
        with open(remote_file, "wb") as f:
            conn.retrbinary('RETR ' + remote_file, f.write, blocksize=1024)
            f.close()

    conn.quit()




