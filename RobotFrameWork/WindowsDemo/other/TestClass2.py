import time
from EX1_TC1 import EX1_TC1

tc1 = EX1_TC1()

t = tc1.Launch('calc')

time.sleep(10)

tc1.OpenCSV("Sample.csv")

d = tc1.Get_Displays(1)

print(d)

tc1.Close_App()

