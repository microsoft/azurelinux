# End-to-end testing on AAD Pod Identity

## Get Started

To run the E2E tests in a given Azure subscription, a running Kubernetes cluster created through AKS Engine or Azure Kubernetes Service (AKS) is required. A service principal with `Contributor` role under the node resource group is also required. To obtain the service principal credentials for AKS, you can refer to [here](https://docs.microsoft.com/en-us/azure/aks/kubernetes-service-principal). For AKS Engine, if you have an existing cluster, search for the `servicePrincipalProfile` field in `apimodel.json` under the deployment folder. Otherwise, refer to [here](https://github.com/Azure/aks-engine/blob/master/docs/topics/service-principals.md). Last but not least, an Azure KeyVault is required to simulate the action of accessing Azure resources. You can run a script to help you provision all of the Azure resources required during the test run:

```bash
# login as a user
az login

export SUBSCRIPTION_ID="<SubscriptionID>"
export RESOURCE_GROUP="<NodeResourceGroup>"
export KEYVAULT_NAME="my-keyvault"
export KEYVAULT_SECRET_NAME="test-secret"

./test/e2e/setup-e2e.sh
```

The E2E test suite extracts runtime configurations through environment variables. Below is a list of environment variables to set before running the E2E test suite.

| Variable                          | Description                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| `SUBSCRIPTION_ID`                 | The Azure subscription ID.                                                               |
| `RESOURCE_GROUP`                  | The resource group of your Azure Kubernetes cluster.                                     |
| `AZURE_CLIENT_ID`                 | The client ID of your service principal.                                                 |
| `AZURE_CLIENT_SECRET`             | The client secret of your service principal.                                             |
| `AZURE_TENANT_ID`                 | The Azure tenant ID.                                                                     |
| `KEYVAULT_NAME`                   | The Azure KeyVault name.                                                                 |
| `KEYVAULT_SECRET_NAME`            | The name of the secret stored in the Azure KeyVault.                                     |
| `KEYVAULT_SECRET_VERSION`         | The version of the secret stored in the Azure KeyVault.                                  |
| `MIC_VERSION`                     | The MIC version.                                                                         |
| `NMI_VERSION`                     | The NMI version.                                                                         |
| `IDENTITY_VALIDATOR_VERSION`      | The identity validator version                                                           |
| `SYSTEM_MSI_CLUSTER`              | Set to `true` if you are using an Azure cluster with system-assigned identity enabled.   |
| `ENABLE_SCALE_FEATURES`           | Set to `true` if you want to enable the scale features.                                  |
| `IMMUTABLE_IDENTITY_CLIENT_ID`    | The client ID of the immutable user-assigned identity created by running setup.sh.       |
| `NMI_MODE`                        | The NMI mode (`standard`, `managed`).                                                    |
| `BLOCK_INSTANCE_METADATA`         | Set to `true` if you want to run test cases related to block-instance-metadata feature.  |
| `SERVICE_PRINCIPAL_CLIENT_ID`     | The client ID of test service principal with Reader role to KeyVault resource group.     |
| `SERVICE_PRINCIPAL_CLIENT_SECRET` | The client secret of test service principal with Reader role to KeyVault resource group. |

Finally, to kick off a test run:

```bash
make e2e
```

## Identity Validator

During the E2E test run, the image [`identityvalidator`](../image/identityvalidator/identityvalidator.go) is deployed as a pod to the cluster to validate the identity assigned to it. The binary `identityvalidator` within the pod is essentially the compiled version of [`identityvalidator.go`](../image/identityvalidator/identityvalidator.go). If the binary execution returns an exit status of 0, it means that the pod identity and its binding are working properly. Otherwise, it means that the pod identity is not established. You can manually try out the identity validator by executing the following command:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: keyvault-identity
spec:
  type: 0
  resourceID: <KeyvaultIdentityResourceID>
  clientID: <KeyvaultIdentityClientID>
EOF

cat <<EOF | kubectl apply -f -
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentityBinding
metadata:
  name: keyvault-identity-binding
spec:
  azureIdentity: keyvault-identity
  selector: keyvault-identity
EOF

kubectl run identityvalidator --image=mcr.microsoft.com/oss/azure/aad-pod-identity/identityvalidator:v1.7.0 --labels=aadpodidbinding=keyvault-identity -- --sleep

kubectl exec identityvalidator -- identityvalidator \
                                  --subscription-id "$SUBSCRIPTION_ID" \
                                  --resource-group "$RESOURCE_GROUP" \
                                  --identity-client-id "$AZURE_CLIENT_ID" \
                                  --keyvault-name "$KEYVAULT_NAME" \
                                  --keyvault-secret-name "$KEYVAULT_SECRET_NAME" \
                                  --keyvault-secret-version "$KEYVAULT_SECRET_VERSION"

# Check the exit status
echo "$?"
```
