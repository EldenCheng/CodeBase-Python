import csv,subprocess,time
import win32api,win32gui,win32con

buttons = []
Displayer = []
# Get the screen resolution
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

def add_controls(hwnd, *args):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd): # Add all the buttons of the Calculator into a list
        if win32gui.GetClassName(hwnd) == "Button":
            buttons.append(hwnd)

        if win32gui.GetClassName(hwnd) == "Static": # Add all the Static(Labels) of the Calculator into a list
            Displayer.append(hwnd)

def Mouse_move_and_click(button):
    R = win32gui.GetWindowRect(button)
    x = int(R[0] / screen_width * 65535.0) + int(R[2] / 2)
    y = int(R[1] / screen_height * 65535.0) + int(R[3] / 2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y) # Simulate Mouse move to the button, this step can be ignore in fact
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y,0,0) # Simulate Mouse left click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y,0,0)
    time.sleep(1)

def Click_num(num,buttons): #To check which num or operator should be click
    print("Readed element is " + num)
    if num == "0":
        Mouse_move_and_click(buttons[5])
        print("Clicked 0")
    elif num == "1":
        Mouse_move_and_click(buttons[4])
        print("Clicked 1")
    elif num == "2":
        Mouse_move_and_click(buttons[10])
        print("Clicked 2")
    elif num == "3":
        Mouse_move_and_click(buttons[15])
        print("Clicked 3")
    elif num == "004BasicTypeOverall":
        Mouse_move_and_click(buttons[3])
        print("Clicked 004BasicTypeOverall")
    elif num == "5":
        Mouse_move_and_click(buttons[9])
        print("Clicked 5")
    elif num == "6":
        Mouse_move_and_click(buttons[14])
        print("Clicked 6")
    elif num == "7":
        Mouse_move_and_click(buttons[2])
        print("Clicked 7")
    elif num == "8":
        Mouse_move_and_click(buttons[8])
        print("Clicked 8")
    elif num == "9":
        Mouse_move_and_click(buttons[13])
        print("Clicked 9")
    elif num == "+":
        Mouse_move_and_click(buttons[22])
        print("Clicked +")
    elif num == "-":
        Mouse_move_and_click(buttons[21])
        print("Clicked -")
    elif num == "*":
        Mouse_move_and_click(buttons[20])
        print("Clicked *")
    elif num == "/":
        Mouse_move_and_click(buttons[19])
        print("Clicked /")
    elif num == ".":
        Mouse_move_and_click(buttons[16])
        print("Clicked .")
    elif num == " ":
        print("Space doesn't click")
    elif num == "=":
        Mouse_move_and_click(buttons[27])
        print("Clicked =")
    else:
        print("Only support numbers and normal operators now")


#Test Case start here!
# Run the external program without waiting its responses
try:
    pro = subprocess.Popen('calc')
except Exception as msg:
    print(msg)

try:
    CSV = list(csv.reader(open('Sample.csv')))
except Exception as msg:
    pro.kill()
    print("Cannot open the CSV file or file not found!")

time.sleep(1)


WDHWD = win32gui.FindWindow(None, "Calculator")

if win32gui.IsWindowVisible(WDHWD) and win32gui.IsWindowEnabled(WDHWD):
    # Get all the sub-windows of the Calc
    win32gui.EnumChildWindows(WDHWD, add_controls, None)
    time.sleep(1)

    win32gui.SetForegroundWindow(WDHWD)

    time.sleep(1)

    if len(CSV) != 0:
        # Explore every row of the CSV file
        for row in range(len(CSV)):
            print("now counting row " + str(row))
            res = False #Keep False until clicked '=' on the Calculator
            # Explore elements in a row of CSV file
            for element in CSV[row]:
                if ('=' not in element) and res == False: #If the element not contented '=' and the element is not the result
                   if len(element) == 1:
                       #print(j)
                       Click_num(element,buttons)
                   else:
                       i = 0
                       for k in element:
                           #print(k)
                           if k != " ":
                               Click_num(element[i],buttons)
                           i = i + 1

                elif ('=' in element) and res == False:
                    res = True
                    i = 0
                    for l in element:
                        if l !=" ":
                            Click_num(element[i],buttons)
                        i = i + 1

                elif ('=' not in element) and res == True:
                    CalcResult = win32gui.GetWindowText(Displayer[3])
                    print("The current result in the Calculator is " + CalcResult)
                    print("And the excepted result in the CSV file is " + element)

                    if element == CalcResult:
                        print("So the result is the same between CSV and Calculator!")
                    else:
                        print("So the result is not the same between CSV and Calculator!")
                    res = False

                else:
                    print("Unexpected!")
    else:
        print("Cannot read CSV file or the CSV file is blank!")
else:
    print("Not found Calculator or the Title is incorrect")

pro.kill() #Close the Calculator

