// +build e2e

package e2e

import (
	"fmt"
	"testing"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/azure"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/exec"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/helm"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/iptables"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/namespace"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/pod"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

const (
	keyvaultIdentity         = "keyvault-identity"
	clusterIdentity          = "cluster-identity"
	keyVaultServicePrincipal = "keyvault-sp"
)

var (
	clusterProxy      framework.ClusterProxy
	config            *framework.Config
	azureClient       azure.Client
	kubeClient        client.Client
	kubeconfigPath    string
	iptablesNamespace *corev1.Namespace
)

func TestE2E(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "aadpodidentity")
}

var _ = BeforeSuite(func() {
	By("Parsing test configuration")
	var err error
	config, err = framework.ParseConfig()
	Expect(err).To(BeNil())

	By("Creating a Cluster Proxy")
	clusterProxy = framework.NewClusterProxy(initScheme())

	By("Creating an Azure Client")
	azureClient = azure.NewClient(config)

	if !config.IsSoakTest {
		By("Installing AAD Pod Identity via Helm")
		helm.Install(helm.InstallInput{
			Config: config,
		})
	}

	kubeClient = clusterProxy.GetClient()
	kubeconfigPath = clusterProxy.GetKubeconfigPath()

	iptablesNamespace = namespace.Create(namespace.CreateInput{
		Creator: kubeClient,
		Name:    "iptables",
	})

	iptables.WaitForRules(iptables.WaitForRulesInput{
		Creator:         kubeClient,
		Getter:          kubeClient,
		Lister:          kubeClient,
		Namespace:       iptablesNamespace.Name,
		KubeconfigPath:  clusterProxy.GetKubeconfigPath(),
		CreateDaemonSet: true,
		ShouldExist:     true,
	})
})

var _ = AfterSuite(func() {
	defer namespace.Delete(namespace.DeleteInput{
		Deleter:   kubeClient,
		Getter:    kubeClient,
		Namespace: iptablesNamespace,
	})

	defer func() {
		if !config.IsSoakTest {
			By("Uninstalling AAD Pod Identity via Helm")
			helm.Uninstall()

			iptables.WaitForRules(iptables.WaitForRulesInput{
				Creator:         kubeClient,
				Getter:          kubeClient,
				Lister:          kubeClient,
				Namespace:       iptablesNamespace.Name,
				KubeconfigPath:  clusterProxy.GetKubeconfigPath(),
				CreateDaemonSet: false,
				ShouldExist:     false,
			})
		}
	}()

	dumpLogs()
})

func initScheme() *runtime.Scheme {
	scheme := runtime.NewScheme()
	framework.TryAddDefaultSchemes(scheme)
	return scheme
}

func dumpLogs() {
	for _, component := range []string{"mic", "nmi"} {
		podList := pod.List(pod.ListInput{
			Lister:    kubeClient,
			Namespace: framework.NamespaceKubeSystem,
			Labels: map[string]string{
				"app.kubernetes.io/component": component,
			},
		})

		for _, pod := range podList.Items {
			By(fmt.Sprintf("Dumping logs for %s scheduled to %s", pod.Name, pod.Spec.NodeName))
			_, err := exec.KubectlLogs(kubeconfigPath, pod.Name, framework.NamespaceKubeSystem)
			Expect(err).To(BeNil())
		}
	}
}
