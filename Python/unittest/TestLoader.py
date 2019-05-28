import unittest

#suite = unittest.TestSuite()#创建测试套件
all_cases1 = unittest.defaultTestLoader.discover('.','*Test*.py') #找到某个目录下所有的以test开头的Python文件里面的测试用例
print(type(all_cases1))



#for case in all_cases:
#    print(case)
#    suite.addTests(case)#把所有的测试用例添加进来


#runner = unittest.TextTestRunner()
#runner.run(all_cases1)
result = unittest.TestResult


#result.
