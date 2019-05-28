import os

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

if __name__ == "__main__":

    print(PATH("adb.cmd"))