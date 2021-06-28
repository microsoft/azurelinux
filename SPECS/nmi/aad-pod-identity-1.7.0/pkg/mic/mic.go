package mic

import (
	"context"
	"fmt"
	"os"
	"reflect"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	"github.com/Azure/aad-pod-identity/pkg/cloudprovider"
	"github.com/Azure/aad-pod-identity/pkg/crd"
	"github.com/Azure/aad-pod-identity/pkg/filewatcher"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/pod"
	"github.com/Azure/aad-pod-identity/pkg/stats"
	"github.com/Azure/aad-pod-identity/pkg/utils"
	"github.com/Azure/aad-pod-identity/version"

	"github.com/fsnotify/fsnotify"
	"golang.org/x/sync/semaphore"
	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/informers"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/kubernetes/scheme"
	typedcorev1 "k8s.io/client-go/kubernetes/typed/core/v1"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/leaderelection"
	"k8s.io/client-go/tools/leaderelection/resourcelock"
	"k8s.io/client-go/tools/record"
	"k8s.io/klog/v2"
)

const (
	stopped = int32(0)
	running = int32(1)
)

// NodeGetter is an abstraction used to get Kubernetes node info.
type NodeGetter interface {
	Get(name string) (*corev1.Node, error)
	Start(<-chan struct{})
}

// TypeUpgradeConfig - configuration aspects of type related changes required for client-go upgrade.
type TypeUpgradeConfig struct {
	// Key in the config map which indicates if a type upgrade has been performed.
	TypeUpgradeStatusKey string
	EnableTypeUpgrade    bool
}

// CMConfig - config map for aad-pod-identity
type CMConfig struct {
	Namespace string
	Name      string
}

// LeaderElectionConfig - used to keep track of leader election config.
type LeaderElectionConfig struct {
	Namespace string
	Name      string
	Duration  time.Duration
	Instance  string
}

// UpdateUserMSIConfig - parameters for retrying cloudprovider's UpdateUserMSI function
type UpdateUserMSIConfig struct {
	MaxRetry      int
	RetryInterval time.Duration
}

// Client has the required pointers to talk to the api server
// and interact with the CRD related datastructure.
type Client struct {
	CRDClient                           crd.ClientInt
	CloudClient                         cloudprovider.ClientInt
	PodClient                           pod.ClientInt
	CloudConfigWatcher                  filewatcher.ClientInt
	EventRecorder                       record.EventRecorder
	EventChannel                        chan aadpodid.EventType
	NodeClient                          NodeGetter
	IsNamespaced                        bool
	SyncLoopStarted                     bool
	syncRetryInterval                   time.Duration
	enableScaleFeatures                 bool
	createDeleteBatch                   int64
	ImmutableUserMSIsMap                map[string]bool
	identityAssignmentReconcileInterval time.Duration

	syncing int32 // protect against conucrrent sync's

	leaderElector *leaderelection.LeaderElector
	*LeaderElectionConfig
	Reporter       *metrics.Reporter
	TypeUpgradeCfg *TypeUpgradeConfig
	CMCfg          *CMConfig
	CMClient       typedcorev1.ConfigMapInterface
}

// Config - MIC Config
type Config struct {
	CloudCfgPath                        string
	RestConfig                          *rest.Config
	IsNamespaced                        bool
	SyncRetryInterval                   time.Duration
	LeaderElectionCfg                   *LeaderElectionConfig
	EnableScaleFeatures                 bool
	CreateDeleteBatch                   int64
	ImmutableUserMSIsList               []string
	CMcfg                               *CMConfig
	TypeUpgradeCfg                      *TypeUpgradeConfig
	UpdateUserMSICfg                    *UpdateUserMSIConfig
	IdentityAssignmentReconcileInterval time.Duration
}

// ClientInt is an abstraction used to perform an MIC sync cycle.
type ClientInt interface {
	Start(exit <-chan struct{})
	Sync(exit <-chan struct{})
}

type trackUserAssignedMSIIds struct {
	addUserAssignedMSIIDs    []string
	removeUserAssignedMSIIDs []string
	assignedIDsToCreate      []aadpodid.AzureAssignedIdentity
	assignedIDsToDelete      []aadpodid.AzureAssignedIdentity
	assignedIDsToUpdate      []aadpodid.AzureAssignedIdentity
	isvmss                   bool
}

// NewMICClient returnes new mic client
func NewMICClient(cfg *Config) (*Client, error) {
	klog.Infof("starting to create the pod identity client. Version: %v. Build date: %v", version.MICVersion, version.BuildDate)

	clientSet := kubernetes.NewForConfigOrDie(cfg.RestConfig)

	k8sVersion, err := clientSet.ServerVersion()
	if err == nil {
		klog.Infof("Kubernetes server version: %s", k8sVersion.String())
	}

	informer := informers.NewSharedInformerFactory(clientSet, 30*time.Second)

	cloudClient, err := cloudprovider.NewCloudProvider(cfg.CloudCfgPath, cfg.UpdateUserMSICfg.MaxRetry, cfg.UpdateUserMSICfg.RetryInterval)
	if err != nil {
		return nil, err
	}
	klog.V(1).Infof("cloud provider initialized")

	eventCh := make(chan aadpodid.EventType, 100)

	crdClient, err := crd.NewCRDClient(cfg.RestConfig, eventCh)
	if err != nil {
		return nil, err
	}
	klog.V(1).Infof("CRD client initialized")

	podClient := pod.NewPodClient(informer, eventCh)
	klog.V(1).Infof("pod Client initialized")

	cloudConfigWatcher, err := filewatcher.NewFileWatcher(
		func(event fsnotify.Event) {
			if event.Op&fsnotify.Write == fsnotify.Write {
				if err := cloudClient.Init(); err != nil {
					return
				}
				klog.V(1).Infof("cloud provider re-initialized")
			}
		}, func(err error) {
			klog.Errorf("failed to handle fsnotify event, error: %+v", err)
		})
	if err != nil {
		return nil, err
	}
	if err := cloudConfigWatcher.Add(cfg.CloudCfgPath); err != nil {
		return nil, err
	}
	klog.V(1).Infof("cloud config watcher initialized")

	eventBroadcaster := record.NewBroadcaster()
	eventBroadcaster.StartRecordingToSink(&typedcorev1.EventSinkImpl{Interface: clientSet.CoreV1().Events("")})
	recorder := eventBroadcaster.NewRecorder(scheme.Scheme, corev1.EventSource{Component: aadpodid.CRDGroup})

	var immutableUserMSIsMap map[string]bool

	if len(cfg.ImmutableUserMSIsList) > 0 {
		// this map contains list of identities that are configured by user as immutable.
		immutableUserMSIsMap = make(map[string]bool)
		for _, item := range cfg.ImmutableUserMSIsList {
			immutableUserMSIsMap[strings.ToLower(item)] = true
		}
	}

	var cmClient typedcorev1.ConfigMapInterface
	if cfg.TypeUpgradeCfg.EnableTypeUpgrade {
		cmClient = clientSet.CoreV1().ConfigMaps(cfg.CMcfg.Namespace)
	}

	c := &Client{
		CRDClient:                           crdClient,
		CloudClient:                         cloudClient,
		PodClient:                           podClient,
		CloudConfigWatcher:                  cloudConfigWatcher,
		EventRecorder:                       recorder,
		EventChannel:                        eventCh,
		NodeClient:                          &NodeClient{informer.Core().V1().Nodes()},
		IsNamespaced:                        cfg.IsNamespaced,
		syncRetryInterval:                   cfg.SyncRetryInterval,
		enableScaleFeatures:                 cfg.EnableScaleFeatures,
		createDeleteBatch:                   cfg.CreateDeleteBatch,
		ImmutableUserMSIsMap:                immutableUserMSIsMap,
		TypeUpgradeCfg:                      cfg.TypeUpgradeCfg,
		CMCfg:                               cfg.CMcfg,
		CMClient:                            cmClient,
		identityAssignmentReconcileInterval: cfg.IdentityAssignmentReconcileInterval,
	}

	leaderElector, err := c.NewLeaderElector(clientSet, recorder, cfg.LeaderElectionCfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create new leader elector, error: %+v", err)
	}
	c.leaderElector = leaderElector

	reporter, err := metrics.NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}
	c.Reporter = reporter
	return c, nil
}

