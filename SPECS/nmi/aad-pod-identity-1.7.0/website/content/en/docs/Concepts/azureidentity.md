---
title: "AzureIdentity"
linkTitle: "AzureIdentity"
weight: 1
date: 2020-11-03
description: >
  Describes one of the following Azure identity resources: 0) user-assigned identity, 1) service principal, or 2) service principal with certifcate.
---

<details>
<summary>Examples</summary>

- user-assigned identity

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: <AzureIdentityName>
spec:
  type: 0
  resourceID: <ResourceID>
  clientID: <ClientID>
```

- service principal (single-tenant)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <SecretName>
type: Opaque
data:
  clientSecret: <ClientSecret>
---
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: <AzureIdentityName>
spec:
  type: 1
  tenantID: <TenantID>
  clientID: <ClientID>
  clientPassword: {"name":"<SecretName>","namespace":"<SecretNamespace>"}
```

- service principal (multi-tenant)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <SecretName>
type: Opaque
data:
  clientSecret: <ClientSecret>
---
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: <AzureIdentityName>
spec:
  type: 1
  tenantID: <PrimaryTenantID>
  auxiliaryTenantIDs:
    - <AuxiliaryTenantID1>
    - <AuxiliaryTenantID2>
  clientID: <ClientID>
  clientPassword: {"name":"<SecretName>","namespace":"<SecretNamespace>"}
```

- service principal (certifcate)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <SecretName>
type: Opaque
data:
  certificate: <Certificate>
  password: <Password>
---
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: <AzureIdentityName>
spec:
  type: 2
  tenantID: <TenantID>
  clientID: <ClientID>
  clientPassword: {"Name":"<SecretName>","Namespace":"<SecretNamespace>"}
```

</details>

## `AzureIdentity`

| Field                                                                                                                   | Description                                                                                                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiVersion`<br>*string*                                                                                                | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources.  |
| `kind`<br>*string*                                                                                                      | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds. |
| `metadata`<br>[*`ObjectMeta`*](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#objectmeta-v1-meta) | Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata                                                                                                                                                                 |
| `spec`<br>[*`AzureIdentitySpec`*](#azureidentityspec)                                                                   | Describes the specifications of an identity resource on Azure.                                                                                                                                                                                                                                      |

## `AzureIdentitySpec`

| Field                                                                                                                                 | Description                                                                                                                                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`<br>*integer*                                                                                                                   | `0`: user-assigned identity.<br>`1`: service principal. <br>`2`: service principal with certificate.                                                                                                                                             |
| `resourceID`<br>*string*                                                                                                              | The resource ID of the user-assigned identity (only applicable when `type` is `0`), i.e. `/subscriptions/<SubscriptionID>/resourcegroups/<ResourceGroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<UserAssignedIdentityName>`. |
| `clientID`<br>*string*                                                                                                                | The client ID of the identity.                                                                                                                                                                                                                   |
| `clientPassword`<br>[*SecretReference*](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#secretreference-v1-core) | The client secret of the identity, represented as a Kubernetes secret (only applicable when `type` is `1` or `2`).                                                                                                                               |
| `tenantID`<br>*string*                                                                                                                | The primary tenant ID of the identity (only applicable when `type` is `1` or `2`).                                                                                                                                                               |
| `auxiliaryTenantIDs`<br>*[]string*                                                                                                    | The auxiliary tenant IDs of the identity (only applicable when `type` is `1`).                                                                                                                                                                   |
| `adEndpoint`<br>*string*                                                                                                              | The Azure Active Directory endpoint.                                                                                                                                                                                                             |
