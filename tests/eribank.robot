*** Settings ***
Library    AppiumLibrary

*** Test Cases ***
Launch Eribank APK
    Open Application    ${remoteURL}    platformName=Android    deviceName=${deviceName}    systemPort=${systemPort}    app=/home/vidhi/Downloads/EriBank.apk
