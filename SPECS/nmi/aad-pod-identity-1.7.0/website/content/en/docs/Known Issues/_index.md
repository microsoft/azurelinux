---
title: "Known Issues"
linkTitle: "Known Issues"
weight: 6
date: 2020-10-04
description: >
  This section lists the major known issues with aad-pod-identity. 
---

For a complete list of issues, please check our [GitHub issues page](https://github.com/Azure/aad-pod-identity/issues) or [file a new issue](https://github.com/Azure/aad-pod-identity/issues/new?assignees=&labels=bug&template=bug_report.md&title=) if your issue is not listed.

- NMI pods not yet running during a cluster autoscaling event
- User-assigned managed identity deleted and recreated with the same name in Azure

## NMI pods not yet running during a cluster autoscaling event

NMI redirects Instance Metadata Service (IMDS) requests to itself by setting up iptables rules after it starts running on the node. During cluster scale up, there **might** be a scenario where the `kube-scheduler` schedules the workload pod before the NMI pod on the new nodes. In such a scenario, the token request will be directly sent to IMDS instead of being intercepted by NMI. What this means is that the workload pod that runs before the NMI pod on the node can access identities that it doesn't have access to.

There is currently no solution in Kubernetes where a node can be set to `NoSchedule` until critical addons have been deployed to the cluster. There was a KEP for this particular enhancement - [kubernetes/enhancements#1003](https://github.com/kubernetes/enhancements/pull/1003) which is now closed.

## User-assigned managed identity deleted and recreated with the same name in Azure

When the user-assigned managed identities have been deleted and re-created in Azure with the same name, the changes aren't automatically reflected in the identities on the underlying VM/VMSS. `az <vm|vmss> identity show -g <resource group> -n <VM/VMSS name>` command output will show the identity with `null` principalID and clientID. Token request for this identity will fail with "identity not found" error.

```json
{
  "principalId": null,
  "tenantId": null,
  "type": "UserAssigned",
  "userAssignedIdentities": {
    "/subscriptions/<sub>/resourcegroups/<resource group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity name>": {
      "clientId": "null",
      "principalId": "null"
    }
  }
}

```

Steps to take if the identity was deleted and re-created with same name -

1. Remove identity manually from the VM/VMSS by running `az <vm|vmss> identity remove -g <rg> -n <VM/VMSS name> --identities <identity resource id>`
2. Update the `AzureIdentity` with the new clientID for the recreated identity

MIC will detect the change in `AzureIdentity` and reassign the identity. This reassignment will ensure the identity with correct clientID exists on the underlying VM/VMSS.