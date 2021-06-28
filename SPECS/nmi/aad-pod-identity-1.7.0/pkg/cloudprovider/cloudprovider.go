package cloudprovider

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/Azure/aad-pod-identity/pkg/config"
	"github.com/Azure/aad-pod-identity/pkg/retry"
	"github.com/Azure/aad-pod-identity/pkg/utils"
	"github.com/Azure/aad-pod-identity/version"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/adal"
	"github.com/Azure/go-autorest/autorest/azure"
	yaml "gopkg.in/yaml.v2"
	"k8s.io/klog/v2"
)

// Client is a cloud provider client
type Client struct {
	VMClient    VMClientInt
	VMSSClient  VMSSClientInt
	RetryClient retry.ClientInt
	ExtClient   compute.VirtualMachineExtensionsClient
	Config      config.AzureConfig
	configFile  string
}

// ClientInt client interface
type ClientInt interface {
	UpdateUserMSI(addUserAssignedMSIIDs, removeUserAssignedMSIIDs []string, name string, isvmss bool) error
	GetUserMSIs(name string, isvmss bool) ([]string, error)
	Init() error
}

const (
	// Occurs when the cluster service principal / managed identity does not
	// have the correct role assignment to access a user-assigned identity.
	linkedAuthorizationFailed retry.RetriableError = "LinkedAuthorizationFailed"
	// Occurs when the user-assigned identity does not exist.
	failedIdentityOperation retry.RetriableError = "FailedIdentityOperation"
	// retryAfterHeaderKey is the retry-after header key in ARM responses.
	retryAfterHeaderKey = "Retry-After"
)

// NewCloudProvider returns a azure cloud provider client
func NewCloudProvider(configFile string, updateUserMSIMaxRetry int, updateUseMSIRetryInterval time.Duration) (c *Client, e error) {
	client := &Client{
		configFile: configFile,
	}
	if err := client.Init(); err != nil {
		return nil, fmt.Errorf("failed to initialize cloud provider client, error: %+v", err)
	}
	client.RetryClient = retry.NewRetryClient(updateUserMSIMaxRetry, updateUseMSIRetryInterval)
	client.RetryClient.RegisterRetriableErrors(linkedAuthorizationFailed, failedIdentityOperation)
	return client, nil
}

// Init initializes the cloud provider client based
// on a config path or environment variables
func (c *Client) Init() error {
	c.Config = config.AzureConfig{}
	if c.configFile != "" {
		klog.V(6).Info("populating AzureConfig from azure.json")
		bytes, err := ioutil.ReadFile(c.configFile)
		if err != nil {
			return fmt.Errorf("failed to config file %s, error: %+v", c.configFile, err)
		}
		if err = yaml.Unmarshal(bytes, &c.Config); err != nil {
			return fmt.Errorf("failed to unmarshal JSON, error: %+v", err)
		}
	} else {
		klog.V(6).Info("populating AzureConfig from secret/environment variables")
		c.Config.Cloud = os.Getenv("CLOUD")
		c.Config.TenantID = os.Getenv("TENANT_ID")
		c.Config.ClientID = os.Getenv("CLIENT_ID")
		c.Config.ClientSecret = os.Getenv("CLIENT_SECRET")
		c.Config.SubscriptionID = os.Getenv("SUBSCRIPTION_ID")
		c.Config.ResourceGroupName = os.Getenv("RESOURCE_GROUP")
		c.Config.VMType = os.Getenv("VM_TYPE")
		c.Config.UseManagedIdentityExtension = strings.EqualFold(os.Getenv("USE_MSI"), "True")
		c.Config.UserAssignedIdentityID = os.Getenv("USER_ASSIGNED_MSI_CLIENT_ID")
	}

	azureEnv, err := azure.EnvironmentFromName(c.Config.Cloud)
	if err != nil {
		return fmt.Errorf("failed to get cloud environment, error: %+v", err)
	}

	err = adal.AddToUserAgent(version.GetUserAgent("MIC", version.MICVersion))
	if err != nil {
		return fmt.Errorf("failed to add MIC to user agent, error: %+v", err)
	}

	oauthConfig, err := adal.NewOAuthConfig(azureEnv.ActiveDirectoryEndpoint, c.Config.TenantID)
	if err != nil {
		return fmt.Errorf("failed to create OAuth config, error: %+v", err)
	}

	var spt *adal.ServicePrincipalToken
	if c.Config.UseManagedIdentityExtension {
		// MSI endpoint is required for both types of MSI - system assigned and user assigned.
		msiEndpoint, err := adal.GetMSIVMEndpoint()
		if err != nil {
			return fmt.Errorf("failed to get MSI endpoint, error: %+v", err)
		}
		// UserAssignedIdentityID is empty, so we are going to use system assigned MSI
		if c.Config.UserAssignedIdentityID == "" {
			klog.Infof("MIC using system assigned identity for authentication.")
			spt, err = adal.NewServicePrincipalTokenFromMSI(msiEndpoint, azureEnv.ResourceManagerEndpoint)
			if err != nil {
				return fmt.Errorf("failed to get token from system-assigned identity, error: %+v", err)
			}
		} else { // User assigned identity usage.
			klog.Infof("MIC using user assigned identity: %s for authentication.", utils.RedactClientID(c.Config.UserAssignedIdentityID))
			spt, err = adal.NewServicePrincipalTokenFromMSIWithUserAssignedID(msiEndpoint, azureEnv.ResourceManagerEndpoint, c.Config.UserAssignedIdentityID)
			if err != nil {
				return fmt.Errorf("failed to get token from user-assigned identity, error: %+v", err)
			}
		}
	} else { // This is the default scenario - use service principal to get the token.
		spt, err = adal.NewServicePrincipalToken(
			*oauthConfig,
			c.Config.ClientID,
			c.Config.ClientSecret,
			azureEnv.ResourceManagerEndpoint,
		)
		if err != nil {
			return fmt.Errorf("failed to get service principal token, error: %+v", err)
		}
	}

	extClient := compute.NewVirtualMachineExtensionsClient(c.Config.SubscriptionID)
	extClient.BaseURI = azure.PublicCloud.ResourceManagerEndpoint
	extClient.Authorizer = autorest.NewBearerAuthorizer(spt)
	extClient.PollingDelay = 5 * time.Second

	c.VMSSClient, err = NewVMSSClient(c.Config, spt)
	if err != nil {
		return fmt.Errorf("failed to create VMSS client, error: %+v", err)
	}
	c.VMClient, err = NewVirtualMachinesClient(c.Config, spt)
	if err != nil {
		return fmt.Errorf("failed to create VM client, error: %+v", err)
	}

	// We explicitly removes http.StatusTooManyRequests from autorest.StatusCodesForRetry.
	// Refer https://github.com/Azure/go-autorest/issues/398.
	statusCodesForRetry := make([]int, 0)
	for _, code := range autorest.StatusCodesForRetry {
		if code != http.StatusTooManyRequests {
			statusCodesForRetry = append(statusCodesForRetry, code)
		}
	}
	autorest.StatusCodesForRetry = statusCodesForRetry

	return nil
}

