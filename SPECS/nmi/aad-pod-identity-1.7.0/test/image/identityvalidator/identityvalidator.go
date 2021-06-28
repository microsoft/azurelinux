package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"time"

	"github.com/pkg/errors"
	"k8s.io/klog/v2"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/Azure/azure-sdk-for-go/services/keyvault/2016-10-01/keyvault"
	"github.com/Azure/azure-sdk-for-go/services/keyvault/auth"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/adal"
	"github.com/Azure/go-autorest/autorest/azure"
	"github.com/spf13/pflag"
)

var (
	sleep                 = pflag.Bool("sleep", false, "Set to true to enter sleep mode")
	subscriptionID        = pflag.String("subscription-id", "", "subscription id for test")
	identityClientID      = pflag.String("identity-client-id", "", "client id for the msi id")
	identityResourceID    = pflag.String("identity-resource-id", "", "resource id for the msi id")
	resourceGroup         = pflag.String("resource-group", "", "any resource group name with reader permission to the aad object")
	keyvaultName          = pflag.String("keyvault-name", "", "the name of the keyvault to extract the secret from")
	keyvaultSecretName    = pflag.String("keyvault-secret-name", "", "the name of the keyvault secret we are extracting with pod identity")
	keyvaultSecretVersion = pflag.String("keyvault-secret-version", "", "the version of the keyvault secret we are extracting with pod identity")
)

const (
	contextTimeout = 150 * time.Second
)

func main() {
	pflag.Parse()

	if *sleep {
		klog.Infof("entering sleep mode")
		for {
			select {}
		}
	}

	podname := os.Getenv("E2E_TEST_POD_NAME")
	podnamespace := os.Getenv("E2E_TEST_POD_NAMESPACE")
	podip := os.Getenv("E2E_TEST_POD_IP")

	klog.Infof("starting identity validator pod %s/%s with pod IP %s", podnamespace, podname, podip)

	msiEndpoint, err := adal.GetMSIVMEndpoint()
	if err != nil {
		klog.Fatalf("failed to get MSI endpoint, error: %+v", err)
	}
	klog.Infof("successfully obtain MSI endpoint: %s\n", msiEndpoint)

	ctx, ctxCancel := context.WithTimeout(context.Background(), contextTimeout)
	defer ctxCancel()

	if *keyvaultName != "" && *keyvaultSecretName != "" {
		// Test if the pod identity is set up correctly
		if err := testUserAssignedIdentityOnPod(ctx, msiEndpoint, *identityClientID, *identityResourceID, *keyvaultName, *keyvaultSecretName, *keyvaultSecretVersion); err != nil {
			klog.Fatalf("testUserAssignedIdentityOnPod failed, %+v", err)
		}
	} else {
		// Test if the cluster-wide user assigned identity is set up correctly
		if err := testClusterWideUserAssignedIdentity(ctx, msiEndpoint, *subscriptionID, *resourceGroup, *identityClientID); err != nil {
			klog.Fatalf("testClusterWideUserAssignedIdentity failed, %+v", err)
		}
	}

	// Test if a service principal token can be obtained when using a system assigned identity
	if t1, err := testSystemAssignedIdentity(msiEndpoint); err != nil || t1 == nil {
		klog.Fatalf("testSystemAssignedIdentity failed, %+v", err)
	}
}

// testClusterWideUserAssignedIdentity will verify whether cluster-wide user assigned identity is working properly
func testClusterWideUserAssignedIdentity(ctx context.Context, msiEndpoint, subscriptionID, resourceGroup, identityClientID string) error {
	if err := os.Setenv("AZURE_CLIENT_ID", identityClientID); err != nil {
		return errors.Wrapf(err, "failed to set AZURE_CLIENT_ID environment variable")
	}
	defer os.Unsetenv("AZURE_CLIENT_ID")
	token, err := adal.NewServicePrincipalTokenFromMSIWithUserAssignedID(msiEndpoint, azure.PublicCloud.ResourceManagerEndpoint, identityClientID)
	if err != nil {
		return errors.Wrapf(err, "failed to get service principal token from user assigned identity")
	}

	vmClient := compute.NewVirtualMachinesClient(subscriptionID)
	vmClient.Authorizer = autorest.NewBearerAuthorizer(token)
	vmlist, err := vmClient.List(ctx, resourceGroup)
	if err != nil {
		return errors.Wrapf(err, "failed to verify cluster-wide user assigned identity")
	}

	klog.Infof("successfully verified cluster-wide user assigned identity. VM count: %d", len(vmlist.Values()))
	return nil
}

