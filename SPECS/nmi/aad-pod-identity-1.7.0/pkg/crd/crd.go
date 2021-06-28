package crd

import (
	"context"
	"encoding/json"
	"fmt"
	"reflect"
	"strings"
	"time"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/stats"

	apierrors "k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/api/meta"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/informers/internalinterfaces"
	clientgoscheme "k8s.io/client-go/kubernetes/scheme"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/klog/v2"
)

const (
	finalizerName = "azureassignedidentity.finalizers.aadpodidentity.k8s.io"
)

// Client represents all the watchers
type Client struct {
	rest                         *rest.RESTClient
	BindingInformer              cache.SharedInformer
	IDInformer                   cache.SharedInformer
	AssignedIDInformer           cache.SharedInformer
	PodIdentityExceptionInformer cache.SharedInformer
	reporter                     *metrics.Reporter
}

// ClientInt is an abstraction used to interact with CRDs.
type ClientInt interface {
	Start(exit <-chan struct{})
	SyncCache(exit <-chan struct{}, initial bool, cacheSyncs ...cache.InformerSynced)
	SyncCacheAll(exit <-chan struct{}, initial bool)
	RemoveAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) error
	CreateAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) error
	UpdateAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) error
	UpdateAzureAssignedIdentityStatus(assignedIdentity *aadpodid.AzureAssignedIdentity, status string) error
	UpgradeAll() error
	ListBindings() (res *[]aadpodid.AzureIdentityBinding, err error)
	ListAssignedIDs() (res *[]aadpodid.AzureAssignedIdentity, err error)
	ListAssignedIDsInMap() (res map[string]aadpodid.AzureAssignedIdentity, err error)
	ListIds() (res *[]aadpodid.AzureIdentity, err error)
	ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error)
	ListPodIdentityExceptions(ns string) (res *[]aadpodid.AzurePodIdentityException, err error)
}

// NewCRDClientLite returns a new CRD lite client and error if any.
func NewCRDClientLite(config *rest.Config, nodeName string, scale, isStandardMode bool) (crdClient *Client, err error) {
	restClient, err := newRestClient(config)
	if err != nil {
		return nil, err
	}

	var assignedIDListInformer, bindingListInformer, idListInformer cache.SharedInformer

	// assigned identity informer is required only for standard mode
	if isStandardMode {
		var assignedIDListWatch *cache.ListWatch
		if scale {
			assignedIDListWatch = newAssignedIDNodeListWatch(restClient, nodeName)
		} else {
			assignedIDListWatch = newAssignedIDListWatch(restClient)
		}

		assignedIDListInformer, err = newAssignedIDInformer(assignedIDListWatch)
		if err != nil {
			return nil, err
		}
	} else {
		// creating binding and identity list informers for non standard mode
		if bindingListInformer, err = newBindingInformerLite(newBindingListWatch(restClient)); err != nil {
			return nil, err
		}
		if idListInformer, err = newIDInformerLite(newIDListWatch(restClient)); err != nil {
			return nil, err
		}
	}
	podIdentityExceptionListWatch := newPodIdentityExceptionListWatch(restClient)
	podIdentityExceptionInformer, err := newPodIdentityExceptionInformer(podIdentityExceptionListWatch)
	if err != nil {
		return nil, err
	}

	reporter, err := metrics.NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}

	return &Client{
		AssignedIDInformer:           assignedIDListInformer,
		PodIdentityExceptionInformer: podIdentityExceptionInformer,
		BindingInformer:              bindingListInformer,
		IDInformer:                   idListInformer,
		rest:                         restClient,
		reporter:                     reporter,
	}, nil
}

// NewCRDClient returns a new CRD client and error if any.
func NewCRDClient(config *rest.Config, eventCh chan aadpodid.EventType) (crdClient *Client, err error) {
	restClient, err := newRestClient(config)
	if err != nil {
		return nil, err
	}

	bindingListWatch := newBindingListWatch(restClient)
	bindingInformer, err := newBindingInformer(restClient, eventCh, bindingListWatch)
	if err != nil {
		return nil, err
	}

	idListWatch := newIDListWatch(restClient)
	idInformer, err := newIDInformer(restClient, eventCh, idListWatch)
	if err != nil {
		return nil, err
	}

	assignedIDListWatch := newAssignedIDListWatch(restClient)
	assignedIDListInformer, err := newAssignedIDInformer(assignedIDListWatch)
	if err != nil {
		return nil, err
	}

	reporter, err := metrics.NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}

	return &Client{
		rest:               restClient,
		BindingInformer:    bindingInformer,
		IDInformer:         idInformer,
		AssignedIDInformer: assignedIDListInformer,
		reporter:           reporter,
	}, nil
}

