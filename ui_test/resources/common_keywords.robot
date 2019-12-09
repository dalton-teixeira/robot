*** Keywords ***
Open Browser To Home Page
    Open browser    ${CONFIG.server}    ${CONFIG.browser}
    Maximize Browser Window
    Set Selenium Speed    ${CONFIG.delay}
