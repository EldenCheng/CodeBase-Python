*** Settings ***
Documentation     Test.

Library           EX1_TC1_Library.py

*** Test Cases ***
Use Mouse Click Calculator
    Launch App    calc
    Title should be    Calculator
    Open CSV    Sample.csv
	Load Row    All
	${Num} =    Get Total Number Length
	
	:FOR    ${Index}    IN RANGE   0    ${Num}
	\    Log    ${Index}
	\    Use Mouse Click    ${Index}
	
	${Excpeted} =    Get Excepted Result
	${Displayed} =    Get Displayed Result
	
	Resut Should Equals    ${Excpeted}    ${Displayed}
	
	[Teardown]    Close App
	
Use Keyboard Press Calculator
    Launch App    calc
    Title should be    Calculator
    Open CSV    Sample.csv
	Load Row    All
	${Num} =    Get Total Number Length
	
	:FOR    ${Index}    IN RANGE   0    ${Num}
	\    Log    ${Index}
	\    Use Keyboard Press    ${Index}
	
	${Excpeted} =    Get Excepted Result
	${Displayed} =    Get Displayed Result
	
	Resut Should Equals    ${Excpeted}    ${Displayed}
	
	[Teardown]    Close App