func newRestClient(config *rest.Config) (r *rest.RESTClient, err error) {
	crdconfig := *config
	crdconfig.GroupVersion = &schema.GroupVersion{Group: aadpodv1.CRDGroup, Version: aadpodv1.CRDVersion}
	crdconfig.APIPath = "/apis"
	crdconfig.ContentType = runtime.ContentTypeJSON
	scheme := runtime.NewScheme()

	scheme.AddKnownTypes(*crdconfig.GroupVersion,
		&aadpodv1.AzureIdentity{},
		&aadpodv1.AzureIdentityList{},
		&aadpodv1.AzureIdentityBinding{},
		&aadpodv1.AzureIdentityBindingList{},
		&aadpodv1.AzureAssignedIdentity{},
		&aadpodv1.AzureAssignedIdentityList{},
		&aadpodv1.AzurePodIdentityException{},
		&aadpodv1.AzurePodIdentityExceptionList{},
	)

	if err := clientgoscheme.AddToScheme(scheme); err != nil {
		return nil, err
	}

	crdconfig.NegotiatedSerializer = serializer.WithoutConversionCodecFactory{CodecFactory: serializer.NewCodecFactory(scheme)}

	// Client interacting with our CRDs
	restClient, err := rest.RESTClientFor(&crdconfig)
	if err != nil {
		return nil, err
	}
	return restClient, nil
}

func newBindingListWatch(r *rest.RESTClient) *cache.ListWatch {
	return cache.NewListWatchFromClient(r, aadpodv1.AzureIDBindingResource, v1.NamespaceAll, fields.Everything())
}

func newBindingInformer(r *rest.RESTClient, eventCh chan aadpodid.EventType, lw *cache.ListWatch) (cache.SharedInformer, error) {
	azBindingInformer := cache.NewSharedInformer(
		lw,
		&aadpodv1.AzureIdentityBinding{},
		time.Minute*10)
	if azBindingInformer == nil {
		return nil, fmt.Errorf("failed to create watcher for %s", aadpodv1.AzureIDBindingResource)
	}
	azBindingInformer.AddEventHandler(
		cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				klog.V(6).Infof("binding created")
				eventCh <- aadpodid.BindingCreated
			},
			DeleteFunc: func(obj interface{}) {
				klog.V(6).Infof("binding deleted")
				eventCh <- aadpodid.BindingDeleted
			},
			UpdateFunc: func(OldObj, newObj interface{}) {
				klog.V(6).Infof("binding updated")
				eventCh <- aadpodid.BindingUpdated
			},
		},
	)
	return azBindingInformer, nil
}

func newIDListWatch(r *rest.RESTClient) *cache.ListWatch {
	return cache.NewListWatchFromClient(r, aadpodv1.AzureIDResource, v1.NamespaceAll, fields.Everything())
}

func newIDInformer(r *rest.RESTClient, eventCh chan aadpodid.EventType, lw *cache.ListWatch) (cache.SharedInformer, error) {
	azIDInformer := cache.NewSharedInformer(
		lw,
		&aadpodv1.AzureIdentity{},
		time.Minute*10)
	if azIDInformer == nil {
		return nil, fmt.Errorf("failed to create watcher for %s", aadpodv1.AzureIDResource)
	}
	azIDInformer.AddEventHandler(
		cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				klog.V(6).Infof("identity created")
				eventCh <- aadpodid.IdentityCreated
			},
			DeleteFunc: func(obj interface{}) {
				klog.V(6).Infof("identity deleted")
				eventCh <- aadpodid.IdentityDeleted
			},
			UpdateFunc: func(OldObj, newObj interface{}) {
				klog.V(6).Infof("identity updated")
				eventCh <- aadpodid.IdentityUpdated
			},
		},
	)
	return azIDInformer, nil
}

