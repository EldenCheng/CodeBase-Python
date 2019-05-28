print("When import")

library = ["time","subprocess","pathlib"]

for l in library:
    exec("import " + l)
    print(l)

