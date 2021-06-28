---
title: "Managed Identity Controller (MIC)"
linkTitle: "Managed Identity Controller (MIC)"
weight: 5
description: >
  A Kubernetes controller that watches for changes to pods, `AzureIdentity` and `AzureIdentityBindings` through the Kubernetes API Server. When it detects a relevant change, the MIC adds or deletes `AzureAssignedIdentity` as needed.
---

Specifically, when a pod is scheduled, the MIC assigns the identity on Azure to the underlying VM/VMSS during the creation phase. When all pods using the identity are deleted, it removes the identity from the underlying VM/VMSS on Azure. The MIC takes similar actions when `AzureIdentity` or `AzureIdentityBinding` are created or deleted.
