import os
import subprocess

import subprocess

print("Please make sure you have connected you mobile(s) to the PC, and press any key to continue.")

#input()

proc = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
devices = str(out).split("\\n")[1:-2]

device_info = "serial_number,device_name\n"
for d in devices:
    temp = d.split("\\t")
    serial_number = temp[0]
    device_name = temp[1][:-2]
    device_info += serial_number + "," + device_name + "\n"

f = open("./device_info.csv","w")
f.write(device_info)
f.close()

#print(devices)