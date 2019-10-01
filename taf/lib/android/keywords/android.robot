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
    [Documentation]    Get list of connected device/emulator(s)
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
    [return]    ${result}

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
    [return]    ${result}

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

Open Airplane Mode
    [Documentation]    Open airplane mode setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.AIRPLANE_MODE_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Battery Saver Mode
    [Documentation]    Open battery saver mode setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.BATTERY_SAVER_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Bluetooth Mode
    [Documentation]    Open bluetooth mode setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.BLUETOOTH_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Data Roaming Page
    [Documentation]    Open data roaming setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.DATA_ROAMING_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Device Info Page
    [Documentation]    Open device info setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.DEVICE_INFO_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Display Page
    [Documentation]    Open display setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.DISPLAY_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Location Page
    [Documentation]    Open location setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.LOCATION_SOURCE_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Default Application Page
    [Documentation]    Open default application setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.MANAGE_DEFAULT_APPS_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Privacy Page
    [Documentation]    Open privacy setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.PRIVACY_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Setting Page
    [Documentation]    Open setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Sound Setting Page
    [Documentation]    Open sound setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.SOUND_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open VPN Setting Page
    [Documentation]    Open vpn setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.VPN_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open WiFi Setting Page
    [Documentation]    Open wifi setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.WIFI_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}

Open Wireless Setting Page
    [Documentation]    Open wireless setting page
    ...
    ...                *Arguments:*
    ...
    ...                *${deviceName}* - Connected device/emulator name
    [Arguments]    ${deviceName}
    ${rc}    ${result} =    Run And Return Rc And Output    adb -s ${deviceName} shell am start -a android.settings.WIRELESS_SETTINGS
    ${status}    Run Keyword And Return Status    Should Be Equal    '${rc}'    '0'
    Run Keyword If    '${status}' == 'False'    Fail    ${result}
