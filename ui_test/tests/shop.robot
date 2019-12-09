*** Settings ***
Documentation     Shop workflows.

Resource    ../resources/common_keywords.robot
Variables   ../resources/config.py
Library     ../resources/HomePage.py
Library     ../resources/TShirtsPage.py
Library     PageObjectLibrary
Library     SeleniumLibrary
Library     Process

Test Teardown   Close Browser

*** Test Cases ***
Shop for any T-Shirt
    Given Open browser to home page
    When click on tshirt
    Then The current page should be    TShirtsPage
    When add to cart
    Then Page Should Contain    Product successfully added to your shopping cart
