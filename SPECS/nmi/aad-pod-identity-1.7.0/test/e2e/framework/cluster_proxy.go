// +build e2e

package framework

import (
	. "github.com/onsi/gomega"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// ClusterProxy defines the behavior of a type that acts as an intermediary with an existing Kubernetes cluster.
// It should work with any Kubernetes cluster, no matter if the Cluster was created by a bootstrap.ClusterProvider,
// by Cluster API (a workload cluster or a self-hosted cluster) or else.
type ClusterProxy interface {
	// GetClient returns a controller-runtime client to the Kubernetes cluster.
	GetClient() client.Client

	// GetClientSet returns a client-go client to the Kubernetes cluster.
	GetClientSet() *kubernetes.Clientset

	// GetKubeconfigPath returns the path to the kubeconfig file for the cluster.
	GetKubeconfigPath() string
}

type clusterProxy struct {
	kubeconfigPath string
	scheme         *runtime.Scheme
}

// NewClusterProxy returns a clusterProxy given a KubeconfigPath and the scheme defining the types hosted in the cluster.
// If a kubeconfig file isn't provided, standard kubeconfig locations will be used (kubectl loading rules apply).
func NewClusterProxy(scheme *runtime.Scheme) ClusterProxy {
	Expect(scheme).NotTo(BeNil(), "scheme is required for NewClusterProxy")

	return &clusterProxy{
		kubeconfigPath: clientcmd.NewDefaultClientConfigLoadingRules().GetDefaultFilename(),
		scheme:         scheme,
	}
}

// GetClient returns a controller-runtime client for the cluster.
func (p *clusterProxy) GetClient() client.Client {
	restConfig := p.getRestConfig()

	c, err := client.New(restConfig, client.Options{Scheme: p.scheme})
	Expect(err).ToNot(HaveOccurred(), "Failed to get controller-runtime client")

	return c
}

// GetClientSet returns a client-go client for the cluster.
func (p *clusterProxy) GetClientSet() *kubernetes.Clientset {
	restConfig := p.getRestConfig()

	cs, err := kubernetes.NewForConfig(restConfig)
	Expect(err).ToNot(HaveOccurred(), "Failed to get client-go client")

	return cs
}

// GetKubeconfigPath returns the path to the kubeconfig file for the cluster.
func (p *clusterProxy) GetKubeconfigPath() string {
	return p.kubeconfigPath
}

func (p *clusterProxy) getRestConfig() *rest.Config {
	config, err := clientcmd.LoadFromFile(p.kubeconfigPath)
	Expect(err).ToNot(HaveOccurred(), "Failed to load Kubeconfig file from %q", p.kubeconfigPath)

	restConfig, err := clientcmd.NewDefaultClientConfig(*config, &clientcmd.ConfigOverrides{}).ClientConfig()
	Expect(err).ToNot(HaveOccurred(), "Failed to get ClientConfig from %q", p.kubeconfigPath)

	restConfig.UserAgent = "aadpodidentity"
	return restConfig
}
