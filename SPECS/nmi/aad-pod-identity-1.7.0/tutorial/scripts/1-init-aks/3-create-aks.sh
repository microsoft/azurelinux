#!/bin/bash

set -e

if [ -z "$RG" ]
then
      echo "Resource Group Name Not Set. Set the env variable with the following command:"
      echo "export RG=\"rg-name\" "
      return 1
fi

if [ -z "$K8S_NAME" ]
then
      echo "Kubernetes Cluster Name Not Set. Set the env variable with the following command:"
      echo "export K8S_NAME=\"K8S_NAME\" "
      return 1
fi

echo "Creating AKS cluster named $K8S_NAME with 1 node. This may take a while..."
set -x

az aks create --resource-group $RG --name $K8S_NAME --node-count 1 --generate-ssh-keys
