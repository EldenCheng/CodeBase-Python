import subprocess, time

#repr 方法是将字符串转换成Python内部实际显示形式，有时可以用来处理带有转义字符，但又不想转义的字符串

path = "C:\Windows\System32\calc.exe"


print(path)
print(repr(path))



def Lanuch(path):
    print(path)
    p = subprocess.Popen(path)

    time.sleep(1)

    p.kill()

Lanuch(path)