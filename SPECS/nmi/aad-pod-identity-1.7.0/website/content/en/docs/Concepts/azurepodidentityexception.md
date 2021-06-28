---
title: "AzurePodIdentityException"
linkTitle: "AzurePodIdentityException"
weight: 4
date: 2020-11-03
description: >
  Allow pods with certain labels to access IMDS without being intercepted by NMI.
---

<details>
<summary>Examples</summary>

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzurePodIdentityException
metadata:
  name: aks-addon-exception
  namespace: kube-system
spec:
  podLabels:
    kubernetes.azure.com/managedby: aks
```

</details>

## `AzurePodIdentityException`

| Field                                                                                                                   | Description                                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiVersion`<br>*string*                                                                                                | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources.  |
| `kind`<br>*string*                                                                                                      | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. |
| `metadata`<br>[*`ObjectMeta`*](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#objectmeta-v1-meta) | Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata                                                                                                                                                                 |
| `spec`<br>[*`AzurePodIdentityExceptionSpec`*](#azurepodidentityexceptionspec)                                           | Describes the specifications of which pods are allowed to access IMDS without being intercepted by NMI.                                                                                                                                                                                             |

## `AzurePodIdentityExceptionSpec`

| Field                              | Description                                           |
|------------------------------------|-------------------------------------------------------|
| `podLabels`<br>*map[string]string* | Pods with matching labels will bypass NMI validation. |
