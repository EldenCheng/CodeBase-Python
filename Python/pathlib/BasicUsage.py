from pathlib import Path

dirpath = Path(r"D:\VBA")

filepath = Path(r"D:\VBA\JustATest.txt")

filepath2 = Path(r".\BasicUsage.py")

#判断是否目录或者文件
print(dirpath.is_dir())

print(filepath.is_file())

#如果是文件的话可以当作二进制文件或者文本文件打开
print(filepath.read_text())

print(filepath.read_bytes())

#可以显示当前文件所有的目录，注意返回的不是str，需要转换
print(filepath.parent)

#逐级返回文件所有的目录，盘符等
for p in filepath.parents:
    print("parents: ", p)

#返回文件所有的盘符
print(filepath.anchor)

#返回文件的绝对路径
print(filepath2.absolute())

#将文件的路径拆开分别放到list的不同element里
print(filepath.parts)


