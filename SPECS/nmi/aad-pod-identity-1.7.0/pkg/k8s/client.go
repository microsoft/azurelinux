package k8s

import (
	"context"
	"fmt"
	"net"
	"os"
	"strings"
	"time"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	crd "github.com/Azure/aad-pod-identity/pkg/crd"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/version"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	informersv1 "k8s.io/client-go/informers/core/v1"
	"k8s.io/client-go/informers/internalinterfaces"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/klog/v2"
)

const (
	getPodListRetries               = 4
	getPodListSleepTimeMilliseconds = 300
)

// Client api client
type Client interface {
	// Start just starts any informers required.
	Start(<-chan struct{})
	// GetPod returns the pod object based on name and namespce
	GetPod(namespace, name string) (v1.Pod, error)
	// GetPodInfo returns the pod name, namespace & replica set name for a given pod ip
	GetPodInfo(podip string) (podns, podname, rsName string, selectors *metav1.LabelSelector, err error)
	// ListPodIds pod matching azure identity or nil
	ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error)
	// ListPodIdsWithBinding pod matching azure identity or nil
	ListPodIdsWithBinding(podns string, labels map[string]string) ([]aadpodid.AzureIdentity, error)
	// GetSecret returns secret the secretRef represents
	GetSecret(secretRef *v1.SecretReference) (*v1.Secret, error)
	// ListPodIdentityExceptions returns list of azurepodidentityexceptions
	ListPodIdentityExceptions(namespace string) (*[]aadpodid.AzurePodIdentityException, error)
}

// KubeClient k8s client
type KubeClient struct {
	// Main Kubernetes client
	ClientSet kubernetes.Interface
	// Crd client used to access our CRD resources.
	CrdClient   *crd.Client
	PodInformer cache.SharedIndexInformer
	reporter    *metrics.Reporter
}

// NewKubeClient new kubernetes api client
func NewKubeClient(nodeName string, scale, isStandardMode bool) (Client, error) {
	config, err := buildConfig()
	if err != nil {
		return nil, err
	}
	config.UserAgent = version.GetUserAgent("NMI", version.NMIVersion)
	clientset, err := getkubeclient(config)
	if err != nil {
		return nil, err
	}
	crdclient, err := crd.NewCRDClientLite(config, nodeName, scale, isStandardMode)
	if err != nil {
		return nil, err
	}
	reporter, err := metrics.NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}

	podInformer := informersv1.NewFilteredPodInformer(clientset, v1.NamespaceAll, 10*time.Minute,
		cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc},
		NodeNameFilter(nodeName))

	kubeClient := &KubeClient{
		CrdClient:   crdclient,
		ClientSet:   clientset,
		PodInformer: podInformer,
		reporter:    reporter,
	}

	return kubeClient, nil
}

// Sync syncs the cache from the K8s client.
func (c *KubeClient) Sync(exit <-chan struct{}) {
	if !cache.WaitForCacheSync(exit, c.PodInformer.HasSynced) {
		klog.Error("pod cache could not be synchronized")
	}
}

// Start the corresponding starts
func (c *KubeClient) Start(exit <-chan struct{}) {
	go c.PodInformer.Run(exit)
	c.CrdClient.StartLite(exit)
	c.Sync(exit)
}

func (c *KubeClient) getReplicasetName(pod v1.Pod) string {
	for _, owner := range pod.OwnerReferences {
		if strings.EqualFold(owner.Kind, "ReplicaSet") {
			return owner.Name
		}
	}
	return ""
}

// NodeNameFilter will tweak the options to include the node name as field
// selector.
func NodeNameFilter(nodeName string) internalinterfaces.TweakListOptionsFunc {
	return func(l *metav1.ListOptions) {
		if l == nil {
			l = &metav1.ListOptions{}
		}
		l.FieldSelector = l.FieldSelector + "spec.nodeName=" + nodeName
	}
}

// GetPod returns pod that matches namespace and name
func (c *KubeClient) GetPod(namespace, name string) (v1.Pod, error) {
	// TODO (aramase) wrap this with retries
	obj, exists, err := c.PodInformer.GetIndexer().GetByKey(namespace + "/" + name)
	if err != nil {
		return v1.Pod{}, fmt.Errorf("failed to get pod %s/%s, error: %+v", namespace, name, err)
	}
	if !exists {
		return v1.Pod{}, fmt.Errorf("pod %s/%s doesn't exist", namespace, name)
	}
	pod, ok := obj.(*v1.Pod)
	if !ok {
		return v1.Pod{}, fmt.Errorf("could not cast %T to v1.Pod", pod)
	}
	return *pod, nil
}

