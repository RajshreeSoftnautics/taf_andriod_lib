*** Settings ***
Library    OperatingSystem
Resource    ${CURDIR}/../taf/lib/android/keywords/android.robot
Resource    ${CURDIR}/../taf/lib/common/keywords/mobilecommon.robot

*** Variables ***
${device}    ${deviceName}

*** Test Cases ***
Get Appium Process
    ${pid}    Get Appium Process Id List
    log to console    \n\n${pid}
    Set Suite Variable    ${pid}

Stop Appium
    ${result}    Stop Appium Server    ${pid[0]}
    log to console    \n\n${result}

Start Appium
    ${result}    Start Appium Server
    log to console    \n\n${result}

Get List
    ${dList}    Get ADB Device List
    log to console    \n\n${dList}
    Set Suite Variable    ${dList}

ADB
    ADB Keyevent    ${device}    3
    Sleep    30s
    Open Device Status Bar    ${device}
    Sleep    30s
    Close Device Status Bar    ${device}
    Sleep    30s
    ${sNum}    Get Android Serial Number    ${device}
    log to console    \n\n${sNum}
    Sleep    30s
    ${sVersion}    Get Android Version    ${device}
    log to console    \n\n${sVersion}
    Sleep    30s
    Open Airplane Mode    ${device}
    Sleep    30s
    Go To Home    ${device}
    Sleep    30s
    Open Battery Saver Mode    ${device}
    Sleep    30s
    Open Browser    ${device}
    Sleep    30s
    Open Contacts    ${device}
    Sleep    30s
    Open Data Roaming Page    ${device}
    Sleep    30s
    Open Default Application Page    ${device}
    Sleep    30s
    Open Device Info Page    ${device}
    Sleep    30s
    Open Display Page    ${device}
    Sleep    30s
    Open Location Page    ${device}
    Sleep    30s
    Open Privacy Page    ${device}
    Sleep    30s
    Open Setting Page    ${device}
    Sleep    30s
    Open Sound Setting Page    ${device}
    Sleep    30s
    Open VPN Setting Page    ${device}
    Sleep    30s
    Open WiFi Setting Page    ${device}
    Sleep    30s
    Turn On WiFi    ${device}
    Sleep    30s
    Turn Off WiFi    ${device}
    Sleep    30s
    Open Wireless Setting Page    ${device}
    Sleep    30s
    Reboot Device    ${device}
    Sleep    30s
    Open Bluetooth Mode    ${device}
    Sleep    30s

WiFi
    [Tags]    wifi only
    Turn On WiFi    ${device}
    Sleep    30s
    Turn Off WiFi    ${device}
