// +build e2e

package e2e

import (
	"fmt"
	"strings"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azure"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureassignedidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentitybinding"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/identityvalidator"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/node"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
)

const (
	immutableIdentity = "immutable-identity"
)

var _ = Describe("When managing identities from the underlying nodes", func() {
	var (
		specName             = "node"
		nodes                *corev1.NodeList
		ns                   *corev1.Namespace
		azureIdentity        *aadpodv1.AzureIdentity
		azureIdentityBinding *aadpodv1.AzureIdentityBinding
	)

	BeforeEach(func() {
		ns = namespace.Create(namespace.CreateInput{
			Creator: kubeClient,
			Name:    specName,
		})

		nodes = node.List(node.ListInput{
			Lister: kubeClient,
		})

		azureIdentity = azureidentity.Create(azureidentity.CreateInput{
			Creator:      kubeClient,
			Config:       config,
			AzureClient:  azureClient,
			Name:         keyvaultIdentity,
			Namespace:    ns.Name,
			IdentityType: aadpodv1.UserAssignedMSI,
			IdentityName: keyvaultIdentity,
		})

		azureIdentityBinding = azureidentitybinding.Create(azureidentitybinding.CreateInput{
			Creator:           kubeClient,
			Name:              keyvaultIdentityBinding,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			Selector:          keyvaultIdentitySelector,
		})
	})

	AfterEach(func() {
		Cleanup(CleanupInput{
			Namespace: ns,
			Getter:    kubeClient,
			Lister:    kubeClient,
			Deleter:   kubeClient,
		})
	})

	It("should not delete a user-assigned identity that is being used by a different pod", func() {
		// This test is specifically testing VMSS behavior
		// As such we'll look through the cluster to see if there are nodes assigned
		// to a VMSS, and if any of thoe VMSS's have more than one node.
		//
		// We cannot do the test if there is not at least1 VMSS with at least 2 nodes
		// attach to it.
		var vmssNodes []corev1.Node
		if vmssNodes = getVMSSNodes(nodes); len(vmssNodes) < 2 {
			Skip("Skipping since there is no VMSS node")
		}

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        vmssNodes[0].Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		userAssignedIdentities := azureClient.ListUserAssignedIdentities(vmssNodes[0].Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)).To(BeTrue())

		// Create a second identity-validator with the same AzureIdentity
		// and AzureIdentityBinding but different VMSS node
		identityValidator2 := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        vmssNodes[1].Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator2.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		userAssignedIdentities = azureClient.ListUserAssignedIdentities(vmssNodes[1].Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)).To(BeTrue())

		identityvalidator.Delete(identityvalidator.DeleteInput{
			Deleter:           kubeClient,
			IdentityValidator: identityValidator2,
		})

		azureassignedidentity.WaitForLen(azureassignedidentity.WaitForLenInput{
			Lister: kubeClient,
			Len:    1,
		})

		By(fmt.Sprintf("Ensuring %s is still assigned to the VMSS", keyvaultIdentity))
		userAssignedIdentities = azureClient.ListUserAssignedIdentities(vmssNodes[0].Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)).To(BeTrue())
	})

	It("should be able to delete AzureAssignedIdentity when the user-assigned is un-assigned from the underlying node", func() {
		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})

		// Since we don't know where the identity-validator is scheduled to,
		// simply delete the user-assigned identity from every node and ignore any error
		for _, node := range nodes.Items {
			if strings.EqualFold(node.ObjectMeta.Labels["kubernetes.io/role"], "master") {
				continue
			}
			azureClient.UnassignUserAssignedIdentity(node.Spec.ProviderID, keyvaultIdentity)
		}

		identityvalidator.Delete(identityvalidator.DeleteInput{
			Deleter:           kubeClient,
			IdentityValidator: identityValidator,
		})

		azureassignedidentity.WaitForLen(azureassignedidentity.WaitForLenInput{
			Lister: kubeClient,
			Len:    0,
		})
	})

	It("should not alter the system-assigned identity after creating and deleting pod identity", func() {
		// Schedule identity-validator to this node
		node := nodes.Items[0]

		err := azureClient.EnableSystemAssignedIdentity(node.Spec.ProviderID)
		Expect(err).To(BeNil())
		defer func() {
			err := azureClient.DisableSystemAssignedIdentity(node.Spec.ProviderID)
			Expect(err).To(BeNil())
		}()

		principalIDBefore, tenantIDBefore := azureClient.GetSystemAssignedIdentityInfo(node.Spec.ProviderID)
		Expect(principalIDBefore).NotTo(BeEmpty())
		Expect(tenantIDBefore).NotTo(BeEmpty())

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        node.Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})

		By("Verifying that the Principal ID and Tenant ID of the system-assigned identity haven't been altered")
		principalIDAfter, tenantIDAfter := azureClient.GetSystemAssignedIdentityInfo(node.Spec.ProviderID)
		Expect(principalIDBefore).To(Equal(principalIDAfter))
		Expect(tenantIDBefore).To(Equal(tenantIDAfter))
	})

	It("should not alter the user-assigned identity on VM after AAD pod identity is created and deleted", func() {
		// Schedule identity-validator to this node
		node := nodes.Items[0]

		err := azureClient.AssignUserAssignedIdentity(node.Spec.ProviderID, clusterIdentity)
		Expect(err).To(BeNil())
		defer func() {
			err := azureClient.UnassignUserAssignedIdentity(node.Spec.ProviderID, clusterIdentity)
			Expect(err).To(BeNil())
		}()

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        node.Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})

		By(fmt.Sprintf("Ensuring both keyvault-identity and cluster-identity are assigned to %s", node.Name))
		userAssignedIdentities := azureClient.ListUserAssignedIdentities(node.Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)).To(BeTrue())
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, clusterIdentity)).To(BeTrue())

		identityvalidator.Delete(identityvalidator.DeleteInput{
			Deleter:           kubeClient,
			IdentityValidator: identityValidator,
		})

		azureassignedidentity.WaitForLen(azureassignedidentity.WaitForLenInput{
			Lister: kubeClient,
			Len:    0,
		})

		By(fmt.Sprintf("Ensuring cluster-identity is still assigned to %s after deleting identity-validator", node.Name))
		userAssignedIdentities = azureClient.ListUserAssignedIdentities(node.Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, clusterIdentity)).To(BeTrue())
	})

	It("should not delete the Immutable Identity from VMSS when the deployment is deleted", func() {
		var vmssNodes []corev1.Node
		if vmssNodes = getVMSSNodes(nodes); len(vmssNodes) < 2 {
			Skip("Skipping since there is no VMSS node")
		}

		// Schedule identity-validator to this node
		node := vmssNodes[0]
		defer func() {
			err := azureClient.UnassignUserAssignedIdentity(node.Spec.ProviderID, immutableIdentity)
			Expect(err).To(BeNil())
		}()

		azureIdentity = azureidentity.Update(azureidentity.UpdateInput{
			Updater:             kubeClient,
			Config:              config,
			AzureClient:         azureClient,
			AzureIdentity:       azureIdentity,
			UpdatedIdentityName: immutableIdentity,
		})

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        node.Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})

		identityvalidator.Delete(identityvalidator.DeleteInput{
			Deleter:           kubeClient,
			IdentityValidator: identityValidator,
		})

		azureassignedidentity.WaitForLen(azureassignedidentity.WaitForLenInput{
			Lister: kubeClient,
			Len:    0,
		})

		By(fmt.Sprintf("Ensuring %s is still assigned to %s", immutableIdentity, node.Name))
		userAssignedIdentities := azureClient.ListUserAssignedIdentities(node.Spec.ProviderID)
		Expect(isUserAssignedIdentityExist(userAssignedIdentities, immutableIdentity)).To(BeTrue())
	})

	It("should reconcile identity assignment on Azure if the user-assigned identity is manually unassigned from the underlying node", func() {
		// Schedule identity-validator to this node
		node := nodes.Items[0]

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: azureIdentityBinding.Spec.Selector,
			NodeName:        node.Name,
		})

		azureassignedidentity.Wait(azureassignedidentity.WaitInput{
			Getter:            kubeClient,
			PodName:           identityValidator.Name,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			StateToWaitFor:    aadpodv1.AssignedIDAssigned,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})

		Eventually(func() bool {
			err := azureClient.UnassignUserAssignedIdentity(node.Spec.ProviderID, keyvaultIdentity)
			Expect(err).To(BeNil())
			userAssignedIdentities := azureClient.ListUserAssignedIdentities(node.Spec.ProviderID)
			return !isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)
		}, framework.Timeout, framework.Polling).Should(BeTrue())

		By(fmt.Sprintf("Waiting for identity assignment of \"%s\" to be reconciled", keyvaultIdentity))
		Eventually(func() bool {
			userAssignedIdentities := azureClient.ListUserAssignedIdentities(node.Spec.ProviderID)
			return isUserAssignedIdentityExist(userAssignedIdentities, keyvaultIdentity)
		}, framework.Timeout, framework.Polling).Should(BeTrue())

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:             kubeClient,
			Config:             config,
			KubeconfigPath:     kubeconfigPath,
			PodName:            identityValidator.Name,
			Namespace:          ns.Name,
			IdentityClientID:   azureIdentity.Spec.ClientID,
			IdentityResourceID: azureIdentity.Spec.ResourceID,
		})
	})
})

func getVMSSNodes(nodes *corev1.NodeList) []corev1.Node {
	vmssNodes := []corev1.Node{}
	for _, node := range nodes.Items {
		if strings.EqualFold(node.ObjectMeta.Labels["kubernetes.io/role"], "master") {
			continue
		}
		if strings.Contains(node.Spec.ProviderID, "virtualMachineScaleSets") {
			vmssNodes = append(vmssNodes, node)
		}
	}

	return vmssNodes
}

func isUserAssignedIdentityExist(identities map[string]bool, identityToCheck string) bool {
	resourceID := fmt.Sprintf(azure.ResourceIDTemplate, config.SubscriptionID, config.IdentityResourceGroup, identityToCheck)
	_, ok := identities[strings.ToLower(resourceID)]
	return ok
}
