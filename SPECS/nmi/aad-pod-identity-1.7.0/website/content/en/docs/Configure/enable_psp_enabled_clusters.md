---
title: "Enable PSP Clusters"
linkTitle: "Enable PSP Clusters"
weight: 8
description: >
  If the cluster has Pod Security Policies (PSP) enabled that block hostNetwork and privileged mode, then the aad-pod-identity will be unable to run.
---

## Policy to allow aad-pod-identity to work in PSP enabled clusters

The NMI component of aad-pod-identity runs on `hostNetwork` and in `privileged` mode. If the cluster has Pod Security Policies (PSP) enabled that block `hostNetwork` and `privileged` mode, then the aad-pod-identity will be unable to run. The following step will create a PSP that allows the required access for aad-pod-identity components only in the desired namespace -


```bash
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/examples/psp-podidentity.yaml
```