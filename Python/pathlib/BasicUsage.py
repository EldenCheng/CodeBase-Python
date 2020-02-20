from pathlib import Path

if __name__ == '__main__':
    dir_path = Path(r"D:\VBA")

    file_path = Path(r"D:\VBA\JustATest.txt")

    file_path2 = Path(r".\BasicUsage.py")

    # 判断是否目录或者文件
    print(dir_path.is_dir())

    print(file_path.is_file())

    # 如果是文件的话可以当作二进制文件或者文本文件打开
    print(file_path.read_text())

    print(file_path.read_bytes())

    # 可以显示当前文件所有的目录，注意返回的不是str，需要转换
    print(file_path.parent)

    # 逐级返回文件所有的目录，盘符等
    for p in file_path.parents:
        print("parents: ", p)

    # 返回文件所有的盘符
    print(file_path.anchor)

    # 返回文件的绝对路径
    print(file_path2.absolute())

    # 将文件的路径拆开分别放到list的不同element里
    print(file_path.parts)

    # 文件名
    print(file_path.name)