func authenticateWithMsiResourceID(msiEndpoint, resourceID, resource string) (*adal.Token, error) {
	// Create HTTP request for a managed services for Azure resources token to access Azure Resource Manager
	msiURL, err := url.Parse(msiEndpoint)
	if err != nil {
		return nil, fmt.Errorf("error parsing MSI endpoint %s: %s", msiEndpoint, err)
	}

	msiParameters := url.Values{}
	msiParameters.Set("resource", resource)
	msiParameters.Set("msi_res_id", resourceID)
	msiURL.RawQuery = msiParameters.Encode()
	req, err := http.NewRequest("GET", msiURL.String(), nil)
	if err != nil {
		return nil, fmt.Errorf("error creating request to %s: %s", msiURL.String(), err)
	}

	req.Header.Add("Metadata", "true")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error executing request to %s: %s", msiURL.String(), err)
	}

	responseBytes, err := ioutil.ReadAll(resp.Body)
	defer resp.Body.Close()
	if err != nil {
		return nil, fmt.Errorf("error parsing response body from %s: %s", msiURL.String(), err)
	}

	var token adal.Token
	err = json.Unmarshal(responseBytes, &token)
	if err != nil {
		return nil, fmt.Errorf("error unmarshaling response from %s: %s", msiURL.String(), err)
	}

	return &token, nil
}

// testUserAssignedIdentityOnPod will verify whether a pod identity is working properly
func testUserAssignedIdentityOnPod(ctx context.Context, msiEndpoint, identityClientID, identityResourceID, keyvaultName, keyvaultSecretName, keyvaultSecretVersion string) error {
	var authorizers []autorest.Authorizer
	keyClient := keyvault.New()

	if identityClientID != "" {
		// When new authorizer is created, azure-sdk-for-go  tries to create data plane authorizer using MSI. It checks the AZURE_CLIENT_ID to get the client id
		// for the user assigned identity. If client id not found, then NewServicePrincipalTokenFromMSI is invoked instead of using the actual
		// user assigned identity. Setting this env var ensures we validate GetSecret using the desired user assigned identity.
		if err := os.Setenv("AZURE_CLIENT_ID", identityClientID); err != nil {
			return errors.Wrapf(err, "failed to set AZURE_CLIENT_ID environment variable")
		}
		defer os.Unsetenv("AZURE_CLIENT_ID")

		authorizer, err := auth.NewAuthorizerFromEnvironment()
		if err != nil {
			return err
		}
		authorizers = append(authorizers, authorizer)
		klog.Infof("added authorizer with clientID: %s", identityClientID)
	}
	if identityResourceID != "" {
		// The sdk doesn't support authenticating by the resource id, but we can get a token manually
		token, err := authenticateWithMsiResourceID(msiEndpoint, identityResourceID, "https://vault.azure.net")
		if err != nil {
			return err
		}
		authorizers = append(authorizers, autorest.NewBearerAuthorizer(token))
		klog.Infof("added authorizer with resourceID: %s", identityResourceID)
	}

	klog.Infof("%s %s %s\n", keyvaultName, keyvaultSecretName, keyvaultSecretVersion)
	for _, authorizer := range authorizers {
		keyClient.Authorizer = authorizer
		secret, err := keyClient.GetSecret(ctx, fmt.Sprintf("https://%s.vault.azure.net", keyvaultName), keyvaultSecretName, keyvaultSecretVersion)
		if err != nil || *secret.Value == "" {
			return errors.Wrapf(err, "failed to verify user assigned identity on pod")
		}
	}
	klog.Infof("successfully verified user-assigned identity on pod")

	return nil
}

// testMSIEndpoint will return a service principal token obtained through a system assigned identity
func testSystemAssignedIdentity(msiEndpoint string) (*adal.Token, error) {
	spt, err := adal.NewServicePrincipalTokenFromMSI(msiEndpoint, azure.PublicCloud.ResourceManagerEndpoint)
	if err != nil {
		return nil, errors.Wrapf(err, "failed to acquire a token using the MSI VM extension")
	}

	if err := spt.Refresh(); err != nil {
		return nil, errors.Wrapf(err, "failed to refresh ServicePrincipalTokenFromMSI using the MSI VM extension, msiEndpoint(%s)", msiEndpoint)
	}

	token := spt.Token()
	if token.IsZero() {
		return nil, errors.Errorf("No token found, MSI VM extension, msiEndpoint(%s)", msiEndpoint)
	}

	klog.Infof("successfully acquired a token using the MSI, msiEndpoint(%s)", msiEndpoint)
	return &token, nil
}
