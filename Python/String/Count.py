
string = "I'm in love with you"

for s in string:
    print(s + ": ", string.count(s))
    string = string.replace(s,"")
    #print(string)