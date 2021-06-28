# AAD Pod Identity Tutorial

This tutorial is based on [this repository](https://github.com/xtellurian/aad-pods).

## Prerequisites

- [Azure Account](https://azure.microsoft.com/en-us/free/)

In this tutorial we are going to be using the Azure CLI, bash scripts, and kubectl. There are three sections, and each section contains several scripts to run. You'll find all the scripts in the `/scripts` directory.

Lines like `./scripts/path/to/script.sh` indicate you should execute that script.

To begin, clone this repository

```sh

git clone https://github.com/Azure/aad-pod-identity
cd aad-pod-identity/docs/tutorial

```

### Using Azure CLI, kubectl and bash

The following steps require the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest), make sure to download and [login](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest) before starting.

If you're on Windows, you should use [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) or another Bash terminal.

You can install kubectl via the Azure CLI, or by [another method](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

`az aks install-cli`

## 1. Create a Kubernetes Cluster on Azure (AKS)

### 1.1. Register the required resource types

`./scripts/1-init-aks/1-azure-provider-registration.sh`

AKS requires the following resources: Microsoft.Network, Microsoft.Storage, Microsoft.Compute, Microsoft.ContainerService. Register them on your subscription with the above script.


### 1.2. Create a Resource Group

Set an environment variable in your shell, for the name of your resource group.

`export RG="k8s-test"`

This resource group is for your AKS cluster. Create it with this command.

`./scripts/1-init-aks/2-create-rg.sh`

### 1.3. Create Azure Kubernetes Service

This will create an AKS instance in the resource group created above. It may take a couple of minutes to complete. Set the name of the this command in the shell.

```sh

K8S_NAME="Cluster-Name"
./scripts/1-init-aks/3-create-aks.sh

```


### 1.4. Configure the kubernetes CLI - `kubectl`

With `kubectl` installed, run the following script

`./scripts/1-init-aks/4-configure-cli.sh`

Now the `kubectl` command should control your AKS cluster. Try it out, it should look similar to below:

```sh

$ kubectl get nodes
NAME                       STATUS    ROLES     AGE       VERSION
aks-nodepool1-15831963-0   Ready     agent     01h       v1.9.6

```

## 2. Configure AKS with required infrastructure on the cluster

Pod Identity requires two components:

 1. Managed Identity Controller (MIC). A pod that binds Azure Ids to other pods - creates azureAssignedIdentity CRD. 
 2. Node Managed Identity (NMI). Identifies the pod based on the remote address of the incoming request, and then queries the k8s (through MIC) for a matching Azure Id. It then make a adal request to get the token for the client id and returns as a response to the request. Implemented as a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/).

Deploy the infrastructure with the following command to deploy MIC, NMI, and MIC CRDs.

`./scripts/2-config-aks/2-deploy-infra.sh`

NOTE: If you have RBAC enabled, use the following deployment instead:

```
kubectl create -f ../../deploy/infra/deployment-rbac.yaml
```

## 3. Deploy the demo

The demo is basic, but does prove the concept.

### 3.1. Create an Azure Id

We will be assigning the demo pod an [Azure Managed Service Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-service-identity/overview). The Azure Id will need to be in the same Resource Group *as was created automatically by the provisioning of the AKS cluster* [see this issue for more information](https://github.com/Azure/aad-pod-identity/issues/38).

You might find the Resource Group name with

`az group list | grep $RG`

Then set the environment variable

`export MC_RG="resource-group-name"`

Run the following to create an azure id

`./scripts/3-deploy-demo/1-create-azure-id.sh`

### 3.2. Deploy demo

The `/deploy/demo/deployment.yaml` describes the pod that will be deployed. 

It automatically adds the following values from your environment:

- subscriptionid: Id of your Azure Subscription
- clientid: From the Azure Id you created in the step above
- resourcegroup: From the Azure Id you created above

Run the following to deploy the demo

`./scripts/3-deploy-demo/2-deploy-demo.sh`

### 3.3. Deploy Azure Id to Kubernetes

We need to tell the cluster about the Id we created, so it can bind it to the pod (the next step). To do that, we will deploy the spec found in `/deploy/demo/aadpodidentity.yaml`. 

Run the following to deploy the Azure ID to Kubernetes:

`./scripts/3-deploy-demo/3-deploy-id-to-k8s.sh`

### 3.4. Bind the Id to our demo pod

Last thing we need to do is bind the Id we created in step 1, and deployed in step 3, to the pod we deployed in step 2.

Deploy the binding with the following

`./scripts/3-deploy-demo/4-deploy-id-binding.sh`

## Did it work?

You'll need to check the logs of each pod to know if everything worked.

First, get the pod names with the following command:

```sh

$ kubectl get pods
NAME                   READY     STATUS    RESTARTS   AGE
demo-757967c54-64pzr   1/1       Running   0          1h     # the demo pod
mic-64ddcf5f65-h4hft   1/1       Running   0          19h    # the MIC pod
nmi-b9xbg              1/1       Running   0          1h     # the NMI pod

```

### Check the Managed Identity Controller pod

Check the logs of the MIC controller and see the binding successfully applied on the node.

```sh

$ kubectl logs mic-64ddcf5f65-h4hft
....
I0606 23:19:45.867711       1 crd.go:123] Got id podid to assign
I0606 23:19:45.867829       1 crd.go:142] Creating assigned Id: demo-5788d95785-ghzwv-default-podid
I0606 23:19:45.874002       1 cloudprovider.go:170] Find aks-nodepool1-15831963-0 in resource group: MC_k8s-test_clusterFrank_eastus
I0606 23:20:11.051552       1 cloudprovider.go:162] Underlying cloud provider operation took 25.04421296s
I0606 23:20:11.051846       1 mic.go:259] Sync took: 25.220821436s
I0606 23:20:11.052905       1 event.go:218] Event(v1.ObjectReference{Kind:"AzureIdentityBinding", Namespace:"default", Name:"myIdBinding", UID:"19a07e0e-69e0-11e8-9e9f-4addade2df92", APIVersion:"aadpodidentity.k8s.io/v1", ResourceVersion:"89529", FieldPath:""}): type: 'Normal' reason: 'binding applied' Binding myIdBinding applied on node aks-nodepool1-15831963-0 for pod demo-5788d95785-ghzwv-default-podid

```

### Check the Node Managed Identity pod

Check the logs of the NMI pod to see only info level logging and 200 responses. If you see 403 or 404 responses, then something is wrong.

```sh

$ kubectl logs nmi-b9xbg
...
time="2018-06-07T01:30:04Z" level=info msg="Status (200) took 55422159 ns" req.method=GET req.path=/metadata/identity/oauth2/token req.remote=10.244.0.25
time="2018-06-07T01:30:04Z" level=info msg="matched identityType:0 clientid:a40e83f9-6198-4633-afae-d860eb5b7f7c resource:https://management.azure.com/" req.method=GET req.path=/metadata/identity/oauth2/token req.remote=10.244.0.25

```

### Check the demo pod

The demo pod should be reporting on the virtual machines in the resource group. If you see intermittant 403 responses, that is OK.

```sh

$ kubectl logs demo-757967c54-64pzr
...
time="2018-06-07T01:32:30Z" level=error msg="failed list all vm compute.VirtualMachinesClient#List: Failure responding to request: StatusCode=403 -- Original Error: autorest/azure: Service returned an error. Status=403 Code=\"AuthorizationFailed\" Message=\"The client '48affddb-9972-4b7e-a82b-c5d32d2a3dd5' with object id '48affddb-9972-4b7e-a82b-c5d32d2a3dd5' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '/subscriptions/c5760548-23c2-4223-b41e-5d68a8320a0c/resourceGroups/MC_k8s-test_clusterFrank_eastus/providers/Microsoft.Compute'.\"" podip=10.244.0.25 podname=demo-757967c54-64pzr podnamespace=demo-757967c54-64pzr
time="2018-06-07T01:32:30Z" level=info msg="successfully acquired a token using the MSI, msiEndpoint(http://169.254.169.254/metadata/identity/oauth2/token)" podip=10.244.0.25 podname=demo-757967c54-64pzr podnamespace=demo-757967c54-64pzr
time="2018-06-07T01:32:30Z" level=info msg="successfully acquired a token, userAssignedID MSI, msiEndpoint(http://169.254.169.254/metadata/identity/oauth2/token) clientID(a40e83f9-6198-4633-afae-d860eb5b7f7c)" podip=10.244.0.25 podname=demo-757967c54-64pzr podnamespace=demo-757967c54-64pzr
time="2018-06-07T01:32:30Z" level=info msg="successfully made GET on instance metadata, {\"compute\":{\"location\":\"eastus\",\"name\":\"aks-nodepool1-15831963-0\",\"offer\":\"UbuntuServer\",\"osType\":\"Linux\",\"placementGroupId\":\"\",\"platformFaultDomain\":\"0\",\"platformUpdateDomain\":\"0\",\"publisher\":\"Canonical\",\"resourceGroupName\":\"MC_k8s-test_clusterFrank_eastus\",\"sku\":\"16.04-LTS\",\"subscriptionId\":\"c5760548-23c2-4223-b41e-5d68a8320a0c\",\"tags\":\"acsengineVersion:v0.17.0-aks;creationSource:aks-aks-nodepool1-15831963-0;orchestrator:Kubernetes:1.9.6;poolName:nodepool1;resourceNameSuffix:15831963\",\"version\":\"16.04.201805090\",\"vmId\":\"3fea4c7e-4aaf-400f-a588-2a851f6fd0cf\",\"vmSize\":\"Standard_DS1_v2\"},\"network\":{\"interface\":[{\"ipv4\":{\"ipAddress\":[{\"privateIpAddress\":\"10.240.0.4\",\"publicIpAddress\":\"\"}],\"subnet\":[{\"address\":\"10.240.0.0\",\"prefix\":\"16\"}]},\"ipv6\":{\"ipAddress\":[]},\"macAddress\":\"000D3A13DEE3\"}]}}" podip=10.244.0.25 podname=demo-757967c54-64pzr podnamespace=demo-757967c54-64pzr

```

### Check the descriptions

`kubectl describe azureidentity`

`kubectl describe azureidentitybinding`

### Video

[![Video of Running required commands](https://img.youtube.com/vi/BXhIMJYDO4w/0.jpg)](https://www.youtube.com/watch?v=BXhIMJYDO4w)

## Continuous Deployment with VSTS

This section is optional. 

It shows how to deploy the same pods and infrastructure as above using [VSTS Continuous Integration](https://www.visualstudio.com/team-services/continuous-integration/).

### Configure Kubernetes Connection in VSTS

Give VSTS permission to use your Kubernetes cluster by adding the endpoint to your project. Click the Cog Wheel, and go to Services. Add a new endpoint, and choose Kubernetes. See [this tutorial](https://almvm.azurewebsites.net/labs/vstsextend/kubernetes/) for a more details.

![Screenshot of Kubernetes Endpoint config in VSTS](images/k8s-endpoint-vsts.png)

### Release Definition

Create a new empty Release Definition, and add this repository and a source with alias `_aad_pods`

Add a Task of type 'Deploy to Kubernetes'. Create one of these tasks for each of the following:

> The command of each is `apply`, and the each below shows the reqired arguments.

- `-f _aad-pods/deploy/infra/deployment.yaml`
- `-f _aad-pods/deploy/demo/deployment.yaml`
- `-f _aad-pods/deploy/demo/aadpodidentity.yaml`
- `-f _aad-pods/deploy/demo/aadpodidentitybinding.yaml`

The result should look like this

![Screenshot of VSTS tasks](images/vsts-deploy-tasks.png)

### Customising each Deployment

You probably don't want to deploy the same Demo every time. To customise the Kubernetes deployment, use the [YAML Writer](https://marketplace.visualstudio.com/items?itemName=jakkaj.vsts-yaml-writer) extension, and edit the values in the YAML files.

