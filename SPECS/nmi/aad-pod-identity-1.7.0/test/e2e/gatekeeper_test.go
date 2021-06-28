// +build e2e

package e2e

import (
	"io/ioutil"
	"os"
	"time"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azureidentity"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/exec"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
)

const (
	gatekeeperDeployment = "https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml"

	azureIdentityFormatTemplate = `
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: azureidentityformat
spec:
  crd:
    spec:
      names:
        kind: azureidentityformat
        listKind: azureidentityformatList
        plural: azureidentityformat
        singular: azureidentityformat
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package azureidentityformat
        violation[{"msg": msg}] {
         input.review.kind.kind == "AzureIdentity"
         # format of resourceId is checked only for user-assigned MSI
         input.review.object.spec.type == 0
         resourceId := input.review.object.spec.resourceID
         result := re_match(` + "`" + `(?i)/subscriptions/(.+?)/resourcegroups/(.+?)/providers/Microsoft.ManagedIdentity/(.+?)/(.+)` + "`" + `,resourceId)
         result == false
         msg := sprintf(` + "`" + `The identity resourceId '%v' is invalid.It must be of the following format: '/subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>'` + "`" + `,[resourceId])
         }`

	azureIdentityConstraint = `
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: azureidentityformat
metadata:
  name: azureidentityformatconstraint
spec:
  match:
    kinds:
      - apiGroups: ["aadpodidentity.k8s.io"]
        kinds: ["AzureIdentity"]`
)

var _ = Describe("When using AAD Pod Identity with Gatekeeper", func() {
	var (
		specName                        = "gatekeeper"
		ns                              *corev1.Namespace
		azureIdentityFormatTemplateFile *os.File
		azureIdentityConstraintFile     *os.File
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

	It("should pass the identity format validation with gatekeeper constraint", func() {
		By("Deploying gatekeeper")
		err := exec.KubectlApply(kubeconfigPath, "gatekeeper-system", []string{"-f", gatekeeperDeployment})
		Expect(err).To(BeNil())
		defer func() {
			err := exec.KubectlDelete(kubeconfigPath, "gatekeeper-system", []string{"-f", gatekeeperDeployment})
			Expect(err).To(BeNil())
		}()

		By("Applying AzureIdentity gatekeeper format")
		azureIdentityFormatTemplateFile, err = ioutil.TempFile("", "")
		Expect(err).To(BeNil())
		defer os.Remove(azureIdentityFormatTemplateFile.Name())

		_, err = azureIdentityFormatTemplateFile.Write([]byte(azureIdentityFormatTemplate))
		Expect(err).To(BeNil())

		err = exec.KubectlApply(kubeconfigPath, ns.Name, []string{"-f", azureIdentityFormatTemplateFile.Name()})
		Expect(err).To(BeNil())
		defer func() {
			err := exec.KubectlDelete(kubeconfigPath, ns.Name, []string{"-f", azureIdentityFormatTemplateFile.Name()})
			Expect(err).To(BeNil())
		}()

		// constraint template takes time to init to handle request, leading to failure
		// added to make reliable, can be converted to deterministic sleep by retrying after GET on expected resource
		time.Sleep(60 * time.Second)

		By("Applying AzureIdentity gatekeeper constraint")
		azureIdentityConstraintFile, err = ioutil.TempFile("", "")
		Expect(err).To(BeNil())
		defer os.Remove(azureIdentityConstraintFile.Name())

		_, err = azureIdentityConstraintFile.Write([]byte(azureIdentityConstraint))
		Expect(err).To(BeNil())

		err = exec.KubectlApply(kubeconfigPath, ns.Name, []string{"-f", azureIdentityConstraintFile.Name()})
		Expect(err).To(BeNil())
		defer func() {
			err := exec.KubectlDelete(kubeconfigPath, ns.Name, []string{"-f", azureIdentityConstraintFile.Name()})
			Expect(err).To(BeNil())
		}()

		// constraint takes time to init
		time.Sleep(60 * time.Second)

		By("Creating an AzureIdentity with invalid ResourceID and ensuring an error has occurred")
		azureidentity.Create(azureidentity.CreateInput{
			Creator:           kubeClient,
			Config:            config,
			AzureClient:       azureClient,
			Name:              "invalid-identity",
			Namespace:         ns.Name,
			IdentityType:      aadpodv1.UserAssignedMSI,
			IdentityName:      keyvaultIdentity,
			InvalidResourceID: true,
		})

		By("Creating an AzureIdentity with valid ResourceID and ensuring no error has occurred")
		azureidentity.Create(azureidentity.CreateInput{
			Creator:      kubeClient,
			Config:       config,
			AzureClient:  azureClient,
			Name:         "valid-identity",
			Namespace:    ns.Name,
			IdentityType: aadpodv1.UserAssignedMSI,
			IdentityName: keyvaultIdentity,
		})
	})
})