// NodeNameFilter - CRDs do not yet support field selectors. Instead of that we
// apply labels with node name and then later use the NodeNameFilter to tweak
// options to filter using nodename label.
func NodeNameFilter(nodeName string) internalinterfaces.TweakListOptionsFunc {
	return func(l *v1.ListOptions) {
		if l == nil {
			l = &v1.ListOptions{}
		}
		l.LabelSelector = l.LabelSelector + "nodename=" + nodeName
	}
}

func newAssignedIDNodeListWatch(r *rest.RESTClient, nodeName string) *cache.ListWatch {
	return cache.NewFilteredListWatchFromClient(r, aadpodv1.AzureAssignedIDResource, v1.NamespaceAll, NodeNameFilter(nodeName))
}

func newAssignedIDListWatch(r *rest.RESTClient) *cache.ListWatch {
	return cache.NewListWatchFromClient(r, aadpodv1.AzureAssignedIDResource, v1.NamespaceAll, fields.Everything())
}

func newAssignedIDInformer(lw *cache.ListWatch) (cache.SharedInformer, error) {
	azAssignedIDInformer := cache.NewSharedInformer(lw, &aadpodv1.AzureAssignedIdentity{}, time.Minute*10)
	if azAssignedIDInformer == nil {
		return nil, fmt.Errorf("failed to create %s informer", aadpodv1.AzureAssignedIDResource)
	}
	return azAssignedIDInformer, nil
}

func newBindingInformerLite(lw *cache.ListWatch) (cache.SharedInformer, error) {
	azBindingInformer := cache.NewSharedInformer(lw, &aadpodv1.AzureIdentityBinding{}, time.Minute*10)
	if azBindingInformer == nil {
		return nil, fmt.Errorf("failed to create %s informer", aadpodv1.AzureIDBindingResource)
	}
	return azBindingInformer, nil
}

func newIDInformerLite(lw *cache.ListWatch) (cache.SharedInformer, error) {
	azIDInformer := cache.NewSharedInformer(lw, &aadpodv1.AzureIdentity{}, time.Minute*10)
	if azIDInformer == nil {
		return nil, fmt.Errorf("failed to create %s informer", aadpodv1.AzureIDResource)
	}
	return azIDInformer, nil
}

func newPodIdentityExceptionListWatch(r *rest.RESTClient) *cache.ListWatch {
	optionsModifier := func(options *v1.ListOptions) {}
	return cache.NewFilteredListWatchFromClient(
		r,
		aadpodv1.AzurePodIdentityExceptionResource,
		v1.NamespaceAll,
		optionsModifier,
	)
}

func newPodIdentityExceptionInformer(lw *cache.ListWatch) (cache.SharedInformer, error) {
	azPodIDExceptionInformer := cache.NewSharedInformer(lw, &aadpodv1.AzurePodIdentityException{}, time.Minute*10)
	if azPodIDExceptionInformer == nil {
		return nil, fmt.Errorf("failed to create %s informer", aadpodv1.AzurePodIdentityExceptionResource)
	}
	return azPodIDExceptionInformer, nil
}

func (c *Client) getObjectList(resource string, i runtime.Object) (runtime.Object, error) {
	options := v1.ListOptions{}
	do := c.rest.Get().Namespace(v1.NamespaceAll).Resource(resource).VersionedParams(&options, v1.ParameterCodec).Do(context.TODO())
	body, err := do.Raw()
	if err != nil {
		return nil, fmt.Errorf("failed to get %s, error: %+v", resource, err)
	}
	err = json.Unmarshal(body, &i)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal to object %T, error: %+v", i, err)
	}
	return i, err
}

func (c *Client) setObject(resource, ns, name string, i interface{}, obj runtime.Object) error {
	err := c.rest.Put().Namespace(ns).Resource(resource).Name(name).Body(i).Do(context.TODO()).Into(obj)
	if err != nil {
		return fmt.Errorf("failed to set object for resource %s, error: %+v", resource, err)
	}
	return nil
}

