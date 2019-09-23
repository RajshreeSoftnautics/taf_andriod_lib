*** Settings ***
Library    AppiumLibrary

*** Test Cases ***
Launch Eribank APK
    Open Application    http://localhost:4723/wd/hub    platformName=Android    deviceName='emulator-5554'    app=/home/vidhi/Downloads/EriBank.apk
