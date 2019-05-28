import subprocess

proc4 = subprocess.Popen("dir *.*", stdout=subprocess.PIPE, shell=True)
(out4, err4) = proc4.communicate()

print(out4)
print(err4)
