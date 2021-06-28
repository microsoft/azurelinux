package cloudprovider

import (
	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
)

const (
	maxIdentitiesCount = 150
)

// truncateVMIdentities truncates a given list of vm identities to maxIdentitiesCount and returns any extra identities.
func truncateVMIdentities(ids map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue) (map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue, map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue) {
	rest := make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	i := 0
	for k, v := range ids {
		if i >= maxIdentitiesCount {
			rest[k] = v
			delete(ids, k)
		}
		i++
	}

	return ids, rest
}

// truncateVMSSIdentities truncates a given list of vmss identities to maxIdentitiesCount and returns any extra identities.
func truncateVMSSIdentities(ids map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue) (map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue, map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue) {
	rest := make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue)
	i := 0
	for k, v := range ids {
		if i >= maxIdentitiesCount {
			rest[k] = v
			delete(ids, k)
		}
		i++
	}

	return ids, rest
}
