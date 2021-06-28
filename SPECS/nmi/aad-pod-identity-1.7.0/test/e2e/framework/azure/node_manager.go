// +build e2e

package azure

const (
	ResourceIDTemplate = "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.ManagedIdentity/userAssignedIdentities/%s"
)

type nodeManager interface {
	// ListUserAssignedIdentities returns a list of user-assigned identities assigned to the node.
	ListUserAssignedIdentities(nodeName string) map[string]bool

	// AssignUserAssignedIdentity assigns a user-assigned identity to a node.
	AssignUserAssignedIdentity(nodeName, identityToAssign string) error

	// UnassignUserAssignedIdentity un-assigns a user-assigned identity from a node.
	UnassignUserAssignedIdentity(nodeName, identityToUnassign string) error

	// EnableSystemAssignedIdentity enables system-assigned identity for a node.
	EnableSystemAssignedIdentity(nodeName string) error

	// DisableSystemAssignedIdentity disables system-assigned identity for a node.
	DisableSystemAssignedIdentity(nodeName string) error

	// GetSystemAssignedIdentityInfo returns the principal ID and tenant ID of the system-assigned identity.
	GetSystemAssignedIdentityInfo(nodeName string) (string, string)
}