// Upgrade performs type upgrade to a specific aad-pod-identity CRD.
func (c *Client) Upgrade(resource string, i runtime.Object) (map[string]runtime.Object, error) {
	m := make(map[string]runtime.Object)
	i, err := c.getObjectList(resource, i)
	if err != nil {
		return m, err
	}

	list, err := meta.ExtractList(i)
	if err != nil {
		return m, fmt.Errorf("failed to extract list for resource %s, error: %+v", resource, err)
	}

	for _, item := range list {
		o, err := meta.Accessor(item)
		if err != nil {
			return m, fmt.Errorf("failed to get object for resource %s, error: %+v", resource, err)
		}
		switch resource {
		case aadpodv1.AzureIDResource:
			var obj aadpodv1.AzureIdentity
			err = c.setObject(resource, o.GetNamespace(), o.GetName(), o, &obj)
			if err != nil {
				return m, err
			}
			m[getMapKey(o.GetNamespace(), o.GetName())] = &obj
		case aadpodv1.AzureIDBindingResource:
			var obj aadpodv1.AzureIdentityBinding
			err = c.setObject(resource, o.GetNamespace(), o.GetName(), o, &obj)
			if err != nil {
				return m, err
			}
			m[getMapKey(o.GetNamespace(), o.GetName())] = &obj
		default:
			err = c.setObject(resource, o.GetNamespace(), o.GetName(), o, nil)
			if err != nil {
				return m, err
			}
		}
	}
	return m, nil
}

// UpgradeAll performs type upgrade to for all aad-pod-identity CRDs.
func (c *Client) UpgradeAll() error {
	updatedAzureIdentities, err := c.Upgrade(aadpodv1.AzureIDResource, &aadpodv1.AzureIdentityList{})
	if err != nil {
		return err
	}
	updatedAzureIdentityBindings, err := c.Upgrade(aadpodv1.AzureIDBindingResource, &aadpodv1.AzureIdentityBindingList{})
	if err != nil {
		return err
	}
	_, err = c.Upgrade(aadpodv1.AzurePodIdentityExceptionResource, &aadpodv1.AzurePodIdentityExceptionList{})
	if err != nil {
		return err
	}

	// update azure assigned identities separately as we need to use the latest
	// updated azure identity and binding as ref. Doing this will ensure upgrade does
	// not trigger any sync cycles
	i, err := c.getObjectList(aadpodv1.AzureAssignedIDResource, &aadpodv1.AzureAssignedIdentityList{})
	if err != nil {
		return err
	}
	list, err := meta.ExtractList(i)
	if err != nil {
		return fmt.Errorf("failed to extract list for resource: %s, error: %+v", aadpodv1.AzureAssignedIDResource, err)
	}
	for _, item := range list {
		o, err := meta.Accessor(item)
		if err != nil {
			return fmt.Errorf("failed to get object for resource: %s, error: %+v", aadpodv1.AzureAssignedIDResource, err)
		}
		obj := o.(*aadpodv1.AzureAssignedIdentity)
		idName := obj.Spec.AzureIdentityRef.Name
		idNamespace := obj.Spec.AzureIdentityRef.Namespace
		bindingName := obj.Spec.AzureBindingRef.Name
		bindingNamespace := obj.Spec.AzureBindingRef.Namespace

		if v, exists := updatedAzureIdentities[getMapKey(idNamespace, idName)]; exists && v != nil {
			obj.Spec.AzureIdentityRef = v.(*aadpodv1.AzureIdentity)
		}
		if v, exists := updatedAzureIdentityBindings[getMapKey(bindingNamespace, bindingName)]; exists && v != nil {
			obj.Spec.AzureBindingRef = v.(*aadpodv1.AzureIdentityBinding)
		}
		err = c.setObject(aadpodv1.AzureAssignedIDResource, o.GetNamespace(), o.GetName(), obj, nil)
		if err != nil {
			return err
		}
	}
	return nil
}

