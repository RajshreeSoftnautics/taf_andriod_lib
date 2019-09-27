*** Settings ***
Library    ${CURDIR}/../src/android.py

*** Keywords ***
Start Appium Server
    [Documentation]    start appium server
    [Arguments]    ${port}=4723
    ${state}    startAppium    ${port}
    [return]    ${state}

Stop Appium Server
    [Documentation]    stop appium server
    [Arguments]    ${port}=4723
    ${state}    stopAppium    ${port}
    [return]    ${state}

Get ADB Device List
    [Documentation]    get list of connected device/emulator(s)
    ${deviceList}    getConnectedDeviceList
    [return]    ${deviceList}

