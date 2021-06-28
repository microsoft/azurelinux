package cloudprovider

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/Azure/aad-pod-identity/pkg/config"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/stats"
	"github.com/Azure/aad-pod-identity/version"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/adal"
	"github.com/Azure/go-autorest/autorest/azure"
	"k8s.io/klog/v2"
)

// VMClient client for VirtualMachines
type VMClient struct {
	client   compute.VirtualMachinesClient
	reporter *metrics.Reporter
	// ARM throttling configures.
	retryAfterReader time.Time
	retryAfterWriter time.Time
}

// VMClientInt is the interface used by "cloudprovider" for interacting with Azure vmas
type VMClientInt interface {
	Get(rgName string, nodeName string) (compute.VirtualMachine, error)
	UpdateIdentities(rg, nodeName string, vmu compute.VirtualMachine) error
}

// NewVirtualMachinesClient creates a new vm client.
func NewVirtualMachinesClient(config config.AzureConfig, spt *adal.ServicePrincipalToken) (c *VMClient, e error) {
	client := compute.NewVirtualMachinesClient(config.SubscriptionID)

	azureEnv, err := azure.EnvironmentFromName(config.Cloud)
	if err != nil {
		return nil, fmt.Errorf("failed to get cloud environment, error: %+v", err)
	}
	client.BaseURI = azureEnv.ResourceManagerEndpoint
	client.Authorizer = autorest.NewBearerAuthorizer(spt)
	client.PollingDelay = 5 * time.Second
	err = client.AddToUserAgent(version.GetUserAgent("MIC", version.MICVersion))
	if err != nil {
		return nil, fmt.Errorf("failed to add MIC to user agent, error: %+v", err)
	}

	reporter, err := metrics.NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}

	return &VMClient{
		client:   client,
		reporter: reporter,
	}, nil
}

// Get gets the passed in vm.
func (c *VMClient) Get(rgName string, nodeName string) (compute.VirtualMachine, error) {
	ctx := context.Background()
	begin := time.Now()
	var err error

	defer func() {
		if err != nil {
			err = c.reporter.ReportCloudProviderOperationError(metrics.GetVMOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		err = c.reporter.ReportCloudProviderOperationDuration(metrics.GetVMOperationName, time.Since(begin))
		if err != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
	}()

	// Report errors if the client is throttled.
	if c.retryAfterReader.After(time.Now()) {
		return compute.VirtualMachine{}, fmt.Errorf("VMGet client throttled, retry after: %v", c.retryAfterReader)
	}

	vm, err := c.client.Get(ctx, rgName, nodeName, "")
	if err != nil {
		resp := vm.Response.Response
		// Update RetryAfterReader so that no more requests would be sent until RetryAfter expires.
		c.retryAfterReader = time.Now().Add(getRetryAfter(resp))
		return vm, fmt.Errorf("failed to get vm %s in resource group %s, error: %+v", nodeName, rgName, err)
	}
	stats.Increment(stats.TotalGetCalls, 1)
	stats.AggregateConcurrent(stats.CloudGet, begin, time.Now())
	return vm, nil
}

// UpdateIdentities updates the user assigned identities for the provided node
func (c *VMClient) UpdateIdentities(rg, nodeName string, vm compute.VirtualMachine) error {
	var future compute.VirtualMachinesUpdateFuture
	var err error
	ctx := context.Background()
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportCloudProviderOperationError(metrics.UpdateVMOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		err = c.reporter.ReportCloudProviderOperationDuration(metrics.UpdateVMOperationName, time.Since(begin))
		if err != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
	}()

	// Report errors if the client is throttled.
	if c.retryAfterWriter.After(time.Now()) {
		return fmt.Errorf("VMUpdate client throttled, retry after: %v", c.retryAfterWriter)
	}

	hasUpdated := false
	remainingIDs := vm.Identity.UserAssignedIdentities
	for !hasUpdated || len(remainingIDs) > 0 {
		hasUpdated = true
		vm.Identity.UserAssignedIdentities, remainingIDs = truncateVMIdentities(remainingIDs)
		if future, err = c.client.Update(ctx, rg, nodeName, compute.VirtualMachineUpdate{Identity: vm.Identity}); err != nil {
			resp := future.Response()
			// Update RetryAfterWriter so that no more requests would be sent until RetryAfter expires.
			c.retryAfterWriter = time.Now().Add(getRetryAfter(resp))
			return fmt.Errorf("failed to update identities for %s in %s, error: %+v", nodeName, rg, err)
		}
		if err = future.WaitForCompletionRef(ctx, c.client.Client); err != nil {
			return fmt.Errorf("failed to wait for identity update completion for vm %s in resource group %s, error: %+v", nodeName, rg, err)
		}
		stats.Increment(stats.TotalPatchCalls, 1)
		stats.AggregateConcurrent(stats.CloudPatch, begin, time.Now())
	}

	return nil
}

type vmIdentityHolder struct {
	vm *compute.VirtualMachine
}

func (h *vmIdentityHolder) IdentityInfo() IdentityInfo {
	if h.vm.Identity == nil {
		return nil
	}
	return &vmIdentityInfo{h.vm.Identity}
}

func (h *vmIdentityHolder) ResetIdentity() IdentityInfo {
	h.vm.Identity = &compute.VirtualMachineIdentity{}
	return h.IdentityInfo()
}

type vmIdentityInfo struct {
	info *compute.VirtualMachineIdentity
}

func (i *vmIdentityInfo) GetUserIdentityList() []string {
	var ids []string
	if i.info == nil {
		return ids
	}
	for id := range i.info.UserAssignedIdentities {
		ids = append(ids, id)
	}
	return ids
}

func (i *vmIdentityInfo) SetUserIdentities(ids map[string]bool) bool {
	if i.info.UserAssignedIdentities == nil {
		i.info.UserAssignedIdentities = make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	}

	nodeList := make(map[string]bool)
	// add all current existing ids
	for id := range i.info.UserAssignedIdentities {
		id = strings.ToLower(id)
		nodeList[id] = true
	}

	// add and remove the new list of identities keeping the same type as before
	userAssignedIdentities := make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	for id, add := range ids {
		id = strings.ToLower(id)
		_, exists := nodeList[id]
		// already exists on node and want to remove existing identity
		if exists && !add {
			userAssignedIdentities[id] = nil
			delete(nodeList, id)
		}
		// doesn't exist on the node and want to add new identity
		if !exists && add {
			userAssignedIdentities[id] = &compute.VirtualMachineIdentityUserAssignedIdentitiesValue{}
			nodeList[id] = true
		}
		// exists and add - will already be in the nodeList and no need to patch for it
		// not exists and delete - no need to patch it as it already doesn't exist
	}

	// all identities are the node are to be removed
	if len(nodeList) == 0 {
		i.info.UserAssignedIdentities = nil
		if i.info.Type == compute.ResourceIdentityTypeSystemAssignedUserAssigned {
			i.info.Type = compute.ResourceIdentityTypeSystemAssigned
		} else {
			i.info.Type = compute.ResourceIdentityTypeNone
		}
		return true
	}

	i.info.Type = getUpdatedResourceIdentityType(i.info.Type)
	i.info.UserAssignedIdentities = userAssignedIdentities
	return len(i.info.UserAssignedIdentities) > 0
}

func (i *vmIdentityInfo) RemoveUserIdentity(delID string) bool {
	delID = strings.ToLower(delID)
	if i.info.UserAssignedIdentities != nil {
		if _, ok := i.info.UserAssignedIdentities[delID]; ok {
			delete(i.info.UserAssignedIdentities, delID)
			return true
		}
	}

	return false
}
