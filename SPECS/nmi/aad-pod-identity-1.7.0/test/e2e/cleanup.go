package e2e

import (
	"context"
	"fmt"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// CleanupInput is the input for Cleanup.
type CleanupInput struct {
	Namespace *corev1.Namespace
	Getter    framework.Getter
	Lister    framework.Lister
	Deleter   framework.Deleter
}

// Cleanup cleans up the test environment after a test case is finished running.
func Cleanup(input CleanupInput) {
	Expect(input.Namespace).NotTo(BeNil(), "input.Namespace is required for e2e.Cleanup")
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for e2e.Cleanup")
	Expect(input.Lister).NotTo(BeNil(), "input.Lister is required for e2e.Cleanup")
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for e2e.Cleanup")

	By(fmt.Sprintf("Deleting all pods in namespace \"%s\"", input.Namespace.Name))

	podList := &corev1.PodList{}
	Expect(input.Lister.List(context.TODO(), podList, client.InNamespace(input.Namespace.Name))).Should(Succeed())
	for _, pod := range podList.Items {
		pod := pod // avoid implicit memory aliasing in for loop
		Expect(input.Deleter.Delete(context.TODO(), &pod)).Should(Succeed())
	}

	Eventually(func() bool {
		podList := &corev1.PodList{}
		Expect(input.Lister.List(context.TODO(), podList, client.InNamespace(input.Namespace.Name))).Should(Succeed())
		return len(podList.Items) == 0
	}, framework.Timeout, framework.Polling).Should(BeTrue())

	namespace.Delete(namespace.DeleteInput{
		Deleter:   input.Deleter,
		Getter:    input.Getter,
		Namespace: input.Namespace,
	})
}