// Run - Initiates the leader election run call to find if its leader and run it
func (c *Client) Run() {
	klog.Info("initiating MIC Leader election")
	// counter to track number of mic election
	c.Reporter.Report(metrics.MICNewLeaderElectionCountM.M(1))
	c.leaderElector.Run(context.Background())
}

// NewLeaderElector - does the required leader election initialization
func (c *Client) NewLeaderElector(clientSet *kubernetes.Clientset, recorder record.EventRecorder, leaderElectionConfig *LeaderElectionConfig) (leaderElector *leaderelection.LeaderElector, err error) {
	c.LeaderElectionConfig = leaderElectionConfig
	resourceLock, err := resourcelock.New(resourcelock.EndpointsResourceLock,
		c.Namespace,
		c.Name,
		clientSet.CoreV1(),
		clientSet.CoordinationV1(),
		resourcelock.ResourceLockConfig{
			Identity:      c.Instance,
			EventRecorder: recorder})
	if err != nil {
		return nil, fmt.Errorf("failed to create resource lock for leader election, error: %+v", err)
	}
	config := leaderelection.LeaderElectionConfig{
		LeaseDuration: c.Duration,
		RenewDeadline: c.Duration / 2,
		RetryPeriod:   c.Duration / 4,
		Callbacks: leaderelection.LeaderCallbacks{
			OnStartedLeading: func(ctx context.Context) {
				c.Start(ctx.Done())
			},
			OnStoppedLeading: func() {
				klog.Error("lost leader lease")
				klog.Flush()
				os.Exit(1)
			},
		},
		Lock: resourceLock,
	}

	leaderElector, err = leaderelection.NewLeaderElector(config)
	if err != nil {
		return nil, err
	}
	return leaderElector, nil
}

// UpgradeTypeIfRequired performs type upgrade for all aad-pod-identity CRDs if required.
func (c *Client) UpgradeTypeIfRequired() error {
	if c.TypeUpgradeCfg.EnableTypeUpgrade {
		cm, err := c.CMClient.Get(context.TODO(), c.CMCfg.Name, v1.GetOptions{})
		// If we get an error and its not NotFound then return, because we cannot proceed.
		if err != nil && !apierrors.IsNotFound(err) {
			return fmt.Errorf("failed to get ConfigMap %s/%s, error: %+v", c.CMCfg.Namespace, c.CMCfg.Name, err)
		}

		// Now either the configmap is not there or we successfully got the configmap
		// Handle the case where the configmap is not found.
		if err != nil && apierrors.IsNotFound(err) {
			// Create the configmap
			newCfgMap := &corev1.ConfigMap{
				ObjectMeta: v1.ObjectMeta{
					Namespace: c.CMCfg.Namespace,
					Name:      c.CMCfg.Name,
				},
			}
			if cm, err = c.CMClient.Create(context.TODO(), newCfgMap, metav1.CreateOptions{}); err != nil {
				return fmt.Errorf("failed to create ConfigMap %s/%s, error: %+v", c.CMCfg.Namespace, c.CMCfg.Name, err)
			}
		}

		// We reach here only if the configmap is present or we created new one.
		// Check if the key for type upgrade is present. If the key is present,
		// then the upgrade is already performed. If not then go through the type upgrade
		// process.
		if v, ok := cm.Data[c.TypeUpgradeCfg.TypeUpgradeStatusKey]; !ok {
			klog.Infof("upgrading the types to work with case sensitive go-client")
			if err := c.CRDClient.UpgradeAll(); err != nil {
				return fmt.Errorf("failed to upgrade type, error: %+v", err)
			}
			klog.Infof("type upgrade completed !!")
			// Upgrade completed so update the data with the upgrade key.
			if cm.Data == nil {
				cm.Data = make(map[string]string)
			}
			cm.Data[c.TypeUpgradeCfg.TypeUpgradeStatusKey] = version.MICVersion
			_, err = c.CMClient.Update(context.TODO(), cm, metav1.UpdateOptions{})
			if err != nil {
				return fmt.Errorf("failed to update ConfigMap key %s failed, error: %+v", c.TypeUpgradeCfg.TypeUpgradeStatusKey, err)
			}
		} else {
			klog.Infof("type upgrade status configmap found from version: %s. Skipping type upgrade!", v)
		}
	}
	return nil
}

// Start starts various go routines to watch for any relevant changes that would trigger a MIC sync.
func (c *Client) Start(exit <-chan struct{}) {
	klog.V(6).Infof("MIC client starting..")

	if err := c.UpgradeTypeIfRequired(); err != nil {
		klog.Fatalf("type upgrade failed with error: %+v", err)
		return
	}

	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		c.PodClient.Start(exit)
		klog.V(6).Infof("pod client started")
		wg.Done()
	}()

	wg.Add(1)
	go func() {
		c.CRDClient.Start(exit)
		klog.V(6).Infof("CRD client started")
		wg.Done()
	}()

	wg.Add(1)
	go func() {
		c.NodeClient.Start(exit)
		klog.V(6).Infof("node client started")
		wg.Done()
	}()

	wg.Add(1)
	go func() {
		c.CloudConfigWatcher.Start(exit)
		klog.V(6).Infof("cloud config watcher started")
		wg.Done()
	}()

	wg.Wait()
	go c.Sync(exit)
}

func (c *Client) canSync() bool {
	return atomic.CompareAndSwapInt32(&c.syncing, stopped, running)
}

func (c *Client) setStopped() {
	atomic.StoreInt32(&c.syncing, stopped)
}

