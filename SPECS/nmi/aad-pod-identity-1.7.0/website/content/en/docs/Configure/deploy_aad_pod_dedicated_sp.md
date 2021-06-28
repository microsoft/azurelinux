---
title: "Deploy AAD Pod Identity with a Dedicated Service Principal"
linkTitle: "Deploy AAD Pod Identity with a Dedicated Service Principal"
weight: 2
description: >
  To enable user to use a separate service principal (aad-pod-identity admin service principal) other than the cluster service princial and to move away from /etc/kubernetes/azure.json.
---

> Available from 1.5 release

## The why

Goal: To enable user to use a separate service principal (aad-pod-identity admin service principal) other than the cluster service princial and to move away from `/etc/kubernetes/azure.json`.

Users now have the option to deploy aad-pod-identity with a separate service principal which is together with its secret and other configurations stored in a Kubernetes secret object.

## Permissions

The permission of the admin service principal needs to be 'Contributor' role over the scope of node resource group starting with "MC_".

Create a new service principal with the permission:

```
az ad sp create-for-rbac -n "<sp_name>" --role "Contributor" --scopes "/subscriptions/<subscription-id>/resourceGroups/<MC_node_resource_group>"
```

> Note the `appId` (client id), `password` (secret) and `tenant` from the resulting json, which will be used in creating the admin secret.

Or assign the permission for an existing service principal:

```
az role assignment create --role "Contributor" --assignee <sp_id> --scope "/subscriptions/<subscription-id>/resourceGroups/<MC_node_resource_group>"
```

For any subsequent user assigned managed identity that's intended for a pod, it's also required to grant the service principal 'Managed Identity Operator' permission (also stated [here](../../getting-started/role-assignment/)):

```
az role assignment create --role "Managed Identity Operator" --assignee <sp_id> --scope <resource id of the managed identity>
```

## Create the admin secret

The `aadpodidentity-admin-secret` contains the following fields:

* Cloud: `<base64-encoded-cloud>`
  * 'Cloud' should be chosen from the following case-insensitive values: `AzurePublicCloud`, `AzureUSGovernmentCloud`, `AzureChinaCloud`, `AzureGermanCloud` (values taken from [here](https://raw.githubusercontent.com/Azure/go-autorest/master/autorest/azure/environments.go)).
* SubscriptionID: `<base64-encoded-subscription-id>`
* ResourceGroup: `<base64-encoded-resource-group>`
  * 'ResourceGroup' is the node resource group where the actual virtual machines or virtual machine scale set resides.
* VMType: `<base64-encoded-vm-type>`
  * 'VMType' is optional and can be one of these values: `standard` for normal virtual machine nodes, and `vmss` for cluster deployed with a virtual machine scale set.
* TenantID: `<base64-encoded-tenant-id>`
* ClientID: `<base64-encoded-client-id>`
* ClientSecret: `<base64-encoded-client-secret>`
  * 'TenantID', 'ClientID' and 'ClientSecret' are service principal's `tenant`, `appId`, `password` respectively.

> Use `echo -n 'secret-content' | base64` to create a base64 encoded string.

Fill out those secret values in the /deploy/infra/noazurejson/deployment.yaml or /deploy/infra/noazurejson/deployment-rbac.yaml before executing `kubectl create -f ./deploy/infra/noazurejson/deployment.yaml` or `kubectl create -f ./deploy/infra/noazurejson/deployment-rbac.yaml`.

> Note that if not use the above yaml's, `aadpodidentity-admin-secret` must be created before deploying `mic` and `mic` must reference the secret as shown in the yaml's.

The secret will be injected as an environment variable into `mic` upon pod creation and cannot be updated during the lifecycle of `mic`. However, redeploying `mic` should pick up the updated service principal's information should they change.