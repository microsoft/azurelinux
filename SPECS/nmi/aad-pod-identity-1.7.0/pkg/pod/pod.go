package pod

import (
	"strings"
	"time"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	"github.com/Azure/aad-pod-identity/pkg/stats"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/labels"
	"k8s.io/apimachinery/pkg/selection"
	"k8s.io/client-go/informers"
	informersv1 "k8s.io/client-go/informers/core/v1"
	"k8s.io/client-go/tools/cache"
	"k8s.io/klog/v2"
)

// Client represents new pod client
type Client struct {
	PodWatcher informersv1.PodInformer
}

// ClientInt represents pod client interface
type ClientInt interface {
	GetPods() (pods []*v1.Pod, err error)
	Start(exit <-chan struct{})
}

// NewPodClient returns new pod client
func NewPodClient(i informers.SharedInformerFactory, eventCh chan aadpodid.EventType) (c ClientInt) {
	podInformer := i.Core().V1().Pods()
	addPodHandler(podInformer, eventCh)

	return &Client{
		PodWatcher: podInformer,
	}
}

func addPodHandler(i informersv1.PodInformer, eventCh chan aadpodid.EventType) {
	i.Informer().AddEventHandler(
		cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				klog.V(6).Infof("pod created")
				eventCh <- aadpodid.PodCreated
			},
			DeleteFunc: func(obj interface{}) {
				klog.V(6).Infof("pod deleted")
				eventCh <- aadpodid.PodDeleted
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				// We are only interested in updates to pod if the node or label changes.
				// Having this check will ensure that mic sync loop does not do extra work
				// for every pod update.
				oldPod, newPod := oldObj.(*v1.Pod), newObj.(*v1.Pod)
				if oldPod.Spec.NodeName != newPod.Spec.NodeName || oldPod.ObjectMeta.Labels[aadpodid.CRDLabelKey] != newPod.ObjectMeta.Labels[aadpodid.CRDLabelKey] {
					klog.V(6).Infof("pod updated")
					eventCh <- aadpodid.PodUpdated
				}
			},
		},
	)
}

func (c *Client) syncCache(exit <-chan struct{}) {
	cacheSyncStarted := time.Now()
	klog.V(6).Infof("wait for cache to sync")
	if !cache.WaitForCacheSync(exit, c.PodWatcher.Informer().HasSynced) {
		klog.Error("wait for pod cache sync failed")
		return
	}
	klog.Infof("pod cache synchronized. Took %s", time.Since(cacheSyncStarted).String())
}

// Start starts watching for any pod-related changes.
func (c *Client) Start(exit <-chan struct{}) {
	go c.PodWatcher.Informer().Run(exit)
	c.syncCache(exit)
	klog.Info("pod watcher started !!")
}

// GetPods returns list of all pods
func (c *Client) GetPods() (pods []*v1.Pod, err error) {
	begin := time.Now()
	crdReq, err := labels.NewRequirement(aadpodid.CRDLabelKey, selection.Exists, nil)
	if err != nil {
		return nil, err
	}
	crdSelector := labels.NewSelector().Add(*crdReq)
	listPods, err := c.PodWatcher.Lister().List(crdSelector)
	if err != nil {
		return nil, err
	}
	stats.Put(stats.PodList, time.Since(begin))
	return listPods, nil
}

// IsPodExcepted returns true if pod label is part of exception crd
func IsPodExcepted(podLabels map[string]string, exceptionList []aadpodid.AzurePodIdentityException) bool {
	return len(exceptionList) > 0 && labelInExceptionList(podLabels, exceptionList)
}

// labelInExceptionList checks if the labels defined in azurepodidentityexception match label defined in pods
func labelInExceptionList(podLabels map[string]string, exceptionList []aadpodid.AzurePodIdentityException) bool {
	for _, exception := range exceptionList {
		for exceptionLabelKey, exceptionLabelValue := range exception.Spec.PodLabels {
			if val, ok := podLabels[exceptionLabelKey]; ok {
				if strings.EqualFold(val, exceptionLabelValue) {
					return true
				}
			}
		}
	}
	return false
}
