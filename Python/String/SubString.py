
def StrLeft(String,Str_index):
    return String[:Str_index]

def StrRight(String,Str_index):
    return String[-(Str_index):]

def Str_sub(String,Str_begin,Str_end):
    return String[Str_begin - 1:Str_end]


String = "abcdefg"

print(String[0]) # Return a

print(String[6]) # Return g

print(String[-1]) # Return g, which count from the last one

print(String[-6])# Return b, which count from the last one

print(String[1:3])# Return bc, substring from the 2nd position to 4th position, but not included the 4th position character

for i in range(7):
    print(String[i])

print(StrLeft(String,2)) # Return ab
print(StrLeft(String,9)) # Return abcdefg

print(StrRight(String,2)) # Return fg
print(StrRight(String,9)) # Return abcdefg

print(Str_sub(String,1,6)) # Return abcdef, the index use the absolute position
print(Str_sub(String,1,9)) # Return abcdefg