import csv,subprocess,time

from VKList import VK
import os.path
import win32api,win32gui,win32con

class EX1_TC1(object):

    def __init__(self):
        self.pro=''
        self.WDHWD=''
        self.CSV=''
        self.buttons = []
        self.Displayer = []
        self.DisplayedResult = []
        self.ExpectResult = []
        # Get the screen resolution
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)
        self.res = False
        self.SupportOperator = ['+','-','*','/']
        self.SupportNumber = ['0','1','2','3','004BasicTypeOverall','5','6','7','8','9']
        self.vk=VK()

    def Launch(self,application):
        #print("The application is " + application)
        if application != "":
            try:
                self.pro=subprocess.Popen(application)
                time.sleep(1)

                self.WDHWD = win32gui.FindWindow(None, "Calculator")
                if win32gui.IsWindowVisible(self.WDHWD) and win32gui.IsWindowEnabled(self.WDHWD):
                    # Get all the sub-windows of the Calc
                    win32gui.EnumChildWindows(self.WDHWD, self.add_controls, None)
                    time.sleep(1)
                else:
                    raise EX1_TC1Error("Not found Calculator or the Title is incorrect")

            except Exception as msg:
                raise AssertionError("Cannot open the Application or the application not exist!")

        else:
            raise AssertionError("The name or the path of Application is null!")

    def add_controls(self,hwnd, *args):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(
                hwnd):  # Add all the buttons of the Calculator into a list
            if win32gui.GetClassName(hwnd) == "Button":
                self.buttons.append(hwnd)

            if win32gui.GetClassName(hwnd) == "Static":  # Add all the Static(Labels) of the Calculator into a list
                self.Displayer.append(hwnd)

    def OpenCSV(self,filename):
        if filename != "":
            try:
                self.CSV = list(csv.reader(open(filename)))
            except Exception as msg:
                raise AssertionError("Cannot open the CSV file or file not found!")
        else:
            raise AssertionError("The csv file name or file path is null!")

    # Can specify start Row and end Row, by default return all rows
    def TraversalCSV_Rows(self,Rowindex=0, length=1):
        rw = []
        if len(self.CSV) > 0 :
            for Rows in self.CSV[Rowindex:Rowindex + length]:
                #print(Rows)
                rw.append(Rows)
        return rw

    # Can specify start Row and end Row, by default return all rows, then specify how many elements need
    def TraversalCSV_Elements(self, Rowindex = 0, length = 1,Elementnum=9999):
        ele = []
        if len(self.CSV) > 0 :
            for Rows in self.CSV[Rowindex:Rowindex + length]:
                for element in Rows[:Elementnum]:
                    #print(element)
                    ele.append(element)
        return ele

    def Mouse_move_and_click(self,button):
        R = win32gui.GetWindowRect(button) # Get the position(x,y), width and height of controller
        # As the original x,y is the most top left of the controller, need to make the position to the center of the
        # controller and switch into absolution position
        x = int(R[0] / self.screen_width * 65535.0) + int(R[2] / 2)
        y = int(R[1] / self.screen_height * 65535.0) + int(R[3] / 2)

        time.sleep(1)

        # Simulate Mouse move to the button, this step can be ignore in fact
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y)
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)  # Simulate Mouse left click
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(1)

    def MouseClick_num(self,num, buttons):  # To check which num or operator should be click
        print("Readed element is " + num)
        if num == "0":
            self.Mouse_move_and_click(buttons[5])
            print("Clicked 0")
        elif num == "1":
            self.Mouse_move_and_click(buttons[4])
            print("Clicked 1")
        elif num == "2":
            self.Mouse_move_and_click(buttons[10])
            print("Clicked 2")
        elif num == "3":
            self.Mouse_move_and_click(buttons[15])
            print("Clicked 3")
        elif num == "004BasicTypeOverall":
            self.Mouse_move_and_click(buttons[3])
            print("Clicked 004BasicTypeOverall")
        elif num == "5":
            self.Mouse_move_and_click(buttons[9])
            print("Clicked 5")
        elif num == "6":
            self.Mouse_move_and_click(buttons[14])
            print("Clicked 6")
        elif num == "7":
            self.Mouse_move_and_click(buttons[2])
            print("Clicked 7")
        elif num == "8":
            self.Mouse_move_and_click(buttons[8])
            print("Clicked 8")
        elif num == "9":
            self.Mouse_move_and_click(buttons[13])
            print("Clicked 9")
        elif num == "+":
            self.Mouse_move_and_click(buttons[22])
            print("Clicked +")
        elif num == "-":
            self.Mouse_move_and_click(buttons[21])
            print("Clicked -")
        elif num == "*":
            self.Mouse_move_and_click(buttons[20])
            print("Clicked *")
        elif num == "/":
            self.Mouse_move_and_click(buttons[19])
            print("Clicked /")
        elif num == ".":
            self.Mouse_move_and_click(buttons[16])
            print("Clicked .")
        elif num == " ":
            print("Space doesn't click")
        elif num == "=":
            self.Mouse_move_and_click(buttons[27])
            print("Clicked =")
        else:
            print("Only support numbers and normal operators now")

    def Click_num(self,num):  # To check which num or operator should be press
        print("Readed element is " + num)
        if num == "0":
            win32api.keybd_event(self.vk.VK_CODE['0'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['0'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 0")
            time.sleep(1)
        elif num == "1":
            win32api.keybd_event(self.vk.VK_CODE['1'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['1'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 1")
            time.sleep(1)
        elif num == "2":
            win32api.keybd_event(self.vk.VK_CODE['2'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['2'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 2")
            time.sleep(1)
        elif num == "3":
            win32api.keybd_event(self.vk.VK_CODE['3'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['3'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 3")
            time.sleep(1)
        elif num == "004BasicTypeOverall":
            win32api.keybd_event(self.vk.VK_CODE['004BasicTypeOverall'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['004BasicTypeOverall'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 004BasicTypeOverall")
            time.sleep(1)
        elif num == "5":
            win32api.keybd_event(self.vk.VK_CODE['5'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['5'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 5")
            time.sleep(1)
        elif num == "6":
            win32api.keybd_event(self.vk.VK_CODE['6'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['6'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 6")
            time.sleep(1)
        elif num == "7":
            win32api.keybd_event(self.vk.VK_CODE['7'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['7'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 7")
            time.sleep(1)
        elif num == "8":
            win32api.keybd_event(self.vk.VK_CODE['8'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['8'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 8")
            time.sleep(1)
        elif num == "9":
            win32api.keybd_event(self.vk.VK_CODE['9'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['9'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed 9")
            time.sleep(1)
        elif num == "+":
            win32api.keybd_event(self.vk.VK_CODE['add_key'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['add_key'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed +")
            time.sleep(1)
        elif num == "-":
            win32api.keybd_event(self.vk.VK_CODE['subtract_key'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['subtract_key'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed -")
            time.sleep(1)
        elif num == "*":
            win32api.keybd_event(self.vk.VK_CODE['multiply_key'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['multiply_key'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed *")
            time.sleep(1)
        elif num == "/":
            win32api.keybd_event(self.vk.VK_CODE['divide_key'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['divide_key'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed /")
            time.sleep(1)
        elif num == ".":
            win32api.keybd_event(self.vk.VK_CODE['.'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['.'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed .")
            time.sleep(1)
        elif num == " ":
            print("Space doesn't click")
        elif num == "=":
            win32api.keybd_event(self.vk.VK_CODE['enter'], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(self.vk.VK_CODE['enter'], 0, win32con.KEYEVENTF_KEYUP, 0)
            print("Pressed =")
            time.sleep(1)
        else:
            print("Only support numbers and normal operators now")

    def NumClick(self,Number,Method):
        win32gui.SetForegroundWindow(self.WDHWD)
        res = False
        if len(Number) != 0:
            #res = False
            #print(self.res)
            for n in Number:
                if ('=' not in n) and self.res == False:
                    if len(n) == 1:
                        if Method == 'm':
                            self.MouseClick_num(n, self.buttons)
                        elif Method == 'k':
                            self.Click_num(n)
                        else:
                            print("Only support Mouse or Keyboard in the test case!")
                        self.VerifyInput(n)
                    else:
                        i = 0
                        for m in n:
                            if m != " ":
                                if Method == 'm':
                                    self.MouseClick_num(n[i], self.buttons)
                                elif Method == 'k':
                                    self.Click_num(n[i])
                                else:
                                    print("Only support Mouse or Keyboard in the test case!")
                                self.VerifyInput(m)
                            i = i + 1
                elif ('=' in n) and self.res == False:
                    self.res = True
                    i = 0
                    for l in n:
                        if l != " ":
                            if Method == 'm':
                                self.MouseClick_num(l,self.buttons)
                            elif Method == 'k':
                                self.Click_num(l)
                            else:
                                print("Only support Mouse or Keyboard in the test case!")
                        i = i + 1
                        #print("After click =: " + str(res))
                elif ('=' not in n) and self.res == True:
                    self.DisplayedResult.append(win32gui.GetWindowText(self.Displayer[3]))
                    self.ExpectResult.append(n)
                    print("The current result in the Calculator is " + self.DisplayedResult[-1])
                    print("And the excepted result in the CSV file is " + self.ExpectResult[-1])
                    self.res = False
                else:
                    raise AssertionError("Unexpected!")
        else:
            raise AssertionError("Does not contented a number!")

    def VerifyInput(self,num):
        if num in self.SupportOperator:
            if num != self.Get_Displays(1)[-1:]:
                raise AssertionError("Clicked unexcepted button or No clicked button!")
        elif num in self.SupportNumber:
            if num != self.Get_Displays(3)[-1:]:
                raise AssertionError("Clicked unexcepted button or No clicked button!")
        elif num == "=":
            pass
        else:
            print("Not support number or operator, so doesn't clicked")

    def Get_DisplayedResut(self):
        return self.DisplayedResult

    def Get_ExpectResut(self):
        return self.ExpectResult

    def Get_WindowTitle(self):
        return win32gui.GetWindowText(self.WDHWD)

    def Get_Displays(self,num):
        return win32gui.GetWindowText(self.Displayer[num])

    def Close_App(self):
        #print("app is " + self.pro)
        self.pro.kill()


class EX1_TC1Error(Exception):
    pass

