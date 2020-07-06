*** Settings ***
Library         REST    https://jsonplaceholder.typicode.com
Documentation   1st case:
...                 Put in to Relay
...                 Get the message from the queue.
...                 Then validate the contract from the message
...             2nd case:
...                 Put in to relay
...                 Then get api and validate the contract


*** Variables ***
${json}         { "id": 11, "name": "Gil Alexander" }
&{dict}         name=Julie Langford


*** Test Cases ***
GET an existing user, notice how the schema gets more accurate
    GET         /users/1                  # this creates a new instance
    Output schema   response body
    Object      response body             # values are fully optional
    Integer     response body id
    String      response body name
#    [Teardown]  Output schema             # note the updated response schema