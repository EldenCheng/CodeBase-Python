"""
在Pyinstaller中, 编译了py文件后, 对应的Python解释器等会自动放在_internal文件夹中, 如果不想使用这个文件夹名字, 其实可以指定这个存放library
文件夹的名字的, 下面就是对应的命令

PyInstaller --onedir --contents-directory “own_dir_name” script.py

如果不想把Python解释器之类的文件夹收藏起来, 可以通过下列的命令
PyInstaller --onedir --contents-directory . script.py
那么Pyinstall就会把打包好的exe文件与解释器文件等等的东西都放在同一个文件夹里面了
"""



if __name__ == '__main__':
    pass