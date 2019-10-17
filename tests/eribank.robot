*** Settings ***
Library    AppiumLibrary

*** Test Cases ***
Launch Eribank APK
    Open Application    ${remoteURL}    platformName=%{platform}    deviceName=${deviceName}    systemPort=${systemPort}    app=%{apkpath}
