package cloudprovider

import (
	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
)

// IdentityHolder represents a resource that contains an Identity object
// This is used to be able to generically intract with multiple resource types (e.g. VirtualMachine and VirtualMachineScaleSet)
// which each contain an identity.
type IdentityHolder interface {
	IdentityInfo() IdentityInfo
	ResetIdentity() IdentityInfo
}

// IdentityInfo is used to interact with different implementations of Azure compute identities.
// This is needed because different Azure resource types (e.g. VirtualMachine and VirtualMachineScaleSet)
// have different identity types.
// This abstracts those differences.
type IdentityInfo interface {
	GetUserIdentityList() []string
	SetUserIdentities(map[string]bool) bool
	RemoveUserIdentity(string) bool
}

// getUpdatedResourceIdentityType returns the new resource identity type
// to be set on the VM/VMSS based on current type
func getUpdatedResourceIdentityType(identityType compute.ResourceIdentityType) compute.ResourceIdentityType {
	switch identityType {
	case "", compute.ResourceIdentityTypeNone, compute.ResourceIdentityTypeUserAssigned:
		return compute.ResourceIdentityTypeUserAssigned
	case compute.ResourceIdentityTypeSystemAssigned, compute.ResourceIdentityTypeSystemAssignedUserAssigned:
		return compute.ResourceIdentityTypeSystemAssignedUserAssigned
	default:
		return compute.ResourceIdentityTypeNone
	}
}
