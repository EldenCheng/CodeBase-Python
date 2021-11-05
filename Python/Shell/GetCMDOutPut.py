import subprocess

if __name__ == '__main__':

    proc4 = subprocess.Popen("dir *.*", stdout=subprocess.PIPE, shell=True)
    (out4, err4) = proc4.communicate()

    print(out4)
    print(err4)
