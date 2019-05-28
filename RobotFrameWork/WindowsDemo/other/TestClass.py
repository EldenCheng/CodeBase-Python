import time
from EX1_TC1 import EX1_TC1

tc1 = EX1_TC1()

t = tc1.Launch('calc')

tc1.OpenCSV("Sample.csv")

ele = tc1.TraversalCSV_Elements(1)

tc1.NumClick(ele,'k')

DR = tc1.Get_DisplayedResut()
ER = tc1.Get_ExpectResut()

j = 0
for i in DR:
    if i == ER[j]:
        print("The result of the " + str(j+1) +"th row is the same!")
    else:
        print("The result of the " + str(j+1) + "th row is not the same!")
    j = j + 1