// Sync perform a sync cycle.
func (c *Client) Sync(exit <-chan struct{}) {
	if !c.canSync() {
		panic("concurrent syncs")
	}
	defer c.setStopped()

	ticker := time.NewTicker(c.syncRetryInterval)
	defer ticker.Stop()

	identityAssignmentReconcileTicker := time.NewTicker(c.identityAssignmentReconcileInterval)
	defer identityAssignmentReconcileTicker.Stop()

	klog.Info("sync thread started.")
	c.SyncLoopStarted = true
	var event aadpodid.EventType
	totalWorkDoneCycles := 0
	totalSyncCycles := 0

	for {
		select {
		case <-exit:
			return
		case event = <-c.EventChannel:
			klog.V(6).Infof("received event: %v", event)
		case <-ticker.C:
			klog.V(6).Infof("running periodic sync loop")
		case <-identityAssignmentReconcileTicker.C:
			klog.V(6).Infof("reconciling identity assignment on Azure")
			c.reconcileIdentityAssignment()
			continue
		}
		totalSyncCycles++
		stats.Init()
		// This is the only place where the AzureAssignedIdentity creation is initiated.
		begin := time.Now()
		workDone := false

		cacheTime := time.Now()

		// There is a delay in data propagation to cache. It's possible that the creates performed in the previous sync cycle
		// are not propagated before this sync cycle began. In order to avoid redoing the cycle, we sync cache again.
		c.CRDClient.SyncCacheAll(exit, false)
		stats.Put(stats.CacheSync, time.Since(cacheTime))

		// List all pods in all namespaces
		systemTime := time.Now()
		listPods, err := c.PodClient.GetPods()
		if err != nil {
			klog.Errorf("failed to list pods, error: %+v", err)
			continue
		}
		listBindings, err := c.CRDClient.ListBindings()
		if err != nil {
			continue
		}
		klog.V(6).Infof("number of bindings: %d", len(*listBindings))
		listIDs, err := c.CRDClient.ListIds()
		if err != nil {
			continue
		}
		klog.V(6).Infof("number of identities: %d", len(*listIDs))
		idMap, err := c.convertIDListToMap(*listIDs)
		if err != nil {
			klog.Errorf("failed to convert ID list to map, error: %+v", err)
			continue
		}

		currentAssignedIDs, err := c.CRDClient.ListAssignedIDsInMap()
		if err != nil {
			continue
		}
		klog.V(6).Infof("number of assigned identities: %d", len(currentAssignedIDs))
		stats.Put(stats.System, time.Since(systemTime))

		beginNewListTime := time.Now()
		newAssignedIDs, nodeRefs, err := c.createDesiredAssignedIdentityList(listPods, listBindings, idMap)
		if err != nil {
			klog.Errorf("failed to create a list of desired AzureAssignedIdentity, error: %+v", err)
			continue
		}
		stats.Put(stats.CurrentState, time.Since(beginNewListTime))

		// Extract add list and delete list based on existing assigned ids in the system (currentAssignedIDs).
		// and the ones we have arrived at in the volatile list (newAssignedIDs).
		addList, err := c.getAzureAssignedIDsToCreate(currentAssignedIDs, newAssignedIDs)
		if err != nil {
			klog.Errorf("failed to get a list of AzureAssignedIdentities to create, error: %+v", err)
			continue
		}
		deleteList, err := c.getAzureAssignedIDsToDelete(currentAssignedIDs, newAssignedIDs)
		if err != nil {
			klog.Errorf("failed to get a list of AzureAssignedIdentities to delete, error: %+v", err)
			continue
		}
		beforeUpdateList, afterUpdateList := c.getAzureAssignedIdentitiesToUpdate(addList, deleteList)
		klog.V(5).Infof("del: %v, add: %v, update: %v", deleteList, addList, afterUpdateList)

		// the node map is used to track assigned ids to create/delete, identities to assign/remove
		// for each node or vmss
		nodeMap := make(map[string]trackUserAssignedMSIIds)

		// separate the add, delete and update list per node
		c.convertAssignedIDListToMap(addList, deleteList, afterUpdateList, nodeMap)

		// process the delete and add list
		// determine the list of identities that need to updated, create a node to identity list mapping for add and delete
		if len(deleteList) > 0 || len(beforeUpdateList) > 0 {
			workDone = true
			c.getListOfIdsToDelete(deleteList, beforeUpdateList, afterUpdateList, newAssignedIDs, nodeMap, nodeRefs)
		}
		if len(addList) > 0 || len(afterUpdateList) > 0 {
			workDone = true
			c.getListOfIdsToAssign(addList, afterUpdateList, nodeMap)
		}

		var wg sync.WaitGroup

		// check if vmss and consolidate vmss nodes into vmss if necessary
		c.consolidateVMSSNodes(nodeMap, &wg)

		// one final createorupdate to each node or vmss in the map
		c.updateNodeAndDeps(newAssignedIDs, nodeMap, nodeRefs, &wg)

		wg.Wait()

		if workDone || ((totalSyncCycles % 1000) == 0) {
			if workDone {
				totalWorkDoneCycles++
			}
			idsFound := 0
			bindingsFound := 0
			if listIDs != nil {
				idsFound = len(*listIDs)
			}
			if listBindings != nil {
				bindingsFound = len(*listBindings)
			}
			klog.Infof("work done: %v. Found %d pods, %d ids, %d bindings", workDone, len(listPods), idsFound, bindingsFound)
			klog.Infof("total work cycles: %d, out of which work was done in: %d", totalSyncCycles, totalWorkDoneCycles)
			stats.Put(stats.Total, time.Since(begin))

			c.Reporter.Report(
				metrics.MICCycleCountM.M(1),
				metrics.MICCycleDurationM.M(metrics.SinceInSeconds(begin)))

			stats.PrintSync()
			if workDone {
				// We need to synchronize the cache inorder to get the latest updates.
				// Even though we sync at the beginning of every cycle, we are still seeing
				// conflicts indicating the assigned identities are not reflecting in
				// the cache. Continue to use the sleep workaround.
				time.Sleep(time.Millisecond * 200)
			}
		}
	}
}

func (c *Client) convertAssignedIDListToMap(addList, deleteList, updateList map[string]aadpodid.AzureAssignedIdentity, nodeMap map[string]trackUserAssignedMSIIds) {
	for _, createID := range addList {
		if trackList, ok := nodeMap[createID.Spec.NodeName]; ok {
			trackList.assignedIDsToCreate = append(trackList.assignedIDsToCreate, createID)
			nodeMap[createID.Spec.NodeName] = trackList
			continue
		}
		nodeMap[createID.Spec.NodeName] = trackUserAssignedMSIIds{assignedIDsToCreate: []aadpodid.AzureAssignedIdentity{createID}}
	}

	for _, delID := range deleteList {
		if trackList, ok := nodeMap[delID.Spec.NodeName]; ok {
			trackList.assignedIDsToDelete = append(trackList.assignedIDsToDelete, delID)
			nodeMap[delID.Spec.NodeName] = trackList
			continue
		}
		nodeMap[delID.Spec.NodeName] = trackUserAssignedMSIIds{assignedIDsToDelete: []aadpodid.AzureAssignedIdentity{delID}}
	}

	for _, updateID := range updateList {
		if trackList, ok := nodeMap[updateID.Spec.NodeName]; ok {
			trackList.assignedIDsToUpdate = append(trackList.assignedIDsToUpdate, updateID)
			nodeMap[updateID.Spec.NodeName] = trackList
			continue
		}
		nodeMap[updateID.Spec.NodeName] = trackUserAssignedMSIIds{assignedIDsToUpdate: []aadpodid.AzureAssignedIdentity{updateID}}
	}
}

func (c *Client) createDesiredAssignedIdentityList(
	listPods []*corev1.Pod, listBindings *[]aadpodid.AzureIdentityBinding, idMap map[string]aadpodid.AzureIdentity) (map[string]aadpodid.AzureAssignedIdentity, map[string]bool, error) {
	// For each pod, check what bindings are matching. For each binding create volatile azure assigned identity.
	// Compare this list with the current list of azure assigned identities.
	// For any new assigned identities found in this volatile list, create assigned identity and assign user assigned msis.
	// For any assigned ids not present the volatile list, proceed with the deletion.
	nodeRefs := make(map[string]bool)
	newAssignedIDs := make(map[string]aadpodid.AzureAssignedIdentity)

	for _, pod := range listPods {
		klog.V(6).Infof("checking pod %s/%s", pod.Namespace, pod.Name)
		if pod.Spec.NodeName == "" {
			// Node is not yet allocated. In that case skip the pod
			klog.Infof("pod %s/%s has no assigned node yet. it will be ignored", pod.Namespace, pod.Name)
			continue
		}
		crdPodLabelVal := pod.Labels[aadpodid.CRDLabelKey]
		klog.V(6).Infof("pod: %s/%s. Label value: %v", pod.Namespace, pod.Name, crdPodLabelVal)
		if crdPodLabelVal == "" {
			// No binding mentioned in the label. Just continue to the next pod
			klog.Infof("pod %s/%s doesn't contain %s label field. it will be ignored", pod.Namespace, pod.Name, aadpodid.CRDLabelKey)
			continue
		}
		var matchedBindings []aadpodid.AzureIdentityBinding
		for _, allBinding := range *listBindings {
			klog.V(6).Infof("check the binding (pod - %s/%s): %s", pod.Namespace, pod.Name, allBinding.Spec.Selector)
			if allBinding.Spec.Selector == crdPodLabelVal {
				klog.V(5).Infof("found binding match for pod %s/%s with binding %s/%s", pod.Namespace, pod.Name, allBinding.Namespace, allBinding.Name)
				matchedBindings = append(matchedBindings, allBinding)
				nodeRefs[pod.Spec.NodeName] = true
			}
		}

		if len(matchedBindings) == 0 {
			klog.Infof("No AzureIdentityBinding found for pod %s/%s that matches selector: %s. it will be ignored", pod.Namespace, pod.Name, crdPodLabelVal)
			continue
		}

		for _, binding := range matchedBindings {
			klog.V(5).Infof("looking up id map: %s/%s", binding.Namespace, binding.Spec.AzureIdentity)
			if azureID, idPresent := idMap[getIDKey(binding.Namespace, binding.Spec.AzureIdentity)]; idPresent {
				// working in Namespaced mode or this specific identity is namespaced
				if c.IsNamespaced || aadpodid.IsNamespacedIdentity(&azureID) {
					// They have to match all
					if !(azureID.Namespace == binding.Namespace && binding.Namespace == pod.Namespace) {
						klog.V(5).Infof("identity %s/%s was matched via binding %s/%s to %s/%s but namespaced identity is enforced, so it will be ignored",
							azureID.Namespace, azureID.Name, binding.Namespace, binding.Name, pod.Namespace, pod.Name)
						continue
					}
				}
				klog.V(5).Infof("identity %s/%s assigned to %s/%s via %s/%s", azureID.Namespace, azureID.Name, pod.Namespace, pod.Name, binding.Namespace, binding.Name)
				assignedID, err := c.makeAssignedIDs(azureID, binding, pod.Name, pod.Namespace, pod.Spec.NodeName)

				if err != nil {
					klog.Errorf("failed to create an AzureAssignedIdentity between pod %s/%s and AzureIdentity %s/%s, error: %+v", pod.Namespace, pod.Name, azureID.Namespace, azureID.Name, err)
					continue
				}
				newAssignedIDs[assignedID.Name] = *assignedID
			} else {
				// This is the case where the identity has been deleted.
				// In such a case, we will skip it from matching binding.
				// This will ensure that the new assigned ids created will not have the
				// one associated with this azure identity.
				klog.Infof("%s identity not found when using %s/%s binding", binding.Spec.AzureIdentity, binding.Namespace, binding.Name)
			}
		}
	}
	return newAssignedIDs, nodeRefs, nil
}

