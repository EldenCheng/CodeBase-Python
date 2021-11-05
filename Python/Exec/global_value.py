
if __name__ == '__main__':

    global global_x
    global_x = "Outside"
    g = {'global_x': global_x}
    loc = {}
    statement = 'from Python.Exec.import_test import Test38\n' \
                'test = Test38()\n' \
                'test.test()'
    exec(statement, g, loc)
    print("print outside: ", loc)