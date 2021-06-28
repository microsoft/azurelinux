// +build e2e

package e2e

import (
	"fmt"
	"os"
	"time"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentitybinding"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/exec"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/helm"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/identityvalidator"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	corev1 "k8s.io/api/core/v1"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("When upgrading AAD Pod Identity", func() {
	var (
		specName                 = "backward-compat"
		ns                       *corev1.Namespace
		keyvaultIdentityBinding  = fmt.Sprintf("%s-binding", keyvaultIdentity)
		keyvaultIdentitySelector = fmt.Sprintf("%s-selector", keyvaultIdentity)
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

	It("should be backward compatible with old and new version of MIC and NMI", func() {
		By("Deleting the ConfigMap used to store upgrade information")
		err := exec.KubectlDelete(kubeconfigPath, framework.NamespaceKubeSystem, []string{
			"--ignore-not-found",
			"cm",
			"aad-pod-identity-config",
			fmt.Sprintf("--namespace=%s", framework.NamespaceKubeSystem),
		})
		Expect(err).To(BeNil())

		configOldVersion := config.DeepCopy()
		configOldVersion.Registry = "mcr.microsoft.com/k8s/aad-pod-identity"
		configOldVersion.MICVersion = "1.5"
		configOldVersion.NMIVersion = "1.5"
		configOldVersion.ImmutableUserMSIs = ""
		configOldVersion.IdentityReconcileInterval = 0
		configOldVersion.BlockInstanceMetadata = false

		helm.Upgrade(helm.UpgradeInput{
			Config: configOldVersion,
		})

		azureIdentityFile, identityClientID := azureidentity.CreateOld(azureidentity.CreateInput{
			Config:       config,
			AzureClient:  azureClient,
			Name:         keyvaultIdentity,
			Namespace:    ns.Name,
			IdentityType: aadpodv1.UserAssignedMSI,
			IdentityName: keyvaultIdentity,
		})
		defer os.Remove(azureIdentityFile)

		err = exec.KubectlApply(kubeconfigPath, ns.Name, []string{"-f", azureIdentityFile})
		Expect(err).To(BeNil())

		azureIdentityBindingFile := azureidentitybinding.CreateOld(azureidentitybinding.CreateInput{
			Name:              keyvaultIdentityBinding,
			Namespace:         ns.Name,
			AzureIdentityName: keyvaultIdentity,
			Selector:          keyvaultIdentitySelector,
		})
		defer os.Remove(azureIdentityBindingFile)

		err = exec.KubectlApply(kubeconfigPath, ns.Name, []string{"-f", azureIdentityBindingFile})
		Expect(err).To(BeNil())

		identityValidator := identityvalidator.Create(identityvalidator.CreateInput{
			Creator:         kubeClient,
			Config:          config,
			Namespace:       ns.Name,
			IdentityBinding: keyvaultIdentitySelector,
		})

		// We won't be able to wait for AzureAssignedIdentity to be Assigned
		// due to change in JSON fields introduced in #398
		// So wait for 60 seconds, which is enough for an identity to be assigned to a VMAS & VMSS node
		By("Waiting for the identity to get assigned to the node")
		time.Sleep(60 * time.Second)

		identityvalidator.Validate(identityvalidator.ValidateInput{
			Getter:           kubeClient,
			Config:           config,
			KubeconfigPath:   kubeconfigPath,
			PodName:          identityValidator.Name,
			Namespace:        ns.Name,
			IdentityClientID: identityClientID,
		})

		helm.Upgrade(helm.UpgradeInput{
			Config: config,
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
