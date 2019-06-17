

d = {"food": "Egg", "num": 4, "product": ["GD", "GZ"]}

try:
    print(d["key"])
except KeyError as keyerror:
    print(keyerror)
except Exception as msg:
    print(msg.__class__)
