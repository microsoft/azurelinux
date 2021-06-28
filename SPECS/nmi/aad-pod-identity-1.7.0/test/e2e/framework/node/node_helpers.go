// +build e2e

package node

import (
	"context"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
)

// ListInput is the input for List.
type ListInput struct {
	Lister framework.Lister
}

// List lists all nodes in the cluster
func List(input ListInput) *corev1.NodeList {
	Expect(input.Lister).NotTo(BeNil(), "input.Lister is required for Node.List")

	nodes := &corev1.NodeList{}
	Expect(input.Lister.List(context.TODO(), nodes)).Should(Succeed())

	return nodes
}
