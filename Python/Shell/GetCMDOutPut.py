import subprocess

if __name__ == '__main__':

    # Python 3.6
    process = subprocess.check_output(['dir'], shell=True)
    print(process.decode('latin-1'))

    proc = subprocess.Popen("dir *.*", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    (out, err) = proc.communicate()

    print(out)
    print(err)

    # result = subprocess.run("dir *.*", shell=True, capture_output=True, text=True)
    result = subprocess.run("dir *.*", shell=True, text=True)

    # print(result.stdout)
    result_txt = result.stdout
    print(result_txt)


