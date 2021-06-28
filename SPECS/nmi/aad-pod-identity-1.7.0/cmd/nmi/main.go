package main

import (
	goflag "flag"
	"net/http"
	_ "net/http/pprof" // #nosec
	"os"
	"strings"

	"github.com/Azure/aad-pod-identity/pkg/log"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/nmi"
	server "github.com/Azure/aad-pod-identity/pkg/nmi/server"
	"github.com/Azure/aad-pod-identity/pkg/probes"
	"github.com/Azure/aad-pod-identity/pkg/utils"
	"github.com/Azure/aad-pod-identity/version"

	"github.com/spf13/pflag"
	"k8s.io/klog/v2"
)

const (
	defaultMetadataIP                         = "169.254.169.254"
	defaultMetadataPort                       = "80"
	defaultNmiPort                            = "2579"
	defaultIPTableUpdateTimeIntervalInSeconds = 60
	defaultlistPodIDsRetryAttemptsForCreated  = 16
	defaultlistPodIDsRetryAttemptsForAssigned = 4
	defaultlistPodIDsRetryIntervalInSeconds   = 5
)

var (
	versionInfo                        = pflag.Bool("version", false, "prints the version information")
	nmiPort                            = pflag.String("nmi-port", defaultNmiPort, "NMI application port")
	metadataIP                         = pflag.String("metadata-ip", defaultMetadataIP, "instance metadata host ip")
	metadataPort                       = pflag.String("metadata-port", defaultMetadataPort, "instance metadata host ip")
	nodename                           = pflag.String("node", "", "node name")
	ipTableUpdateTimeIntervalInSeconds = pflag.Int("ipt-update-interval-sec", defaultIPTableUpdateTimeIntervalInSeconds, "update interval of iptables")
	forceNamespaced                    = pflag.Bool("forceNamespaced", false, "Forces mic to namespace identities, binding, and assignment")
	micNamespace                       = pflag.String("MICNamespace", "default", "MIC namespace to short circuit MIC token requests")
	httpProbePort                      = pflag.String("http-probe-port", "8080", "Http health and liveness probe port")
	retryAttemptsForCreated            = pflag.Int("retry-attempts-for-created", defaultlistPodIDsRetryAttemptsForCreated, "Number of retries in NMI to find assigned identity in CREATED state")
	retryAttemptsForAssigned           = pflag.Int("retry-attempts-for-assigned", defaultlistPodIDsRetryAttemptsForAssigned, "Number of retries in NMI to find assigned identity in ASSIGNED state")
	findIdentityRetryIntervalInSeconds = pflag.Int("find-identity-retry-interval", defaultlistPodIDsRetryIntervalInSeconds, "Retry interval to find assigned identities in seconds")
	enableProfile                      = pflag.Bool("enableProfile", false, "Enable/Disable pprof profiling")
	enableScaleFeatures                = pflag.Bool("enableScaleFeatures", false, "Enable/Disable features for scale clusters")
	blockInstanceMetadata              = pflag.Bool("block-instance-metadata", false, "Block instance metadata endpoints")
	metadataHeaderRequired             = pflag.Bool("metadata-header-required", false, "Metadata header required for querying Azure Instance Metadata service")
	prometheusPort                     = pflag.String("prometheus-port", "9090", "Prometheus port for metrics")
	operationMode                      = pflag.String("operation-mode", "standard", "NMI operation mode")
	allowNetworkPluginKubenet          = pflag.Bool("allow-network-plugin-kubenet", false, "Allow running aad-pod-identity in cluster with kubenet")
	kubeletConfig                      = pflag.String("kubelet-config", "/etc/default/kubelet", "Path to kubelet default config")
)

func main() {
	klog.InitFlags(nil)
	defer klog.Flush()

	logOptions := log.NewOptions()
	logOptions.AddFlags()

	// this is done for glog used by client-go underneath
	pflag.CommandLine.AddGoFlagSet(goflag.CommandLine)

	pflag.Parse()

	if err := logOptions.Apply(); err != nil {
		klog.Fatalf("unable to apply logging options, error: %+v", err)
	}

	if *versionInfo {
		version.PrintVersionAndExit()
	}

	// check if the cni is kubenet from the --network-plugin defined in kubelet config
	isKubenet, err := utils.IsKubenetCNI(*kubeletConfig)
	if err != nil {
		klog.Fatalf("failed to check if CNI plugin is kubenet, error: %+v", err)
	}
	if !*allowNetworkPluginKubenet && isKubenet {
		klog.Fatalf("AAD Pod Identity is not supported for Kubenet. Review https://azure.github.io/aad-pod-identity/docs/configure/aad_pod_identity_on_kubenet/ for more details.")
	}

	klog.Infof("starting nmi process. Version: %v. Build date: %v.", version.NMIVersion, version.BuildDate)

	if *enableProfile {
		profilePort := "6060"
		klog.Infof("starting profiling on port %s", profilePort)
		go func() {
			addr := "localhost:" + profilePort
			if err := http.ListenAndServe(addr, nil); err != nil {
				klog.Errorf("failed to listen and serve %s, error: %+v", addr, err)
			}
		}()
	}
	if *enableScaleFeatures {
		klog.Infof("features for scale clusters enabled")
	}

	// normalize operation mode
	*operationMode = strings.ToLower(*operationMode)

	client, err := nmi.GetKubeClient(*nodename, *operationMode, *enableScaleFeatures)
	if err != nil {
		klog.Fatalf("failed to get kube client, error: %+v", err)
	}

	exit := make(<-chan struct{})
	client.Start(exit)
	*forceNamespaced = *forceNamespaced || "true" == os.Getenv("FORCENAMESPACED")
	klog.Infof("running NMI in namespaced mode: %v", *forceNamespaced)

	s := server.NewServer(*micNamespace, *blockInstanceMetadata, *metadataHeaderRequired)
	s.KubeClient = client
	s.MetadataIP = *metadataIP
	s.MetadataPort = *metadataPort
	s.NMIPort = *nmiPort
	s.NodeName = *nodename
	s.IPTableUpdateTimeIntervalInSeconds = *ipTableUpdateTimeIntervalInSeconds

	nmiConfig := nmi.Config{
		Mode:                               strings.ToLower(*operationMode),
		RetryAttemptsForCreated:            *retryAttemptsForCreated,
		RetryAttemptsForAssigned:           *retryAttemptsForAssigned,
		FindIdentityRetryIntervalInSeconds: *findIdentityRetryIntervalInSeconds,
		Namespaced:                         *forceNamespaced,
	}

	// Create new token client based on the nmi mode
	tokenClient, err := nmi.GetTokenClient(client, nmiConfig)
	if err != nil {
		klog.Fatalf("failed to initialize token client, error: %+v", err)
	}
	s.TokenClient = tokenClient

	// Health probe will always report success once its started. The contents
	// will report "Active" once the iptables rules are set
	probes.InitAndStart(*httpProbePort, &s.Initialized)

	// Register and expose metrics views
	if err = metrics.RegisterAndExport(*prometheusPort); err != nil {
		klog.Fatalf("failed to register and export metrics on port %s, error: %+v", *prometheusPort, err)
	}
	if err := s.Run(); err != nil {
		klog.Fatalf("%s", err)
	}
}
