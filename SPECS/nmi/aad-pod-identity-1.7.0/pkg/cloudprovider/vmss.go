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

// VMSSClient is used to interact with Azure virtual machine scale sets.
type VMSSClient struct {
	client   compute.VirtualMachineScaleSetsClient
	reporter *metrics.Reporter
	// ARM throttling configures.
	retryAfterReader time.Time
	retryAfterWriter time.Time
}

// VMSSClientInt is the interface used by "cloudprovider" for interacting with Azure vmss
type VMSSClientInt interface {
	Get(rgName, name string) (compute.VirtualMachineScaleSet, error)
	UpdateIdentities(rg, vmssName string, vmu compute.VirtualMachineScaleSet) error
}

// NewVMSSClient creates a new vmss client.
func NewVMSSClient(config config.AzureConfig, spt *adal.ServicePrincipalToken) (c *VMSSClient, e error) {
	client := compute.NewVirtualMachineScaleSetsClient(config.SubscriptionID)

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

	return &VMSSClient{
		client:   client,
		reporter: reporter,
	}, nil
}

// UpdateIdentities updates the user assigned identities for the provided node
func (c *VMSSClient) UpdateIdentities(rg, vmssName string, vmss compute.VirtualMachineScaleSet) error {
	var future compute.VirtualMachineScaleSetsUpdateFuture
	var err error
	ctx := context.Background()
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportCloudProviderOperationError(metrics.UpdateVMSSOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		err = c.reporter.ReportCloudProviderOperationDuration(metrics.UpdateVMSSOperationName, time.Since(begin))
		if err != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
	}()

	// Report errors if the client is throttled.
	if c.retryAfterWriter.After(time.Now()) {
		return fmt.Errorf("VMSSUpdate client throttled, retry after: %v", c.retryAfterWriter)
	}

	hasUpdated := false
	remainingIDs := vmss.Identity.UserAssignedIdentities
	for !hasUpdated || len(remainingIDs) > 0 {
		hasUpdated = true
		vmss.Identity.UserAssignedIdentities, remainingIDs = truncateVMSSIdentities(remainingIDs)
		if future, err = c.client.Update(ctx, rg, vmssName, compute.VirtualMachineScaleSetUpdate{Identity: vmss.Identity}); err != nil {
			resp := future.Response()
			// Update RetryAfterWriter so that no more requests would be sent until RetryAfter expires.
			c.retryAfterWriter = time.Now().Add(getRetryAfter(resp))
			return fmt.Errorf("failed to update identities for %s in %s, error: %+v", vmssName, rg, err)
		}
		if err = future.WaitForCompletionRef(ctx, c.client.Client); err != nil {
			return fmt.Errorf("failed to wait for identity update completion for vmss %s in resource group %s, error: %+v", vmssName, rg, err)
		}
		stats.Increment(stats.TotalPatchCalls, 1)
		stats.AggregateConcurrent(stats.CloudPatch, begin, time.Now())
	}

	return nil
}

// Get gets the passed in vmss.
func (c *VMSSClient) Get(rgName string, vmssName string) (ret compute.VirtualMachineScaleSet, err error) {
	ctx := context.Background()
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportCloudProviderOperationError(metrics.GetVmssOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		err = c.reporter.ReportCloudProviderOperationDuration(metrics.GetVmssOperationName, time.Since(begin))
		if err != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
	}()

	// Report errors if the client is throttled.
	if c.retryAfterReader.After(time.Now()) {
		return compute.VirtualMachineScaleSet{}, fmt.Errorf("VMSSGet client throttled, retry after: %v", c.retryAfterReader)
	}

	vmss, err := c.client.Get(ctx, rgName, vmssName)
	if err != nil {
		resp := vmss.Response.Response
		// Update RetryAfterReader so that no more requests would be sent until RetryAfter expires.
		c.retryAfterReader = time.Now().Add(getRetryAfter(resp))
		return vmss, fmt.Errorf("failed to get vmss %s in resource group %s, error: %+v", vmssName, rgName, err)
	}
	stats.Increment(stats.TotalGetCalls, 1)
	stats.AggregateConcurrent(stats.CloudGet, begin, time.Now())
	return vmss, nil
}

// vmssIdentityHolder implements `IdentityHolder` for vmss resources.
type vmssIdentityHolder struct {
	vmss *compute.VirtualMachineScaleSet
}

func (h *vmssIdentityHolder) IdentityInfo() IdentityInfo {
	if h.vmss.Identity == nil {
		return nil
	}
	return &vmssIdentityInfo{h.vmss.Identity}
}

func (h *vmssIdentityHolder) ResetIdentity() IdentityInfo {
	h.vmss.Identity = &compute.VirtualMachineScaleSetIdentity{
		Type:                   compute.ResourceIdentityTypeUserAssigned,
		UserAssignedIdentities: make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue),
	}
	return h.IdentityInfo()
}

type vmssIdentityInfo struct {
	info *compute.VirtualMachineScaleSetIdentity
}

func (i *vmssIdentityInfo) GetUserIdentityList() []string {
	var ids []string
	if i.info == nil {
		return ids
	}
	for id := range i.info.UserAssignedIdentities {
		ids = append(ids, id)
	}
	return ids
}

func (i *vmssIdentityInfo) SetUserIdentities(ids map[string]bool) bool {
	if i.info.UserAssignedIdentities == nil {
		i.info.UserAssignedIdentities = make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue)
	}

	nodeList := make(map[string]bool)
	// add all current existing ids
	for id := range i.info.UserAssignedIdentities {
		id = strings.ToLower(id)
		nodeList[id] = true
	}

	// add and remove the new list of identities keeping the same type as before
	userAssignedIdentities := make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue)
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
			userAssignedIdentities[id] = &compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue{}
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

func (i *vmssIdentityInfo) RemoveUserIdentity(delID string) bool {
	delID = strings.ToLower(delID)
	if i.info.UserAssignedIdentities != nil {
		if _, ok := i.info.UserAssignedIdentities[delID]; ok {
			delete(i.info.UserAssignedIdentities, delID)
			return true
		}
	}

	return false
}
