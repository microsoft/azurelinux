package main

import (
	"flag"
	"net/http"
	_ "net/http/pprof" // #nosec
	"os"
	"strings"
	"time"

	"github.com/Azure/aad-pod-identity/pkg/log"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/mic"
	"github.com/Azure/aad-pod-identity/pkg/probes"
	"github.com/Azure/aad-pod-identity/version"

	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/klog/v2"
)

var (
	kubeconfig                          string
	cloudconfig                         string
	forceNamespaced                     bool
	versionInfo                         bool
	syncRetryDuration                   time.Duration
	leaderElectionCfg                   mic.LeaderElectionConfig
	httpProbePort                       string
	enableProfile                       bool
	enableScaleFeatures                 bool
	createDeleteBatch                   int64
	clientQPS                           float64
	prometheusPort                      string
	immutableUserMSIs                   string
	cmConfig                            mic.CMConfig
	typeUpgradeConfig                   mic.TypeUpgradeConfig
	updateUserMSIConfig                 mic.UpdateUserMSIConfig
	identityAssignmentReconcileInterval time.Duration
)

func main() {
	klog.InitFlags(nil)
	defer klog.Flush()

	logOptions := log.NewOptions()
	logOptions.AddFlags()

	hostName, err := os.Hostname()
	if err != nil {
		klog.Fatalf("failed to get hostname, error: %+v", err)
	}
	flag.StringVar(&kubeconfig, "kubeconfig", "", "Path to the kube config")
	flag.StringVar(&cloudconfig, "cloudconfig", "", "Path to cloud config e.g. Azure.json file")
	flag.BoolVar(&forceNamespaced, "forceNamespaced", false, "Forces namespaced identities, binding, and assignment")
	flag.BoolVar(&versionInfo, "version", false, "Prints the version information")
	flag.DurationVar(&syncRetryDuration, "syncRetryDuration", 3600*time.Second, "The interval in seconds at which sync loop should periodically check for errors and reconcile.")

	// Leader election parameters
	flag.StringVar(&leaderElectionCfg.Instance, "leader-election-instance", hostName, "leader election instance name. default is 'hostname'")
	flag.StringVar(&leaderElectionCfg.Namespace, "leader-election-namespace", "default", "namespace to create leader election objects")
	flag.StringVar(&leaderElectionCfg.Name, "leader-election-name", "aad-pod-identity-mic", "leader election name")
	flag.DurationVar(&leaderElectionCfg.Duration, "leader-election-duration", time.Second*15, "leader election duration")

	// Probe port
	flag.StringVar(&httpProbePort, "http-probe-port", "8080", "http liveliness probe port")

	// Prometheus port
	flag.StringVar(&prometheusPort, "prometheus-port", "8888", "Prometheus port for metrics")

	// Profile
	flag.BoolVar(&enableProfile, "enableProfile", false, "Enable/Disable pprof profiling")

	// Enable scale features handles the label based azureassignedidentity.
	flag.BoolVar(&enableScaleFeatures, "enableScaleFeatures", false, "Enable/Disable new features used for clusters at scale")

	// createDeleteBatch can be used for tuning the number of outstanding api server operations we do per node/VMSS.
	flag.Int64Var(&createDeleteBatch, "createDeleteBatch", 20, "Per node/VMSS create/delete batches")

	// Client QPS is used to configure the client-go QPS throttling and bursting.
	flag.Float64Var(&clientQPS, "clientQps", 5, "Client QPS used for throttling of calls to kube-api server")

	// Identities that should be never removed from Azure AD (used defined managed identities)
	flag.StringVar(&immutableUserMSIs, "immutable-user-msis", "", "prevent deletion of these IDs from the underlying VM/VMSS")

	// Config map for aad-pod-identity
	flag.StringVar(&cmConfig.Name, "config-map-name", "aad-pod-identity-config", "Configmap name")
	// Config map details for the type changes in the context of client-go upgrade.
	flag.StringVar(&typeUpgradeConfig.TypeUpgradeStatusKey, "type-upgrade-status-key", "type-upgrade-status", "Configmap key for type upgrade status")
	flag.BoolVar(&typeUpgradeConfig.EnableTypeUpgrade, "enable-type-upgrade", true, "Enable type upgrade")

	// Parameters for retrying cloudprovider's UpdateUserMSI function
	flag.IntVar(&updateUserMSIConfig.MaxRetry, "update-user-msi-max-retry", 2, "The maximum retry of UpdateUserMSI call")
	flag.DurationVar(&updateUserMSIConfig.RetryInterval, "update-user-msi-retry-interval", 1*time.Second, "The duration to wait before retrying UpdateUserMSI")

	// Parameters for reconciling identity assignment on Azure
	flag.DurationVar(&identityAssignmentReconcileInterval, "identity-assignment-reconcile-interval", 3*time.Minute, "The interval between reconciling identity assignment on Azure based on an existing list of AzureAssignedIdentities")

	flag.Parse()

	if err := logOptions.Apply(); err != nil {
		klog.Fatalf("unable to apply logging options, error: %+v", err)
	}

	podns := os.Getenv("MIC_POD_NAMESPACE")
	if podns == "" {
		klog.Fatalf("namespace not specified. Please add meta.namespace as env variable MIC_POD_NAMESPACE")
	}
	cmConfig.Namespace = podns

	if versionInfo {
		version.PrintVersionAndExit()
	}
	klog.Infof("starting mic process. Version: %v. Build date: %v", version.MICVersion, version.BuildDate)
	if cloudconfig == "" {
		klog.Warningf("--cloudconfig not passed will use aadpodidentity-admin-secret")
	}
	if kubeconfig == "" {
		klog.Warningf("--kubeconfig not passed will use InClusterConfig")
	}
	if enableProfile {
		profilePort := "6060"
		klog.Infof("starting profiling on port %s", profilePort)
		go func() {
			addr := "localhost:" + profilePort
			if err := http.ListenAndServe(addr, nil); err != nil {
				klog.Errorf("failed to listen and serve %s, error: %+v", addr, err)
			}
		}()
	}

	if enableScaleFeatures {
		klog.Infof("enabling features for scale clusters")
	}

	klog.Infof("kubeconfig (%s) cloudconfig (%s)", kubeconfig, cloudconfig)
	config, err := buildConfig(kubeconfig)
	if err != nil {
		klog.Fatalf("failed to build config from %s, error: %+v", kubeconfig, err)
	}
	config.UserAgent = version.GetUserAgent("MIC", version.MICVersion)

	forceNamespaced = forceNamespaced || "true" == os.Getenv("FORCENAMESPACED")
	klog.Infof("running MIC in namespaced mode: %v", forceNamespaced)

	config.QPS = float32(clientQPS)
	config.Burst = int(clientQPS)
	klog.Infof("client QPS set to: %v. Burst to: %v", config.QPS, config.Burst)

	var immutableUserMSIsList []string
	if immutableUserMSIs != "" {
		immutableUserMSIsList = strings.Split(immutableUserMSIs, ",")
	}

	micConfig := &mic.Config{
		CloudCfgPath:                        cloudconfig,
		RestConfig:                          config,
		IsNamespaced:                        forceNamespaced,
		SyncRetryInterval:                   syncRetryDuration,
		LeaderElectionCfg:                   &leaderElectionCfg,
		EnableScaleFeatures:                 enableScaleFeatures,
		CreateDeleteBatch:                   createDeleteBatch,
		ImmutableUserMSIsList:               immutableUserMSIsList,
		CMcfg:                               &cmConfig,
		TypeUpgradeCfg:                      &typeUpgradeConfig,
		UpdateUserMSICfg:                    &updateUserMSIConfig,
		IdentityAssignmentReconcileInterval: identityAssignmentReconcileInterval,
	}

	micClient, err := mic.NewMICClient(micConfig)
	if err != nil {
		klog.Fatalf("failed to create MIC client, error: %+v", err)
	}

	// Health probe will always report success once its started.
	// MIC instance will report the contents as "Active" only once its elected the leader
	// and starts the sync loop.
	probes.InitAndStart(httpProbePort, &micClient.SyncLoopStarted)

	// Register and expose metrics views
	if err = metrics.RegisterAndExport(prometheusPort); err != nil {
		klog.Fatalf("failed to register and export metrics on port %s, error: %+v", prometheusPort, err)
	}

	// Starts the leader election loop
	micClient.Run()
	klog.Info("aad-pod-identity controller initialized!!")
	select {}
}

// Create the client config. Use kubeconfig if given, otherwise assume in-cluster.
func buildConfig(kubeconfigPath string) (*rest.Config, error) {
	if kubeconfigPath != "" {
		return clientcmd.BuildConfigFromFlags("", kubeconfigPath)
	}
	return rest.InClusterConfig()
}
