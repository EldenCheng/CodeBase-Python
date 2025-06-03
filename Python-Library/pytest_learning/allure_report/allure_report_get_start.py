"""
Allure Report
安装方式
1. 安装测试框架的Adapter, 在Python中就是pip install allure-pytest
2. 安装命令行工具, 在Windows中, 可以使用scoop来安装, 也可以在Github上下载exe文件然后把它加到环境变量中
"""
import logging
import os
import allure
import pytest

"""
spec: https://allurereport.org/docs/pytest-configuration/#options-affecting-test-selection
使用allure, 需要传递一些allure对应的参数到pytest框架, 让pytest框架能够把一些数据写入到allure中, 传递参数可以使用pytest的命令行开关, 比如
python -m pytest --alluredir ./allure-data --clean-alluredir

又或者在pytest.ini中定义addopts项目, 例子请参考本文件同一目录下的pytest.ini, 要注意当定义了addopts后, 所有运行的pytest测试默认都会调用
这些参数
比如有用的参数如下:
1. --alluredir [目录], 用于指定allure存放测试结果的目录, 默认是每次运行测试的结果都会混合在旧的测试结果中的, 程序会自动建立这个目录
2. --clean-alluredir, 在运行新的测试前, 把结果目录中旧的测试结果清空
3. --allure-severities, --allure-epics, --allure-features, --allure-stories, --allure-ids, --allure-label,--inversion
   如果test case中有使用对应的表头, 那么就可以使用上面的这些参数开控制pytest运行的test case的范围, 其中, --inversion表示运行不符合限定范围
   的test case, 比如python -m pytest --allure-label owner=Elden --inversion, 就是运行除了标签是owner=Elden之外的所有test case
"""

"""
spec: https://allurereport.org/docs/gettingstarted-readability/#description-links-and-other-metadata Meta-data在Report中的作用
      https://allurereport.org/docs/pytest-reference/#metadata 定义Meta-data
首先, 可以定义一些Report所用到的meta-data, 下面是一些典型的, 当然这些表头可以在测试文件中分开定义, 也可以在pytest的fixture中统一定义,
下面是当前版本的allure所支持的所有能定义的meta-data:
`allure.title`, `allure.description`, `allure.description_html`, `allure.label`, `allure.severity`, `allure.epic`,
`allure.feature`, `allure.story`, `allure.suite`, `allure.parent_suite`, `allure.sub_suite`, `allure.tag`,`allure.id`,
`allure.manual`, `allure.link`, `allure.issue`, `allure.testcase`, `allure.step`

其中, allure.step中是最常用的, 因为一个测试中, 一个test会包括多个step
"""

"""
allure可以附上各种各样的文件作为附件, 当然, 用得最多的还是图像
如果附上的是文字(比如json)或者图像(截图), 可以直接使用allure.attach方法
如果附上的是一个文件, 比如zip, 可以使用allure.attach.file方法
"""

"""
系统环境参数, 在运行完成后, 可以在allure report的数据目录里定义一个叫environment.properties, 然后把系统环境的参数输入, 那么生成report时, report就会
包括这些参数, 例子请参考本文件相同目录下的environment.properties文件
"""

"""
Executor参数, 这个参数主要用于CI流程中, 用以指明是CI中那一个build触发的测试流程, 可以在运行后放置到allure report的数据目录里, 生成report时
report就会包括这些参数, 例子请参考本文件相同目录下的executor.json

又或者可以单纯用于定义谁做的测试, 例子请参考本文件相同目录下的executor2.json
"""

"""
History, 当使用数据生成一个report之后, report目录里会包含一个History目录, 先把这个目录拷贝出来, 然后运行下一次相同的测试, 再把History目录复制到
新一次的allure data目录中, 再生成report, 那么新的report就会带有一些history的内容, allure report中, 好像最高支持最近10次的history
"""

"""
运行完之后, allure generate -o .\allure-report --single-file report 创建一个可视化test report, -o是输出路径, 
注: 1. --single-file是生成单文件report, 使用单文件report是为防止浏览器的安全设置阻挡打不开report, 单文件就不会有这个问题
       但single-file有个问题就是没有了history目录, 可能会对测试的tend之类的图表会造成影响
    2. 程序会自动建立文件目录
"""

"""
如果不是生成单个文件的report, 直接使用浏览器打开index.html可能会由于安全性设置的问题加载不出来数据, 这就需要使用参数暂时关闭浏览器的安全设置
, 具体可以参考本文件相同目录下的open_allure_report.bat里的命令行, 也可以在快捷方式里添加参数, 可以参考Google Chrome.lnk
又或者可以使用allure open [报告目录]来打开报告
"""

@allure.title("Test Allure Report")
@allure.description("This test attempt to test how the Allure Report works")
@allure.tag("Allure Report", "Get Start")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Elden")
@allure.link("https://dev.example.com/", name="Website")
@allure.issue("AUTH-123")
@allure.testcase("TMS-456")

def test_allure_get_start():

    # 这里建议把Step独立写出来, 这样的话写脚本时就能清楚地分开每一个step的逻辑
    step = "Open a website"
    # 要注意, 如果需要在pytest中显示log, 需要在pytest.ini上增加log相关的设置, 具体可参考本文件同目录下的pytest.ini
    logging.info(step) # 可打印, 可不打印, 打印的好处是可以在运行是清楚地看到现在test case运行到哪一步
    # print(step) # 使用print的话, 只会在测试运行完成后, 才能显示在输出设备上
    with allure.step(step):
        pass

    step = "Check the website's title"
    logging.info(step)
    # print(step)
    with allure.step(step):
        assert True

    step = "Capture the snapshot of the website"
    logging.info(step)
    # print(step)
    with allure.step(step):
        capture_file = rb = open("./website_snapshot.PNG", 'rb').read()
        # attach方法只接受byte与str
        allure.attach(capture_file, name="full-page", attachment_type=allure.attachment_type.PNG)

    step = "And attach a JSON file"
    logging.info(step)
    # print(step)
    with allure.step(step):
        allure.attach.file("./test_case.json", name="Json-example", attachment_type=allure.attachment_type.JSON)

if __name__ == '__main__':
    pytest.main(["-s", "allure_report_get_start.py"])



