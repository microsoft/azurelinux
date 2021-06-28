// +build e2e

package azureidentitybinding

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"strings"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

const (
	apiVersion = "aadpodidentity.k8s.io/v1"
	kind       = "AzureIdentityBinding"
)

// CreateInput is the input for Create.
type CreateInput struct {
	Creator           framework.Creator
	Name              string
	Namespace         string
	AzureIdentityName string
	Selector          string
}

// Create creates an AzureIdentityBinding resource.
func Create(input CreateInput) *aadpodv1.AzureIdentityBinding {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for AzureIdentityBinding.Create")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for AzureIdentityBinding.Create")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for AzureIdentityBinding.Create")
	Expect(input.AzureIdentityName).NotTo(BeEmpty(), "input.AzureIdentityName is required for AzureIdentityBinding.Create")
	Expect(input.Selector).NotTo(BeEmpty(), "input.Selector is required for AzureIdentityBinding.Create")

	By(fmt.Sprintf("Creating AzureIdentityBinding \"%s\"", input.Name))

	azureIdentityBinding := &aadpodv1.AzureIdentityBinding{
		ObjectMeta: metav1.ObjectMeta{
			Name:      input.Name,
			Namespace: input.Namespace,
		},
		Spec: aadpodv1.AzureIdentityBindingSpec{
			AzureIdentity: input.AzureIdentityName,
			Selector:      input.Selector,
		},
	}

	Expect(input.Creator.Create(context.TODO(), azureIdentityBinding)).Should(Succeed())

	return azureIdentityBinding
}

// CreateOldInput creates an old AzureIdentityBinding resource.
// The JSON fields of old AzureIdentityBinding have their first letter capitalized, which we do not support for v1.6.0 and onward.
// However, we provide support to update existing outdated AzureIdentityBinding.
func CreateOld(input CreateInput) string {
	type azureIdentityBindingOld struct {
		APIVersion string `json:"apiVersion"`
		Kind       string `json:"kind"`
		*aadpodv1.AzureIdentityBinding
	}

	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for AzureIdentityBinding.CreateOld")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for AzureIdentityBinding.CreateOld")
	Expect(input.AzureIdentityName).NotTo(BeEmpty(), "input.AzureIdentityName is required for AzureIdentityBinding.CreateOld")
	Expect(input.Selector).NotTo(BeEmpty(), "input.Selector is required for AzureIdentityBinding.CreateOld")

	By(fmt.Sprintf("Creating old AzureIdentityBinding \"%s\"", input.Name))

	azureIdentityBinding := azureIdentityBindingOld{
		APIVersion: apiVersion,
		Kind:       kind,
		AzureIdentityBinding: &aadpodv1.AzureIdentityBinding{
			ObjectMeta: metav1.ObjectMeta{
				Name:      input.Name,
				Namespace: input.Namespace,
			},
			Spec: aadpodv1.AzureIdentityBindingSpec{
				AzureIdentity: input.AzureIdentityName,
				Selector:      input.Selector,
			},
		},
	}

	tmpFile, err := ioutil.TempFile("", "")
	Expect(err).To(BeNil())

	a, err := json.Marshal(azureIdentityBinding)
	Expect(err).To(BeNil())

	// Outdated JSON fields start with a capitalized letter
	converion := map[string]string{
		"\"azureIdentity\"": "\"AzureIdentity\"",
		"\"selector\"":      "\"Selector\"",
	}

	converted := string(a)
	for original, replacement := range converion {
		converted = strings.Replace(converted, original, replacement, -1)
	}

	_, err = tmpFile.Write([]byte(converted))
	Expect(err).To(BeNil())

	return tmpFile.Name()
}

// DeleteInput is the input for Delete.
type DeleteInput struct {
	Deleter              framework.Deleter
	AzureIdentityBinding *aadpodv1.AzureIdentityBinding
}

// Delete deletes an AzureIdentityBinding resource.
func Delete(input DeleteInput) {
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for AzureIdentityBinding.Delete")
	Expect(input.AzureIdentityBinding).NotTo(BeNil(), "input.AzureIdentityBinding is required for AzureIdentityBinding.Delete")

	By(fmt.Sprintf("Deleting AzureIdentityBinding \"%s\"", input.AzureIdentityBinding.Name))
	Expect(input.Deleter.Delete(context.TODO(), input.AzureIdentityBinding)).Should(Succeed())
}
