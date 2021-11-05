import tempfile

if __name__ == '__main__':

    file = tempfile.mktemp()
    print(file)
    file2 = tempfile.NamedTemporaryFile(prefix='screenshot', suffix='png',)
    print(file2.name)