// StartLite to be used only case of lite client
func (c *Client) StartLite(exit <-chan struct{}) {
	var cacheHasSynced []cache.InformerSynced

	if c.AssignedIDInformer != nil {
		go c.AssignedIDInformer.Run(exit)
		cacheHasSynced = append(cacheHasSynced, c.AssignedIDInformer.HasSynced)
	}
	if c.BindingInformer != nil {
		go c.BindingInformer.Run(exit)
		cacheHasSynced = append(cacheHasSynced, c.BindingInformer.HasSynced)
	}
	if c.IDInformer != nil {
		go c.IDInformer.Run(exit)
		cacheHasSynced = append(cacheHasSynced, c.IDInformer.HasSynced)
	}
	if c.PodIdentityExceptionInformer != nil {
		go c.PodIdentityExceptionInformer.Run(exit)
		cacheHasSynced = append(cacheHasSynced, c.PodIdentityExceptionInformer.HasSynced)
	}
	c.SyncCache(exit, true, cacheHasSynced...)
	klog.Info("CRD lite informers started ")
}

// Start starts all informer routines to watch for CRD-related changes.
func (c *Client) Start(exit <-chan struct{}) {
	go c.BindingInformer.Run(exit)
	go c.IDInformer.Run(exit)
	go c.AssignedIDInformer.Run(exit)
	c.SyncCache(exit, true, c.BindingInformer.HasSynced, c.IDInformer.HasSynced, c.AssignedIDInformer.HasSynced)
	klog.Info("CRD informers started")
}

// SyncCache synchronizes cache
func (c *Client) SyncCache(exit <-chan struct{}, initial bool, cacheSyncs ...cache.InformerSynced) {
	if !cache.WaitForCacheSync(exit, cacheSyncs...) {
		if !initial {
			klog.Errorf("cache failed to be synchronized")
			return
		}
		panic("Cache failed to be synchronized")
	}
}

// SyncCacheAll - sync all caches related to the client.
func (c *Client) SyncCacheAll(exit <-chan struct{}, initial bool) {
	c.SyncCache(exit, initial, c.BindingInformer.HasSynced, c.IDInformer.HasSynced, c.AssignedIDInformer.HasSynced)
}

// RemoveAssignedIdentity removes the assigned identity
func (c *Client) RemoveAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) (err error) {
	klog.V(6).Infof("deleting assigned id %s/%s", assignedIdentity.Namespace, assignedIdentity.Name)
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportKubernetesAPIOperationError(metrics.AssignedIdentityDeletionOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		c.reporter.Report(
			metrics.AssignedIdentityDeletionCountM.M(1),
			metrics.AssignedIdentityDeletionDurationM.M(metrics.SinceInSeconds(begin)))

	}()

	var res aadpodv1.AzureAssignedIdentity
	err = c.rest.Delete().Namespace(assignedIdentity.Namespace).Resource(aadpodid.AzureAssignedIDResource).Name(assignedIdentity.Name).Do(context.TODO()).Into(&res)
	if apierrors.IsNotFound(err) {
		return nil
	}
	if err != nil {
		return err
	}
	if hasFinalizer(&res) {
		removeFinalizer(&res)
		// update the assigned identity without finalizer and resource will be garbage collected
		err = c.rest.Put().Namespace(assignedIdentity.Namespace).Resource(aadpodid.AzureAssignedIDResource).Name(assignedIdentity.Name).Body(&res).Do(context.TODO()).Error()
	}

	klog.V(5).Infof("deleting %s took: %v", assignedIdentity.Name, time.Since(begin))
	stats.AggregateConcurrent(stats.DeleteAzureAssignedIdentity, begin, time.Now())
	return err
}

// CreateAssignedIdentity creates new assigned identity
func (c *Client) CreateAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) (err error) {
	klog.Infof("creating assigned id %s/%s", assignedIdentity.Namespace, assignedIdentity.Name)
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportKubernetesAPIOperationError(metrics.AssignedIdentityAdditionOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
			return
		}
		c.reporter.Report(
			metrics.AssignedIdentityAdditionCountM.M(1),
			metrics.AssignedIdentityAdditionDurationM.M(metrics.SinceInSeconds(begin)))

	}()

	var res aadpodv1.AzureAssignedIdentity
	v1AssignedID := aadpodv1.ConvertInternalAssignedIdentityToV1AssignedIdentity(*assignedIdentity)
	if !hasFinalizer(&v1AssignedID) {
		v1AssignedID.SetFinalizers(append(v1AssignedID.GetFinalizers(), finalizerName))
	}
	err = c.rest.Post().Namespace(assignedIdentity.Namespace).Resource(aadpodid.AzureAssignedIDResource).Body(&v1AssignedID).Do(context.TODO()).Into(&res)
	if err != nil {
		return err
	}

	klog.V(5).Infof("time taken to create %s/%s: %v", assignedIdentity.Namespace, assignedIdentity.Name, time.Since(begin))
	stats.AggregateConcurrent(stats.CreateAzureAssignedIdentiy, begin, time.Now())
	return nil
}

