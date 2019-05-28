import os

mydir = "c:\\mydir"
os.environ["TEMP"] = mydir+";" + os.environ["TEMP"]
print(os.environ["TEMP"])