---
title: "AzureIdentityBinding"
linkTitle: "AzureIdentityBinding"
weight: 2
date: 2020-11-03
description: >
  Describes the identity binding relationship between an `AzureIdentity` and a pod with a specific selector as part of its label.
---

<details>
<summary>Examples</summary>

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentityBinding
metadata:
  name: <AzureIdentityBindingName>
spec:
  azureIdentity: "<AzureIdentityName>"
  selector: "<Selector>"
```

</details>

## `AzureIdentityBinding`

| Field                                                                                                                   | Description                                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiVersion`<br>*string*                                                                                                | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources.  |
| `kind`<br>*string*                                                                                                      | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. |
| `metadata`<br>[*`ObjectMeta`*](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#objectmeta-v1-meta) | Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata                                                                                                                                                                 |
| `spec`<br>[*`AzureIdentityBindingSpec`*](#azureidentitybindingspec)                                                     | Describes the specifications of an identity binding relationship between an [`AzureIdentity`](../azureidentity) and pod(s).                                                                                                                                                                         |

## `AzureIdentityBindingSpec`

| Field                       | Description                                                                                                                                                                                                |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `azureIdentity`<br>*string* | The name of the [`AzureIdentity`](../azureidentity) that should be assigned to the pod(s) if matching selector is found.                                                                                   |
| `selector`<br>*string*      | The selector to identify which pods should be assigned to the `AzureIdentity` above. It will go through a list of pods and look for value of pod label with key `aadpodidbinding` that is equal to itself. |