// getListOfIdsToDelete will go over the delete list to determine if the id is required to be deleted
// only user assigned identity not in use are added to the remove list for the node
func (c *Client) getListOfIdsToDelete(deleteList, beforeUpdateList, afterUpdateList, newAssignedIDs map[string]aadpodid.AzureAssignedIdentity,
	nodeMap map[string]trackUserAssignedMSIIds,
	nodeRefs map[string]bool) {
	vmssGroups, err := getVMSSGroups(c.NodeClient, nodeRefs)
	if err != nil {
		klog.Errorf("failed to get VMSS groups, error: %+v", err)
		return
	}

	consolidatedMapToCheck := make(map[string]aadpodid.AzureAssignedIdentity)
	for name, id := range newAssignedIDs {
		consolidatedMapToCheck[name] = id
	}
	for name, id := range afterUpdateList {
		consolidatedMapToCheck[name] = id
	}

	for _, delID := range deleteList {
		err := c.shouldRemoveID(delID, consolidatedMapToCheck, nodeMap, vmssGroups)
		if err != nil {
			klog.Errorf("failed to check if identity should be removed, error: %+v", err)
		}
	}
	// this loop checks the azure identity before it was updated and cleans up
	// the old identity
	for _, oldUpdateID := range beforeUpdateList {
		err := c.shouldRemoveID(oldUpdateID, consolidatedMapToCheck, nodeMap, vmssGroups)
		if err != nil {
			klog.Errorf("failed to check if identity should be removed, error: %+v", err)
		}
	}
}

// getListOfIdsToAssign will add the id to the append list for node if it's user assigned identity
func (c *Client) getListOfIdsToAssign(addList, updateList map[string]aadpodid.AzureAssignedIdentity, nodeMap map[string]trackUserAssignedMSIIds) {
	for _, createID := range addList {
		c.shouldAssignID(createID, nodeMap)
	}
	for _, updateID := range updateList {
		c.shouldAssignID(updateID, nodeMap)
	}
}

func (c *Client) shouldAssignID(assignedID aadpodid.AzureAssignedIdentity, nodeMap map[string]trackUserAssignedMSIIds) {
	id := assignedID.Spec.AzureIdentityRef
	isUserAssignedMSI := c.checkIfUserAssignedMSI(*id)

	if assignedID.Status.Status == "" || assignedID.Status.Status == aadpodid.AssignedIDCreated {
		if isUserAssignedMSI {
			c.appendToAddListForNode(id.Spec.ResourceID, assignedID.Spec.NodeName, nodeMap)
		}
	}
	klog.V(5).Infof("binding applied: %+v", assignedID.Spec.AzureBindingRef)
}

func (c *Client) shouldRemoveID(assignedID aadpodid.AzureAssignedIdentity,
	newAssignedIDs map[string]aadpodid.AzureAssignedIdentity,
	nodeMap map[string]trackUserAssignedMSIIds, vmssGroups *vmssGroupList) error {
	klog.V(5).Infof("deletion of id: %s", assignedID.Name)
	inUse, err := c.checkIfInUse(assignedID, newAssignedIDs, vmssGroups)
	if err != nil {
		return err
	}

	id := assignedID.Spec.AzureIdentityRef
	isUserAssignedMSI := c.checkIfUserAssignedMSI(*id)
	isImmutableIdentity := c.checkIfIdentityImmutable(id.Spec.ClientID)
	// this case includes Assigned state and empty state to ensure backward compatibility
	if assignedID.Status.Status == aadpodid.AssignedIDAssigned || assignedID.Status.Status == "" {
		// only user assigned identities that are not in use and are not defined as
		// immutable will be removed from underlying node/vmss
		if !inUse && isUserAssignedMSI && !isImmutableIdentity {
			c.appendToRemoveListForNode(id.Spec.ResourceID, assignedID.Spec.NodeName, nodeMap)
		}
	}
	klog.V(5).Infof("binding removed: %+v", assignedID.Spec.AzureBindingRef)
	return nil
}

func (c *Client) matchAssignedID(x aadpodid.AzureAssignedIdentity, y aadpodid.AzureAssignedIdentity) (ret bool) {
	bindingX := x.Spec.AzureBindingRef
	bindingY := y.Spec.AzureBindingRef

	idX := x.Spec.AzureIdentityRef
	idY := y.Spec.AzureIdentityRef

	klog.V(7).Infof("assignedidX - %+v\n", x)
	klog.V(7).Infof("assignedidY - %+v\n", y)

	klog.V(7).Infof("bindingX - %+v\n", bindingX)
	klog.V(7).Infof("bindingY - %+v\n", bindingY)

	klog.V(7).Infof("idX - %+v\n", idX)
	klog.V(7).Infof("idY - %+v\n", idY)

	return bindingX.Name == bindingY.Name &&
		bindingX.ResourceVersion == bindingY.ResourceVersion &&
		idX.Name == idY.Name &&
		idX.ResourceVersion == idY.ResourceVersion &&
		x.Spec.Pod == y.Spec.Pod &&
		x.Spec.PodNamespace == y.Spec.PodNamespace &&
		x.Spec.NodeName == y.Spec.NodeName
}

func (c *Client) getAzureAssignedIDsToCreate(old, new map[string]aadpodid.AzureAssignedIdentity) (map[string]aadpodid.AzureAssignedIdentity, error) {
	// everything in new needs to be created
	if len(old) == 0 {
		return new, nil
	}

	create := make(map[string]aadpodid.AzureAssignedIdentity)
	begin := time.Now()

	for assignedIDName, newAssignedID := range new {
		oldAssignedID, exists := old[assignedIDName]
		idMatch := false
		if exists {
			idMatch = c.matchAssignedID(oldAssignedID, newAssignedID)
		}
		if idMatch && oldAssignedID.Status.Status == aadpodid.AssignedIDCreated {
			// if the old assigned id is in created state, then the identity assignment to the node
			// is not done. Adding to the list will ensure we retry identity assignment to node for
			// this assigned identity.
			klog.V(5).Infof("ok: %v, Create added: %s as assignedID in CREATED state", idMatch, assignedIDName)
			create[assignedIDName] = oldAssignedID
		}
		if !idMatch {
			// We are done checking that this new id is not present in the old
			// list. So we will add it to the create list.
			klog.V(5).Infof("ok: %v, Create added: %s", idMatch, assignedIDName)
			create[assignedIDName] = newAssignedID
		}
	}
	stats.Put(stats.FindAzureAssignedIdentitiesToCreate, time.Since(begin))
	return create, nil
}

