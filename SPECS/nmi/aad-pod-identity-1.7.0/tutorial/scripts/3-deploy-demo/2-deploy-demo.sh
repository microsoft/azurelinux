#!/bin/bash

cd "${0%/*}"

file="../../../../deploy/demo/deployment.yaml"

set -e
echo "To deploy the demo app, update the /deploy/demo.deployment.yaml arguments with \
your subscription, clientID and resource group. \
Make sure your identity with the client ID has reader permission to the resource group provided in the input."

read -p "Press enter to continue"

client_id=$(az identity show -n demo-aad1 -g ${MC_RG} | jq -r .clientId)
subscription_id=$(az account show | jq -r .id)

perl -pi -e "s/CLIENT_ID/${client_id}/" ${file}
perl -pi -e "s/SUBSCRIPTION_ID/${subscription_id}/" ${file}
perl -pi -e "s/RESOURCE_GROUP/${MC_RG}/" ${file}



# aad-pod-identity/deploy/demo/deployment.yaml is the original file 
set -x

kubectl apply -f ${file} 
