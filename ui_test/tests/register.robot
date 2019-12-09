*** Settings ***
Documentation     Register account workflows.

Resource    ../resources/common_keywords.robot
Variables   ../resources/config.py
Library     ../resources/HomePage.py
Library     ../resources/LoginPage.py
Library     ../resources/RegisterPage.py
Library     ../resources/MyAccountPage.py
Library     PageObjectLibrary
Library     SeleniumLibrary
Library     Process

Test Teardown   Close Browser

*** Test Cases ***
Register account
    Given Open browser to home page
    When Click on login
    And Create new account
    And Fill out customer form
    And Click on submit account
    Then The current page should be    MyAccountPage