func (c *Client) getAzureAssignedIDsToDelete(old, new map[string]aadpodid.AzureAssignedIdentity) (map[string]aadpodid.AzureAssignedIdentity, error) {
	delete := make(map[string]aadpodid.AzureAssignedIdentity)
	// nothing to delete
	if len(old) == 0 {
		return delete, nil
	}
	// delete everything as nothing in new
	if len(new) == 0 {
		return old, nil
	}

	begin := time.Now()
	for assignedIDName, oldAssignedID := range old {
		newAssignedID, exists := new[assignedIDName]
		idMatch := false
		if exists {
			idMatch = c.matchAssignedID(oldAssignedID, newAssignedID)
		}
		// assigned identity exists in the desired list too which means
		// it should not be deleted
		if exists && idMatch {
			continue
		}
		// We are done checking that this old id is not present in the new
		// list. So we will add it to the delete list.
		delete[assignedIDName] = oldAssignedID
	}
	stats.Put(stats.FindAzureAssignedIdentitiesToDelete, time.Since(begin))
	return delete, nil
}

// getAzureAssignedIdentitiesToUpdate returns a list of assignedIDs that need to be updated
// because of change in azureIdentity or azurerIdentityBinding
// returns 2 maps, first the assigned IDs currently on cluster, second the assignedID value to update with
func (c *Client) getAzureAssignedIdentitiesToUpdate(add, del map[string]aadpodid.AzureAssignedIdentity) (map[string]aadpodid.AzureAssignedIdentity, map[string]aadpodid.AzureAssignedIdentity) {
	beforeUpdate := make(map[string]aadpodid.AzureAssignedIdentity)
	afterUpdate := make(map[string]aadpodid.AzureAssignedIdentity)
	// no updates required as assigned identities will not be in both lists
	if len(add) == 0 || len(del) == 0 {
		return beforeUpdate, afterUpdate
	}
	for assignedIDName, addAssignedID := range add {
		if delAssignedID, exists := del[assignedIDName]; exists {
			// assigned identity exists in add and del list
			// update the assigned identity to the latest
			addAssignedID.ObjectMeta = delAssignedID.ObjectMeta
			beforeUpdate[assignedIDName] = delAssignedID
			afterUpdate[assignedIDName] = addAssignedID
			// since this is part of update, remove the assignedID from the add and del list
			delete(add, assignedIDName)
			delete(del, assignedIDName)
		}
	}
	return beforeUpdate, afterUpdate
}

func (c *Client) makeAssignedIDs(azID aadpodid.AzureIdentity, azBinding aadpodid.AzureIdentityBinding, podName, podNameSpace, nodeName string) (res *aadpodid.AzureAssignedIdentity, err error) {
	binding := azBinding
	id := azID

	labels := make(map[string]string)
	labels["nodename"] = nodeName

	oMeta := v1.ObjectMeta{
		Name:   c.getAssignedIDName(podName, podNameSpace, azID.Name),
		Labels: labels,
	}
	assignedID := &aadpodid.AzureAssignedIdentity{
		ObjectMeta: oMeta,
		Spec: aadpodid.AzureAssignedIdentitySpec{
			AzureIdentityRef: &id,
			AzureBindingRef:  &binding,
			Pod:              podName,
			PodNamespace:     podNameSpace,
			NodeName:         nodeName,
		},
		Status: aadpodid.AzureAssignedIdentityStatus{
			AvailableReplicas: 1,
		},
	}
	// if we are in namespaced mode (or az identity is namespaced)
	if c.IsNamespaced || aadpodid.IsNamespacedIdentity(&id) {
		assignedID.Namespace = azID.Namespace
	} else {
		// eventually this should be identity namespace
		// but to maintain back compat we will use existing
		// behavior
		assignedID.Namespace = "default"
	}

	klog.V(6).Infof("binding - %+v identity - %+v", azBinding, azID)
	klog.V(5).Infof("making assigned ID: %+v", assignedID)
	return assignedID, nil
}

func (c *Client) createAssignedIdentity(assignedID *aadpodid.AzureAssignedIdentity) error {
	err := c.CRDClient.CreateAssignedIdentity(assignedID)
	if err != nil {
		return err
	}
	return nil
}

func (c *Client) removeAssignedIdentity(assignedID *aadpodid.AzureAssignedIdentity) error {
	err := c.CRDClient.RemoveAssignedIdentity(assignedID)
	if err != nil {
		return err
	}
	return nil
}

func (c *Client) updateAssignedIdentity(assignedID *aadpodid.AzureAssignedIdentity) error {
	return c.CRDClient.UpdateAssignedIdentity(assignedID)
}

func (c *Client) appendToRemoveListForNode(resourceID, nodeName string, nodeMap map[string]trackUserAssignedMSIIds) {
	if trackList, ok := nodeMap[nodeName]; ok {
		trackList.removeUserAssignedMSIIDs = append(trackList.removeUserAssignedMSIIDs, resourceID)
		nodeMap[nodeName] = trackList
		return
	}
	nodeMap[nodeName] = trackUserAssignedMSIIds{removeUserAssignedMSIIDs: []string{resourceID}}
}

func (c *Client) appendToAddListForNode(resourceID, nodeName string, nodeMap map[string]trackUserAssignedMSIIds) {
	if trackList, ok := nodeMap[nodeName]; ok {
		trackList.addUserAssignedMSIIDs = append(trackList.addUserAssignedMSIIDs, resourceID)
		nodeMap[nodeName] = trackList
		return
	}
	nodeMap[nodeName] = trackUserAssignedMSIIds{addUserAssignedMSIIDs: []string{resourceID}}
}

func (c *Client) checkIfUserAssignedMSI(id aadpodid.AzureIdentity) bool {
	return id.Spec.Type == aadpodid.UserAssignedMSI
}

func (c *Client) getAssignedIDName(podName, podNameSpace, idName string) string {
	return podName + "-" + podNameSpace + "-" + idName
}

func (c *Client) checkIfMSIExistsOnNode(id *aadpodid.AzureIdentity, nodeName string, nodeMSIList []string) bool {
	for _, userAssignedMSI := range nodeMSIList {
		if strings.EqualFold(userAssignedMSI, id.Spec.ResourceID) {
			return true
		}
	}
	return false
}

func (c *Client) getUserMSIListForNode(nodeOrVMSSName string, isvmss bool) ([]string, error) {
	return c.CloudClient.GetUserMSIs(nodeOrVMSSName, isvmss)
}

func getIDKey(ns, name string) string {
	return strings.Join([]string{ns, name}, "/")
}

func (c *Client) convertIDListToMap(azureIdentities []aadpodid.AzureIdentity) (m map[string]aadpodid.AzureIdentity, err error) {
	m = make(map[string]aadpodid.AzureIdentity, len(azureIdentities))
	for _, azureIdentity := range azureIdentities {
		// validate the resourceID in azure identity for type 0 (UserAssignedMSI) to ensure format is as expected
		if c.checkIfUserAssignedMSI(azureIdentity) {
			err := utils.ValidateResourceID(azureIdentity.Spec.ResourceID)
			if err != nil {
				klog.Errorf("ignoring azure identity %s/%s, error: %+v", azureIdentity.Namespace, azureIdentity.Name, err)
				continue
			}
		}
		m[getIDKey(azureIdentity.Namespace, azureIdentity.Name)] = azureIdentity
	}
	return m, nil
}

func (c *Client) checkIfInUse(checkAssignedID aadpodid.AzureAssignedIdentity, assignedIDMap map[string]aadpodid.AzureAssignedIdentity, vmssGroups *vmssGroupList) (bool, error) {
	for _, assignedID := range assignedIDMap {
		checkID := checkAssignedID.Spec.AzureIdentityRef
		id := assignedID.Spec.AzureIdentityRef
		// If they have the same client id, reside on the same node but the pod name is different, then the
		// assigned id is in use.
		// This is applicable only for user assigned MSI since that is node specific. Ignore other cases.
		if checkID.Spec.Type != aadpodid.UserAssignedMSI {
			continue
		}

		if checkAssignedID.Spec.Pod == assignedID.Spec.Pod {
			// No need to do the rest of the checks in this case, since it's the same assignment
			// The same identity won't be assigned to a pod twice, so it's the same reference.
			continue
		}

		if checkID.Spec.ClientID != id.Spec.ClientID {
			continue
		}

		if checkAssignedID.Spec.NodeName == assignedID.Spec.NodeName {
			return true, nil
		}

		vmss, err := getVMSSGroupFromPossiblyUnreferencedNode(c.NodeClient, vmssGroups, checkAssignedID.Spec.NodeName)
		if err != nil {
			return false, err
		}

		// check if this identity is used on another node in the same vmss
		// This check is needed because vmss identities currently operate on all nodes
		// in the vmss not just a single node.
		if vmss != nil && vmss.hasNode(assignedID.Spec.NodeName) {
			return true, nil
		}
	}

	return false, nil
}

