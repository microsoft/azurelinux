---
title: "Standard Walkthrough"
linkTitle: "Standard Walkthrough"
weight: 1
description: >
  You will need Azure CLI installed and a Kubernetes cluster running on Azure, either managed by AKS or provisioned with AKS Engine.
---

Run the following commands to set Azure-related environment variables and login to Azure via `az login`:

```bash
export SUBSCRIPTION_ID="<SubscriptionID>"
export RESOURCE_GROUP="<AKSResourceGroup>"
export CLUSTER_NAME="<AKSClusterName>"
export CLUSTER_LOCATION="<AKSClusterLocation>"

export IDENTITY_RESOURCE_GROUP="MC_${RESOURCE_GROUP}_${CLUSTER_NAME}_${CLUSTER_LOCATION}"
export IDENTITY_NAME="demo"

# login as a user and set the appropriate subscription ID
az login
az account set -s "${SUBSCRIPTION_ID}"
```

> For AKS clusters, there are two resource groups that you need to be aware of - the resource group where you deploy your AKS cluster to (denoted by the environment variable `RESOURCE_GROUP`), and the node resource group (`MC_<AKSResourceGroup>_<AKSClusterName>_<AKSClusterLocation>`). The latter contains all of the infrastructure resources associated with the cluster like VM/VMSS and VNet. Depending on where you deploy your user-assigned identities, you might need additional role assignments. Please refer to [Role Assignment](../../getting-started/role-assignment/) for more information. For this demo, it is recommended to deploy the demo identity to your node resource group (the one with `MC_` prefix).

### 1. Deploy aad-pod-identity

Deploy `aad-pod-identity` components to an RBAC-enabled cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/deployment-rbac.yaml

# For AKS clusters, deploy the MIC and AKS add-on exception by running -
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/mic-exception.yaml
```

Deploy `aad-pod-identity` components to a non-RBAC cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/deployment.yaml

# For AKS clusters, deploy the MIC and AKS add-on exception by running -
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/deploy/infra/mic-exception.yaml
```

Deploy `aad-pod-identity` using [Helm 3](https://v3.helm.sh/):

```bash
helm repo add aad-pod-identity https://raw.githubusercontent.com/Azure/aad-pod-identity/master/charts
helm install aad-pod-identity aad-pod-identity/aad-pod-identity
```

For a list of overwritable values when installing with Helm, please refer to [this section](https://github.com/Azure/aad-pod-identity/tree/master/charts/aad-pod-identity#configuration).

> Important: For AKS clusters with [limited egress traffic](https://docs.microsoft.com/en-us/azure/aks/limit-egress-traffic), Please install aad-pod-identity in `kube-system` namespace using the helm charts.

```bash
helm install aad-pod-identity aad-pod-identity/aad-pod-identity --namespace=kube-system
```

### 2. Create an identity on Azure

Create an identity on Azure and store the client ID and resource ID of the identity as environment variables:

```bash
az identity create -g ${IDENTITY_RESOURCE_GROUP} -n ${IDENTITY_NAME}
export IDENTITY_CLIENT_ID="$(az identity show -g ${IDENTITY_RESOURCE_GROUP} -n ${IDENTITY_NAME} --query clientId -otsv)"
export IDENTITY_RESOURCE_ID="$(az identity show -g ${IDENTITY_RESOURCE_GROUP} -n ${IDENTITY_NAME} --query id -otsv)"
```

Assign the role "Reader" to the identity so it has read access to the resource group. At the same time, store the identity assignment ID as an environment variable.

```bash
export IDENTITY_ASSIGNMENT_ID="$(az role assignment create --role Reader --assignee ${IDENTITY_CLIENT_ID} --scope /subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${IDENTITY_RESOURCE_GROUP} --query id -otsv)"
```

### 3. Deploy `AzureIdentity`

Create an `AzureIdentity` in your cluster that references the identity you created above:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: ${IDENTITY_NAME}
spec:
  type: 0
  resourceID: ${IDENTITY_RESOURCE_ID}
  clientID: ${IDENTITY_CLIENT_ID}
EOF
```

> Set `type: 0` for user-assigned MSI, `type: 1` for Service Principal with client secret, or `type: 2` for Service Principal with certificate. For more information, see [here](https://github.com/Azure/aad-pod-identity/tree/master/deploy/demo).

### 4. (Optional) Match pods in the namespace

For matching pods in the namespace, please refer to the [namespaced documentation](../../configure/match_pods_in_namespace/).

### 5. Deploy `AzureIdentityBinding`

Create an `AzureIdentityBinding` that reference the `AzureIdentity` you created above:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentityBinding
metadata:
  name: ${IDENTITY_NAME}-binding
spec:
  azureIdentity: ${IDENTITY_NAME}
  selector: ${IDENTITY_NAME}
EOF
```

### 6. Deployment and Validation

For a pod to match an identity binding, it needs a label with the key `aadpodidbinding` whose value is that of the `selector:` field in the `AzureIdentityBinding`. Deploy a pod that validates the functionality:

```bash
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: demo
  labels:
    aadpodidbinding: $IDENTITY_NAME
spec:
  containers:
  - name: demo
    image: mcr.microsoft.com/oss/azure/aad-pod-identity/demo:v1.7.0
    args:
      - --subscriptionid=${SUBSCRIPTION_ID}
      - --clientid=${IDENTITY_CLIENT_ID}
      - --resourcegroup=${IDENTITY_RESOURCE_GROUP}
    env:
      - name: MY_POD_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.name
      - name: MY_POD_NAMESPACE
        valueFrom:
          fieldRef:
            fieldPath: metadata.namespace
      - name: MY_POD_IP
        valueFrom:
          fieldRef:
            fieldPath: status.podIP
  nodeSelector:
    kubernetes.io/os: linux
EOF
```

> `mcr.microsoft.com/oss/azure/aad-pod-identity/demo` is an image that demostrates the use of AAD pod identity. The source code can be found [here](https://github.com/Azure/aad-pod-identity/blob/master/cmd/demo/main.go).

To verify that the pod is indeed using the identity correctly:

```bash
kubectl logs demo
```

If successful, the log output would be similar to the following output:

```log
...
successfully doARMOperations vm count 1
successfully acquired a token using the MSI, msiEndpoint(http://169.254.169.254/metadata/identity/oauth2/token)
successfully acquired a token, userAssignedID MSI, msiEndpoint(http://169.254.169.254/metadata/identity/oauth2/token) clientID(xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
successfully made GET on instance metadata
...
```

Once you are done with the demo, clean up your resources:

```bash
kubectl delete pod demo
kubectl delete azureidentity ${IDENTITY_NAME}
kubectl delete azureidentitybinding ${IDENTITY_NAME}-binding
az role assignment delete --id ${IDENTITY_ASSIGNMENT_ID}
az identity delete -g ${IDENTITY_RESOURCE_GROUP} -n ${IDENTITY_NAME}
```

## Uninstall Notes

The NMI pods modify the nodes' [iptables] to intercept calls to IMDS endpoint within a node. This allows NMI to insert identities assigned to a pod before executing the request on behalf of the caller.

These iptables entries will be cleaned up when the pod-identity pods are uninstalled. However, if the pods are terminated for unexpected reasons, the iptables entries can be removed with these commands on the node:

```bash
# remove the custom chain reference
iptables -t nat -D PREROUTING -j aad-metadata

# flush the custom chain
iptables -t nat -F aad-metadata

# remove the custom chain
iptables -t nat -X aad-metadata
```