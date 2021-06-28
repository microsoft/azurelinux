// +build e2e

package e2e

import (
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azurepodidentityexception"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/identityvalidator"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/node"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
)

var _ = Describe("When deploying AzurePodIdentityException", func() {
	var (
		specName = "identity-exception"
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

	It("should pass validation by bypassing NMI using AzurePodIdentityException CRD", func() {
		nodes := node.List(node.ListInput{
			Lister: kubeClient,
		})

		// Schedule identity-validator to this node
		node := nodes.Items[0]

		err := azureClient.AssignUserAssignedIdentity(node.Spec.ProviderID, keyvaultIdentity)
		Expect(err).To(BeNil())
		err = azureClient.EnableSystemAssignedIdentity(node.Spec.ProviderID)
		Expect(err).To(BeNil())
		defer func() {
			err := azureClient.UnassignUserAssignedIdentity(node.Spec.ProviderID, keyvaultIdentity)
			Expect(err).To(BeNil())
			err = azureClient.DisableSystemAssignedIdentity(node.Spec.ProviderID)
			Expect(err).To(BeNil())
		}()

		podLabels := map[string]string{
			"thispod": "shouldexcept",
		}

		azurepodidentityexception.Create(azurepodidentityexception.CreateInput{
			Creator:   kubeClient,
			Name:      "identity-exception",
			Namespace: ns.Name,
			PodLabels: podLabels,
		})

		identityClientID := azureClient.GetIdentityClientID(keyvaultIdentity)
		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:   kubeClient,
			Config:    config,
			Namespace: ns.Name,
			PodLabels: podLabels,
			NodeName:  node.Name,
		})

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:           kubeClient,
			Config:           config,
			KubeconfigPath:   kubeconfigPath,
			PodName:          identityValidator.Name,
			Namespace:        ns.Name,
			IdentityClientID: identityClientID,
		})
	})
})