func (c *Client) getUniqueIDs(idList []string) []string {
	idSet := make(map[string]struct{})
	var uniqueList []string

	for _, id := range idList {
		idSet[id] = struct{}{}
	}
	for id := range idSet {
		uniqueList = append(uniqueList, id)
	}
	return uniqueList
}

func (c *Client) updateAssignedIdentityStatus(assignedID *aadpodid.AzureAssignedIdentity, status string) error {
	return c.CRDClient.UpdateAzureAssignedIdentityStatus(assignedID, status)
}

func (c *Client) updateNodeAndDeps(newAssignedIDs map[string]aadpodid.AzureAssignedIdentity, nodeMap map[string]trackUserAssignedMSIIds, nodeRefs map[string]bool, wg *sync.WaitGroup) {
	for nodeName, nodeTrackList := range nodeMap {
		wg.Add(1)
		go c.updateUserMSI(newAssignedIDs, nodeName, nodeTrackList, nodeRefs, wg)
	}
}

func (c *Client) updateUserMSI(newAssignedIDs map[string]aadpodid.AzureAssignedIdentity, nodeOrVMSSName string, nodeTrackList trackUserAssignedMSIIds, nodeRefs map[string]bool, wg *sync.WaitGroup) {
	defer wg.Done()
	beginAdding := time.Now()
	klog.Infof("processing node %s, add [%d], del [%d], update [%d]", nodeOrVMSSName,
		len(nodeTrackList.assignedIDsToCreate), len(nodeTrackList.assignedIDsToDelete), len(nodeTrackList.assignedIDsToUpdate))

	ctx := context.TODO()
	// We have to ensure that we don't overwhelm the API server with too many
	// requests in flight. We use a token based approach implemented using semaphore to
	// ensure that only given createDeleteBatch requests are in flight at any point in time.
	// Note that at this point in the code path, we are doing this in parallel per node/VMSS already.
	semCreateOrUpdate := semaphore.NewWeighted(c.createDeleteBatch)

	for _, createID := range nodeTrackList.assignedIDsToCreate {
		if err := semCreateOrUpdate.Acquire(ctx, 1); err != nil {
			klog.Errorf("failed to acquire semaphore in the create loop, error: %+v", err)
			return
		}
		go func(assignedID aadpodid.AzureAssignedIdentity) {
			defer semCreateOrUpdate.Release(1)
			if assignedID.Status.Status == "" {
				binding := assignedID.Spec.AzureBindingRef

				// this is the state when the azure assigned identity is yet to be created
				klog.V(5).Infof("initiating AzureAssignedIdentity creation for pod - %s, binding - %s", assignedID.Spec.Pod, binding.Name)

				assignedID.Status.Status = aadpodid.AssignedIDCreated
				err := c.createAssignedIdentity(&assignedID)
				if err != nil {
					message := fmt.Sprintf("failed to create AzureAssignedIdentity %s/%s for pod %s/%s, error: %+v", assignedID.Name, assignedID.Namespace, assignedID.Spec.PodNamespace, assignedID.Spec.Pod, err)
					c.EventRecorder.Event(binding, corev1.EventTypeWarning, "binding apply error", message)
					klog.Error(message)
				}
			}
		}(createID)
	}

	for _, updateID := range nodeTrackList.assignedIDsToUpdate {
		if err := semCreateOrUpdate.Acquire(ctx, 1); err != nil {
			klog.Errorf("failed to acquire semaphore in the update loop, error: %+v", err)
			return
		}
		go func(assignedID aadpodid.AzureAssignedIdentity) {
			defer semCreateOrUpdate.Release(1)
			if assignedID.Status.Status == "" {
				binding := assignedID.Spec.AzureBindingRef

				// this is the state when the azure assigned identity is yet to be created
				klog.V(5).Infof("initiating assigned id creation for pod - %s, binding - %s", assignedID.Spec.Pod, binding.Name)

				assignedID.Status.Status = aadpodid.AssignedIDCreated
				err := c.updateAssignedIdentity(&assignedID)
				if err != nil {
					message := fmt.Sprintf("failed to update AzureAssignedIdentity %s/%s for pod %s/%s, error: %+v", assignedID.Namespace, assignedID.Name, assignedID.Spec.Pod, assignedID.Spec.PodNamespace, err)
					c.EventRecorder.Event(binding, corev1.EventTypeWarning, "binding apply error", message)
					klog.Error(message)
				}
			}
		}(updateID)
	}

	// Ensure that all creates are complete
	if err := semCreateOrUpdate.Acquire(ctx, c.createDeleteBatch); err != nil {
		klog.Errorf("failed to acquire semaphore at the end of creates, error: %+v", err)
		return
	}
	// generate unique list so we don't make multiple calls to assign/remove same id
	addUserAssignedMSIIDs := c.getUniqueIDs(nodeTrackList.addUserAssignedMSIIDs)
	removeUserAssignedMSIIDs := c.getUniqueIDs(nodeTrackList.removeUserAssignedMSIIDs)
	createOrUpdateList := append([]aadpodid.AzureAssignedIdentity{}, nodeTrackList.assignedIDsToCreate...)
	createOrUpdateList = append(createOrUpdateList, nodeTrackList.assignedIDsToUpdate...)

	err := c.CloudClient.UpdateUserMSI(addUserAssignedMSIIDs, removeUserAssignedMSIIDs, nodeOrVMSSName, nodeTrackList.isvmss)
	if err != nil {
		klog.Errorf("failed to update user-assigned identities on node %s (add [%d], del [%d], update[%d]), error: %+v", nodeOrVMSSName, len(nodeTrackList.assignedIDsToCreate), len(nodeTrackList.assignedIDsToDelete), len(nodeTrackList.assignedIDsToUpdate), err)
		idList, getErr := c.getUserMSIListForNode(nodeOrVMSSName, nodeTrackList.isvmss)
		if getErr != nil {
			klog.Errorf("failed to get a list of user-assigned identites from node %s, error: %+v", nodeOrVMSSName, getErr)
			return
		}

		for _, createID := range createOrUpdateList {
			createID := createID // avoid implicit memory aliasing in for loop
			id := createID.Spec.AzureIdentityRef
			binding := createID.Spec.AzureBindingRef

			isUserAssignedMSI := c.checkIfUserAssignedMSI(*id)
			idExistsOnNode := c.checkIfMSIExistsOnNode(id, createID.Spec.NodeName, idList)

			if isUserAssignedMSI && !idExistsOnNode {
				message := fmt.Sprintf("failed to apply binding %s/%s node %s for pod %s/%s, error: %+v", binding.Namespace, binding.Name, createID.Spec.NodeName, createID.Spec.PodNamespace, createID.Spec.Pod, err)
				c.EventRecorder.Event(binding, corev1.EventTypeWarning, "binding apply error", message)
				klog.Error(message)
				continue
			}
			// the identity was successfully assigned to the node
			c.EventRecorder.Event(binding, corev1.EventTypeNormal, "binding applied",
				fmt.Sprintf("binding %s applied on node %s for pod %s", binding.Name, createID.Spec.NodeName, createID.Name))

			klog.Infof("identity %s/%s has successfully been assigned to node %s", id.Namespace, id.Name, createID.Spec.NodeName)

			// Identity is successfully assigned to node, so update the status of assigned identity to assigned
			if updateErr := c.updateAssignedIdentityStatus(&createID, aadpodid.AssignedIDAssigned); updateErr != nil {
				message := fmt.Sprintf("failed to update AzureAssignedIdentity %s/%s status to %s for pod %s/%s, error: %+v", createID.Namespace, createID.Name, aadpodid.AssignedIDAssigned, createID.Spec.PodNamespace, createID.Spec.Pod, updateErr)
				c.EventRecorder.Event(&createID, corev1.EventTypeWarning, "status update error", message)
				klog.Error(message)
			}

			isCreateOperation := false
			for _, i := range nodeTrackList.assignedIDsToCreate {
				if reflect.DeepEqual(createID, i) {
					isCreateOperation = true
					break
				}
			}
			if isCreateOperation {
				stats.Increment(stats.TotalAzureAssignedIdentitiesCreated, 1)
			} else {
				stats.Increment(stats.TotalAzureAssignedIdentitiesUpdated, 1)
			}
		}

		for _, delID := range nodeTrackList.assignedIDsToDelete {
			delID := delID // avoid implicit memory aliasing in for loop
			id := delID.Spec.AzureIdentityRef
			removedBinding := delID.Spec.AzureBindingRef
			isUserAssignedMSI := c.checkIfUserAssignedMSI(*id)
			idExistsOnNode := c.checkIfMSIExistsOnNode(id, delID.Spec.NodeName, idList)
			vmssGroups, getErr := getVMSSGroups(c.NodeClient, nodeRefs)
			if getErr != nil {
				klog.Errorf("failed to get VMSS groups, error: %+v", getErr)
				continue
			}
			inUse, checkErr := c.checkIfInUse(delID, newAssignedIDs, vmssGroups)
			if checkErr != nil {
				klog.Errorf("failed to check if identity is in use, error: %+v", getErr)
				continue
			}
			// the identity still exists on node, which means removing the identity from the node failed
			if isUserAssignedMSI && !inUse && idExistsOnNode {
				klog.Errorf("failed to remove AzureIdentityBinding %s from node %s for pod %s/%s, error: %+v", removedBinding.Name, delID.Spec.NodeName, delID.Spec.PodNamespace, delID.Spec.Pod, err)
				continue
			}

			klog.Infof("updating msis on node %s failed, but identity %s/%s has successfully been removed from node", delID.Spec.NodeName, id.Namespace, id.Name)

			// remove assigned identity crd from cluster as the identity has successfully been removed from the node
			err = c.removeAssignedIdentity(&delID)
			if err != nil {
				klog.Errorf("failed to remove AzureAssignedIdentity %s, error: %+v", delID.Name, err)
				continue
			}
			klog.Infof("deleted assigned identity %s/%s", delID.Namespace, delID.Name)
			stats.Increment(stats.TotalAzureAssignedIdentitiesDeleted, 1)
		}
		stats.Put(stats.TotalAzureAssignedIdentitiesCreateOrUpdate, time.Since(beginAdding))
		return
	}

	semUpdate := semaphore.NewWeighted(c.createDeleteBatch)

	for _, createID := range createOrUpdateList {
		if err := semUpdate.Acquire(ctx, 1); err != nil {
			klog.Errorf("failed to acquire semaphore in the update loop, error: %+v", err)
			return
		}
		go func(assignedID aadpodid.AzureAssignedIdentity) {
			defer semUpdate.Release(1)
			binding := assignedID.Spec.AzureBindingRef
			// update the status to assigned for assigned identity as identity was successfully assigned to node.
			err := c.updateAssignedIdentityStatus(&assignedID, aadpodid.AssignedIDAssigned)
			if err != nil {
				message := fmt.Sprintf("failed to update AzureAssignedIdentity %s/%s status to %s for pod %s, error: %+v", assignedID.Namespace, assignedID.Name, aadpodid.AssignedIDAssigned, assignedID.Spec.Pod, err.Error())
				c.EventRecorder.Event(&assignedID, corev1.EventTypeWarning, "status update error", message)
				klog.Error(message)
				return
			}
			c.EventRecorder.Event(binding, corev1.EventTypeNormal, "binding applied",
				fmt.Sprintf("Binding %s applied on node %s for pod %s", binding.Name, assignedID.Spec.NodeName, assignedID.Name))
		}(createID)
	}

	// Ensure that all updates are complete
	if err := semUpdate.Acquire(ctx, c.createDeleteBatch); err != nil {
		klog.Errorf("failed to acquire semaphore at the end of updates, error: %+v", err)
		return
	}

	semDel := semaphore.NewWeighted(c.createDeleteBatch)

	for _, delID := range nodeTrackList.assignedIDsToDelete {
		if err := semDel.Acquire(ctx, 1); err != nil {
			klog.Errorf("failed to acquire semaphore in the delete loop, error: %+v", err)
			return
		}
		go func(assignedID aadpodid.AzureAssignedIdentity) {
			defer semDel.Release(1)
			// update the status for the assigned identity to Unassigned as the identity has been successfully removed from node.
			// this will ensure on next sync loop we only try to delete the assigned identity instead of doing everything.
			err := c.updateAssignedIdentityStatus(&assignedID, aadpodid.AssignedIDUnAssigned)
			if err != nil {
				message := fmt.Sprintf("failed to update AzureAssignedIdentity %s/%s status to %s for pod %s/%s, error: %+v", assignedID.Namespace, assignedID.Name, aadpodid.AssignedIDUnAssigned, assignedID.Spec.PodNamespace, assignedID.Spec.Pod, err)
				c.EventRecorder.Event(&assignedID, corev1.EventTypeWarning, "status update error", message)
				klog.Error(message)
				return
			}
			// remove assigned identity crd from cluster as the identity has successfully been removed from the node
			err = c.removeAssignedIdentity(&assignedID)
			if err != nil {
				klog.Errorf("failed to remove AzureAssignedIdentity %s/%s, error: %+v", assignedID.Namespace, assignedID.Name, err)
				return
			}
			klog.V(1).Infof("deleted assigned identity %s/%s", assignedID.Namespace, assignedID.Name)
		}(delID)
	}

	// Ensure that all deletes are complete
	if err := semDel.Acquire(ctx, c.createDeleteBatch); err != nil {
		klog.Errorf("failed to acquire semaphore at the end of deletes, error: %+v", err)
		return
	}

	stats.Increment(stats.TotalAzureAssignedIdentitiesCreated, len(nodeTrackList.assignedIDsToCreate))
	stats.Increment(stats.TotalAzureAssignedIdentitiesUpdated, len(nodeTrackList.assignedIDsToUpdate))
	stats.Increment(stats.TotalAzureAssignedIdentitiesDeleted, len(nodeTrackList.assignedIDsToDelete))
	stats.Put(stats.TotalAzureAssignedIdentitiesCreateOrUpdate, time.Since(beginAdding))
}

