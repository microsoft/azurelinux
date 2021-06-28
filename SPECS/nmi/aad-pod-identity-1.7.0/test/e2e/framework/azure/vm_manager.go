// +build e2e

package azure

import (
	"context"
	"fmt"
	"strings"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	. "github.com/onsi/ginkgo"
)

type vmManager struct {
	config   *framework.Config
	vmClient compute.VirtualMachinesClient
}

func newVMManager(config *framework.Config, vmClient compute.VirtualMachinesClient) nodeManager {
	return &vmManager{
		config:   config,
		vmClient: vmClient,
	}
}

// ListUserAssignedIdentities returns a list of user-assigned identities assigned to the node.
func (m *vmManager) ListUserAssignedIdentities(vmName string) map[string]bool {
	userAssignedIdentities := make(map[string]bool)
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil || vm.Identity == nil {
		return userAssignedIdentities
	}

	for id := range vm.Identity.UserAssignedIdentities {
		userAssignedIdentities[strings.ToLower(id)] = true
	}

	return userAssignedIdentities
}

// AssignUserAssignedIdentity assigns a user-assigned identity to a node.
func (m *vmManager) AssignUserAssignedIdentity(vmName, identityToAssign string) error {
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil {
		return err
	}

	if vm.Identity == nil {
		vm.Identity = &compute.VirtualMachineIdentity{
			UserAssignedIdentities: map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{},
		}
	}
	if vm.Identity.UserAssignedIdentities == nil {
		vm.Identity.UserAssignedIdentities = make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	}

	identityAssignResourceID := fmt.Sprintf(ResourceIDTemplate, m.config.SubscriptionID, m.config.IdentityResourceGroup, identityToAssign)
	for identity := range vm.Identity.UserAssignedIdentities {
		// identity already exists and doesn't need to be re-assigned
		if strings.EqualFold(identity, identityAssignResourceID) {
			return nil
		}
	}

	vm.Identity.UserAssignedIdentities = map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{
		identityAssignResourceID: {},
	}
	switch vm.Identity.Type {
	case compute.ResourceIdentityTypeSystemAssigned:
		vm.Identity.Type = compute.ResourceIdentityTypeSystemAssignedUserAssigned
	default:
		vm.Identity.Type = compute.ResourceIdentityTypeUserAssigned
	}

	By(fmt.Sprintf("Assigning \"%s\" to \"%s\"", identityToAssign, vmName))
	return m.updateIdentity(vmName, vm.Identity)
}

// UnassignUserAssignedIdentity un-assigns a user-assigned identity from a node.
func (m *vmManager) UnassignUserAssignedIdentity(vmName, identityToUnassign string) error {
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil {
		return err
	}

	if vm.Identity == nil || len(vm.Identity.UserAssignedIdentities) == 0 {
		return nil
	}

	var hasOtherIdentitiesAssigned bool
	for identity := range vm.Identity.UserAssignedIdentities {
		if s := strings.Split(identity, "/"); strings.EqualFold(s[len(s)-1], identityToUnassign) {
			By(fmt.Sprintf("Un-assigning \"%s\" from \"%s\"", identityToUnassign, vmName))
			// when using PATCH for deleting identities, the identities need to exist in the map
			// with nil value to force the deletion
			vm.Identity.UserAssignedIdentities[identity] = nil
			continue
		}
		hasOtherIdentitiesAssigned = true
	}

	if !hasOtherIdentitiesAssigned {
		vm.Identity.UserAssignedIdentities = nil
		switch vm.Identity.Type {
		case compute.ResourceIdentityTypeSystemAssignedUserAssigned:
			vm.Identity.Type = compute.ResourceIdentityTypeSystemAssigned
		default:
			vm.Identity.Type = compute.ResourceIdentityTypeNone
		}
	}

	return m.updateIdentity(vmName, vm.Identity)
}

// EnableSystemAssignedIdentity enables system-assigned identity for a node.
func (m *vmManager) EnableSystemAssignedIdentity(vmName string) error {
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil {
		return err
	}

	if vm.Identity == nil {
		vm.Identity = &compute.VirtualMachineIdentity{
			Type: compute.ResourceIdentityTypeSystemAssigned,
		}
	} else {
		switch vm.Identity.Type {
		case compute.ResourceIdentityTypeSystemAssigned, compute.ResourceIdentityTypeSystemAssignedUserAssigned:
			return nil
		case compute.ResourceIdentityTypeUserAssigned:
			vm.Identity.Type = compute.ResourceIdentityTypeSystemAssignedUserAssigned
			for identity := range vm.Identity.UserAssignedIdentities {
				vm.Identity.UserAssignedIdentities[identity] = &compute.VirtualMachineIdentityUserAssignedIdentitiesValue{}
			}
		default:
			vm.Identity.Type = compute.ResourceIdentityTypeSystemAssigned
		}
	}

	By(fmt.Sprintf("Enabling system-assigned identity for %s", vmName))
	return m.updateIdentity(vmName, vm.Identity)
}

// DisableSystemAssignedIdentity disables system-assigned identity for a node.
func (m *vmManager) DisableSystemAssignedIdentity(vmName string) error {
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil {
		return err
	}

	if vm.Identity == nil {
		return nil
	}

	switch vm.Identity.Type {
	case compute.ResourceIdentityTypeNone, compute.ResourceIdentityTypeUserAssigned:
		return nil
	case compute.ResourceIdentityTypeSystemAssignedUserAssigned:
		vm.Identity.Type = compute.ResourceIdentityTypeUserAssigned
		for identity := range vm.Identity.UserAssignedIdentities {
			vm.Identity.UserAssignedIdentities[identity] = &compute.VirtualMachineIdentityUserAssignedIdentitiesValue{}
		}
	default:
		vm.Identity.UserAssignedIdentities = nil
		vm.Identity.Type = compute.ResourceIdentityTypeNone
	}

	By(fmt.Sprintf("Disabling system-assigned identity for %s", vmName))
	return m.updateIdentity(vmName, vm.Identity)
}

// GetSystemAssignedIdentityInfo returns the principal ID and tenant ID of the system-assigned identity.
func (m *vmManager) GetSystemAssignedIdentityInfo(vmName string) (string, string) {
	vm, err := m.vmClient.Get(context.TODO(), m.config.NodeResourceGroup, vmName, compute.InstanceView)
	if err != nil {
		return "", ""
	}

	if vm.Identity == nil || (vm.Identity.Type != compute.ResourceIdentityTypeSystemAssigned && vm.Identity.Type != compute.ResourceIdentityTypeSystemAssignedUserAssigned) {
		return "", ""
	}

	return *vm.Identity.PrincipalID, *vm.Identity.TenantID
}

func (m *vmManager) updateIdentity(vmName string, vmIdentity *compute.VirtualMachineIdentity) error {
	if future, err := m.vmClient.Update(context.TODO(), m.config.NodeResourceGroup, vmName, compute.VirtualMachineUpdate{Identity: vmIdentity}); err != nil {
		return err
	} else {
		if err := future.WaitForCompletionRef(context.TODO(), m.vmClient.Client); err != nil {
			return err
		}
	}

	return nil
}
