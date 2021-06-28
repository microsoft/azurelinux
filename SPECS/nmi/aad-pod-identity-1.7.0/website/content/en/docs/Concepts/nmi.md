---
title: "Node Managed Identity (NMI)"
linkTitle: "Node Managed Identity (NMI)"
weight: 5
description: >
  Makes an Azure Active Directory Authentication Library ([ADAL](https://docs.microsoft.com/en-us/azure/active-directory/azuread-dev/active-directory-authentication-libraries)) request to get a token on behalf of pods by intercepting IMDS traffic on each node and redirect them to itself.
---

The authorization request to fetch a Service Principal Token from an MSI endpoint is sent to Azure Instance Metadata Service (IMDS) endpoint (169.254.169.254), which is redirected to the NMI pod. The redirection is accomplished by adding iptable rules to redirect all non-host traffic with IMDS endpoint on port 80 as destination to the NMI endpoint. The NMI server identifies the pod based on the remote address of the request and then queries Kubernetes (through `AzureAssignedIdentity`) for a matching Azure identity. NMI then makes an Azure Active Directory Authentication Library ([ADAL](https://docs.microsoft.com/en-us/azure/active-directory/azuread-dev/active-directory-authentication-libraries)) request to get the token for the client ID and returns it as a response. If the request had client ID as part of the query, it is validated against the admin-configured client ID.

Here is an example cURL command that will fetch an access token to access ARM within a pod identified by an AAD-Pod-Identity selector:

```bash
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F' -H Metadata:true -s
```

For different ways to acquire an access token within a pod, please refer to this [documentation](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token).

Similarly, a host can make an authorization request to fetch Service Principal Token for a resource directly from the NMI host endpoint (http://127.0.0.1:2579/host/token/). The request must include the pod namespace `podns` and the pod name `podname` in the request header and the resource endpoint of the resource requesting the token. The NMI server identifies the pod based on the `podns` and `podname` in the request header and then queries k8s (through `AzureAssignedIdentity`) for a matching azure identity. Then NMI makes an ADAL request to get a token for the resource in the request, returning the `token` and the `clientid` as a response.

Here is an example cURL command:

```bash
curl http://127.0.0.1:2579/host/token/?resource=https://vault.azure.net -H "podname: nginx-flex-kv-int" -H "podns: default"
```

For more information, please refer to the [design documentation](../../design).