// cleanUpAllAssignedIdentitiesOnNode deletes all assigned identities associated with a the node
func (c *Client) cleanUpAllAssignedIdentitiesOnNode(node string, nodeTrackList trackUserAssignedMSIIds, wg *sync.WaitGroup) {
	defer wg.Done()
	klog.Infof("deleting all assigned identites for %s as node not found", node)
	for _, deleteID := range nodeTrackList.assignedIDsToDelete {
		deleteID := deleteID // avoid implicit memory aliasing in for loop
		binding := deleteID.Spec.AzureBindingRef

		err := c.removeAssignedIdentity(&deleteID)
		if err != nil {
			message := fmt.Sprintf("failed to remove AzureIdentityBinding %s/%s from node %s for pod %s/%s, error: %v", binding.Namespace, binding.Name, deleteID.Spec.NodeName, deleteID.Spec.PodNamespace, deleteID.Spec.Pod, err)
			c.EventRecorder.Event(binding, corev1.EventTypeWarning, "binding remove error", message)
			klog.Error(message)
			continue
		}
		c.EventRecorder.Event(binding, corev1.EventTypeNormal, "binding removed",
			fmt.Sprintf("Binding %s removed from node %s for pod %s", binding.Name, deleteID.Spec.NodeName, deleteID.Spec.Pod))
	}
}

