package cloudprovider

import (
	"fmt"
	"testing"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/stretchr/testify/assert"
)

func TestTruncateVMIdentities(t *testing.T) {
	ids := map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{
		"id-1": {},
		"id-2": {},
	}
	truncated, rest := truncateVMIdentities(ids)
	assert.Equal(t, truncated, ids)
	assert.Equal(t, rest, make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue))

	ids = make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	for i := 0; i < maxIdentitiesCount+50; i++ {
		ids[fmt.Sprintf("id-%d", i)] = &compute.VirtualMachineIdentityUserAssignedIdentitiesValue{}
	}
	truncated, rest = truncateVMIdentities(ids)
	assert.Len(t, truncated, maxIdentitiesCount)
	assert.Len(t, rest, 50)

	// ensuring a key does not exist in both maps
	for i := 0; i < maxIdentitiesCount+50; i++ {
		key := fmt.Sprintf("id-%d", i)
		_, ok1 := ids[key]
		_, ok2 := rest[key]
		assert.False(t, ok1 && ok2, "%s exists in both ids and rest", key)
		assert.True(t, ok1 || ok2, "%s does not exist in both ids and rest", key)
	}
}

func TestTruncateVMSSIdentities(t *testing.T) {
	ids := map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue{
		"id-1": {},
		"id-2": {},
	}
	truncated, rest := truncateVMSSIdentities(ids)
	assert.Equal(t, truncated, ids)
	assert.Equal(t, rest, make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue))

	ids = make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue)
	for i := 0; i < maxIdentitiesCount+50; i++ {
		ids[fmt.Sprintf("id-%d", i)] = &compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue{}
	}
	truncated, rest = truncateVMSSIdentities(ids)
	assert.Len(t, truncated, maxIdentitiesCount)
	assert.Len(t, rest, 50)

	// ensuring a key does not exist in both maps
	for i := 0; i < maxIdentitiesCount+50; i++ {
		key := fmt.Sprintf("id-%d", i)
		_, ok1 := ids[key]
		_, ok2 := rest[key]
		assert.False(t, ok1 && ok2, "%s exists in both ids and rest", key)
		assert.True(t, ok1 || ok2, "%s does not exist in both ids and rest", key)
	}
}
