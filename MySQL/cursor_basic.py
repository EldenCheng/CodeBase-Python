import mysql.connector
from mysql.connector import Error as DB_Error

if __name__ == '__main__':
    config ={
        'user': 'root',
        'password': 'Wesoft1234',
        'host': 'localhost',
        'raise_on_warnings': True
    }
    try:
        cnx = mysql.connector.connect(**config)
    except DB_Error as err:
        print("捕捉到异常: ", err)

    # 在运行一个SQL语句之前, 先初始化一个cursor
    # 刚初始化的cursor没有指向任何table, 所以实际上也并没有指向任何一个数据库记录
    cursor = cnx.cursor()
    print("初始化的cursor不会指向任何数据记录: ", cursor.column_names)

    # 如果什么参数都不指定, cursor可以执行一般的数据库管理(比如use, create database, insert之类的SQL语句)
    cursor.execute('USE employees')
    cursor.execute("INSERT INTO employees (first_name, last_name, birth_date) VALUES ('Elden', 'Cheng', '1981-09-02')")

    cursor.execute('select * from employees')
    for c in cursor:
        print(c)
    cursor.close()  # 由于上面的循环操作了指针下移, 所以这里关闭指针不会报错

    # 要注意如果查询之后没有操作指针, 就尝试关闭close指针或者同步数据库的数据, 比如fetchone的话
    # 就有可能会报Unread result found
    # 主要是因为普通的cursor没有缓存, 所以如果在没有访问过所有数据的话, connector会认为数据可能会丢失, 所以不允许这种操作
    # (具体可能更复杂, 可以参考https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone)
    lazy_cursor = cnx.cursor()
    lazy_cursor.execute('USE employees')
    lazy_cursor.execute('select * from employees')
    try:
        lazy_cursor.close()
    except Exception as msg:
        print(msg)
        # 一个connection只能有一个cursor, 所以这里先把lazy_cursor关闭方便下面的演示
        for lc in lazy_cursor:
            pass
        lazy_cursor.close()

    # 指定cursor类型为buffer cursor就可以避免上面的错误, 但buffer cursor会需要一定的空间存放buffer
    # 有可能影响性能
    buffer_cursor = cnx.cursor(buffered=True)
    buffer_cursor.execute('USE employees')
    buffer_cursor.execute('select * from employees')
    buffer_cursor.close()  # 这个不会报错

    # 如果不指定返回值的类型, 查询得到的数据默认按元组返回数据(不包括列名, 按列的顺序直接返回数据)
    # 指定dictionary=True标志表示cursor buffer的数据以字典类型存放(以列名为Key, 数据为value)
    # 指定name_tuple=True标志表示cursor buffer的数据是使用Row类型存放的数据

    default_cursor = cnx.cursor(buffered=True)
    default_cursor.execute('USE employees')
    default_cursor.execute('select * from employees')
    print("默认的查询结果: ", list(default_cursor))
    default_cursor.close()

    dict_cursor = cnx.cursor(buffered=True, dictionary=True)
    dict_cursor.execute('USE employees')
    dict_cursor.execute('select * from employees')
    print("指定查询结果为字典类型: ", list(dict_cursor))
    dict_cursor.close()

    name_cursor = cnx.cursor(buffered=True, named_tuple=True)
    name_cursor.execute('USE employees')
    name_cursor.execute('select * from employees')
    rows = list(name_cursor)
    print("指定查询结果为named_tuple类型: ", rows)
    print("使用列名获取Row1的first name的值: ", rows[0].first_name)  #使用列名获取值
    print("使用列顺序获取Row1的first name的值: ", rows[0][2])  # 使用列名的顺序获取值
    name_cursor.close()

    # 除了获取数据库的存放的值外, 还可以获取到数据表的一些属性
    cursor = cnx.cursor(buffered=True)
    cursor.execute('USE employees')
    cursor.execute('select * from employees')
    print("获取数据表的所有列名: ", cursor.column_names)
    print("返回所有列的描述(数据类型, 约束等等): ", cursor.description)
    print("获取数据表是否有行: ", cursor.with_rows)
    print("获取数据表的记录的总行数: ", cursor.rowcount)
    print("获取数据表的记录的最后一行的id: ", cursor.lastrowid)
    print("获取上一条SQL语句", cursor.statement)

    cursor.close()
    cnx.close()