// UpdateAssignedIdentity updates an existing assigned identity
func (c *Client) UpdateAssignedIdentity(assignedIdentity *aadpodid.AzureAssignedIdentity) (err error) {
	klog.Infof("updating assigned id %s/%s", assignedIdentity.Namespace, assignedIdentity.Name)
	begin := time.Now()

	defer func() {
		if err != nil {
			err = c.reporter.ReportKubernetesAPIOperationError(metrics.AssignedIdentityUpdateOperationName)
			klog.Warningf("failed to report metrics, error: %+v", err)
			return
		}
		c.reporter.Report(
			metrics.AssignedIdentityUpdateCountM.M(1),
			metrics.AssignedIdentityUpdateDurationM.M(metrics.SinceInSeconds(begin)))

	}()

	v1AssignedID := aadpodv1.ConvertInternalAssignedIdentityToV1AssignedIdentity(*assignedIdentity)
	err = c.rest.Put().Namespace(assignedIdentity.Namespace).Resource(aadpodid.AzureAssignedIDResource).Name(assignedIdentity.Name).Body(&v1AssignedID).Do(context.TODO()).Error()
	if err != nil {
		return fmt.Errorf("failed to update AzureAssignedIdentity, error: %+v", err)
	}

	klog.V(5).Infof("time taken to update %s/%s: %v", assignedIdentity.Namespace, assignedIdentity.Name, time.Since(begin))
	stats.AggregateConcurrent(stats.UpdateAzureAssignedIdentity, begin, time.Now())
	return nil
}

// ListBindings returns a list of azureidentitybindings
func (c *Client) ListBindings() (res *[]aadpodid.AzureIdentityBinding, err error) {
	begin := time.Now()

	var resList []aadpodid.AzureIdentityBinding

	list := c.BindingInformer.GetStore().List()
	for _, binding := range list {
		o, ok := binding.(*aadpodv1.AzureIdentityBinding)
		if !ok {
			return nil, fmt.Errorf("failed to cast %T to %s", binding, aadpodv1.AzureIDBindingResource)
		}
		// Note: List items returned from cache have empty Kind and API version..
		// Work around this issue since we need that for event recording to work.
		o.SetGroupVersionKind(schema.GroupVersionKind{
			Group:   aadpodv1.CRDGroup,
			Version: aadpodv1.CRDVersion,
			Kind:    reflect.TypeOf(*o).String()})

		internalBinding := aadpodv1.ConvertV1BindingToInternalBinding(*o)

		resList = append(resList, internalBinding)
		klog.V(6).Infof("appending binding: %s/%s to list.", o.Namespace, o.Name)
	}

	stats.Aggregate(stats.AzureIdentityBindingList, time.Since(begin))
	return &resList, nil
}

// ListAssignedIDs returns a list of azureassignedidentities
func (c *Client) ListAssignedIDs() (res *[]aadpodid.AzureAssignedIdentity, err error) {
	begin := time.Now()

	var resList []aadpodid.AzureAssignedIdentity

	list := c.AssignedIDInformer.GetStore().List()
	for _, assignedID := range list {
		o, ok := assignedID.(*aadpodv1.AzureAssignedIdentity)
		if !ok {
			return nil, fmt.Errorf("failed to cast %T to %s", assignedID, aadpodv1.AzureAssignedIDResource)
		}
		// Note: List items returned from cache have empty Kind and API version..
		// Work around this issue since we need that for event recording to work.
		o.SetGroupVersionKind(schema.GroupVersionKind{
			Group:   aadpodv1.CRDGroup,
			Version: aadpodv1.CRDVersion,
			Kind:    reflect.TypeOf(*o).String()})
		out := aadpodv1.ConvertV1AssignedIdentityToInternalAssignedIdentity(*o)
		resList = append(resList, out)
		klog.V(6).Infof("appending AzureAssignedIdentity: %s/%s to list.", o.Namespace, o.Name)
	}

	stats.Aggregate(stats.AzureAssignedIdentityList, time.Since(begin))
	return &resList, nil
}

