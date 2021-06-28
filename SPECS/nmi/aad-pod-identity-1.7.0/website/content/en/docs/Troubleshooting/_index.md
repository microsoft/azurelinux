---
title: "Troubleshooting"
linkTitle: "Troubleshooting"
weight: 7
date: 2020-10-04
description: >
  An overview of a list of components to assist in troubleshooting.
---

## Logging

Below is a list of commands you can use to view relevant logs of aad-pod-identity components.

### Isolate errors from logs

You can use `grep ^E` and `--since` flag from `kubectl` to isolate any errors occurred after a given duration.

```bash
kubectl logs -l component=mic --since=1h | grep ^E
kubectl logs -l component=nmi --since=1h | grep ^E
```

> It is always a good idea to include relevant logs from MIC and NMI when opening a new [issue](https://github.com/Azure/aad-pod-identity/issues).

### Ensure that iptables rule exists

To ensure that the correct iptables rule is injected to each node via the [NMI](../concepts/nmi) pods, the following command ensures that on a given node, there exists an iptables rule where all packets with a destination IP of 169.254.169.254 (IMDS endpoint) are routed to port 2579 of the host network.

```bash
NMI_POD=$(kubectl get pod -l component=nmi -ojsonpath='{.items[?(@.spec.nodeName=="<NodeName>")].metadata.name}')
kubectl exec $NMI_POD -- iptables -t nat -S aad-metadata
```

The expected output should be:

```log
-N aad-metadata
-A aad-metadata ! -s 127.0.0.1/32 -d 169.254.169.254/32 -p tcp -m tcp --dport 80 -j DNAT --to-destination 10.240.0.34:2579
-A aad-metadata -j RETURN
```

### Run a pod to validate your identity setup

You could run the following commands to validate your identity setup (assuming you have the proper `AzureIdentity` and `AzureIdentityBinding` deployed):

```bash
kubectl run azure-cli -it --image=mcr.microsoft.com/azure-cli --labels=aadpodidbinding=<selector defined in AzureIdentityBinding> /bin/bash

# within the azure-cli shell
az login -i --debug
```

`az login -i` will use the Azure identity bound to the `azure-cli` pod and perform a login to Azure via Azure CLI. If succeeded, you would have an output as below:

```log
urllib3.connectionpool : Starting new HTTP connection (1): 169.254.169.254:80
urllib3.connectionpool : http://169.254.169.254:80 "GET /metadata/identity/oauth2/token?resource=https%3A%2F%2Fmanagement.core.windows.net%2F&api-version=2018-02-01 HTTP/1.1" 200 1667
msrestazure.azure_active_directory : MSI: Retrieving a token from http://169.254.169.254/metadata/identity/oauth2/token, with payload {'resource': 'https://management.core.windows.net/', 'api-version': '2018-02-01'}
msrestazure.azure_active_directory : MSI: Token retrieved
MSI: token was retrieved. Now trying to initialize local accounts...
...
[
  {
    "environmentName": "AzureCloud",
    "homeTenantId": "<REDACTED>",
    "id": "<REDACTED>",
    "isDefault": true,
    "managedByTenants": [],
    "name": "<REDACTED>",
    "state": "Enabled",
    "tenantId": "<REDACTED>",
    "user": {
      "assignedIdentityInfo": "MSI",
      "name": "systemAssignedIdentity",
      "type": "servicePrincipal"
    }
  }
]
```

Based on the logs above, Azure CLI was able to retrieve a token from `http://169.254.169.254:80/metadata/identity/oauth2/token`. Its request is routed to the NMI pod that is running within the same node. Identify which node the Azure CLI pod is scheduled to by running the following command:

```bash
kubectl get pods -owide

NAME                                    READY   STATUS    RESTARTS   AGE   IP             NODE                                 NOMINATED NODE   READINESS GATES
azure-cli                               1/1     Running   1          12s   10.240.0.117   k8s-agentpool1-95854893-vmss000002   <none>           <none>
```

Take a note at the node the pod is scheduled to and its IP address. Check the logs of the NMI pod that is scheduled to the same node. You should be able to see a token requested by the azure-cli pod, identified by its pod IP address `10.240.0.117`:

```bash
kubectl logs <nmi pod name>

...
I0821 18:22:50.810806       1 standard.go:72] no clientID or resourceID in request. default/azure-cli has been matched with azure identity default/demo
I0821 18:22:50.810895       1 standard.go:178] matched identityType:0 clientid:7eb6##### REDACTED #####a6a9 resource:https://management.core.windows.net/
I0821 18:22:51.348117       1 server.go:190] status (200) took 537597287 ns for req.method=GET reg.path=/metadata/identity/oauth2/token req.remote=10.240.0.117
...
```

## Common Issues

Common issues or questions that users have run into when using pod identity are detailed below.

### Ignoring azure identity \<podns\>/\<podname\>, error: Invalid resource id: "", must match /subscriptions/\<subid\>/resourcegroups/\<resourcegroup\>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/\<name\>

If you are using MIC v1.6.0+, you will need to ensure the correct capitalization of `AzureIdentity` and `AzureIdentityBinding` fields. For more information, please refer to [this section](../#v160-breaking-change).

### LinkedAuthorizationFailed

If you received the following error message in MIC:

```log
Code="LinkedAuthorizationFailed" Message="The client '<ClientID>' with object id '<ObjectID>' has permission to perform action 'Microsoft.Compute/<VMType>/write' on scope '<VM/VMSS scope>'; however, it does not have permission to perform action 'Microsoft.ManagedIdentity/userAssignedIdentities/assign/action' on the linked scope(s) '<UserAssignedIdentityScope>' or the linked scope(s) are invalid."
```

It means that your cluster service principal / managed identity does not have the correct role assignment to assign the chosen user-assigned identities to the VM/VMSS. For more information, please follow this [documentation](../getting-started/role-assignment/) to allow your cluster service principal / managed identity to perform identity-related operation.

Past issues:

- https://github.com/Azure/aad-pod-identity/issues/585

### Unable to remove `AzureAssignedIdentity` after MIC pods are deleted

With release `1.6.1`, finalizers have been added to `AzureAssignedIdentity` to ensure the identities are successfully cleaned up by MIC before they're deleted. However, in scenarios where the MIC deployment is force deleted before it has completed the clean up of identities from the underlying node, the `AzureAssignedIdentity` will be left behind as it contains a finalizer.

To delete all `AzureAssignedIdentity`, run the following command:
```bash
kubectl get azureassignedidentity -A -o=json | jq '.items[].metadata.finalizers=null' | kubectl apply -f -
kubectl delete azureassignedidentity --all
```

To delete only a specific `AzureAssignedIdentity`, run the following command:
```bash
kubectl get azureassignedidentity <name> -n <namespace> -o=json | jq '.items[].metadata.finalizers=null' | kubectl apply -f -
kubectl delete azureassignedidentity <name> -n <namespace>
```

Past issues:
- https://github.com/Azure/aad-pod-identity/issues/644