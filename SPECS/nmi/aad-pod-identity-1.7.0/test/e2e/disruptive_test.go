// +build e2e

package e2e

import (
	"sync"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureassignedidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentitybinding"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/identityvalidator"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/mic"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	corev1 "k8s.io/api/core/v1"

	. "github.com/onsi/ginkgo"
)

var _ = Describe("When AAD Pod Identity operations are disrupted", func() {
	var (
		specName = "disruptive"
		ns       *corev1.Namespace
	)

	BeforeEach(func() {
		ns = namespace.Create(namespace.CreateInput{
			Creator: kubeClient,
			Name:    specName,
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

	It("should pass the identity validation even when MIC leader is changed", func() {
		var wg sync.WaitGroup
		wg.Add(2)

		go func() {
			defer wg.Done()
			mic.DeleteLeader(mic.DeleteLeaderInput{
				Getter:  kubeClient,
				Deleter: kubeClient,
			})
		}()

		go func() {
			defer wg.Done()
			azureIdentity := azureidentity.Create(azureidentity.CreateInput{
				Creator:      kubeClient,
				Config:       config,
				AzureClient:  azureClient,
				Name:         keyvaultIdentity,
				Namespace:    ns.Name,
				IdentityType: aadpodv1.UserAssignedMSI,
				IdentityName: keyvaultIdentity,
			})

			azureIdentityBinding := azureidentitybinding.Create(azureidentitybinding.CreateInput{
				Creator:           kubeClient,
				Name:              keyvaultIdentityBinding,
				Namespace:         ns.Name,
				AzureIdentityName: azureIdentity.Name,
				Selector:          keyvaultIdentitySelector,
			})

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
		}()

		wg.Wait()
	})
})
