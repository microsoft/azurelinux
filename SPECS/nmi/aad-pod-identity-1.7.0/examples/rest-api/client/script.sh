#!/bin/sh

echo "Hello ${RESOURCE}"

i=0
while true
do
    echo "Iteration $i"

    jwt=$(curl -sS http://169.254.169.254/metadata/identity/oauth2/token/?resource=$RESOURCE)
    echo "Full token:  $jwt"
    token=$(echo $jwt | jq -r '.access_token')
    echo "Access token:  $token"
    curl -v -H 'Accept: application/json' -H "Authorization: Bearer ${token}" $SERVICE_URL

    i=$((i+1))
    sleep 1
done