// ListAssignedIDsInMap gets the list of current assigned ids, adds it to a map
// with assigned identity name as key and assigned identity as value.
func (c *Client) ListAssignedIDsInMap() (map[string]aadpodid.AzureAssignedIdentity, error) {
	begin := time.Now()

	result := make(map[string]aadpodid.AzureAssignedIdentity)
	list := c.AssignedIDInformer.GetStore().List()
	for _, assignedID := range list {

		o, ok := assignedID.(*aadpodv1.AzureAssignedIdentity)
		if !ok {
			return nil, fmt.Errorf("failed to cast %T to %s", assignedID, aadpodv1.AzureAssignedIDResource)
		}
		// Note: List items returned from cache have empty Kind and API version..
		// Work around this issue since we need that for event recording to work.
		o.SetGroupVersionKind(schema.GroupVersionKind{
			Group:   aadpodv1.CRDGroup,
			Version: aadpodv1.CRDVersion,
			Kind:    reflect.TypeOf(*o).String()})

		out := aadpodv1.ConvertV1AssignedIdentityToInternalAssignedIdentity(*o)
		// assigned identities names are unique across namespaces as we use pod name-<id ns>-<id name>
		result[o.Name] = out
		klog.V(6).Infof("added to map with key: %s", o.Name)
	}

	stats.Aggregate(stats.AzureAssignedIdentityList, time.Since(begin))
	return result, nil
}

// ListIds returns a list of azureidentities
func (c *Client) ListIds() (res *[]aadpodid.AzureIdentity, err error) {
	begin := time.Now()

	var resList []aadpodid.AzureIdentity

	list := c.IDInformer.GetStore().List()
	for _, id := range list {
		o, ok := id.(*aadpodv1.AzureIdentity)
		if !ok {
			return nil, fmt.Errorf("failed to cast %T to %s", id, aadpodv1.AzureIDResource)
		}
		// Note: List items returned from cache have empty Kind and API version..
		// Work around this issue since we need that for event recording to work.
		o.SetGroupVersionKind(schema.GroupVersionKind{
			Group:   aadpodv1.CRDGroup,
			Version: aadpodv1.CRDVersion,
			Kind:    reflect.TypeOf(*o).String()})

		out := aadpodv1.ConvertV1IdentityToInternalIdentity(*o)

		resList = append(resList, out)
		klog.V(6).Infof("appending AzureIdentity %s/%s to list.", o.Namespace, o.Name)
	}

	stats.Aggregate(stats.AzureIdentityList, time.Since(begin))
	return &resList, nil
}

// ListPodIdentityExceptions returns list of azurepodidentityexceptions
func (c *Client) ListPodIdentityExceptions(ns string) (res *[]aadpodid.AzurePodIdentityException, err error) {
	begin := time.Now()

	var resList []aadpodid.AzurePodIdentityException

	list := c.PodIdentityExceptionInformer.GetStore().List()
	for _, binding := range list {
		o, ok := binding.(*aadpodv1.AzurePodIdentityException)
		if !ok {
			return nil, fmt.Errorf("failed to cast %T to %s", binding, aadpodid.AzurePodIdentityExceptionResource)
		}
		if o.Namespace == ns {
			// Note: List items returned from cache have empty Kind and API version..
			// Work around this issue since we need that for event recording to work.
			o.SetGroupVersionKind(schema.GroupVersionKind{
				Group:   aadpodv1.CRDGroup,
				Version: aadpodv1.CRDVersion,
				Kind:    reflect.TypeOf(*o).String()})
			out := aadpodv1.ConvertV1PodIdentityExceptionToInternalPodIdentityException(*o)

			resList = append(resList, out)
			klog.V(6).Infof("appending exception: %s/%s to list.", o.Namespace, o.Name)
		}
	}

	stats.Aggregate(stats.AzurePodIdentityExceptionList, time.Since(begin))
	return &resList, nil
}