// GetUserMSIs will return a list of all identities on the node or vmss based on value of isvmss
func (c *Client) GetUserMSIs(name string, isvmss bool) ([]string, error) {
	idH, _, err := c.getIdentityResource(name, isvmss)
	if err != nil {
		return nil, fmt.Errorf("failed to get identity resource, error: %v", err)
	}
	info := idH.IdentityInfo()
	if info == nil {
		return []string{}, nil
	}
	idList := info.GetUserIdentityList()
	return idList, nil
}

// UpdateUserMSI will batch process the removal and addition of ids
func (c *Client) UpdateUserMSI(addUserAssignedMSIIDs, removeUserAssignedMSIIDs []string, name string, isvmss bool) error {
	idH, updateFunc, err := c.getIdentityResource(name, isvmss)
	if err != nil {
		return fmt.Errorf("failed to get identity resource, error: %v", err)
	}

	info := idH.IdentityInfo()
	if info == nil {
		info = idH.ResetIdentity()
	}

	ids := make(map[string]bool)
	// remove msi ids from the list
	for _, userAssignedMSIID := range removeUserAssignedMSIIDs {
		ids[userAssignedMSIID] = false
	}
	// add new ids to the list
	// add is done after setting del ids in the map to ensure an identity if in
	// both add and del list is not deleted
	for _, userAssignedMSIID := range addUserAssignedMSIIDs {
		ids[userAssignedMSIID] = true
	}

	if requiresUpdate := info.SetUserIdentities(ids); !requiresUpdate {
		return nil
	}

	klog.Infof("updating user-assigned identities on %s, assign [%d], unassign [%d]", name, len(addUserAssignedMSIIDs), len(removeUserAssignedMSIIDs))
	timeStarted := time.Now()
	shouldRetry := func(err error) bool {
		if err == nil {
			return false
		}

		// Filter previously-assigned IDs based on which identities
		// are erroneous from the last occurred error
		erroneousIDs := extractIdentitiesFromError(err)
		removedAny := false
		for _, erroneousID := range erroneousIDs {
			if removed := info.RemoveUserIdentity(erroneousID); removed {
				removedAny = true
				klog.Infof("removing %s from ID list since it is erroneous", erroneousID)
			}
		}

		// Only retry if there is at least one ID after deleting
		remainingIDs := info.GetUserIdentityList()
		if removedAny && len(remainingIDs) > 0 {
			klog.Infof("attempting to retry with ID list %v", remainingIDs)
			return true
		}

		return false
	}
	if err := c.RetryClient.Do(updateFunc, shouldRetry); err != nil {
		return err
	}

	klog.V(6).Infof("UpdateUserMSI of %s completed in %s", name, time.Since(timeStarted))

	return nil
}

