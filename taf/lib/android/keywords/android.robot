*** Settings ***
Library    ${CURDIR}/../src/android.py

*** Keywords ***
Start Appium Server
    [Documentation]    start appium server
    ...
    ...                *Arguments:*
    ...
    ...                *${port}* - Appium server Port number
    [Arguments]    ${port}=4723
    ${state}    startAppium    ${port}
    [return]    ${state}

Stop Appium Server
    [Documentation]    stop appium server
    ...
    ...                *Arguments:*
    ...
    ...                *${port}* - Appium server Port number
    [Arguments]    ${port}=4723
    ${state}    stopAppium    ${port}
    [return]    ${state}

Get ADB Device List
    [Documentation]    get list of connected device/emulator(s)
    ${deviceList}    getConnectedDeviceList
    [return]    ${deviceList}

Reboot Device
    [Documentation]    Reboot connected device
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} reboot
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Get Android Version
    [Documentation]    Get connected device android version
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell getprop ro.build.version.release
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Get Android Serial Number
    [Documentation]    Get connected device serial number
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} get-serialno
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Device Status Bar
    [Documentation]    Open device status bar
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell service call statusbar 1
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Close Device Status Bar
    [Documentation]    Close device status bar
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell service call statusbar 2
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Go To Home
    [Documentation]    Go to home page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell input keyevent 3
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Browser
    [Documentation]    Open browser page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell input keyevent 64
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Contacts
    [Documentation]    Open device contacts
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell input keyevent 207
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

ADB Keyevent
    [Documentation]    Run ADB Keyevent
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    ...
    ...                *${key}* - ADB Keyevent that user want to run
    [Arguments]    ${deviceName}    ${key}
    ${key}    Convert To Integer    ${key}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell input keyevent ${key}
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Get Android Logs
    [Documentation]    Get android logs and store to given path
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    ...
    ...                *${filePath}* - Absolute file path where user want to store android logs
    [Arguments]    ${deviceName}    ${filePath}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} logcat > ${filePath}
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}
