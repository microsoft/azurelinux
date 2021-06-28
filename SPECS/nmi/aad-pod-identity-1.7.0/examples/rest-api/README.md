# Using AAD Pod Identity with a custom REST API

We will look at the scenario where a client pod is calling a service (REST API) with an AAD Pod Identity.

The client is a bash script running in a pod.  The client has a corresponding user managed identity which will be exposed as an AAD Pod Identity.  The client will request a token, pass it as authorization HTTP header to query a REST API.

The REST API is implemented in C# / .NET Core and is running in pod as well.  It simply validates it receives a bearer token in the authorization header of each request.  The REST API has a corresponding Azure AD Application.  The client requests a token with that AAD application as the *resource*.

![Solution Overview](images/pod-identity-rest.png)

## Prerequisites

* An AKS cluster with [AAD Pod Identity installed on it](https://github.com/Azure/aad-pod-identity/blob/master/README.md)

## Identity

In this section, we'll create the user managed identity used for the client.

First, let's define those variable:

```bash
rg=<name of the resource group where AKS is>
cluster=<name of the AKS cluster>
```

Then, let's create the user managed identity:

```bash
az identity create -g $rg -n client-principal \
    --query "{ClientId: clientId, ManagedIdentityId: id, TenantId:  tenantId}" -o jsonc
```

This returns three values in a JSON document.  We will use those values later on.

We need to assign the Service Principal running the cluster the *Managed Identity Operator* role on the user managed identity:

```bash
aksPrincipalId=$(az aks show -g $rg -n $cluster --query "servicePrincipalProfile.clientId" -o tsv)
managedId=$(az identity show -g $rg -n client-principal --query "id" -o tsv)
az role assignment create --role "Managed Identity Operator" \
--assignee $aksPrincipalId --scope $managedId
```

The first line acquires the AKS service principal client ID.  The second line acquires the client ID of the user managed identity (the *ManagedIdentityId* returned in the JSON above).  The third line performs the role assignment.

## Identity & Binding in Kubernetes

In this section, we'll configure AAD pod identity with the user managed identity.

We'll create a Kubernetes namespace to put all our resources.  It makes it easier to clean up afterwards.

```bash
kubectl create namespace pir
kubectl label namespace/pir description=PodIdentityRestApi
```

Let's customize [identity.yaml](identity.yaml):

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: client-principal
spec:
  type: 0
  resourceID: <resource-id of client-principal>
  clientID: <client-id of client-principal>
```

*ResourceID* should be set to the value of *ManagedIdentityId* in the JSON from the previous section.  That is the resource ID of the user managed identity.

*ClientID* should be set to the value of *ClientId* in the JSON from the previous section.  That is the client id of the user managed identity.

We **do not need to customize** [binding.yaml](binding.yaml).

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentityBinding
metadata:
  name: client-principal-binding
spec:
  azureIdentity: client-principal
  selector:  client-principal-pod-binding
```

We can now deploy those two files in the *pir* namespace:

```bash
kubectl apply -f identity.yaml --namespace pir
kubectl apply -f binding.yaml --namespace pir
```

We can check the resources got deployed:

```bash
$ kubectl get AzureIdentity --namespace pir

NAME               AGE
client-principal   12s

$ kubectl get AzureIdentityBinding --namespace pir

NAME                       AGE
client-principal-binding   32s
```

## Application

In this section, we will simply create the Azure AD application corresponding to the REST API Service:

```bash
appId=$(az ad app create --display-name myapi \
    --identifier-uris http://myapi.restapi.aad-pod-identity \
    --query "appId" -o tsv)
echo $appId
```

The application's name is *myapi*.  The identifier uri is irrelevant but required.

## Client

In [client-pod.yaml](client-pod.yaml), we need to customize the value of the environment variable *RESOURCE* to the value of *$appId* computed above, i.e. the client id of the Azure AD application:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: aad-id-client-pod
  labels:
    app: aad-id-client
    platform: cli
    aadpodidbinding:  client-principal-pod-binding
spec:
  containers:
  - name: main-container
    image: vplauzon/aad-pod-id-client
    env:
    - name: RESOURCE
      value: <Application Id>
    - name: SERVICE_URL
      value: http://aad-id-service
```

The client will use that when requesting a token.

The client's code is packaged in a container.  The core of the code is [script.sh](client/script.sh):

```bash
#!/bin/sh

echo "Hello ${RESOURCE}"

i=0
while true
do
    echo "Iteration $i"

    jwt=$(curl -sS http://169.254.169.254/metadata/identity/oauth2/token/?resource=$RESOURCE)
    echo "Full token:  $jwt"
    token=$(echo $jwt | jq -r '.access_token')
    echo "Access token:  $token"
    curl -v -H 'Accept: application/json' -H "Authorization: Bearer ${token}" $SERVICE_URL

    i=$((i+1))
    sleep 1
done
```

Every second the script queries a token from http://169.254.169.254 which is exposed by AAD Pod Identity (more specifically the *Node Managed Identity* component, or NMI).

We use the [jq](https://stedolan.github.io/jq/) tool to parse the JSON of the token.  We extract the access token element which we then pass as in an HTTP header using *curl*.

## Service

In [service.yaml](service.yaml), we need to customize the value for APPLICATION_ID & TENANT_ID.

APPLICATION_ID's value is the same as the RESOURCE from previous section, i.e. *$appId*.  TENANT_ID is the ID of the tenant owning the identities.  It was given in the JSON as the output of the user managed identity.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: aad-id-service
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    app: aad-id-service
---
apiVersion: v1
kind: Pod
metadata:
  name: aad-id-service-pod
  labels:
    app: aad-id-service
    platform: csharp
spec:
  containers:
  - name: api-container
    image: vplauzon/aad-pod-id-svc
    ports:
    - containerPort: 80
    env:
    - name: TENANT_ID
      value: <ID of TENANT owning the identities>
    - name: APPLICATION_ID
      value: <Application Id>
```

Here we defined a service and a pod implementing the service.  The service is available on port 80.

[The code for the service](service) is packaged in a container.  The core of it is [Startup.cs](service/MyApiSolution/MyApi/Startup.cs), more specifically its *ConfigureServices* method:

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services
        .AddAuthentication()
        .AddJwtBearer(options =>
        {
            options.Audience = _applicationId;
            options.Authority = $"https://sts.windows.net/{_tenantId}/";
        });
    services.AddAuthorization(options =>
    {
        var defaultAuthorizationPolicyBuilder = new AuthorizationPolicyBuilder(
            JwtBearerDefaults.AuthenticationScheme);

        defaultAuthorizationPolicyBuilder =
            defaultAuthorizationPolicyBuilder.RequireAuthenticatedUser();
        options.DefaultPolicy = defaultAuthorizationPolicyBuilder.Build();
    });
    services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
}
```

Here we specify that a [Json Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token) (JWT) is required for authentication as default.  I.e. we do not need to put a *[Authentication]* attribute on controllers.

## Test

Let's deploy the service & client.

```bash
kubectl apply -f service.yaml --namespace pir
kubectl apply -f client-pod.yaml --namespace pir
kubectl get AzureAssignedIdentity --all-namespaces
```

The last command should return an entry.  This is showing that Azure Pod Identity did bind an identity to a pod.

We can then monitor the client:

```bash
kubectl logs aad-id-client-pod --namespace pir -f
```

Every second, we should see something like this:

```bash
Iteration 6
Full token:  {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCIsImtpZCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCJ9.eyJhdWQiOiI2ZmZhNjBiYy0yODZkLTRiMzAtOWMxYi0wMDBlODcyYjQxMzIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaWF0IjoxNTUxMTkxMjM5LCJuYmYiOjE1NTExOTEyMzksImV4cCI6MTU1MTIyMDMzOSwiYWlvIjoiNDJKZ1lEanNuTTk4L0lqWDlQM1hmTU5zOW0zK0FnQT0iLCJhcHBpZCI6IjIxMWZlNTQ3LThhYzItNGE2Zi05MjYyLWFkZjMwNDM3ZTAzYiIsImFwcGlkYWNyIjoiMiIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJvaWQiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJzdWIiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJ0aWQiOiI3MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDciLCJ1dGkiOiJWMHdhSDQwbEtFS1RCQ29SUV82X0FBIiwidmVyIjoiMS4wIn0.I4hZusEV-A17rJSQW1CBH3oSVd0wedoXPVoPEXGxGdxYvXJCKYL1Mz0HoMJcp8s2_Z59Q16GHdvlWwnQNAhFIdfENF8Rj_jJ0ndh1ZtU1ioIPHWH461794bP38aUg-tBmxnfP-ZSjz-iiifx2n_iERTqlya4os80_WQm_OejW5kfrmpx6P7zcM5eqw7C_oKkM1l8BhhlDdwWnAc0pu5YWbMhgZBtJc9kzKh2IQyLmRkwbZEMJ-cJ_Xuay4jPccP-dGFylrC2KRQlWzovVraubX9vqkfL8f_eYPZIuhcUC1M2paf8wgQUyZWdvh-HzWKD5LdDCuvZCLeWpxaePTGhLA","refresh_token":"","expires_in":"28800","expires_on":"1551220339","not_before":"1551191239","resource":"6ffa60bc-286d-4b30-9c1b-000e872b4132","token_type":"Bearer"}
Access token:  eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCIsImtpZCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCJ9.eyJhdWQiOiI2ZmZhNjBiYy0yODZkLTRiMzAtOWMxYi0wMDBlODcyYjQxMzIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaWF0IjoxNTUxMTkxMjM5LCJuYmYiOjE1NTExOTEyMzksImV4cCI6MTU1MTIyMDMzOSwiYWlvIjoiNDJKZ1lEanNuTTk4L0lqWDlQM1hmTU5zOW0zK0FnQT0iLCJhcHBpZCI6IjIxMWZlNTQ3LThhYzItNGE2Zi05MjYyLWFkZjMwNDM3ZTAzYiIsImFwcGlkYWNyIjoiMiIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJvaWQiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJzdWIiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJ0aWQiOiI3MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDciLCJ1dGkiOiJWMHdhSDQwbEtFS1RCQ29SUV82X0FBIiwidmVyIjoiMS4wIn0.I4hZusEV-A17rJSQW1CBH3oSVd0wedoXPVoPEXGxGdxYvXJCKYL1Mz0HoMJcp8s2_Z59Q16GHdvlWwnQNAhFIdfENF8Rj_jJ0ndh1ZtU1ioIPHWH461794bP38aUg-tBmxnfP-ZSjz-iiifx2n_iERTqlya4os80_WQm_OejW5kfrmpx6P7zcM5eqw7C_oKkM1l8BhhlDdwWnAc0pu5YWbMhgZBtJc9kzKh2IQyLmRkwbZEMJ-cJ_Xuay4jPccP-dGFylrC2KRQlWzovVraubX9vqkfL8f_eYPZIuhcUC1M2paf8wgQUyZWdvh-HzWKD5LdDCuvZCLeWpxaePTGhLA
* Rebuilt URL to: http://aad-id-service/
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 10.0.253.247...
* TCP_NODELAY set
* Connected to aad-id-service (10.0.253.247) port 80 (#0)
> GET / HTTP/1.1
> Host: aad-id-service
> User-Agent: curl/7.59.0
> Accept: application/json
> Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCIsImtpZCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCJ9.eyJhdWQiOiI2ZmZhNjBiYy0yODZkLTRiMzAtOWMxYi0wMDBlODcyYjQxMzIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaWF0IjoxNTUxMTkxMjM5LCJuYmYiOjE1NTExOTEyMzksImV4cCI6MTU1MTIyMDMzOSwiYWlvIjoiNDJKZ1lEanNuTTk4L0lqWDlQM1hmTU5zOW0zK0FnQT0iLCJhcHBpZCI6IjIxMWZlNTQ3LThhYzItNGE2Zi05MjYyLWFkZjMwNDM3ZTAzYiIsImFwcGlkYWNyIjoiMiIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJvaWQiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJzdWIiOiI5YTU5NTgwNC00ZjJhLTRkZDItYjYzOC00YWVkZTY0MTU3OGQiLCJ0aWQiOiI3MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDciLCJ1dGkiOiJWMHdhSDQwbEtFS1RCQ29SUV82X0FBIiwidmVyIjoiMS4wIn0.I4hZusEV-A17rJSQW1CBH3oSVd0wedoXPVoPEXGxGdxYvXJCKYL1Mz0HoMJcp8s2_Z59Q16GHdvlWwnQNAhFIdfENF8Rj_jJ0ndh1ZtU1ioIPHWH461794bP38aUg-tBmxnfP-ZSjz-iiifx2n_iERTqlya4os80_WQm_OejW5kfrmpx6P7zcM5eqw7C_oKkM1l8BhhlDdwWnAc0pu5YWbMhgZBtJc9kzKh2IQyLmRkwbZEMJ-cJ_Xuay4jPccP-dGFylrC2KRQlWzovVraubX9vqkfL8f_eYPZIuhcUC1M2paf8wgQUyZWdvh-HzWKD5LdDCuvZCLeWpxaePTGhLA
>
< HTTP/1.1 200 OK
< Date: Tue, 26 Feb 2019 14:49:44 GMT
< Content-Type: application/json; charset=utf-8
< Server: Kestrel
< Transfer-Encoding: chunked
<
{ [23 bytes data]
100    13    0    13    0     0    812      0 --:--:-- --:--:-- --:--:--   812
* Connection #0 to host aad-id-service left intact
```

It shows the token being acquired, passed in the *Authorization* header as a *Bearer* token.  The response is a 200, showing the authentication works.

Now we can verified the authentication is happening by removing it.  Lets the logs be carried through.  In a different terminal, let's run the following command:

```bash
kubectl delete AzureIdentityBinding client-principal-binding --namespace pir
```

This basically delete the binding of the identity.  As soon as that command returns, we should see the logs changing in something like:

```bash
Iteration 269
Full token:  no AzureAssignedIdentity found for pod:pir/aad-id-client-pod
parse error: Invalid literal at line 1, column 3
Access token:
* Rebuilt URL to: http://aad-id-service/
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 10.0.253.247...
* TCP_NODELAY set
* Connected to aad-id-service (10.0.253.247) port 80 (#0)
> GET / HTTP/1.1
> Host: aad-id-service
> User-Agent: curl/7.59.0
> Accept: application/json
> Authorization: Bearer
>
< HTTP/1.1 401 Unauthorized
< Date: Tue, 26 Feb 2019 14:54:18 GMT
< Server: Kestrel
< Content-Length: 0
< WWW-Authenticate: Bearer
<
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* Connection #0 to host aad-id-service left intact
```

We see the token isn't provided to the pod anymore.  Since we do not pass a valid token, the service reject the call with a **401 Unauthorized**.

We can easily go back to previous state by running:

```bash
kubectl apply -f binding.yaml --namespace pir
```

Again, as soon as the command returns the logs resume the **200 OK** response.

## Clean up

In order to clean up both the Azure and Kubernetes resources we've been using, we can run the following commands:

```bash
kubectl delete namespace pir
az identity delete -g $rg -n client-principal
az ad app delete --id $appId
```

The first line deletes the Kubernetes namespace and everything underneath it, i.e. identity, binding, client & service.  The second line deletes the Azure User Managed Identity.  The third line deletes the Azure AD application.

## Notes

###	Build client docker container
sudo docker build -t vplauzon/aad-pod-id-client .

###	Publish client image
sudo docker push vplauzon/aad-pod-id-client

###	Build service docker container
sudo docker build -t vplauzon/aad-pod-id-svc .

###	Publish service image
sudo docker push vplauzon/aad-pod-id-svc

