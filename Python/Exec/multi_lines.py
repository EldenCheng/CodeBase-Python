

if __name__ == '__main__':
    # 如果要在一个exec里执行多行语句, 可以在每一行后面加\n
    statement1 = "print('hello world')\n" \
                 "print('we are the worlk')"
    # statement2 = "print('we are the worlk')"

    exec(statement1)