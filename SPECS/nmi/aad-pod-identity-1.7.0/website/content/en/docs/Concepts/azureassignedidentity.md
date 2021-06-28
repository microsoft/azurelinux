---
title: "AzureAssignedIdentity"
linkTitle: "AzureAssignedIdentity"
weight: 3
date: 2020-11-03
description: >
  Describes the current state of identity binding relationship between an [`AzureIdentity`](../azureidentity) and a pod.
---

> Note: the lifecycle of `AzureAssignedIdentity` is fully managed by [MIC](../block-diagram-and-design). Users should not manually modify the fields.

## `AzureAssignedIdentity`

| Field                                                                                                                   | Description                                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiVersion`<br>*string*                                                                                                | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources.  |
| `kind`<br>*string*                                                                                                      | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. |
| `metadata`<br>[*`ObjectMeta`*](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#objectmeta-v1-meta) | Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata                                                                                                                                                                 |
| `spec`<br>[*`AzureAssignedIdentitySpec`*](#azureassignedidentityspec)                                                   | Describes the current state of identity binding relationship between an [`AzureIdentity`](../azureidentity) and a pod.                                                                                                                                                                              |

## `AzureAssignedIdentitySpec`

| Field                                                                  | Description                                                                                                                         |
|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `azureIdentityRef`<br>[*AzureIdentity*](../azureidentity)              | The [`AzureIdentity`](../azureidentity) that is bound to the pod.                                                                   |
| `azureBindingRef`<br>[*AzureIdentityBinding*](../azureidentitybinding) | The [`AzureIdentityBinding`](../azureidentitybinding) that is binding the [`AzureIdentity`](../azureidentity) and the pod together. |
| `pod`<br>*string*                                                      | The name of the pod that is bound to the [`AzureIdentity`](../azureidentity).                                                       |
| `podNamespace`<br>*string*                                             | The namespace of the pod that is bound to the [`AzureIdentity`](../azureidentity).                                                  |
| `nodename`<br>*string*                                                 | The name of the node that the pod is scheduled to.                                                                                  |
