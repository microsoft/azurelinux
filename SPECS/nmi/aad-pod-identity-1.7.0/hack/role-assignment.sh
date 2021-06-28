#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

[[ ! -z "${SUBSCRIPTION_ID:-}" ]] || (echo 'Must specify SUBSCRIPTION_ID' && exit 1)
[[ ! -z "${RESOURCE_GROUP:-}" ]] || (echo 'Must specify RESOURCE_GROUP' && exit 1)
[[ ! -z "${CLUSTER_NAME:-}" ]] || (echo 'Must specify CLUSTER_NAME' && exit 1)
[[ ! -z "${CLUSTER_LOCATION:-}" ]] || (echo 'Must specify CLUSTER_LOCATION' && exit 1)

echo "az login as a user and set the appropriate subscription ID"
az login
az account set -s "${SUBSCRIPTION_ID}"

echo "Retrieving your cluster identity ID, which will be used for role assignment"
ID="$(az aks show -g ${RESOURCE_GROUP} -n ${CLUSTER_NAME} --query servicePrincipalProfile.clientId -otsv)"

echo "Checking if the aks cluster is using managed identity"
if [[ "${ID:-}" == "msi" ]]; then
  ID="$(az aks show -g ${RESOURCE_GROUP} -n ${CLUSTER_NAME} --query identityProfile.kubeletidentity.clientId -otsv)"
fi

echo "Performing role assignments"
az role assignment create --role "Managed Identity Operator" --assignee "${ID}" --scope "/subscriptions/${SUBSCRIPTION_ID}/resourcegroups/MC_${RESOURCE_GROUP}_${CLUSTER_NAME}_${CLUSTER_LOCATION}"
az role assignment create --role "Virtual Machine Contributor" --assignee "${ID}" --scope "/subscriptions/${SUBSCRIPTION_ID}/resourcegroups/MC_${RESOURCE_GROUP}_${CLUSTER_NAME}_${CLUSTER_LOCATION}"

# your resource group that is used to store your user-assigned identities
# assuming it is within the same subscription as your AKS node resource group
if [[ -n "${IDENTITY_RESOURCE_GROUP:-}" ]]; then
  az role assignment create --role "Managed Identity Operator" --assignee "${ID}" --scope "/subscriptions/${SUBSCRIPTION_ID}/resourcegroups/${IDENTITY_RESOURCE_GROUP}"
fi
