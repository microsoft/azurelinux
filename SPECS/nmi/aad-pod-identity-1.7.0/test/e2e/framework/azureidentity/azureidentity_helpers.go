// +build e2e

package azureidentity

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"strings"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azure"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

const (
	invalidResourceIDTemplate = "/subscriptions/%s/providers/Microsoft.ManagedIdentity/userAssignedIdentities/%s"

	apiVersion = "aadpodidentity.k8s.io/v1"
	kind       = "AzureIdentity"
)

// CreateInput is the input for Create and CreateOld.
type CreateInput struct {
	Creator           framework.Creator
	Config            *framework.Config
	AzureClient       azure.Client
	Name              string
	Namespace         string
	IdentityName      string
	IdentityType      aadpodv1.IdentityType
	InvalidResourceID bool
	TenantID          string
	SPClientID        string
	SPClientPassword  corev1.SecretReference
}

// Create creates an AzureIdentity resource.
func Create(input CreateInput) *aadpodv1.AzureIdentity {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for AzureIdentity.Create")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for AzureIdentity.Create")
	Expect(input.AzureClient).NotTo(BeNil(), "input.AzureClient is required for AzureIdentity.Create")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for AzureIdentity.Create")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for AzureIdentity.Create")
	Expect(input.IdentityName).NotTo(BeEmpty(), "input.IdentityName is required for AzureIdentity.Create")
	Expect(input.IdentityType).NotTo(BeNil(), "input.IdentityType is required for AzureIdentity.Create")

	By(fmt.Sprintf("Creating AzureIdentity \"%s\"", input.Name))

	identityClientID := input.AzureClient.GetIdentityClientID(input.IdentityName)
	azureIdentity := &aadpodv1.AzureIdentity{
		ObjectMeta: metav1.ObjectMeta{
			Name:      input.Name,
			Namespace: input.Namespace,
		},
	}

	if input.IdentityType == aadpodv1.UserAssignedMSI {
		azureIdentity.Spec = aadpodv1.AzureIdentitySpec{
			Type:       input.IdentityType,
			ResourceID: fmt.Sprintf(azure.ResourceIDTemplate, input.Config.SubscriptionID, input.Config.IdentityResourceGroup, input.IdentityName),
			ClientID:   identityClientID,
		}
	} else {
		azureIdentity.Spec = aadpodv1.AzureIdentitySpec{
			Type:           input.IdentityType,
			ClientID:       input.SPClientID,
			TenantID:       input.TenantID,
			ClientPassword: input.SPClientPassword,
		}
	}

	// For gatekeeper test case
	if input.InvalidResourceID {
		azureIdentity.Spec.ResourceID = fmt.Sprintf(invalidResourceIDTemplate, input.Config.SubscriptionID, input.IdentityName)
		Expect(input.Creator.Create(context.TODO(), azureIdentity)).ShouldNot(Succeed())
	} else {
		Expect(input.Creator.Create(context.TODO(), azureIdentity)).Should(Succeed())
	}

	return azureIdentity
}

