import tempfile

file = tempfile.mktemp()

print(file)

file2 = tempfile.NamedTemporaryFile(suffix='screenshot', prefix='png')

print(file2.name)
