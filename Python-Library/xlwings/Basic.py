'''
xlwings 这个库是通过打开excel的实例来实现excel的操作
'''

import xlwings

#wb_temp = xlwings.Book("./Report3.xlsx")

Apps = xlwings.apps

App = xlwings.App(visible=True)

book = App.books[0]


App.quit()

#wb_temp.close()

#wb_temp.app.quit()

