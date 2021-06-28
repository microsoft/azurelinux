package pod

import (
	"context"
	"fmt"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// ListInput is the input of List.
type ListInput struct {
	Lister    framework.Lister
	Namespace string
	Labels    map[string]string
}

// List returns a list of pods based on labels.
func List(input ListInput) *corev1.PodList {
	Expect(input.Lister).NotTo(BeNil(), "input.Lister is required for Pod.List")
	Expect(input.Namespace).NotTo(BeNil(), "input.Namespace is required for Pod.List")
	Expect(len(input.Labels) == 0).NotTo(BeTrue(), "input.Labels is required for Pod.List")

	By(fmt.Sprintf("Listing pods with labels %v in %s namespace", input.Labels, input.Namespace))

	pods := &corev1.PodList{}
	Expect(input.Lister.List(context.TODO(), pods, client.InNamespace(input.Namespace), client.MatchingLabels(input.Labels))).Should(Succeed())

	return pods
}
