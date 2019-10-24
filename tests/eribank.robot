*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Resource    ${CURDIR}/../taf/lib/android/keywords/android.robot

*** Variables ***
${uName}    com.experitest.ExperiBank:id/usernameTextField
${pWord}    com.experitest.ExperiBank:id/passwordTextField
${userName}    company
${password}    company
${login}    com.experitest.ExperiBank:id/loginButton
${logout}    com.experitest.ExperiBank:id/logoutButton

*** Test Cases ***
Launch Eribank APK
    Open Application    ${remoteURL}    platformName=%{platform}    deviceName=${deviceName}    udid=${deviceName}    systemPort=${systemPort}    app=%{apkpath}

Login To Eribank
    Input Text    ${uName}    ${userName}
    Input Text    ${pWord}    ${password}
    Click Element    ${login}

Logout From Eribank
    Wait Until Page Contains Element    ${logout}
    Click Element    ${logout}
    Wait Until Page Contains Element    ${login}

Get Coordinates
    Open WiFi Setting Page    ${deviceName}
    Sleep    20s
    ${coordinates}    Android Get X Y Coordinate    //android.widget.LinearLayout[@index=6]    //android.widget.LinearLayout[@index=1]
    Sleep    40s
    Swipe    ${coordinates[0]}    ${coordinates[1]}    ${coordinates[2]}    ${coordinates[3]}
