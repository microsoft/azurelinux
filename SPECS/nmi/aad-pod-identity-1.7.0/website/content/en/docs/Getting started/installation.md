---
title: "Installation"
linkTitle: "Installation"
weight: 2
description: >
  How to install AAD Pod Identity on your clusters.
---

## Quick Install

To install/upgrade AAD Pod Identity on RBAC-enabled clusters:

```
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/v1.7.0/deploy/infra/deployment-rbac.yaml
```

<details>
<summary>Result</summary>

```
serviceaccount/aad-pod-id-nmi-service-account created
customresourcedefinition.apiextensions.k8s.io/azureassignedidentities.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azureidentitybindings.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azureidentities.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azurepodidentityexceptions.aadpodidentity.k8s.io created
clusterrole.rbac.authorization.k8s.io/aad-pod-id-nmi-role created
clusterrolebinding.rbac.authorization.k8s.io/aad-pod-id-nmi-binding created
daemonset.apps/nmi created
serviceaccount/aad-pod-id-mic-service-account created
clusterrole.rbac.authorization.k8s.io/aad-pod-id-mic-role created
clusterrolebinding.rbac.authorization.k8s.io/aad-pod-id-mic-binding created
deployment.apps/mic created
```

</details><br/>

To install/upgrade aad-pod-identity on RBAC-disabled clusters:

```
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/v1.7.0/deploy/infra/deployment.yaml
```

<details>
<summary>Result</summary>

```
customresourcedefinition.apiextensions.k8s.io/azureassignedidentities.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azureidentitybindings.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azureidentities.aadpodidentity.k8s.io created
customresourcedefinition.apiextensions.k8s.io/azurepodidentityexceptions.aadpodidentity.k8s.io created
daemonset.apps/nmi created
deployment.apps/mic created
```

</details><br/>

For AKS clusters, you will have to allow MIC and AKS add-ons to access IMDS without being intercepted by NMI:

```
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/v1.7.0/deploy/infra/mic-exception.yaml
```

> WARNING: failure to apply `mic-exception.yaml` in AKS clusters will result in token failures for AKS addons using managed identity for authentication.

<details>
<summary>Result</summary>

```
azurepodidentityexception.aadpodidentity.k8s.io/mic-exception created
azurepodidentityexception.aadpodidentity.k8s.io/aks-addon-exception created
```

</details>

## Helm

AAD Pod Identity allows users to customize their installation via Helm.

> Although AAD Pod Identity helm chart is backward with Helm 2, it is recommended to use Helm 3 instead.

```
helm repo add aad-pod-identity https://raw.githubusercontent.com/Azure/aad-pod-identity/master/charts

# Helm 3
helm install aad-pod-identity aad-pod-identity/aad-pod-identity

# Helm 2
helm install aad-pod-identity/aad-pod-identity --set=installCRDs=true
```

### Values

For a list of customizable values that can be injected when invoking `helm install`, please see the [Helm chart configurations](https://github.com/Azure/aad-pod-identity/tree/master/charts/aad-pod-identity#configuration).
