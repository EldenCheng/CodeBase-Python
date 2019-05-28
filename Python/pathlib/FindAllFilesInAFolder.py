from pathlib import Path

#列出所有在指定目录下的某种文件，与Dir命令有相似，但返回的是Windir object，所以不能直接当str用，要转换
allexefiles = list(Path(r"c:\program files").rglob('*.exe'))

for e in allexefiles:
    print(e)

