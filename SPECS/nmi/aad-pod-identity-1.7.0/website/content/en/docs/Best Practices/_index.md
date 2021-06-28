---
title: "Best Practices"
linkTitle: "Best Practices"
weight: 5
date: 2020-10-04
description: >
  This document highlights the best practices when using aad-pod-identity.
---

## Retry on token retrieval

aad-pod-identity retrieves access tokens on behalf of your workload by intercepting token requests to the Instance Metadata Service (IMDS) endpoint (169.254.169.254). However, it does not perform any sort of token caching. We believe that either the users or the SDK that your application is using is responsible for token management.

Note that there is a brief window between when your application started running and the identity gets assigned to the underlying node. If your application tried to retrieve an access token during that period, it might fail. The following table describes the duration that you could expect to wait based on your cluster's node type:

| Node Type                 | Identity Assignment Duration |
|---------------------------|------------------------------|
| Virtual Machine           | 10 - 20 seconds              |
| Virtual Machine Scale Set | 40 - 60 seconds              |

> Note: the delay only occurs when the user-assigned identity is not assigned to the underlying node on Azure. Subsequent token requests will not incur this delay after identity assignment.

By default, when fetching an access token, NMI performs 16 retries with 5 seconds in between each retry to check whether the `AzureIdentity` assigned to your pod has been successfully assigned to the underlying node on Azure. It will return an error if it is still not assigned after `16 retries x 5 seconds = 80 seconds`. Also, your workload might encounter an error if it times out before NMI finishes this operation. You can adjust the number of retries and the delay in between each retry via the NMI flags `--retry-attempts-for-created` and `--find-identity-retry-interval`.

Additional retry logic is also implemented internally in most of Azure's SDKs to prevent your application from erroring out. For example, [azure-sdk-for-go](https://github.com/Azure/azure-sdk-for-go) by default performs five retries with exponential backoff when fetching an access token from IMDS.

Alternatively, you could set up a simple init container to probe for successful identity assignment by MIC and prevent applications from starting prematurely. Here is an example init-container with Azure CLI.

```yaml
...
initContainers:
- name: init
  image: mcr.microsoft.com/azure-cli
  command:
    - sh
    - -c
    - az login --identity --debug
...
```

## A pod using multiple AzureIdentities

In some scenarios, you might want to assign multiple `AzureIdentities` to a workload. Here is an example of how to achieve that:

### AzureIdentities

```yaml
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentity
metadata:
  name: az-id-1
spec:
  type: 0
  resourceID: <ResourceID of az-id-1>
  clientID: <ClientID of az-id-1>
```

```yaml
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentity
metadata:
  name: az-id-2
spec:
  type: 0
  resourceID: <ResourceID of az-id-2>
  clientID: <ClientID of az-id-2>
```

### AzureIdentityBinding

```yaml
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentityBinding
metadata:
  name: az-id-1-binding
spec:
  azureIdentity: az-id-1
  selector: az-id-combined
```

```yaml
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentityBinding
metadata:
  name: az-id-2-binding
spec:
  azureIdentity: az-id-2
  selector: az-id-combined
```

### Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo
  labels:
    aadpodidbinding: az-id-combined
...
```

## Pods using unauthorized AzureIdentities

By default, aad-pod-identity matches pods with `AzureIdentities` across all namespaces. That means that a malicious pod could assign itself an unauthorized pod identity label and acquire a token with that particular `AzureIdentity`. This scenario can be mitigated by performing the following:

- Deploy aad-pod-identity with [namespaced mode](../configure/match_pods_in_namespace/). This will restrict pods from binding with `AzureIdentities` across different namespaces. Note that `AzureIdentities` and `AzureIdentityBindings` must be deployed to the same namespace as your workload when using namespaced mode.

- Set up Kubernetes-native RBAC to restrict access and creation of `AzureIdentities` across sensitive namespaces.

- Set up RBAC on Azure to restrict access and creation of user-assigned identities.

## Using aad-pod-identity in different Kubernetes workloads

### [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: azure-cli
spec:
  selector:
    matchLabels:
      name: azure-cli
  template:
    metadata:
      labels:
        name: azure-cli
        aadpodidbinding: <selector defined in AzureIdentityBinding>
    spec:
      containers:
      - name: azure-cli
        image: mcr.microsoft.com/azure-cli
        command:
          - sh
          - -c
          - az login --identity --debug
```

### [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: azure-cli
spec:
  selector:
    matchLabels:
      name: azure-cli
  template:
    metadata:
      labels:
        name: azure-cli
        aadpodidbinding: <selector defined in AzureIdentityBinding>
    spec:
      containers:
      - name: azure-cli
        image: mcr.microsoft.com/azure-cli
        command:
          - sh
          - -c
          - az login --identity --debug
```

### [Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: azure-cli
spec:
  template:
    metadata:
      labels:
        aadpodidbinding: <selector defined in AzureIdentityBinding>
    spec:
      containers:
      - name: azure-cli
        image: mcr.microsoft.com/azure-cli
        command:
          - sh
          - -c
          - az login --identity --debug
      restartPolicy: Never
  backoffLimit: 4
```

### [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: azure-cli
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            aadpodidbinding: <selector defined in AzureIdentityBinding>
        spec:
          containers:
          - name: azure-cli
            image: mcr.microsoft.com/azure-cli
            command:
            - sh
            - -c
            - az login --identity --debug
          restartPolicy: OnFailure
```