// +build e2e

package e2e

import (
	"fmt"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureassignedidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentitybinding"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/identityvalidator"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/secret"

	. "github.com/onsi/ginkgo"
	corev1 "k8s.io/api/core/v1"
)

var (
	keyvaultSPBinding  = fmt.Sprintf("%s-binding", keyVaultServicePrincipal)
	keyvaultSPSelector = fmt.Sprintf("%s-selector", keyVaultServicePrincipal)
)

var _ = Describe("When deploying service principal", func() {
	var (
		specName             = "service-principal"
		ns                   *corev1.Namespace
		azureIdentity        *aadpodv1.AzureIdentity
		azureIdentityBinding *aadpodv1.AzureIdentityBinding
		clientPasswordSecret *corev1.Secret
		identityValidator    *corev1.Pod
	)

	BeforeEach(func() {
		ns = namespace.Create(namespace.CreateInput{
			Creator: kubeClient,
			Name:    specName,
		})

		clientPasswordSecret = secret.Create(secret.CreateInput{
			Creator:      kubeClient,
			Config:       config,
			Name:         keyVaultServicePrincipal,
			Namespace:    ns.Name,
			ClientSecret: config.ServicePrincipalClientSecret,
		})

		azureIdentity = azureidentity.Create(azureidentity.CreateInput{
			Creator:          kubeClient,
			Config:           config,
			AzureClient:      azureClient,
			Name:             keyVaultServicePrincipal,
			Namespace:        ns.Name,
			IdentityType:     aadpodv1.ServicePrincipal,
			IdentityName:     keyvaultIdentity,
			TenantID:         config.AzureTenantID,
			SPClientID:       config.ServicePrincipalClientID,
			SPClientPassword: corev1.SecretReference{Name: clientPasswordSecret.Name, Namespace: ns.Name},
		})

		azureIdentityBinding = azureidentitybinding.Create(azureidentitybinding.CreateInput{
			Creator:           kubeClient,
			Name:              keyvaultSPBinding,
			Namespace:         ns.Name,
			AzureIdentityName: azureIdentity.Name,
			Selector:          keyvaultSPSelector,
		})

		identityValidator = identityvalidator.Create(identityvalidator.CreateInput{
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
	})

	AfterEach(func() {
		Cleanup(CleanupInput{
			Namespace: ns,
			Getter:    kubeClient,
			Lister:    kubeClient,
			Deleter:   kubeClient,
		})
	})

	It("should pass the identity validation", func() {
		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:           kubeClient,
			Config:           config,
			KubeconfigPath:   kubeconfigPath,
			PodName:          identityValidator.Name,
			Namespace:        ns.Name,
			IdentityClientID: azureIdentity.Spec.ClientID,
		})
	})
})
