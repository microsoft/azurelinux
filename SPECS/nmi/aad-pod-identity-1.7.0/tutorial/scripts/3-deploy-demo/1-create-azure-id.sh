#!/bin/bash

set -e

set -x

# had to create the identity in the generated RG
# https://github.com/Azure/aad-pod-identity/issues/38
# you will need to replace the resource group below with the correct name
# you may need to look in the Azure Portal to find the correct name
# or you can use the CLI with something like 
# $az group list | grep 'k8s'

if [ -z "$MC_RG" ]
then
      echo "K8S Resource Group Name Not Set. Set the env variable with the following command:"
      echo "export MC_RG=\"resource-group-name\" "
      return 1
fi

if [ -z "$SUB_ID" ]
then
      SUB_ID=$(az account show | jq -r .id)
      echo "Subscription ${SUB_ID} detected from environment"
fi

export principalid=$(az identity create --name demo-aad1 --resource-group $MC_RG --query 'principalId' -o tsv)
az role assignment create --role Reader --assignee $principalid --scope /subscriptions/$SUB_ID/resourcegroups/$MC_RG
