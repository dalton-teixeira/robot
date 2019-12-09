*** Settings ***
Library         REST   https://fakerestapi.azurewebsites.net/api


*** Test Cases ***
Valid Book
    When GET            /Books/1
    Then String         response body Title         Book 1

New Book
    When POST           /Books                      ${CURDIR}/../resources/book.json
    Then String         response body Title         New Book
    And Integer         response body ID            99


Edit Book
    When PUT            /Books/99                   ${CURDIR}/../resources/book_edited.json
    Then String         response body Title         Edited Book
    And Integer         response body PageCount     130

Delete
    When DELETE         /Books/99
    Then Integer        response status             200    202     204

Valid users
    When GET            /Books
    Then Integer        response status             200    202     204


