import mysql.connector
from mysql.connector import Error as DB_Error
from mysql.connector import errorcode

if __name__ == '__main__':

    # 简单地连接MySQL Server
    cnx = mysql.connector.connect(user='root', password='Wesoft1234', host='localhost', database='sys')
    print('MySQL基本连接: ', cnx)
    cnx.close()

    # 可以尝试捕获errorcode Exception来处理连接时的异常
    try:
        cnx = mysql.connector.connect(user='root', password='Wesoft123', host='localhost', database='sys')
    except DB_Error as err:
        print("捕捉到异常: ", err)
        print("错误代码: ", err.errno)
        print("对应的错误代码库: ", errorcode.ER_ACCESS_DENIED_ERROR)

    try:
        cnx = mysql.connector.connect(user='root', password='Wesoft1234', host='localhost', database='sys1')
    except DB_Error as err:
        print("捕捉到异常: ", err)

    # 可以利用Python的参数解包功能, 将MySQL连接参数先写入一个字典, 再将字典解包作为连接的参数
    config ={
        'user': 'root',
        'password': 'Wesoft1234',
        'host': 'localhost',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    print("使用字典解包作为连接参数: ", cnx)
    cnx.close()
