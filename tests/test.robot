*** Settings ***
Suite Setup    Should be equal    0    0

*** Test Cases ***
TC1
    [Tags]    1    sanity
    Should be equal    WO    WO

TC2
    Should be equal    by    y

TC3
    [Tags]    3
    Sleep    30s
    Should be equal    by    y
