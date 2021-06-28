---
title: "Pod Identity in Custom Cloud"
linkTitle: "Pod Identity in Custom Cloud"
weight: 5
description: >
  Using AAD Pod Identity in custom Azure cloud environment.
---

This document highlights the steps to configure and use AAD Pod Identity in custom Azure cloud environments.

1. Ensure the cloud name in `/etc/kubernetes/azure.json` is set to `AzureStackCloud`

    ```json
    {
        "cloud": "AzureStackCloud",
        "tenantId": "xxxx",
        "subscriptionId": "xxxx",
        ...
    }
    ```

2. Mount the JSON file that contains the custom cloud environment details. The custom cloud environment file is stored in the file system of the Kubernetes node. The `go-autorest` library is configured to [read the Azure environment from file](https://github.com/Azure/go-autorest/blob/autorest/v0.10.0/autorest/azure/environments.go#L219-L221) by default for `AzureStackCloud`

    > NOTE: In case of AKS clusters, the custom cloud environment file is `/etc/kubernetes/akscustom.json`

    The file needs to be mounted only for the MIC pods.

    Add the custom environment file volume mount in MIC deployment:
    ```yaml
    - name: custom-env-file
      mountPath: /etc/kubernetes/akscustom.json
      readOnly: true
    ```
    Add the custom environment file volume in MIC deployment:
    ```yaml
    - name: custom-env-file
      hostPath:
        path: /etc/kubernetes/akscustom.json
    ```

3. Set the `AZURE_ENVIRONMENT_FILEPATH` environment variable as part of MIC deployment. This is used by `go-autorest` to [read the custom cloud environment file](https://github.com/Azure/go-autorest/blob/autorest/v0.10.0/autorest/azure/environments.go#L26-L28).

    Add the environment variable to MIC deployment:
    ```yaml
    - name: AZURE_ENVIRONMENT_FILEPATH
      value: "/etc/kubernetes/akscustom.json"
    ```
