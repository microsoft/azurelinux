package main

import (
	"encoding/json"
	"flag"
	"os"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	"github.com/Azure/aad-pod-identity/pkg/crd"
	"github.com/Azure/aad-pod-identity/version"

	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/klog/v2"
)

var (
	kubeconfig string
)

func main() {
	defer klog.Flush()
	flag.StringVar(&kubeconfig, "kubeconfig", "", "Path to the kube config")

	_ = flag.Set("logtostderr", "true")
	_ = flag.Set("v", "10")

	flag.Parse()

	klog.V(2).Infof("starting simple process. Version: %v. Build date: %v", version.MICVersion, version.BuildDate)
	if kubeconfig == "" {
		klog.Warningf("--kubeconfig not passed will use InClusterConfig")
	}

	klog.V(2).Infof("kubeconfig (%s)", kubeconfig)
	config, err := buildConfig(kubeconfig)
	if err != nil {
		klog.Fatalf("failed to build config from %s, error: %+v", kubeconfig, err)
	}

	eventCh := make(chan aadpodid.EventType, 100)
	crdClient, err := crd.NewCRDClient(config, eventCh)
	if err != nil {
		klog.Fatalf("%+v", err)
	}

	// Starts the leader election loop
	var exit <-chan struct{}
	crdClient.Start(exit)
	crdClient.SyncCacheAll(exit, true)

	ids, err := crdClient.ListIds()
	if err != nil {
		klog.Fatalf("could not get the identities: %+v", err)
	}
	klog.Infof("Identities len: %d", len(*ids))
	for _, v := range *ids {
		buf, err := json.MarshalIndent(v, "", "    ")
		if err != nil {
			klog.Errorf("failed to marshal JSON, error: %+v", err)
			os.Exit(1)
		}
		klog.Infof("\n%s", string(buf))
	}

	bindings, err := crdClient.ListBindings()
	if err != nil {
		klog.Fatalf("could not get the bindings: %+v", err)
	}
	klog.Infof("bindings len: %d", len(*bindings))
	for _, v := range *bindings {
		buf, err := json.MarshalIndent(v, "", "    ")
		if err != nil {
			klog.Errorf("failed to marshal JSON, error: %+v", err)
			os.Exit(1)
		}
		klog.Infof("\n%s", string(buf))
	}

	assignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		klog.Fatalf("could not get assigned ID")
	}

	for _, a := range *assignedIDs {
		buf, err := json.MarshalIndent(a, "", "    ")
		if err != nil {
			klog.Errorf("failed to marshal JSON, error: %+v", err)
			os.Exit(1)
		}
		klog.Infof("\n%s", string(buf))
	}
	klog.Info("\ndone !")
}

// Create the client config. Use kubeconfig if given, otherwise assume in-cluster.
func buildConfig(kubeconfigPath string) (*rest.Config, error) {
	if kubeconfigPath != "" {
		return clientcmd.BuildConfigFromFlags("", kubeconfigPath)
	}
	return rest.InClusterConfig()
}
