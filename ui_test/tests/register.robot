*** Settings ***
Documentation     Register account workflows.

Variables   ../resources/config.py
Library    ../resources/HomePage.py
Library    ../resources/LoginPage.py
Library    ../resources/RegisterPage.py
Library    ../resources/MyAccountPage.py
Library     PageObjectLibrary
Library     SeleniumLibrary
Library     Process

#Test Teardown   Close Browser

*** Test Cases ***
Register account
    Given Open browser to home page
    When click on login
    When create new account
    When fill out customer form
    Then The current page should be    MyAccountPage


*** Keywords ***
Open Browser To Home Page
    Open browser    ${CONFIG.server}    ${CONFIG.browser}
    Maximize Browser Window
    Set Selenium Speed    ${CONFIG.delay}
