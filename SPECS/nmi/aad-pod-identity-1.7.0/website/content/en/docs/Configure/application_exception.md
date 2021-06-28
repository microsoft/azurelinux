---
title: "Disable AAD Pod Identity for a specific Pod/Application"
linkTitle: "Disable AAD Pod Identity for a specific Pod/Application"
weight: 3
description: >
  NMI pods modify the nodes' iptables to intercept calls to Azure Instance Metadata endpoint. This means any request that's made to the Metadata endpoint will be intercepted by NMI even if the pod doesn't use aad-pod-identity.
---

> Available from 1.5 release

NMI pods modify the nodes' iptables to intercept calls to Azure Instance Metadata endpoint. This means any request that's made to the Metadata endpoint will be intercepted by NMI even if the pod doesn't use aad-pod-identity. `AzurePodIdentityException` CRD can be configured to inform aad-pod-identity that any requests to metadata endpoint originating from a pod that matches labels defined in CRD should be proxied without any processing in NMI. NMI will proxy the request to the metdata endpoint and return the token back as is without any validation.

1. Create the `AzurePodIdentityException` with the same label that will be defined in the pod -

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzurePodIdentityException
metadata:
  name: test-exception
spec:
  podLabels:
    foo: bar
    app: custom
```

Use the [sample template](https://github.com/Azure/aad-pod-identity/blob/master/examples/azurepodidentityexception.yaml), replace the podLabels with a list of desired values and then create the resource on the cluster:

```shell
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/examples/azurepodidentityexception.yaml
```

When creating application pods that will not be using aad-pod-identity for calls to Azure Instance Metadata endpoint, include at least one of the labels in `spec.template.metadata.labels`.

Example pod with same label as above defined in the spec -

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample
  labels:
    app: sample
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample
  template:
    metadata:
      labels:
        app: sample
        foo: bar      <------- Label defined in exception CRD included in deployment
    spec:
      [...]
```

To verify the pods have the right label that match the ones defined in the exception crd -
```shell
kubectl get pods --show-labels
NAME                           READY   STATUS    RESTARTS   AGE   LABELS
sample-td                      1/1     Running   0          16s   app=sample,foo=bar
```

**NOTE**
- `AzurePodIdentityException` is per namespace. This means if the same label needs to be used in multiple namespaces to except pods, a CRD resource needs to be created in each namespace.
- All the labels defined in the exception CRD doesn't need to be defined in the deployment/pod spec. A single match is enough for the pod to be excepted.