func (c *Client) getIdentityResource(name string, isvmss bool) (idH IdentityHolder, update func() error, retErr error) {
	rg := c.Config.ResourceGroupName

	if isvmss {
		vmss, err := c.VMSSClient.Get(rg, name)
		if err != nil {
			return nil, nil, fmt.Errorf("failed to get vmss %s in resource group %s, error: %+v", name, rg, err)
		}

		update = func() error {
			return c.VMSSClient.UpdateIdentities(rg, name, vmss)
		}
		idH = &vmssIdentityHolder{&vmss}
		return idH, update, nil
	}

	vm, err := c.VMClient.Get(rg, name)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to get vm %s in resource group %s, error: %+v", name, rg, err)
	}
	update = func() error {
		return c.VMClient.UpdateIdentities(rg, name, vm)
	}
	idH = &vmIdentityHolder{&vm}
	return idH, update, nil
}

const nestedResourceIDPatternText = `(?i)subscriptions/(.+)/resourceGroups/(.+)/providers/(.+?)/(.+?)/(.+?)/(.+)`
const resourceIDPatternText = `(?i)subscriptions/(.+)/resourceGroups/(.+)/providers/(.+?)/(.+?)/(.+)`

var (
	nestedResourceIDPattern = regexp.MustCompile(nestedResourceIDPatternText)
	resourceIDPattern       = regexp.MustCompile(resourceIDPatternText)
)

const (
	// VMResourceType virtual machine resource type
	VMResourceType = "virtualMachines"
	// VMSSResourceType virtual machine scale sets resource type
	VMSSResourceType = "virtualMachineScaleSets"
)

// ParseResourceID is a slightly modified version of https://github.com/Azure/go-autorest/blob/528b76fd0ebec0682f3e3da7c808cd472b999615/autorest/azure/azure.go#L175
// The modification here is to support a nested resource such as is the case for a node resource in a vmss.
func ParseResourceID(resourceID string) (azure.Resource, error) {
	match := nestedResourceIDPattern.FindStringSubmatch(resourceID)
	if len(match) == 0 {
		match = resourceIDPattern.FindStringSubmatch(resourceID)
	}

	if len(match) < 6 {
		return azure.Resource{}, fmt.Errorf("failed to parse %s: invalid resource ID format", resourceID)
	}

	result := azure.Resource{
		SubscriptionID: match[1],
		ResourceGroup:  match[2],
		Provider:       match[3],
		ResourceType:   match[4],
		ResourceName:   path.Base(match[5]),
	}

	return result, nil
}

const (
	// This matches identity resource IDs on an error message from ARM
	userAssignedIdentitiesPatternText = `'(,?(?i)/subscriptions/[a-zA-Z0-9-_]+/resourcegroups/[a-zA-Z0-9-_]+/providers/Microsoft.ManagedIdentity/userAssignedIdentities/[a-zA-Z0-9-_]+)+'`
)

var (
	userAssignedIdentitiesPattern = regexp.MustCompile(userAssignedIdentitiesPatternText)
)

func extractIdentitiesFromError(err error) []string {
	var extracted []string
	if err == nil {
		return extracted
	}

	matches := userAssignedIdentitiesPattern.FindStringSubmatch(err.Error())
	if len(matches) == 0 {
		return extracted
	}

	match := matches[0]
	// Remove leading and trailing single quotes
	match = match[1 : len(match)-1]

	for _, id := range strings.Split(match, ",") {
		// Sanity check
		if err := utils.ValidateResourceID(id); err != nil {
			klog.Errorf("failed to validate %s, error: %+v", id, err)
			continue
		}
		extracted = append(extracted, id)
	}

	return extracted
}

// getRetryAfter gets the retryAfter from http response.
// The value of Retry-After can be either the number of seconds or a date in RFC1123 format.
func getRetryAfter(resp *http.Response) time.Duration {
	if resp == nil {
		return 0
	}

	ra := resp.Header.Get(retryAfterHeaderKey)
	if ra == "" {
		return 0
	}

	var dur time.Duration
	if retryAfter, _ := strconv.Atoi(ra); retryAfter > 0 {
		dur = time.Duration(retryAfter) * time.Second
	} else if t, err := time.Parse(time.RFC1123, ra); err == nil {
		dur = time.Until(t)
	}
	return dur
}
