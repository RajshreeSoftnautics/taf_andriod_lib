*** Settings ***
Library    ${CURDIR}/../src/mobilecommon.py

*** Keywords ***
Get Appium Process Id List
    [Documentation]    Check appium server running or not and return process id list
    ${processList}    checkAppiumStatus
    [return]    ${processList}

Start Appium Server
    [Documentation]    start appium server
    ...
    ...                *Arguments:*
    ...
    ...                *${port}* - Appium server port number
    [Arguments]    ${port}=4723
    ${state}    startAppium    ${port}
    [return]    ${state}

Stop Appium Server
    [Documentation]    stop appium server
    ...
    ...                *Arguments:*
    ...
    ...                *${pid}* - Appium server process id
    [Arguments]    ${pid}
    ${state}    stopAppium    ${pid}
    [return]    ${state}
