*** Settings ***
Library           Selenium2Library

*** Test Cases ***
test01
    [Documentation]    测试淘宝
    Open Browser    https://login.taobao.com/member/login.jhtml    chrome
    maximize browser window
    #Maximize Browser Window
    Click Element    xpath=//*[@id="J_Quick2Static"]
    #Click Element    id=J_Quick2Static
    Sleep    1
    Input Text    xpath=//*[@id="TPL_username_1"]    123
    Input Text    xpath=//*[@id="TPL_password_1"]    123
    ${title_1}    Get Title
    Click Button     xpath=//*[@id="J_SubmitStatic"]
    Sleep     2
    ${title_2}    Get Title
    should not contain    ${title_2}    ${title_1}
    Close browser