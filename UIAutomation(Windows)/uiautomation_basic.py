"""
UIAutomation是微软Windows自带的一个Automation的接口库, 而有人将这些接口用Python打包了一下形成了一个python库uiautomation
安装方式"pip install uiautomation"
(https://github.com/yinkaisheng/Python-UIAutomation-for-Windows/blob/master/readme_cn.md)

uiautomation封装了微软UIAutomation API，支持自动化Win32，MFC，WPF，Modern UI(Metro UI), Qt, IE,
Firefox(version<=56 or >=60, Firefox57是第一个Rust开发版本,前几个Rust开发版本个人测试发现不支持),
Chrome和基于Electron开发的应用程序(Chrome浏览器和Electron应用需要加启动参数--force-renderer-accessibility才能支持UIAutomation).

最新版uiautomation2.0只支持Python 3版本，依赖comtypes和typing这两个包。 2.0版本之前的代码请参考API changes修改代码。

uiautomation支持在Windows XP SP3或更高版本的Windows桌面系统上运行。

如果是Windows XP系统，请确保系统目录有这个文件：UIAutomationCore.dll。如果没有，需要安装补丁 KB971513 才能支持UIAutomtion.

在Windows 7或更高版本Windows系统上使用uiautomation时，要以管理员权限运行Python， 否则uiautomation运行时很多函数可能会执行失败。
或者先以管理员权限运行cmd.exe，在cmd中再调用Python，如下图中cmd窗口标题中显示了管理员。

安装pip install uiautomation后，在Python的Scripts(比如C:\Python37\Scripts)目录中会有一个文件automation.py，
或者使用源码根目录里的automation.py。automation.py是用来枚举控件树结构的一个脚本。
"""

# 由于Windows自带的UI Automation是一个dll, 提供的接口是以C++来描述的, 所以作者在打包接口到Python时使用了很多c type

# 下面以作者Github上的一个demo做例子
import time

import uiautomation as auto
import subprocess

if __name__ == '__main__':
    auto.uiautomation.SetGlobalSearchTimeout(15)  # 设置全局搜索超时时间
    auto.ShowDesktop()  # 等于Win+D
    subprocess.Popen('notepad')  # 等于Win+R 再输入notepad回车
    time.sleep(1)
    '''
    查找ClassName为Notepad的Window控件, 查找深度1
    1. 注意查找深度是以当控件为0而定义的, 一般设置为1的话就表示搜索到当前控件的下一层
    2. GUI最顶层的控件是Windows桌面, 而一般来说一个程序的顶层控件都是一个WindowControl
    3. 在Windows的UIAutomation中, 所能够控制的控件一定是属于某种Control类型的, 比如一个Window就属于WindowControl
    WindowControl里面包含的其它控件, 比如notepad的Menu,就属于MenuBarControl
    '''
    note = auto.WindowControl(searchDepth=1, ClassName="Notepad")
    note.SetActive()  #
    edit = note.EditControl()  # 查找notepad window下的第一个edit控件, 不指定任何条件的话默认就是返回找到的第一个控件

    '''
    而不同的Control类型会支持不同的操作, UIAutomation中, 把一些相同的操作包装成为了Pattern, 一种Control能够支持不同的Pattern, 
    而不同的Control也可以支持同一种Pattern(表示这些Control都支持对它进行相同的操作)
    比如下面的EditControl就支持ValuePattern, 就可以使用ValuePattern包装的方法去操作这个Control
    '''
    edit_value_pattern = edit.GetValuePattern()  # 可以使用edit.GetPattern(auto.PatternId.ValuePattern)
    edit_value_pattern.SetValue("Hello World")
    edit.SendKeys('{Ctrl}{End}{Enter}By Elden')  # 当然可以使用模拟按键的方法来输入文字, 但这个方法主要还是用来向控件发送快捷键

    title_bar = note.TitleBarControl()  # 只有一个title bar
    # title bar上有三个按键, 最小化,最大化与关闭, 指定获得找到的ButtonControl的第2个
    max_size = title_bar.ButtonControl(foundIndex=2)
    max_size.Click()

    # 使用控件名字来查找控件(一般来说控件名字都与控件上显示出来的文字一样的)
    close = title_bar.ButtonControl(Name='Close')
    close.Click()
    auto.SendKeys('{Alt}n')





