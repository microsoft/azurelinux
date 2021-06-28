# aad-pod-identity

[aad-pod-identity](https://github.com/Azure/aad-pod-identity) enables Kubernetes applications to access cloud resources securely with [Azure Active Directory](https://azure.microsoft.com/en-us/services/active-directory/) (AAD).

## TL;DR

```console
helm repo add aad-pod-identity https://raw.githubusercontent.com/Azure/aad-pod-identity/master/charts

# Helm 3
helm install aad-pod-identity aad-pod-identity/aad-pod-identity

# Helm 2
helm install aad-pod-identity/aad-pod-identity --set=installCRDs=true
```

## Helm chart and aad-pod-identity versions

| Helm Chart Version | AAD Pod Identity Version |
| ------------------ | ------------------------ |
| `1.5.2`            | `1.5.2`                  |
| `1.5.3`            | `1.5.3`                  |
| `1.5.4`            | `1.5.4`                  |
| `1.5.5`            | `1.5.5`                  |
| `1.5.6`            | `1.5.5`                  |
| `1.6.0`            | `1.6.0`                  |
| `2.0.0`            | `1.6.1`                  |
| `2.0.1`            | `1.6.2`                  |
| `2.0.2`            | `1.6.3`                  |

## Introduction

A simple [helm](https://helm.sh/) chart for setting up the components needed to use [Azure Active Directory Pod Identity](https://github.com/Azure/aad-pod-identity) in Kubernetes.

This helm chart will deploy the following resources:
* AzureIdentity `CustomResourceDefinition`
* AzureIdentityBinding `CustomResourceDefinition`
* AzureAssignedIdentity `CustomResourceDefinition`
* AzurePodIdentityException `CustomResourceDefinition`
* AzureIdentity instance (optional)
* AzureIdentityBinding instance (optional)
* Managed Identity Controller (MIC) `Deployment`
* Node Managed Identity (NMI) `DaemonSet`

## Getting Started
The following steps will help you create a new Azure identity ([Managed Service Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) or [Service Principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)) and assign it to pods running in your Kubernetes cluster.

### Prerequisites
* [Azure Subscription](https://azure.microsoft.com/)
* [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/services/kubernetes-service/) or [AKS Engine](https://github.com/Azure/aks-engine) deployment
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (authenticated to your Kubernetes cluster)
* [Helm 3](https://v3.helm.sh/)
* [Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* [git](https://git-scm.com/downloads)

> It is recommended to use [Helm 3](https://v3.helm.sh/) for installation and uninstallation, however, [Helm 2](https://v2.helm.sh/) is also supported.

<details>
<summary><strong>[Optional] Creating user identity</strong></summary>

1. Create a new [Azure User Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) using the Azure CLI:
> __NOTE:__ It's simpler to use the same resource group as your Kubernetes nodes are deployed in. For AKS this is the MC_* resource group. If you can't use the same resource group, you'll need to grant the Kubernetes cluster's service principal the "Managed Identity Operator" role.
```shell
az identity create -g <resource-group> -n <id-name>
```

2. Assign your newly created identity the appropriate role to the resource you want to access.
</details>


#### Installing charts

* If you need one or more `AzureIdentity` and `AzureIdentityBinding` resources to be created as part of the chart installation, add them to the azureidentities list in the values.yaml and replace the resourceID, clientID using the values for the respective user identities.
* If you need the aad-pod-identity deployment to use its own service principal credentials instead of the cluster service principal `/etc/kubernetes/azure.json`, then uncomment this section and add the appropriate values for each required field.
* To use a User Managed Identity instead of a service principal set `clientID` and `clientSecret` to `msi`,  set `useMSI` to `true`, and `userAssignedMSIClientID` to the client ID of the User Managed Identity.

```
adminsecret:
  cloud: <cloud environment name>
  subscriptionID: <subscription id>
  resourceGroup: <node resource group>
  vmType: <`standard` for normal virtual machine nodes, and `vmss` for cluster deployed with a virtual machine scale set>
  tenantID: <service principal tenant id>
  clientID: <service principal client id. Set to `msi` when using a User Managed Identity>
  clientSecret: <service principal client secret. Set to `msi` when using a User Managed Identity>
  useMSI: <set to true when using a User Managed Identity>
  userAssignedMSIClientID: <client id for the User Managed Identity>
```

To install the chart with the release name `my-release`:

```console
helm install --name my-release aad-pod-identity/aad-pod-identity
```

Deploy your application to Kubernetes. The application can use [ADAL](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-authentication-libraries) to request a token from the MSI endpoint as usual. If you do not currently have such an application, a demo application is available [here](https://github.com/Azure/aad-pod-identity#demo-app). If you do use the demo application, please update the `deployment.yaml` with the appropriate subscription ID, client ID and resource group name. Also make sure the selector you defined in your `AzureIdentityBinding` matches the `aadpodidbinding` label on the deployment.

## Uninstalling the Chart

To uninstall/delete the last deployment:

```console
helm ls

# Helm 3
helm uninstall <ReleaseName>

# Helm 2
helm delete <ReleaseName> --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

> The CRD created by the chart are not removed by default and should be manually cleaned up (if required)

```bash
kubectl delete crd azureassignedidentities.aadpodidentity.k8s.io
kubectl delete crd azureidentities.aadpodidentity.k8s.io
kubectl delete crd azureidentitybindings.aadpodidentity.k8s.io
kubectl delete crd azurepodidentityexceptions.aadpodidentity.k8s.io
```

## Upgrade guide

### Upgrading from chart version 1.5.5

1.5.5 helm chart had introduced 2 labels which could possibly change with chart upgrade:

```yaml
      app.kubernetes.io/managed-by: Helm
      helm.sh/chart: aad-pod-identity-1.5.5
```

This has been fixed in chart version `1.5.6` to prevent any issues with future upgrades of helm chart. For upgrading from 1.5.5 to any new chart version, a suggested workaround is editing the nmi and mic manifests to remove those 2 labels from `selector.matchLabels`:

```bash
kubectl get ds aad-pod-identity-nmi -o jsonpath='{.spec.selector.matchLabels}'
map[app.kubernetes.io/component:nmi app.kubernetes.io/instance:pod-identity app.kubernetes.io/managed-by:Helm app.kubernetes.io/name:aad-pod-identity helm.sh/chart:aad-pod-identity-1.5.5]

kubectl edit ds aad-pod-identity-nmi
(Remove `app.kubernetes.io/managed-by: Helm` and `helm.sh/chart: aad-pod-identity-1.5.5` from the spec.selector.matchLabels)

kubectl get deploy aad-pod-identity-mic -o jsonpath='{.spec.selector.matchLabels}'
map[app.kubernetes.io/component:mic app.kubernetes.io/instance:pod-identity app.kubernetes.io/managed-by:Helm app.kubernetes.io/name:aad-pod-identity helm.sh/chart:aad-pod-identity-1.5.5]

kubectl edit deploy aad-pod-identity-mic
(Remove `app.kubernetes.io/managed-by: Helm` and `helm.sh/chart: aad-pod-identity-1.5.5` from the spec.selector.matchLabels)
```
Once this is done, the helm upgrade command will succeed.


### Upgrading to a New Major Chart Version

A major chart version change (like v1.6.0 -> v2.0.0) indicates that there is a backward-incompatible (breaking) change needing manual actions.

#### 2.0.0

This version removes the `azureIdentity` and `azureIdentityBinding` values in favor of `azureIdentities`, a list of identities and their respective bindings, to support the creation of multiple AzureIdentity and AzureIdentityBinding resources.

The following is a basic example of the required change in the user-supplied values file.

```diff
- azureIdentity:
-   enabled: true
-   name: "azure-identity"
-   namespace: "azure-identity-namespace"
-   type: 0
-   resourceID: "resource-id"
-   clientID: "client-id"
- azureIdentityBinding:
-   name: "azure-identity-binding"
-   selector: "demo"
+ azureIdentities:
+   - name: "azure-identity"
+     namespace: "azure-identity-namespace"
+     type: 0
+     resourceID: "resource-id"
+     clientID: "client-id"
+     binding:
+       name: "azure-identity-binding"
+       selector: "demo"
```

## Configuration

The following tables list the configurable parameters of the aad-pod-identity chart and their default values.

| Parameter                                 | Description                                                                                                                                                                                                                                                                                                                   | Default                                                        |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `nameOverride`                            | String to partially override aad-pod-identity.fullname template with a string (will prepend the release name)                                                                                                                                                                                                                 | `""`                                                           |
| `fullnameOverride`                        | String to fully override aad-pod-identity.fullname template with a string                                                                                                                                                                                                                                                     | `""`                                                           |
| `image.repository`                        | Image repository                                                                                                                                                                                                                                                                                                              | `mcr.microsoft.com/oss/azure/aad-pod-identity`                 |
| `image.pullPolicy`                        | Image pull policy                                                                                                                                                                                                                                                                                                             | `Always`                                                       |
| `imagePullSecrets`                        | One or more secrets to be used when pulling images                                                                                                                                                                                                                                                                            | `[]`                                                           |
| `forceNameSpaced`                         | By default, AAD Pod Identity matches pods to identities across namespaces. To match only pods in the namespace containing AzureIdentity set this to true.                                                                                                                                                                     | `false`                                                        |
| `installMICException`                     | When NMI runs on a node where MIC is running, then MIC token request call is also intercepted by NMI. MIC can't get a valid token to initialize and then assign the identity. Installing an exception for MIC would ensure all token requests for MIC pods directly go to IMDS and not go through the pod-identity validation | `true`                                                         |
| `adminsecret.cloud`                       | Azure cloud environment name                                                                                                                                                                                                                                                                                                  | ` `                                                            |
| `adminsecret.subscriptionID`              | Azure subscription ID                                                                                                                                                                                                                                                                                                         | ` `                                                            |
| `adminsecret.resourceGroup`               | Azure resource group                                                                                                                                                                                                                                                                                                          | ` `                                                            |
| `adminsecret.vmType`                      | `standard` for normal virtual machine nodes, and `vmss` for cluster deployed with a virtual machine scale set                                                                                                                                                                                                                 | ` `                                                            |
| `adminsecret.tenantID`                    | Azure service principal tenantID                                                                                                                                                                                                                                                                                              | ` `                                                            |
| `adminsecret.clientID`                    | Azure service principal clientID or `msi` when using a managed identity                                                                                                                                                                                                                                                       | ` `                                                            |
| `adminsecret.clientSecret`                | Azure service principal clientSecret or `msi` when using a user managed identity                                                                                                                                                                                                                                              | ` `                                                            |
| `adminsecret.useMSI`                      | Set to `true` when using a user managed identity                                                                                                                                                                                                                                                                              | ` `                                                            |
| `adminsecret.userAssignedMSIClientID`     | Azure user managed identity client ID                                                                                                                                                                                                                                                                                         | ` `                                                            |
| `mic.image`                               | MIC image name                                                                                                                                                                                                                                                                                                                | `mic`                                                          |
| `mic.tag`                                 | MIC image tag                                                                                                                                                                                                                                                                                                                 | `v1.7.0`                                                       |
| `mic.priorityClassName`                   | MIC priority class (can only be set when deploying to kube-system namespace)                                                                                                                                                                                                                                                  |                                                                |
| `mic.logVerbosity`                        | Log level. Uses V logs (klog)                                                                                                                                                                                                                                                                                                 | `0`                                                            |
| `mic.loggingFormat`                       | Log format. One of (text                                                                                                                                                                                                                                                                                                      | json)                                                          | `text` |
| `mic.resources`                           | Resource limit for MIC                                                                                                                                                                                                                                                                                                        | `{}`                                                           |
| `mic.podAnnotations`                      | Pod annotations for MIC                                                                                                                                                                                                                                                                                                       | `{}`                                                           |
| `mic.tolerations`                         | Affinity settings                                                                                                                                                                                                                                                                                                             | `{}`                                                           |
| `mic.affinity`                            | List of node taints to tolerate                                                                                                                                                                                                                                                                                               | `[]`                                                           |
| `mic.leaderElection.instance`             | Override leader election instance name                                                                                                                                                                                                                                                                                        | If not provided, default value is `hostname`                   |
| `mic.leaderElection.namespace`            | Override the namespace to create leader election objects                                                                                                                                                                                                                                                                      | `default`                                                      |
| `mic.leaderElection.name`                 | Override leader election name                                                                                                                                                                                                                                                                                                 | If not provided, default value is `aad-pod-identity-mic`       |
| `mic.leaderElection.duration`             | Override leader election duration                                                                                                                                                                                                                                                                                             | If not provided, default value is `15s`                        |
| `mic.probePort`                           | Override http liveliness probe port                                                                                                                                                                                                                                                                                           | If not provided, default port is `8080`                        |
| `mic.syncRetryDuration`                   | Override interval in seconds at which sync loop should periodically check for errors and reconcile                                                                                                                                                                                                                            | If not provided, default value is `3600s`                      |
| `mic.immutableUserMSIs`                   | List of  user-defined identities that shouldn't be deleted from VM/VMSS.                                                                                                                                                                                                                                                      | If not provided, default value is empty                        |
| `mic.cloudConfig`                         | The cloud configuration used to authenticate with Azure                                                                                                                                                                                                                                                                       | If not provided, default value is `/etc/kubernetes/azure.json` |
| `mic.updateUserMSIMaxRetry`               | The maximum retry of UpdateUserMSI call in case of assignment errors                                                                                                                                                                                                                                                          | If not provided, default value is `2`                          |
| `mic.updateUserMSIRetryInterval`          | The duration to wait before retrying UpdateUserMSI (batch assigning/un-assigning identity from VM/VMSS) in case of errors                                                                                                                                                                                                     | If not provided, default value is `1s`                         |
| `mic.identityAssignmentReconcileInterval` | The interval between reconciling identity assignment on Azure based on an existing list of AzureAssignedIdentities                                                                                                                                                                                                            | If not provided, default value is `3m`                         |
| `nmi.image`                               | NMI image name                                                                                                                                                                                                                                                                                                                | `nmi`                                                          |
| `nmi.tag`                                 | NMI image tag                                                                                                                                                                                                                                                                                                                 | `v1.7.0`                                                       |
| `nmi.priorityClassName`                   | NMI priority class (can only be set when deploying to kube-system namespace)                                                                                                                                                                                                                                                  |                                                                |
| `nmi.logVerbosity`                        | Log level. Uses V logs (klog)                                                                                                                                                                                                                                                                                                 | `0`                                                            |
| `nmi.loggingFormat`                       | Log format. One of (text                                                                                                                                                                                                                                                                                                      | json)                                                          | `text` |
| `nmi.resources`                           | Resource limit for NMI                                                                                                                                                                                                                                                                                                        | `{}`                                                           |
| `nmi.podAnnotations`                      | Pod annotations for NMI                                                                                                                                                                                                                                                                                                       | `{}`                                                           |
| `nmi.tolerations`                         | Affinity settings                                                                                                                                                                                                                                                                                                             | `{}`                                                           |
| `nmi.affinity`                            | List of node taints to tolerate                                                                                                                                                                                                                                                                                               | `[]`                                                           |
| `nmi.ipTableUpdateTimeIntervalInSeconds`  | Override iptables update interval in seconds                                                                                                                                                                                                                                                                                  | `60`                                                           |
| `nmi.micNamespace`                        | Override mic namespace to short circuit MIC token requests                                                                                                                                                                                                                                                                    | If not provided, default is `default` namespace                |
| `nmi.probePort`                           | Override http liveliness probe port                                                                                                                                                                                                                                                                                           | If not provided, default is `8085`                             |
| `nmi.retryAttemptsForCreated`             | Override number of retries in NMI to find assigned identity in CREATED state                                                                                                                                                                                                                                                  | If not provided, default is  `16`                              |
| `nmi.retryAttemptsForAssigned`            | Override number of retries in NMI to find assigned identity in ASSIGNED state                                                                                                                                                                                                                                                 | If not provided, default is  `4`                               |
| `nmi.findIdentityRetryIntervalInSeconds`  | Override retry interval to find assigned identities in seconds                                                                                                                                                                                                                                                                | If not provided, default is  `5`                               |
| `nmi.allowNetworkPluginKubenet`           | Allow running aad-pod-identity in cluster with kubenet                                                                                                                                                                                                                                                                        | `false`                                                        |
| `rbac.enabled`                            | Create and use RBAC for all aad-pod-identity resources                                                                                                                                                                                                                                                                        | `true`                                                         |
| `rbac.allowAccessToSecrets`               | NMI requires permissions to get secrets when service principal (type: 1) is used in AzureIdentity. If using only MSI (type: 0) in AzureIdentity, secret get permission can be disabled by setting this to false.                                                                                                              | `true`                                                         |
| `azureIdentities`                         | List of azure identities and azure identity bindings resources to create                                                                                                                                                                                                                                                      | `[]`                                                           |
| `installCRDs`                             | If true, install necessary custom resources                                                                                                                                                                                                                                                                                   | `false`                                                        |

## Troubleshooting

If the helm chart is deleted and then reinstalled without manually deleting the crds, then you can get an error like -

```console
➜ helm install aad-pod-identity/aad-pod-identity --name pod-identity
Error: customresourcedefinitions.apiextensions.k8s.io "azureassignedidentities.aadpodidentity.k8s.io" already exists
```

In this case, since there is no update to the crd definition since it was last installed, you can use a parameter to say not to use hook to install the CRD:

```console
helm install aad-pod-identity/aad-pod-identity --name pod-identity --no-hooks
```
