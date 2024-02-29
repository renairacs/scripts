#!/bin/bash

#Function to find an account by name
find_account_by_id() {
    local account_id="$1"
    local result
    result=$(aws organizations list-accounts --query "Accounts[?Id=='$account_id'][Id,Name,Status]" --output text)
    if [ $? -ne 0 ]; then
        echo "error"
        exit 1
    fi
    if [ -z "$result" ]; then
        echo "Account ID not found"
    else
        echo "Account ID: $result"
    fi
    #echo "$result" | jq -r --arg name "$account_name" '.Accounts[] | select(.Name == $name)'
}

echo "Type the account id:"
read account_id
find_account_by_id "$account_id"
