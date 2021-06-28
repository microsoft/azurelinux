// +build e2e

package e2e

import (
	"context"
	"fmt"
	"strings"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/exec"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/iptables"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/mic"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/pod"
	corev1 "k8s.io/api/core/v1"
	"sigs.k8s.io/controller-runtime/pkg/client"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("When liveness probe is enabled", func() {
	It("should pass liveness probe test", func() {
		pods := &corev1.PodList{}
		Expect(kubeClient.List(context.TODO(), pods, client.InNamespace(framework.NamespaceKubeSystem))).Should(Succeed())

		micPods := pod.List(pod.ListInput{
			Lister:    kubeClient,
			Namespace: framework.NamespaceKubeSystem,
			Labels: map[string]string{
				"app.kubernetes.io/component": "mic",
			},
		})

		micLeader := mic.GetLeader(mic.GetLeaderInput{
			Getter: kubeClient,
		})

		for _, micPod := range micPods.Items {
			busyboxPod, namespace := iptables.GetBusyboxPodByNode(iptables.GetBusyboxPodByNodeInput{
				NodeName: micPod.Spec.NodeName,
			})

			cmd := "clean-install wget"
			_, err := exec.KubectlExec(kubeconfigPath, busyboxPod.Name, namespace, strings.Split(cmd, " "))
			Expect(err).To(BeNil())

			cmd = fmt.Sprintf("wget http://%s:8080/healthz -q -O -", micPod.Status.PodIP)
			stdout, err := exec.KubectlExec(kubeconfigPath, busyboxPod.Name, namespace, strings.Split(cmd, " "))
			Expect(err).To(BeNil())
			if micPod.Name == micLeader.Name {
				By(fmt.Sprintf("Ensuring that %s's health probe is active", micPod.Name))
				Expect(strings.EqualFold(stdout, "Active")).To(BeTrue())
			} else {
				By(fmt.Sprintf("Ensuring that %s's health probe is not active", micPod.Name))
				Expect(strings.EqualFold(stdout, "Not Active")).To(BeTrue())
			}
		}

		nmiPods := pod.List(pod.ListInput{
			Lister:    kubeClient,
			Namespace: framework.NamespaceKubeSystem,
			Labels: map[string]string{
				"app.kubernetes.io/component": "nmi",
			},
		})

		for _, nmiPod := range nmiPods.Items {
			busyboxPod, namespace := iptables.GetBusyboxPodByNode(iptables.GetBusyboxPodByNodeInput{
				NodeName: nmiPod.Spec.NodeName,
			})

			cmd := "clean-install wget"
			_, err := exec.KubectlExec(kubeconfigPath, busyboxPod.Name, namespace, strings.Split(cmd, " "))
			Expect(err).To(BeNil())

			cmd = fmt.Sprintf("wget http://%s:8085/healthz -q -O -", nmiPod.Status.PodIP)
			stdout, err := exec.KubectlExec(kubeconfigPath, busyboxPod.Name, namespace, strings.Split(cmd, " "))
			Expect(err).To(BeNil())

			By(fmt.Sprintf("Ensuring that %s's health probe is active", nmiPod.Name))
			Expect(strings.EqualFold(stdout, "Active")).To(BeTrue())
		}
	})
})