// consolidateVMSSNodes takes a list of all nodes that are part of the current sync cycle, checks if the nodes are
// part of vmss and combines the vmss nodes into vmss name. This consolidation is needed because vmss identities
// currently operate on all nodes in the vmss not just a single node.
func (c *Client) consolidateVMSSNodes(nodeMap map[string]trackUserAssignedMSIIds, wg *sync.WaitGroup) {
	vmssMap := make(map[string][]string)

	for nodeName, nodeTrackList := range nodeMap {
		node, err := c.NodeClient.Get(nodeName)
		if err != nil && !strings.Contains(err.Error(), "not found") {
			klog.Errorf("failed to get node %s, error: %+v", nodeName, err)
			continue
		}
		if err != nil && strings.Contains(err.Error(), "not found") {
			klog.Warningf("failed to get node %s while updating user-assigned identities, error: %+v", nodeName, err)
			wg.Add(1)
			// node is no longer found in the cluster, all the assigned identities that were created in this sync loop
			// and those that already exist for this node need to be deleted.
			go c.cleanUpAllAssignedIdentitiesOnNode(nodeName, nodeTrackList, wg)
			delete(nodeMap, nodeName)
			continue
		}
		vmssName, isvmss, err := isVMSS(node)
		if err != nil {
			klog.Errorf("failed to check if node %s is VMSS, error: %+v", nodeName, err)
			continue
		}
		if isvmss {
			if nodes, ok := vmssMap[vmssName]; ok {
				nodes = append(nodes, nodeName)
				vmssMap[vmssName] = nodes
				continue
			}
			vmssMap[vmssName] = []string{nodeName}
		}
	}

	// aggregate vmss nodes into vmss name
	for vmssName, vmssNodes := range vmssMap {
		if len(vmssNodes) < 1 {
			continue
		}

		vmssTrackList := trackUserAssignedMSIIds{}
		for _, vmssNode := range vmssNodes {
			vmssTrackList.addUserAssignedMSIIDs = append(vmssTrackList.addUserAssignedMSIIDs, nodeMap[vmssNode].addUserAssignedMSIIDs...)
			vmssTrackList.removeUserAssignedMSIIDs = append(vmssTrackList.removeUserAssignedMSIIDs, nodeMap[vmssNode].removeUserAssignedMSIIDs...)
			vmssTrackList.assignedIDsToCreate = append(vmssTrackList.assignedIDsToCreate, nodeMap[vmssNode].assignedIDsToCreate...)
			vmssTrackList.assignedIDsToDelete = append(vmssTrackList.assignedIDsToDelete, nodeMap[vmssNode].assignedIDsToDelete...)
			vmssTrackList.assignedIDsToUpdate = append(vmssTrackList.assignedIDsToUpdate, nodeMap[vmssNode].assignedIDsToUpdate...)
			vmssTrackList.isvmss = true

			delete(nodeMap, vmssNode)
			nodeMap[getVMSSName(vmssName)] = vmssTrackList
		}
	}
}

// checkIfIdentityImmutable checks if the identity is immutable
// if identity is immutable, then it will not be removed from underlying node/vmss
// returns true if identity is immutable
func (c *Client) checkIfIdentityImmutable(id string) bool {
	// no immutable identity list defined, then identity is not immutable and can be safely removed
	if c.ImmutableUserMSIsMap == nil {
		return false
	}
	// identity is immutable, so should not be deleted from the underlying node/vmss
	if _, exists := c.ImmutableUserMSIsMap[id]; exists {
		return true
	}
	return false
}

// generateIdentityAssignmentState generates the current and desired state of each node's identity
// assignments based on an existing list of AzureAssignedIdentity as the source of truth.
func (c *Client) generateIdentityAssignmentState() (currentState map[string]map[string]bool, desiredState map[string]map[string]bool, isVMSSMap map[string]bool, err error) {
	type nodeMetadata struct {
		nodeName string
		isVMSS   bool
	}

	assignedIDs, err := c.CRDClient.ListAssignedIDs()
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to list AzureAssignedIdentities, error: %+v", err)
	}

	nodeMetadataCache := make(map[string]nodeMetadata)
	isVMSSMap = make(map[string]bool)
	currentState = make(map[string]map[string]bool)
	desiredState = make(map[string]map[string]bool)
	for _, assignedID := range *assignedIDs {
		if _, ok := nodeMetadataCache[assignedID.Spec.NodeName]; !ok {
			node, err := c.NodeClient.Get(assignedID.Spec.NodeName)
			if err != nil {
				return nil, nil, nil, fmt.Errorf("failed to get node %s, error: %+v", assignedID.Spec.NodeName, err)
			}

			nodeName, isVMSS, err := isVMSS(node)
			if err != nil {
				return nil, nil, nil, fmt.Errorf("failed to check if node %s is VMSS, error: %+v", assignedID.Spec.NodeName, err)
			} else if isVMSS {
				nodeName = getVMSSName(nodeName)
			} else {
				// VM node name does not require conversion
				nodeName = assignedID.Spec.NodeName
			}

			// cache node metadata to avoid excessive GET calls
			nodeMetadataCache[assignedID.Spec.NodeName] = nodeMetadata{
				nodeName: nodeName,
				isVMSS:   isVMSS,
			}
		}

		nodeName := nodeMetadataCache[assignedID.Spec.NodeName].nodeName
		isVMSS := nodeMetadataCache[assignedID.Spec.NodeName].isVMSS
		isVMSSMap[nodeName] = isVMSS

		// only consider AzureAssignedIdentities in ASSIGNED state
		// do not consider AzureAssignedIdentities in CREATED state because they are either:
		// 1. in the process of assigning the identities on Azure or
		// 2. encountering errors when assigning identities on Azure
		if assignedID.Status.Status == aadpodid.AssignedIDAssigned && assignedID.Spec.AzureIdentityRef.Spec.Type == aadpodid.UserAssignedMSI {
			if _, ok := desiredState[nodeName]; !ok {
				desiredState[nodeName] = make(map[string]bool)
			}
			desiredState[nodeName][assignedID.Spec.AzureIdentityRef.Spec.ResourceID] = true
		}

		if _, ok := currentState[nodeName]; !ok {
			currentState[nodeName] = make(map[string]bool)
			idList, err := c.getUserMSIListForNode(nodeName, isVMSS)
			if err != nil {
				return nil, nil, nil, fmt.Errorf("failed to get a list of user-assigned identites from node %s, error: %+v", nodeName, err)
			}

			for _, identityResourceID := range idList {
				currentState[nodeName][identityResourceID] = true
			}
		}
	}

	return currentState, desiredState, isVMSSMap, nil
}

// generateIdentityAssignmentDiff perform a diff between current
// and desired state of identity assignment on Azure and returns
// a map with the node name as the key and a list of user-assigned
// identities we should assign to the node as the value.
func generateIdentityAssignmentDiff(currentState map[string]map[string]bool, desiredState map[string]map[string]bool) map[string][]string {
	diff := make(map[string][]string)
	for nodeName, identityResourceIDs := range desiredState {
		var identitiesToAssign []string
		for identityResourceID := range identityResourceIDs {
			if _, ok := currentState[nodeName]; ok && currentState[nodeName][identityResourceID] {
				continue
			}
			identitiesToAssign = append(identitiesToAssign, identityResourceID)
		}

		if len(identitiesToAssign) > 0 {
			diff[nodeName] = identitiesToAssign
		}
	}

	return diff
}

// reconcileIdentityAssignment uses the existing list of AzureAssignedIdentities
// as the single source of truth and reconciles identity assignment on Azure.
func (c *Client) reconcileIdentityAssignment() {
	currentState, desiredState, isVMSSMap, err := c.generateIdentityAssignmentState()
	if err != nil {
		klog.Errorf("failed to generate identity assignment state, error: %+v", err)
		return
	}

	klog.V(6).Infof("current state of identity assignment on Azure: %+v", currentState)
	klog.V(6).Infof("desired state of identity assignment on Azure: %+v", desiredState)

	diff := generateIdentityAssignmentDiff(currentState, desiredState)
	for nodeNameOnAzure, identitiesToAssign := range diff {
		klog.Infof("reconciling identity assignment for %v on node %s", identitiesToAssign, nodeNameOnAzure)
		if err := c.CloudClient.UpdateUserMSI(identitiesToAssign, nil, nodeNameOnAzure, isVMSSMap[nodeNameOnAzure]); err != nil {
			klog.Errorf("failed to update user-assigned identities on node %s, error: %+v", nodeNameOnAzure, err)
		}
	}
}
