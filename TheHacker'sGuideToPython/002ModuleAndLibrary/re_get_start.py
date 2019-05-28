import re

string = '$200+taxes&fees'

ret = re.match(r"\$[0-9]\d*\+taxes&fees", string)

if ret:
    print("匹配成功")
else:
    print("匹配失败")
