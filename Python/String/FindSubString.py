String = "abcdefg"

print("If found, return the start postion of the sub string: " + str(String.find("fg"))) # Return 5

print("If not found, return: " + str(String.find("hij"))) # Returen -1

print("If found in range of set start and end: " + str(String.find("cd",1,4))) # Return 2

print("If partly found in rage of set start and end: " + str(String.find("cde",1,3))) # Return -1

print("If not found in rage of set start and end: " + str(String.find("fg",1,3))) # Return -1