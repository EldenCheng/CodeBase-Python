

if __name__ == '__main__':
    t = ("1", "2", "3")
    s = ("4",)
    print("Tuple + Tuple operation: ", t + s)

    try:
        print(t + "4")
    except Exception as msg:
        print("Tuple + String operation, report TypeError: {0}".format(msg))
