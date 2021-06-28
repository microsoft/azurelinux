#!/bin/bash

cd "${0%/*}"

file="../../../../deploy/demo/aadpodidentity.yaml"

set -e

echo "To give the Azure Id to the cluster, update the deploy/aadpodidentity.yaml spec with \
your subscription, clientID, resource group, and type (0=Azure Id, 1=Service Principal). "

read -p "Press enter to continue"

set -x

client_id=$(az identity show -n demo-aad1 -g ${MC_RG} | jq -r .clientId)
resource_id=$(az identity show -n demo-aad1 -g ${MC_RG} | jq -r .id)

perl -pi -e "s/CLIENT_ID/${client_id}/" ${file}
perl -pi -e "s/RESOURCE_ID/${resource_id//\//\\/}/" ${file}

kubectl apply -f ${file}
