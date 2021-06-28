// +build e2e

package azure

import (
	"context"
	"strings"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	"github.com/Azure/azure-sdk-for-go/profiles/latest/msi/mgmt/msi"
	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/adal"
	"github.com/Azure/go-autorest/autorest/azure"
	. "github.com/onsi/gomega"
)

// Client defines the behavior of a type that acts as an intermediary with ARM.
type Client interface {
	// GetIdentityClientID returns the client ID of a user-assigned identity.
	GetIdentityClientID(identityName string) string

	// ListUserAssignedIdentities returns a list of user-assigned identities assigned to the node.
	ListUserAssignedIdentities(providerID string) map[string]bool

	// AssignUserAssignedIdentity assigns a user-assigned identity to a node.
	AssignUserAssignedIdentity(providerID, identityToAssign string) error

	// UnassignUserAssignedIdentity un-assigns a user-assigned identity from a node.
	UnassignUserAssignedIdentity(providerID, identityToUnassign string) error

	// EnableSystemAssignedIdentity enables system-assigned identity for a node.
	EnableSystemAssignedIdentity(providerID string) error

	// DisableSystemAssignedIdentity disables system-assigned identity for a node.
	DisableSystemAssignedIdentity(providerID string) error

	// GetSystemAssignedIdentityInfo returns the principal ID and tenant ID of the system-assigned identity.
	GetSystemAssignedIdentityInfo(providerID string) (string, string)
}

type client struct {
	config              *framework.Config
	identityClientIDMap map[string]string
	msiClient           msi.UserAssignedIdentitiesClient
	vmManager           nodeManager
	vmssManager         nodeManager
}

// NewClient returns an implementation of Client given a test configuration.
func NewClient(config *framework.Config) Client {
	oauthConfig, err := getOAuthConfig(azure.PublicCloud, config.SubscriptionID, config.AzureTenantID)
	Expect(err).To(BeNil())

	armSpt, err := adal.NewServicePrincipalToken(*oauthConfig, config.AzureClientID, config.AzureClientSecret, azure.PublicCloud.ServiceManagementEndpoint)
	Expect(err).To(BeNil())

	c := &client{
		config:              config,
		identityClientIDMap: make(map[string]string),
		msiClient:           msi.NewUserAssignedIdentitiesClient(config.SubscriptionID),
	}

	authorizer := autorest.NewBearerAuthorizer(armSpt)
	c.msiClient.Authorizer = authorizer

	vmClient := compute.NewVirtualMachinesClient(config.SubscriptionID)
	vmClient.Authorizer = authorizer
	c.vmManager = newVMManager(config, vmClient)

	vmssClient := compute.NewVirtualMachineScaleSetsClient(config.SubscriptionID)
	vmssClient.Authorizer = authorizer
	c.vmssManager = newVMSSManager(config, vmssClient)

	return c
}

// GetIdentityClientID returns the client ID of a user-assigned identity.
func (c *client) GetIdentityClientID(identityName string) string {
	if clientID, ok := c.identityClientIDMap[identityName]; ok {
		return clientID
	}

	result, err := c.msiClient.Get(context.TODO(), c.config.IdentityResourceGroup, identityName)
	if err != nil {
		// Dummy client ID
		return "00000000-0000-0000-0000-000000000000"
	}

	clientID := result.UserAssignedIdentityProperties.ClientID.String()
	c.identityClientIDMap[identityName] = clientID

	return clientID
}

// ListUserAssignedIdentities returns a list of user-assigned identities assigned to the node.
func (c *client) ListUserAssignedIdentities(providerID string) map[string]bool {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.ListUserAssignedIdentities(nodeName)
}

// AssignUserAssignedIdentity assigns a user-assigned identity to a node.
func (c *client) AssignUserAssignedIdentity(providerID, identityToAssign string) error {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.AssignUserAssignedIdentity(nodeName, identityToAssign)
}

// UnassignUserAssignedIdentity un-assigns a user-assigned identity from a node.
func (c *client) UnassignUserAssignedIdentity(providerID, identityToAssign string) error {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.UnassignUserAssignedIdentity(nodeName, identityToAssign)
}

// EnableSystemAssignedIdentity enables system-assigned identity for a node.
func (c *client) EnableSystemAssignedIdentity(providerID string) error {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.EnableSystemAssignedIdentity(nodeName)
}

// DisableSystemAssignedIdentity disables system-assigned identity for a node.
func (c *client) DisableSystemAssignedIdentity(providerID string) error {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.DisableSystemAssignedIdentity(nodeName)
}

// GetSystemAssignedIdentityInfo returns the principal ID and tenant ID of the system-assigned identity.
func (c *client) GetSystemAssignedIdentityInfo(providerID string) (string, string) {
	nodeManager, nodeName := c.getNodeManager(providerID)
	return nodeManager.GetSystemAssignedIdentityInfo(nodeName)
}

func (c *client) getNodeManager(providerID string) (nodeManager, string) {
	if s := strings.Split(providerID, "/"); strings.EqualFold(s[len(s)-4], "virtualMachineScaleSets") {
		// VMSS name is the third last element of the slice
		return c.vmssManager, s[len(s)-3]
	} else {
		// VM name is the last element of the slice
		return c.vmManager, s[len(s)-1]
	}
}

func getOAuthConfig(env azure.Environment, subscriptionID, tenantID string) (*adal.OAuthConfig, error) {
	oauthConfig, err := adal.NewOAuthConfig(env.ActiveDirectoryEndpoint, tenantID)
	if err != nil {
		return nil, err
	}

	return oauthConfig, nil
}