// GetPodInfo get pod ns,name from apiserver
func (c *KubeClient) GetPodInfo(podip string) (podns, poddname, rsName string, labels *metav1.LabelSelector, err error) {
	if podip == "" {
		return "", "", "", nil, fmt.Errorf("pod IP is empty")
	}

	podList, err := c.getPodListRetry(podip, getPodListRetries, getPodListSleepTimeMilliseconds)

	if err != nil {
		return "", "", "", nil, err
	}
	numMatching := len(podList)
	if numMatching == 1 {
		return podList[0].Namespace, podList[0].Name, c.getReplicasetName(*podList[0]), &metav1.LabelSelector{
			MatchLabels: podList[0].Labels}, nil
	}

	return "", "", "", nil, fmt.Errorf("failed to match pod IP %s with %v", podip, podList)
}

func isPhaseValid(p v1.PodPhase) bool {
	return p == v1.PodPending || p == v1.PodRunning
}

func (c *KubeClient) getPodList(podip string) ([]*v1.Pod, error) {
	var podList []*v1.Pod
	list := c.PodInformer.GetStore().List()
	for _, o := range list {
		pod, ok := o.(*v1.Pod)
		if !ok {
			err := fmt.Errorf("could not cast %T to v1.Pod", pod)
			return nil, err
		}
		if pod.Status.PodIP == podip && isPhaseValid(pod.Status.Phase) {
			podList = append(podList, pod)
		}
	}
	if len(podList) == 0 {
		return nil, fmt.Errorf("pod list is empty")
	}
	return podList, nil
}

func (c *KubeClient) getPodListRetry(podip string, retries int, sleeptime time.Duration) ([]*v1.Pod, error) {
	var podList []*v1.Pod
	var err error
	i := 0

	for {
		// Atleast run the getpodlist once.
		podList, err = c.getPodList(podip)
		if err == nil {
			return podList, nil
		}
		metricErr := c.reporter.ReportKubernetesAPIOperationError(metrics.GetPodListOperationName)
		if metricErr != nil {
			klog.Warningf("failed to report metrics, error: %+v", metricErr)
		}

		if i >= retries {
			break
		}
		i++
		klog.Warningf("list pod error: %+v. Retrying, attempt number: %d", err, i)
		time.Sleep(sleeptime * time.Millisecond)
	}
	// We reach here only if there is an error and we have exhausted all retries.
	// Return the last error
	return nil, err
}

// GetLocalIP returns the non loopback local IP of the host
func GetLocalIP() (string, error) {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return "", err
	}
	for _, address := range addrs {
		// check the address type and if it is not a loopback
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				return ipnet.IP.String(), nil
			}
		}
	}
	return "", fmt.Errorf("non loopback IP address not found")
}

// ListPodIds lists matching ids for pod or error
func (c *KubeClient) ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error) {
	return c.CrdClient.ListPodIds(podns, podname)
}

// ListPodIdsWithBinding list matching ids for pod based on the bindings
func (c *KubeClient) ListPodIdsWithBinding(podns string, labels map[string]string) ([]aadpodid.AzureIdentity, error) {
	return c.CrdClient.GetPodIDsWithBinding(podns, labels)
}

// ListPodIdentityExceptions lists azurepodidentityexceptions
func (c *KubeClient) ListPodIdentityExceptions(ns string) (*[]aadpodid.AzurePodIdentityException, error) {
	return c.CrdClient.ListPodIdentityExceptions(ns)
}

// GetSecret returns secret the secretRef represents
func (c *KubeClient) GetSecret(secretRef *v1.SecretReference) (*v1.Secret, error) {
	secret, err := c.ClientSet.CoreV1().Secrets(secretRef.Namespace).Get(context.TODO(), secretRef.Name, metav1.GetOptions{})
	if err != nil {
		merr := c.reporter.ReportKubernetesAPIOperationError(metrics.GetSecretOperationName)
		if merr != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
		return nil, err
	}
	return secret, nil
}

func getkubeclient(config *rest.Config) (*kubernetes.Clientset, error) {
	// creates the clientset
	kubeClient, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, err
	}

	return kubeClient, err
}

// Create the client config. Use kubeconfig if given, otherwise assume in-cluster.
func buildConfig() (*rest.Config, error) {
	kubeconfigPath := os.Getenv("KUBECONFIG")
	if kubeconfigPath != "" {
		return clientcmd.BuildConfigFromFlags("", kubeconfigPath)
	}

	return rest.InClusterConfig()
}
