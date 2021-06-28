// +build e2e

package namespace

import (
	"context"
	"fmt"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"sigs.k8s.io/controller-runtime/pkg/client"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// CreateInput is the input for Create.
type CreateInput struct {
	Creator framework.Creator
	Name    string
}

// Create creates a namespace.
func Create(input CreateInput) *corev1.Namespace {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for Namespace.Create")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for Namespace.Create")

	ns := &corev1.Namespace{
		ObjectMeta: metav1.ObjectMeta{
			GenerateName: fmt.Sprintf("%s-", input.Name),
		},
	}

	Expect(input.Creator.Create(context.TODO(), ns)).Should(Succeed())
	By(fmt.Sprintf("Creating namespace \"%s\"", ns.Name))

	return ns
}

// DeleteInput is the input for Delete.
type DeleteInput struct {
	Deleter   framework.Deleter
	Getter    framework.Getter
	Namespace *corev1.Namespace
}

// Delete deletes a namespace.
func Delete(input DeleteInput) {
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for Namespace.Delete")
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for Namespace.Delete")
	Expect(input.Namespace).NotTo(BeNil(), "input.Namespace is required for Namespace.Delete")

	By(fmt.Sprintf("Deleting namespace \"%s\"", input.Namespace.Name))
	Expect(input.Deleter.Delete(context.TODO(), input.Namespace)).Should(Succeed())

	Eventually(func() bool {
		return input.Getter.Get(context.TODO(), client.ObjectKey{Name: input.Namespace.Name}, &corev1.Namespace{}) != nil
	}, framework.Timeout, framework.Polling).Should(BeTrue())
}
