---
title: "Match Pods in the Namespace"
linkTitle: "Match Pods in the Namespace"
weight: 1
description: >
  By default, AAD Pod Identity matches pods to identities across namespaces.
---

> Available from [1.3.0-mic-1.4.0-nmi release](https://github.com/Azure/aad-pod-identity/releases/tag/1.3.0-mic-1.4.0-nmi)

By default, AAD Pod Identity matches pods to identities across namespaces. To match only pods in the namespace containing `AzureIdentity`, use one of these techniques:

* Attach a `aadpodidentity.k8s.io/Behavior: namespaced` annotation to each `AzureIdentity` resource.

    Here is the `AzureIdentity` manifest from the previous step with this annotation added:

    ```yaml
    apiVersion: "aadpodidentity.k8s.io/v1"
    kind: AzureIdentity
    metadata:
      name: <a-idname>
      annotations:
        aadpodidentity.k8s.io/Behavior: namespaced
    spec:
      type: 0
      resourceID: /subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>
      clientID: <clientId>
    ```

* Add the `--forceNamespaced` command line argument or set the `FORCENAMESPACED=true` environment variable when starting both the MIC and NMI components.

    Here is a section from the MIC deployment which adds *both* the command line argument and the environment variable for illustration. Pick one approach and use it to update both the MIC deployment and the NMI daemon set.

    ```yaml
        spec:
          containers:
          - name: mic
            image: "mcr.microsoft.com/k8s/aad-pod-identity/mic:1.3"
            imagePullPolicy: Always
            args:
              - "--cloudconfig=/etc/kubernetes/azure.json"
              - "--logtostderr"
              - "--forceNamespaced"
            env:
              - name: FORCENAMESPACED
                value: "true"