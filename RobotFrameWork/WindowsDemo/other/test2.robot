*** Settings ***
Documentation     Test.

Library           EX1_TC1_Library.py

*** Test Cases ***
Use Keyboard Press Calculator Keybroad
    Launch App    calc
    Title should be    Calculator
    Open CSV    Sample.csv
	Load Row    2
	${Num} =    Get Total Number Length
	
	:FOR    ${Index}    IN RANGE   0    ${Num}
	\    Log    ${Index}
	\    Use Keyboard Press    ${Index}
	
	${Excpeted} =    Get Excepted Result
	${Displayed} =    Get Displayed Result
	
	Resut Should Equals    ${Excpeted}    ${Displayed}
	
	[Teardown]    Close App




