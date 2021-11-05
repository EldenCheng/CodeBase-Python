from ftplib import FTP_TLS

if __name__ == '__main__':
    ftps = FTP_TLS(timeout=100)
    # 下面的用法与普通FTP一样
    ftps.connect('ftphost', 21)
    ftps.auth()
    ftps.prot_p()
    ftps.login('username', 'password')
    current_folder = ftps.pwd()
    print(current_folder)
    ftps.dir()
    ftps.quit()
