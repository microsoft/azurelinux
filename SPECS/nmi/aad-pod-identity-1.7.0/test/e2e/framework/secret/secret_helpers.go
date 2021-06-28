// +build e2e

package secret

import (
	"context"
	"fmt"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// CreateInput is the input for Create.
type CreateInput struct {
	Creator      framework.Creator
	Config       *framework.Config
	Name         string
	Namespace    string
	ClientSecret string
}

// Create creates a Secret resource.
func Create(input CreateInput) *corev1.Secret {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for Secret.Create")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for Secret.Create")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for Secret.Create")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for Secret.Create")
	Expect(input.ClientSecret).NotTo(BeEmpty(), "input.ClientSecret is required for Secret.Create")

	By(fmt.Sprintf("Creating Secret \"%s\"", input.Name))

	secret := &corev1.Secret{
		ObjectMeta: metav1.ObjectMeta{
			Name:      input.Name,
			Namespace: input.Namespace,
		},
		Type: corev1.SecretTypeOpaque,
		Data: map[string][]byte{"clientSecret": []byte(input.ClientSecret)},
	}

	Expect(input.Creator.Create(context.TODO(), secret)).Should(Succeed())
	return secret
}

// DeleteInput is the input for Delete.
type DeleteInput struct {
	Deleter framework.Deleter
	Secret  *corev1.Secret
}

// Delete deletes a Secret resource.
func Delete(input DeleteInput) {
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for Secret.Delete")
	Expect(input.Secret).NotTo(BeNil(), "input.AzureIdentity is required for Secret.Delete")

	By(fmt.Sprintf("Deleting Secret \"%s\"", input.Secret.Name))
	Expect(input.Deleter.Delete(context.TODO(), input.Secret)).Should(Succeed())
}