// CreateOldInput creates an old AzureIdentity resource.
// The JSON fields of old AzureIdentity have their first letter capitalized, which we do not support for v1.6.0 and onward.
// However, we provide support to update existing outdated AzureIdentity.
func CreateOld(input CreateInput) (string, string) {
	type azureIdentityOld struct {
		APIVersion string `json:"apiVersion"`
		Kind       string `json:"kind"`
		*aadpodv1.AzureIdentity
	}

	Expect(input.Config).NotTo(BeNil(), "input.Config is required for AzureIdentity.CreateOld")
	Expect(input.AzureClient).NotTo(BeNil(), "input.AzureClient is required for AzureIdentity.CreateOld")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for AzureIdentity.CreateOld")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for AzureIdentity.CreateOld")
	Expect(input.IdentityName).NotTo(BeEmpty(), "input.IdentityName is required for AzureIdentity.CreateOld")
	Expect(input.IdentityType).NotTo(BeNil(), "input.IdentityType is required for AzureIdentity.CreateOld")

	By(fmt.Sprintf("Creating old AzureIdentity \"%s\"", input.Name))

	identityClientID := input.AzureClient.GetIdentityClientID(input.IdentityName)
	azureIdentity := azureIdentityOld{
		APIVersion: apiVersion,
		Kind:       kind,
		AzureIdentity: &aadpodv1.AzureIdentity{
			ObjectMeta: metav1.ObjectMeta{
				Name:      input.Name,
				Namespace: input.Namespace,
			},
			Spec: aadpodv1.AzureIdentitySpec{
				Type:       input.IdentityType,
				ResourceID: fmt.Sprintf(azure.ResourceIDTemplate, input.Config.SubscriptionID, input.Config.IdentityResourceGroup, input.IdentityName),
				ClientID:   identityClientID,
			},
		},
	}

	tmpFile, err := ioutil.TempFile("", "")
	Expect(err).To(BeNil())

	a, err := json.Marshal(azureIdentity)
	Expect(err).To(BeNil())

	// Outdated JSON fields start with a capitalized letter
	converion := map[string]string{
		"\"clientID\"":   "\"ClientID\"",
		"\"resourceID\"": "\"ResourceID\"",
	}

	converted := string(a)
	for original, replacement := range converion {
		converted = strings.Replace(converted, original, replacement, -1)
	}

	_, err = tmpFile.Write([]byte(converted))
	Expect(err).To(BeNil())

	return tmpFile.Name(), identityClientID
}

// UpdateInput is the input for Update.
type UpdateInput struct {
	Updater             framework.Updater
	Config              *framework.Config
	AzureClient         azure.Client
	AzureIdentity       *aadpodv1.AzureIdentity
	UpdatedIdentityName string
}

// Update updates an AzureIdentity resource.
func Update(input UpdateInput) *aadpodv1.AzureIdentity {
	Expect(input.Updater).NotTo(BeNil(), "input.Updater is required for AzureIdentity.Update")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for AzureIdentity.Update")
	Expect(input.AzureClient).NotTo(BeNil(), "input.AzureClient is required for AzureIdentity.Update")
	Expect(input.AzureIdentity).NotTo(BeNil(), "input.AzureIdentity is required for AzureIdentity.Update")
	Expect(input.UpdatedIdentityName).NotTo(BeEmpty(), "input.UpdatedIdentityName is required for AzureIdentity.Update")

	By(fmt.Sprintf("Updating AzureIdentity \"%s\" to use \"%s\"", input.AzureIdentity.Name, input.UpdatedIdentityName))

	identityClientID := input.AzureClient.GetIdentityClientID(input.UpdatedIdentityName)
	Expect(identityClientID).NotTo(BeEmpty(), "identityClientID is required for AzureIdentity.Update")

	input.AzureIdentity.Spec.ClientID = identityClientID
	input.AzureIdentity.Spec.ResourceID = fmt.Sprintf(azure.ResourceIDTemplate, input.Config.SubscriptionID, input.Config.IdentityResourceGroup, input.UpdatedIdentityName)

	Expect(input.Updater.Update(context.TODO(), input.AzureIdentity)).Should(Succeed())

	return input.AzureIdentity
}

// DeleteInput is the input for Delete.
type DeleteInput struct {
	Deleter       framework.Deleter
	AzureIdentity *aadpodv1.AzureIdentity
}

// Delete deletes an AzureIdentity resource.
func Delete(input DeleteInput) {
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for AzureIdentity.Delete")
	Expect(input.AzureIdentity).NotTo(BeNil(), "input.AzureIdentity is required for AzureIdentity.Delete")

	By(fmt.Sprintf("Deleting AzureIdentity \"%s\"", input.AzureIdentity.Name))
	Expect(input.Deleter.Delete(context.TODO(), input.AzureIdentity)).Should(Succeed())
}