// ListPodIds - given a pod with pod name space
// returns a map with list of azure identities in each state
func (c *Client) ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error) {
	list, err := c.ListAssignedIDs()
	if err != nil {
		return nil, err
	}

	idStateMap := make(map[string][]aadpodid.AzureIdentity)
	for _, v := range *list {
		if v.Spec.Pod == podname && v.Spec.PodNamespace == podns {
			idStateMap[v.Status.Status] = append(idStateMap[v.Status.Status], *v.Spec.AzureIdentityRef)
		}
	}
	return idStateMap, nil
}

// GetPodIDsWithBinding returns list of azure identity based on bindings
// that match pod label.
func (c *Client) GetPodIDsWithBinding(namespace string, labels map[string]string) ([]aadpodid.AzureIdentity, error) {
	// get all bindings
	bindings, err := c.ListBindings()
	if err != nil {
		return nil, err
	}
	if bindings == nil {
		return nil, fmt.Errorf("binding list is nil from cache")
	}
	matchingIds := make(map[string]bool)
	podLabel := labels[aadpodid.CRDLabelKey]

	for _, binding := range *bindings {
		// check if binding selector in pod labels
		if podLabel == binding.Spec.Selector && binding.Namespace == namespace {
			matchingIds[binding.Spec.AzureIdentity] = true
		}
	}
	// get the azure identity objects based on the list generated
	azIdentities, err := c.ListIds()
	if err != nil {
		return nil, err
	}
	if azIdentities == nil {
		return nil, fmt.Errorf("azure identities list is nil from cache")
	}
	var azIds []aadpodid.AzureIdentity
	for _, azIdentity := range *azIdentities {
		if _, exists := matchingIds[azIdentity.Name]; exists && azIdentity.Namespace == namespace {
			azIds = append(azIds, azIdentity)
		}
	}
	return azIds, nil
}

type patchStatusOps struct {
	Op    string      `json:"op"`
	Path  string      `json:"path"`
	Value interface{} `json:"value"`
}

// UpdateAzureAssignedIdentityStatus updates the status field in AzureAssignedIdentity to indicate current status
func (c *Client) UpdateAzureAssignedIdentityStatus(assignedIdentity *aadpodid.AzureAssignedIdentity, status string) (err error) {
	klog.Infof("updating AzureAssignedIdentity %s/%s status to %s", assignedIdentity.Namespace, assignedIdentity.Name, status)

	defer func() {
		if err != nil {
			err = c.reporter.ReportKubernetesAPIOperationError(metrics.UpdateAzureAssignedIdentityStatusOperationName)
			if err != nil {
				klog.Warningf("failed to report metrics, error: %+v", err)
			}
		}
	}()

	ops := make([]patchStatusOps, 1)
	ops[0].Op = "replace"
	ops[0].Path = "/status/status"
	ops[0].Value = status

	patchBytes, err := json.Marshal(ops)
	if err != nil {
		return err
	}

	begin := time.Now()
	err = c.rest.
		Patch(types.JSONPatchType).
		Namespace(assignedIdentity.Namespace).
		Resource(aadpodid.AzureAssignedIDResource).
		Name(assignedIdentity.Name).
		Body(patchBytes).
		Do(context.TODO()).
		Error()
	klog.V(5).Infof("patch of %s took: %v", assignedIdentity.Name, time.Since(begin))
	return err
}

func getMapKey(ns, name string) string {
	return strings.Join([]string{ns, name}, "/")
}

func removeFinalizer(assignedID *aadpodv1.AzureAssignedIdentity) {
	assignedID.SetFinalizers(removeString(finalizerName, assignedID.GetFinalizers()))
}

func hasFinalizer(assignedID *aadpodv1.AzureAssignedIdentity) bool {
	return containsString(finalizerName, assignedID.GetFinalizers())
}

func containsString(s string, items []string) bool {
	for _, item := range items {
		if item == s {
			return true
		}
	}
	return false
}

func removeString(s string, items []string) []string {
	var rval []string
	for _, item := range items {
		if item != s {
			rval = append(rval, item)
		}
	}
	return rval
}
