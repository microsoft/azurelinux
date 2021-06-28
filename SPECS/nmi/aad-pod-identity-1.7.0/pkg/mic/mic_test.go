package mic

import (
	"errors"
	"fmt"
	"sort"
	"strings"
	"sync"
	"testing"
	"time"

	internalaadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	cp "github.com/Azure/aad-pod-identity/pkg/cloudprovider"
	"github.com/Azure/aad-pod-identity/pkg/config"
	"github.com/Azure/aad-pod-identity/pkg/crd"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/retry"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
	"github.com/stretchr/testify/assert"
	api "k8s.io/api/core/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/klog/v2"
)

var (
	testResourceID = "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/identity1"
)

/****************** CLOUD PROVIDER MOCK ****************************/
type TestCloudClient struct {
	*cp.Client
	// testVMClient is test validation purpose.
	testVMClient   *TestVMClient
	testVMSSClient *TestVMSSClient
}

type TestVMClient struct {
	*cp.VMClient

	mu       sync.Mutex
	nodeMap  map[string]*compute.VirtualMachine
	nodeIDs  map[string]map[string]bool
	err      *error
	identity *compute.VirtualMachineIdentity
}

func (c *TestVMClient) SetError(err error) {
	c.err = &err
}

func (c *TestVMClient) UnsetError() {
	c.err = nil
}

func (c *TestVMClient) Get(rgName string, nodeName string) (compute.VirtualMachine, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	stored := c.nodeMap[nodeName]
	if stored == nil {
		vm := new(compute.VirtualMachine)
		c.nodeMap[nodeName] = vm
		c.nodeIDs[nodeName] = make(map[string]bool)
		vm.Identity = &compute.VirtualMachineIdentity{}
		return *vm, nil
	}

	storedIDs := c.nodeIDs[nodeName]
	newVMIdentity := make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue)
	for id := range storedIDs {
		newVMIdentity[id] = &compute.VirtualMachineIdentityUserAssignedIdentitiesValue{}
	}
	stored.Identity.UserAssignedIdentities = newVMIdentity
	return *stored, nil
}

func (c *TestVMClient) UpdateIdentities(rg, nodeName string, vm compute.VirtualMachine) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.err != nil {
		defer c.UnsetError()
		return *c.err
	}
	if vm.Identity != nil && vm.Identity.UserAssignedIdentities != nil {
		for k, v := range vm.Identity.UserAssignedIdentities {
			if v == nil {
				delete(c.nodeIDs[nodeName], k)
			} else {
				c.nodeIDs[nodeName][k] = true
			}
		}
	}
	if vm.Identity != nil && vm.Identity.UserAssignedIdentities == nil {
		for k := range c.nodeIDs[nodeName] {
			delete(c.nodeIDs[nodeName], k)
		}
	}
	c.nodeMap[nodeName] = &vm
	return nil
}

func (c *TestVMClient) ListMSI() (ret map[string]*[]string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	ret = make(map[string]*[]string)

	for key, val := range c.nodeMap {
		var ids []string
		for k := range val.Identity.UserAssignedIdentities {
			ids = append(ids, k)
		}
		ret[key] = &ids
	}
	return ret
}

func (c *TestVMClient) CompareMSI(nodeName string, expectedUserIDs []string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	stored := c.nodeMap[nodeName]
	if stored == nil || stored.Identity == nil {
		return false
	}

	var actualUserIDs []string
	for k := range c.nodeIDs[nodeName] {
		actualUserIDs = append(actualUserIDs, k)
	}
	if actualUserIDs == nil {
		if len(expectedUserIDs) == 0 && stored.Identity.Type == compute.ResourceIdentityTypeNone { // Validate that we have reset the resource type as none.
			return true
		}
		return false
	}

	sort.Strings(actualUserIDs)
	sort.Strings(expectedUserIDs)
	for i := range actualUserIDs {
		if !strings.EqualFold(actualUserIDs[i], expectedUserIDs[i]) {
			return false
		}
	}

	return true
}

type TestVMSSClient struct {
	*cp.VMSSClient

	mu       sync.Mutex
	nodeMap  map[string]*compute.VirtualMachineScaleSet
	nodeIDs  map[string]map[string]bool
	err      *error
	identity *compute.VirtualMachineScaleSetIdentity
}

func (c *TestVMSSClient) SetError(err error) {
	c.err = &err
}

func (c *TestVMSSClient) UnsetError() {
	c.err = nil
}

func (c *TestVMSSClient) Get(rgName string, nodeName string) (compute.VirtualMachineScaleSet, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	stored := c.nodeMap[nodeName]
	if stored == nil {
		vmss := new(compute.VirtualMachineScaleSet)
		c.nodeMap[nodeName] = vmss
		c.nodeIDs[nodeName] = make(map[string]bool)
		vmss.Identity = &compute.VirtualMachineScaleSetIdentity{}
		return *vmss, nil
	}

	storedIDs := c.nodeIDs[nodeName]
	newVMSSIdentity := make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue)
	for id := range storedIDs {
		newVMSSIdentity[id] = &compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue{}
	}
	stored.Identity.UserAssignedIdentities = newVMSSIdentity
	return *stored, nil
}

func (c *TestVMSSClient) UpdateIdentities(rg, nodeName string, vmss compute.VirtualMachineScaleSet) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.err != nil {
		defer c.UnsetError()
		return *c.err
	}
	if vmss.Identity != nil && vmss.Identity.UserAssignedIdentities != nil {
		for k, v := range vmss.Identity.UserAssignedIdentities {
			if v == nil {
				delete(c.nodeIDs[nodeName], k)
			} else {
				c.nodeIDs[nodeName][k] = true
			}
		}
	}
	if vmss.Identity != nil && vmss.Identity.UserAssignedIdentities == nil {
		for k := range c.nodeIDs[nodeName] {
			delete(c.nodeIDs[nodeName], k)
		}
	}

	c.nodeMap[nodeName] = &vmss
	return nil
}

func (c *TestVMSSClient) ListMSI() (ret map[string]*[]string) {
	ret = make(map[string]*[]string)

	for key, val := range c.nodeMap {
		var ids []string
		for k := range val.Identity.UserAssignedIdentities {
			ids = append(ids, k)
		}
		ret[key] = &ids
	}
	return ret
}

func (c *TestVMSSClient) CompareMSI(nodeName string, expectedUserIDs []string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	stored := c.nodeMap[nodeName]
	if stored == nil || stored.Identity == nil {
		return false
	}

	var actualUserIDs []string
	for k := range c.nodeIDs[nodeName] {
		actualUserIDs = append(actualUserIDs, k)
	}

	if actualUserIDs == nil {
		if len(expectedUserIDs) == 0 && stored.Identity.Type == compute.ResourceIdentityTypeNone { // Validate that we have reset the resource type as none.
			return true
		}
		return false
	}

	sort.Strings(actualUserIDs)
	sort.Strings(expectedUserIDs)
	for i := range actualUserIDs {
		if !strings.EqualFold(actualUserIDs[i], expectedUserIDs[i]) {
			return false
		}
	}

	return true
}

func (c *TestCloudClient) GetUserMSIs(name string, isvmss bool) ([]string, error) {
	var ret []string
	if isvmss {
		vmss, _ := c.testVMSSClient.Get("", name)
		for id := range vmss.Identity.UserAssignedIdentities {
			ret = append(ret, id)
		}
	} else {
		vm, _ := c.testVMClient.Get("", name)
		for id := range vm.Identity.UserAssignedIdentities {
			ret = append(ret, id)
		}
	}

	return ret, nil
}

func (c *TestCloudClient) ListMSI() (ret map[string]*[]string) {
	if c.Client.Config.VMType == "vmss" {
		return c.testVMSSClient.ListMSI()
	}
	return c.testVMClient.ListMSI()
}

func (c *TestCloudClient) CompareMSI(nodeName string, userIDs []string) bool {
	if c.Client.Config.VMType == "vmss" {
		return c.testVMSSClient.CompareMSI(nodeName, userIDs)
	}
	return c.testVMClient.CompareMSI(nodeName, userIDs)
}

func (c *TestCloudClient) PrintMSI() {
	for key, val := range c.ListMSI() {
		klog.Infof("\nnode name: %s", key)
		if val != nil {
			for i, id := range *val {
				klog.Infof("%d) %s", i, id)
			}
		}
	}
}

func (c *TestCloudClient) SetError(err error) {
	c.testVMClient.SetError(err)
	c.testVMSSClient.SetError(err)
}

func (c *TestCloudClient) UnsetError() {
	c.testVMClient.UnsetError()
	c.testVMSSClient.UnsetError()
}

func NewTestVMClient() *TestVMClient {
	nodeMap := make(map[string]*compute.VirtualMachine)
	nodeIDs := make(map[string]map[string]bool)
	vmClient := &cp.VMClient{}
	identity := &compute.VirtualMachineIdentity{
		UserAssignedIdentities: make(map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue),
	}

	return &TestVMClient{
		VMClient: vmClient,
		nodeMap:  nodeMap,
		nodeIDs:  nodeIDs,
		identity: identity,
	}
}

func NewTestVMSSClient() *TestVMSSClient {
	nodeMap := make(map[string]*compute.VirtualMachineScaleSet)
	nodeIDs := make(map[string]map[string]bool)
	vmssClient := &cp.VMSSClient{}
	identity := &compute.VirtualMachineScaleSetIdentity{
		UserAssignedIdentities: make(map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue),
	}

	return &TestVMSSClient{
		VMSSClient: vmssClient,
		nodeMap:    nodeMap,
		nodeIDs:    nodeIDs,
		identity:   identity,
	}
}

func NewTestCloudClient(cfg config.AzureConfig) *TestCloudClient {
	vmClient := NewTestVMClient()
	vmssClient := NewTestVMSSClient()
	retryClient := retry.NewRetryClient(2, 0)
	cloudClient := &cp.Client{
		Config:      cfg,
		VMClient:    vmClient,
		VMSSClient:  vmssClient,
		RetryClient: retryClient,
	}

	return &TestCloudClient{
		cloudClient,
		vmClient,
		vmssClient,
	}
}

/****************** POD MOCK ****************************/
type TestPodClient struct {
	mu   sync.Mutex
	pods []*corev1.Pod
}

func NewTestPodClient() *TestPodClient {
	var pods []*corev1.Pod
	return &TestPodClient{
		pods: pods,
	}
}

func (c *TestPodClient) Start(exit <-chan struct{}) {
	klog.Info("start called from the test interface")
}

func (c *TestPodClient) GetPods() ([]*corev1.Pod, error) {
	// TODO: Add label matching. For now we add only pods which we want to add.
	c.mu.Lock()
	defer c.mu.Unlock()

	pods := make([]*corev1.Pod, len(c.pods))
	copy(pods, c.pods)

	return pods, nil
}

func (c *TestPodClient) AddPod(podName, podNs, nodeName, binding string) {
	labels := make(map[string]string)
	labels[aadpodid.CRDLabelKey] = binding
	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      podName,
			Namespace: podNs,
			Labels:    labels,
		},
		Spec: corev1.PodSpec{
			NodeName: nodeName,
		},
	}

	c.mu.Lock()
	defer c.mu.Unlock()
	c.pods = append(c.pods, pod)
}

func (c *TestPodClient) DeletePod(podName string, podNs string) {
	var newPods []*corev1.Pod
	changed := false

	c.mu.Lock()
	defer c.mu.Unlock()

	for _, pod := range c.pods {
		if pod.Name == podName && pod.Namespace == podNs {
			changed = true
			continue
		} else {
			newPods = append(newPods, pod)
		}
	}
	if changed {
		c.pods = newPods
	}
}

/****************** CRD MOCK ****************************/

type TestCrdClient struct {
	*crd.Client
	mu            sync.Mutex
	assignedIDMap map[string]*internalaadpodid.AzureAssignedIdentity
	bindingMap    map[string]*aadpodid.AzureIdentityBinding
	idMap         map[string]*aadpodid.AzureIdentity
	err           *error
}

func NewTestCrdClient(config *rest.Config) *TestCrdClient {
	return &TestCrdClient{
		assignedIDMap: make(map[string]*internalaadpodid.AzureAssignedIdentity),
		bindingMap:    make(map[string]*aadpodid.AzureIdentityBinding),
		idMap:         make(map[string]*aadpodid.AzureIdentity),
	}
}

func (c *TestCrdClient) Start(exit <-chan struct{}) {
}

func (c *TestCrdClient) SyncCache(exit <-chan struct{}, initial bool, cacheSyncs ...cache.InformerSynced) {

}

func (c *TestCrdClient) SyncCacheAll(exit <-chan struct{}, initial bool) {

}

func (c *TestCrdClient) CreateCrdWatchers(eventCh chan internalaadpodid.EventType) (err error) {
	return nil
}

func (c *TestCrdClient) RemoveAssignedIdentity(assignedIdentity *internalaadpodid.AzureAssignedIdentity) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.err != nil {
		return *c.err
	}
	delete(c.assignedIDMap, assignedIdentity.Name)
	return nil
}

// This function is not used currently
// TODO: consider remove
func (c *TestCrdClient) CreateAssignedIdentity(assignedIdentity *internalaadpodid.AzureAssignedIdentity) error {
	assignedIdentityToStore := *assignedIdentity // Make a copy to store in the map.
	c.mu.Lock()
	c.assignedIDMap[assignedIdentity.Name] = &assignedIdentityToStore
	c.mu.Unlock()
	return nil
}

func (c *TestCrdClient) UpdateAssignedIdentity(assignedIdentity *internalaadpodid.AzureAssignedIdentity) error {
	assignedIdentityToStore := *assignedIdentity // Make a copy to store in the map.
	c.mu.Lock()
	c.assignedIDMap[assignedIdentity.Name] = &assignedIdentityToStore
	c.mu.Unlock()
	return nil
}

func (c *TestCrdClient) UpdateAzureAssignedIdentityStatus(assignedIdentity *internalaadpodid.AzureAssignedIdentity, status string) error {
	assignedIdentity.Status.Status = status
	assignedIdentityToStore := *assignedIdentity // Make a copy to store in the map.
	c.mu.Lock()
	c.assignedIDMap[assignedIdentity.Name] = &assignedIdentityToStore
	c.mu.Unlock()
	return nil
}

func (c *TestCrdClient) CreateBinding(name, ns, idName, selector, resourceVersion string) {
	binding := &aadpodid.AzureIdentityBinding{
		ObjectMeta: metav1.ObjectMeta{
			Name:            name,
			Namespace:       ns,
			ResourceVersion: resourceVersion,
		},
		Spec: aadpodid.AzureIdentityBindingSpec{
			AzureIdentity: idName,
			Selector:      selector,
		},
	}
	c.mu.Lock()
	c.bindingMap[getIDKey(ns, name)] = binding
	c.mu.Unlock()
}

func (c *TestCrdClient) CreateID(idName, ns string, t aadpodid.IdentityType, rID, cID string, cp *api.SecretReference, tID, adRID, adEpt, resourceVersion string) {
	id := &aadpodid.AzureIdentity{
		ObjectMeta: metav1.ObjectMeta{
			Name:            idName,
			Namespace:       ns,
			ResourceVersion: resourceVersion,
		},
		Spec: aadpodid.AzureIdentitySpec{
			Type:         t,
			ResourceID:   rID,
			ClientID:     cID,
			TenantID:     tID,
			ADResourceID: adRID,
			ADEndpoint:   adEpt,
		},
	}
	c.mu.Lock()
	c.idMap[getIDKey(ns, idName)] = id
	c.mu.Unlock()
}

func (c *TestCrdClient) ListIds() (res *[]internalaadpodid.AzureIdentity, err error) {
	idList := make([]internalaadpodid.AzureIdentity, 0)
	c.mu.Lock()
	for _, v := range c.idMap {
		currID := aadpodid.ConvertV1IdentityToInternalIdentity(*v)
		idList = append(idList, currID)
	}
	c.mu.Unlock()
	return &idList, nil
}

func (c *TestCrdClient) ListBindings() (res *[]internalaadpodid.AzureIdentityBinding, err error) {
	bindingList := make([]internalaadpodid.AzureIdentityBinding, 0)
	c.mu.Lock()
	for _, v := range c.bindingMap {
		newBinding := aadpodid.ConvertV1BindingToInternalBinding(*v)
		bindingList = append(bindingList, newBinding)
	}
	c.mu.Unlock()
	return &bindingList, nil
}

func (c *TestCrdClient) ListAssignedIDs() (res *[]internalaadpodid.AzureAssignedIdentity, err error) {
	assignedIDList := make([]internalaadpodid.AzureAssignedIdentity, 0)
	c.mu.Lock()
	for _, v := range c.assignedIDMap {
		assignedIDList = append(assignedIDList, *v)
	}
	c.mu.Unlock()
	return &assignedIDList, nil
}

func (c *TestCrdClient) ListAssignedIDsInMap() (res map[string]internalaadpodid.AzureAssignedIdentity, err error) {
	assignedIDMap := make(map[string]internalaadpodid.AzureAssignedIdentity)
	c.mu.Lock()
	for k, v := range c.assignedIDMap {
		assignedIDMap[k] = *v
	}
	c.mu.Unlock()
	return assignedIDMap, nil
}

func (c *Client) ListPodIds(podns, podname string) (map[string][]internalaadpodid.AzureIdentity, error) {
	return map[string][]internalaadpodid.AzureIdentity{}, nil
}

func (c *Client) ListPodIdentityExceptions(ns string) (*[]internalaadpodid.AzurePodIdentityException, error) {
	return nil, nil
}

func (c *TestCrdClient) SetError(err error) {
	c.err = &err
}

func (c *TestCrdClient) UnsetError() {
	c.err = nil
}

func (c *TestCrdClient) waitForAssignedIDs(count int) bool {
	i := 0
	for i < 10 {
		time.Sleep(1 * time.Second)

		assignedIDs, err := c.ListAssignedIDs()
		if err != nil {
			return false
		}
		if len(*assignedIDs) == count {
			return true
		}
		i++
	}
	return false
}

/************************ NODE MOCK *************************************/

type TestNodeClient struct {
	mu    sync.Mutex
	nodes map[string]*corev1.Node
}

func NewTestNodeClient() *TestNodeClient {
	return &TestNodeClient{nodes: make(map[string]*corev1.Node)}
}

func (c *TestNodeClient) Get(name string) (*corev1.Node, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	node, exists := c.nodes[name]
	if !exists {
		return nil, errors.New("node not found")
	}
	return node, nil
}

func (c *TestNodeClient) Delete(name string) {
	c.mu.Lock()
	delete(c.nodes, name)
	c.mu.Unlock()
}

func (c *TestNodeClient) Start(<-chan struct{}) {}

func (c *TestNodeClient) AddNode(name string, opts ...func(*corev1.Node)) {
	c.mu.Lock()
	defer c.mu.Unlock()

	n := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: name}, Spec: corev1.NodeSpec{
		ProviderID: "azure:///subscriptions/testSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachines/" + name,
	}}
	for _, o := range opts {
		o(n)
	}
	c.nodes[name] = n
}

/************************ EVENT RECORDER MOCK *************************************/
type LastEvent struct {
	Type    string
	Reason  string
	Message string
}

type TestEventRecorder struct {
	mu        sync.Mutex
	lastEvent *LastEvent

	eventChannel chan bool
}

func (c *TestEventRecorder) WaitForEvents(expectedCount int) bool {
	count := 0
	for {
		select {
		case <-c.eventChannel:
			count++
			if expectedCount == count {
				return true
			}
		case <-time.After(2 * time.Minute):
			return false
		}
	}
}

func (c *TestEventRecorder) Event(object runtime.Object, t string, r string, message string) {
	c.mu.Lock()

	c.lastEvent.Type = t
	c.lastEvent.Reason = r
	c.lastEvent.Message = message

	c.mu.Unlock()

	c.eventChannel <- true
}

func (c *TestEventRecorder) Validate(e *LastEvent) bool {
	c.mu.Lock()

	t := c.lastEvent.Type
	r := c.lastEvent.Reason
	m := c.lastEvent.Message

	c.mu.Unlock()

	if t != e.Type || r != e.Reason || m != e.Message {
		klog.Errorf("event mismatch. expected - (t:%s, r:%s, m:%s). got - (t:%s, r:%s, m:%s)", e.Type, e.Reason, e.Message, t, r, m)
		return false
	}
	return true
}

func (c *TestEventRecorder) Eventf(object runtime.Object, t string, r string, messageFmt string, args ...interface{}) {

}

func (c *TestEventRecorder) PastEventf(object runtime.Object, timestamp metav1.Time, t string, m1 string, messageFmt string, args ...interface{}) {

}

func (c *TestEventRecorder) AnnotatedEventf(object runtime.Object, annotations map[string]string, eventtype, reason, messageFmt string, args ...interface{}) {

}

/************************ MIC MOCK *************************************/
func NewMICTestClient(eventCh chan internalaadpodid.EventType,
	cpClient *TestCloudClient,
	crdClient *TestCrdClient,
	podClient *TestPodClient,
	nodeClient *TestNodeClient,
	eventRecorder *TestEventRecorder, isNamespaced bool,
	createDeleteBatch int64,
	immutableUserMSIs map[string]bool) *TestMICClient {

	reporter, _ := metrics.NewReporter()

	realMICClient := &Client{
		CloudClient:                         cpClient,
		CRDClient:                           crdClient,
		EventRecorder:                       eventRecorder,
		PodClient:                           podClient,
		EventChannel:                        eventCh,
		NodeClient:                          nodeClient,
		syncRetryInterval:                   120 * time.Second,
		IsNamespaced:                        isNamespaced,
		createDeleteBatch:                   createDeleteBatch,
		ImmutableUserMSIsMap:                immutableUserMSIs,
		Reporter:                            reporter,
		identityAssignmentReconcileInterval: 3 * time.Minute,
	}

	return &TestMICClient{
		realMICClient,
	}
}

type TestMICClient struct {
	*Client
}

/************************ UNIT TEST *************************************/

func TestMapMICClient_1(t *testing.T) {
	idList := []internalaadpodid.AzureIdentity{
		{
			ObjectMeta: metav1.ObjectMeta{
				Name:      "testazid1",
				Namespace: "default",
			},
			Spec: internalaadpodid.AzureIdentitySpec{
				ResourceID: testResourceID,
			},
		},
		{
			ObjectMeta: metav1.ObjectMeta{
				Name:      "testazid2",
				Namespace: "ns00",
			},
			Spec: internalaadpodid.AzureIdentitySpec{
				ResourceID: testResourceID,
			},
		},
		{
			ObjectMeta: metav1.ObjectMeta{
				Name:      "testazid3",
				Namespace: "default",
			},
			Spec: internalaadpodid.AzureIdentitySpec{
				ResourceID: "testResourceID",
			},
		},
		{
			ObjectMeta: metav1.ObjectMeta{
				Name:      "testazid5",
				Namespace: "default",
			},
			Spec: internalaadpodid.AzureIdentitySpec{
				Type:     internalaadpodid.ServicePrincipal,
				TenantID: "tenantid",
				ClientID: "clientid",
			},
		},
	}

	micClient := &TestMICClient{}
	idMap, err := micClient.convertIDListToMap(idList)
	if err != nil {
		t.Fatalf("expected err to be nil, got: %+v", err)
	}

	tests := []struct {
		name        string
		idName      string
		idNamespace string
		shouldExist bool
	}{
		{
			name:        "default/testazid1 exists",
			idName:      "testazid1",
			idNamespace: "default",
			shouldExist: true,
		},
		{
			name:        "ns00/testazid2 in ns00 ns exists",
			idName:      "testazid2",
			idNamespace: "ns00",
			shouldExist: true,
		},
		{
			name:        "default/testazid3 doesn't exist as resource id invalid",
			idName:      "testazid3",
			idNamespace: "default",
			shouldExist: false,
		},
		{
			name:        "default/testazid4 doesn't exist",
			idName:      "testazid4",
			idNamespace: "default",
			shouldExist: false,
		},
		{
			name:        "ns00/testazid1 doesn't exist",
			idName:      "testazid1",
			idNamespace: "ns00",
			shouldExist: false,
		},
		{
			name:        "default/testazid5 for type 1 does exist",
			idName:      "testazid5",
			idNamespace: "default",
			shouldExist: true,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			azureID, idPresent := idMap[getIDKey(test.idNamespace, test.idName)]
			if test.shouldExist != idPresent {
				t.Fatalf("expected exist: %v, but identity %s/%s in map exist: %v",
					test.shouldExist, test.idNamespace, test.idName, idPresent)
			}
			if test.shouldExist && (azureID.Name != test.idName || azureID.Namespace != test.idNamespace) {
				t.Fatalf("expected identity %s/%s, got %s/%s", test.idNamespace, test.idName, azureID.Namespace, azureID.Name)
			}
		})
	}
}

func (c *TestMICClient) testRunSync() func(t *testing.T) {
	done := make(chan struct{})
	exit := make(chan struct{})
	var closeOnce sync.Once

	go func() {
		c.Sync(exit)
		close(done)
	}()

	return func(t *testing.T) {
		t.Helper()

		closeOnce.Do(func() {
			close(exit)
		})

		timeout := time.NewTimer(30 * time.Second)
		defer timeout.Stop()

		select {
		case <-done:
		case <-timeout.C:
			t.Fatal("timeout waiting for sync to exit")
		}
	}
}

func TestSimpleMICClient(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	crdClient.CreateID("test-id", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding", "default", "test-id", "test-select", "")

	nodeClient.AddNode("test-node")
	podClient.AddPod("test-pod", "default", "test-node", "test-select")

	eventCh <- internalaadpodid.PodCreated
	defer micClient.testRunSync()(t)

	evtRecorder.WaitForEvents(1)
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 0")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}

	assignedID := (*listAssignedIDs)[0]
	if !(assignedID.Spec.Pod == "test-pod" && assignedID.Spec.PodNamespace == "default" && assignedID.Spec.NodeName == "test-node" &&
		assignedID.Spec.AzureBindingRef.Name == "testbinding" && assignedID.Spec.AzureIdentityRef.Name == "test-id") {
		t.Fatalf("assigned ID spec: %v mismatch", assignedID)
	}

	// Test2: Remove assigned id event test
	podClient.DeletePod("test-pod", "default")
	eventCh <- internalaadpodid.PodDeleted
	if !crdClient.waitForAssignedIDs(0) {
		t.Fatalf("expected len of assigned identities to be 0")
	}

	// Test3: Error from cloud provider event test
	err = errors.New("error returned from cloud provider")
	cloudClient.SetError(err)

	podClient.AddPod("test-pod", "default", "test-node", "test-select")
	eventCh <- internalaadpodid.PodCreated
	evtRecorder.WaitForEvents(1)
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if (*listAssignedIDs)[0].Status.Status != aadpodid.AssignedIDCreated {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDCreated, (*listAssignedIDs)[0].Status.Status)
	}
}

func TestUpdateAssignedIdentities(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	crdClient.CreateID("test-id", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "rv1")
	crdClient.CreateBinding("testbinding", "default", "test-id", "test-select", "")

	nodeClient.AddNode("test-node")
	podClient.AddPod("test-pod", "default", "test-node", "test-select")

	eventCh <- internalaadpodid.PodCreated
	defer micClient.testRunSync()(t)

	evtRecorder.WaitForEvents(1)
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}

	assignedID := (*listAssignedIDs)[0]
	if !(assignedID.Spec.Pod == "test-pod" && assignedID.Spec.PodNamespace == "default" && assignedID.Spec.NodeName == "test-node" &&
		assignedID.Spec.AzureBindingRef.Name == "testbinding" && assignedID.Spec.AzureIdentityRef.Name == "test-id" &&
		assignedID.Spec.AzureIdentityRef.ResourceVersion == "rv1" && assignedID.Spec.AzureIdentityRef.Spec.ClientID == "test-user-msi-clientid") {
		t.Fatalf("assigned ID spec: %v mismatch", assignedID)
	}

	newResourceID := testResourceID + "-new"
	crdClient.CreateID("test-id", "default", aadpodid.UserAssignedMSI, newResourceID, "test-user-msi-clientid", nil, "", "", "", "changedrv2")
	crdClient.CreateID("test-id-2", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "rv2")
	crdClient.CreateBinding("testbinding2", "default", "test-id-2", "test-select", "")

	eventCh <- internalaadpodid.IdentityUpdated
	eventCh <- internalaadpodid.IdentityCreated
	eventCh <- internalaadpodid.BindingCreated

	evtRecorder.WaitForEvents(1)
	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	// check updated assigned identity has the right resource id
	if listAssignedIDs != nil {
		for _, assignedID := range *listAssignedIDs {
			if assignedID.Name != "test-pod-default-test-id" {
				continue
			}
			if !(assignedID.Spec.Pod == "test-pod" && assignedID.Spec.PodNamespace == "default" && assignedID.Spec.NodeName == "test-node" &&
				assignedID.Spec.AzureBindingRef.Name == "testbinding" && assignedID.Spec.AzureIdentityRef.Name == "test-id" &&
				assignedID.Spec.AzureIdentityRef.ResourceVersion == "changedrv2" && assignedID.Spec.AzureIdentityRef.Spec.ClientID == "test-user-msi-clientid" &&
				assignedID.Spec.AzureIdentityRef.Spec.ResourceID == newResourceID) {
				t.Fatalf("assigned ID spec: %v mismatch", assignedID)
			}
		}
	}
}

func TestAddUpdateDel(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	crdClient.CreateID("test-id-0", "default", aadpodid.UserAssignedMSI, fmt.Sprintf("%s-%d", testResourceID, 0), "test-user-msi-clientid-0", nil, "", "", "", "rv-0")
	crdClient.CreateBinding("testbinding-0", "default", "test-id-0", "test-select-0", "")

	crdClient.CreateID("test-id-1", "default", aadpodid.UserAssignedMSI, fmt.Sprintf("%s-%d", testResourceID, 1), "test-user-msi-clientid-1", nil, "", "", "", "rv-1")
	crdClient.CreateBinding("testbinding-1", "default", "test-id-1", "test-select-1", "")

	crdClient.CreateID("test-id-2", "default", aadpodid.UserAssignedMSI, fmt.Sprintf("%s-%d", testResourceID, 2), "test-user-msi-clientid-2", nil, "", "", "", "rv-2")
	crdClient.CreateBinding("testbinding-2", "default", "test-id-2", "test-select-2", "")

	nodeClient.AddNode("test-node")
	podClient.AddPod("test-pod-0", "default", "test-node", "test-select-0")
	podClient.AddPod("test-pod-1", "default", "test-node", "test-select-1")
	podClient.AddPod("test-pod-2", "default", "test-node", "test-select-2")

	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated

	defer micClient.testRunSync()(t)

	evtRecorder.WaitForEvents(3)
	if !crdClient.waitForAssignedIDs(3) {
		t.Fatalf("expected len of assigned identities to be 3")
	}

	crdClient.CreateID("test-id-0", "default", aadpodid.UserAssignedMSI, fmt.Sprintf("%s-%d", testResourceID, 4), "test-user-msi-clientid-4", nil, "", "", "", "updated-rv-0")
	crdClient.CreateID("test-id-3", "default", aadpodid.UserAssignedMSI, fmt.Sprintf("%s-%d", testResourceID, 3), "test-user-msi-clientid-3", nil, "", "", "", "rv-3")
	crdClient.CreateBinding("testbinding-3", "default", "test-id-3", "test-select-2", "")
	podClient.DeletePod("test-pod-1", "default")

	eventCh <- internalaadpodid.IdentityCreated
	eventCh <- internalaadpodid.BindingCreated
	eventCh <- internalaadpodid.IdentityUpdated
	eventCh <- internalaadpodid.PodDeleted

	evtRecorder.WaitForEvents(2)
	if !crdClient.waitForAssignedIDs(3) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("failed to list assigned ids, error: %+v", err)
	}
	// check the updated identity has the correct azureid ref
	for _, assignedID := range *listAssignedIDs {
		if assignedID.Name != "test-pod-0-default-test-id-0" {
			continue
		}
		if !(assignedID.Spec.Pod == "test-pod-0" && assignedID.Spec.PodNamespace == "default" && assignedID.Spec.NodeName == "test-node" &&
			assignedID.Spec.AzureBindingRef.Name == "testbinding-0" && assignedID.Spec.AzureIdentityRef.Name == "test-id-0" &&
			assignedID.Spec.AzureIdentityRef.ResourceVersion == "updated-rv-0" && assignedID.Spec.AzureIdentityRef.Spec.ClientID == "test-user-msi-clientid-4" &&
			assignedID.Spec.AzureIdentityRef.Spec.ResourceID == fmt.Sprintf("%s-%d", testResourceID, 4)) {
			t.Fatalf("azure identity spec mismatch")
		}
	}
}

func TestAddDelMICClient(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	// Test to add and delete at the same time.
	// Add a pod, identity and binding.
	crdClient.CreateID("test-id2", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding2", "default", "test-id2", "test-select2", "")

	nodeClient.AddNode("test-node2")
	podClient.AddPod("test-pod2", "default", "test-node2", "test-select2")

	crdClient.CreateID("test-id4", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding4", "default", "test-id4", "test-select4", "")
	podClient.AddPod("test-pod4", "default", "test-node2", "test-select4")

	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated

	stopSync1 := micClient.testRunSync()
	defer stopSync1(t)

	if !evtRecorder.WaitForEvents(2) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}

	// Delete the pod
	podClient.DeletePod("test-pod2", "default")
	podClient.DeletePod("test-pod4", "default")

	// Add a new pod, with different id and binding on the same node.
	crdClient.CreateID("test-id3", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding3", "default", "test-id3", "test-select3", "")
	podClient.AddPod("test-pod3", "default", "test-node2", "test-select3")

	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodDeleted
	eventCh <- internalaadpodid.PodDeleted

	stopSync1(t)
	defer micClient.testRunSync()(t)

	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned failed")
	}

	assignedID := (*listAssignedIDs)[0].Name
	expectedID := "test-pod3-default-test-id3"
	if assignedID != expectedID {
		t.Fatalf("Expected %s. Got: %s", expectedID, assignedID)
	}
}

func TestMicAddDelVMSS(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{VMType: "vmss"})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	// Test to add and delete at the same time.
	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	nodeClient.AddNode("test-node1", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss1/virtualMachines/0"
	})

	nodeClient.AddNode("test-node2", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss1/virtualMachines/1"
	})

	nodeClient.AddNode("test-node3", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss2/virtualMachines/0"
	})

	podClient.AddPod("test-pod1", "default", "test-node1", "test-select1")
	podClient.AddPod("test-pod2", "default", "test-node2", "test-select1")
	podClient.AddPod("test-pod3", "default", "test-node3", "test-select1")

	defer micClient.testRunSync()(t)

	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated
	if !evtRecorder.WaitForEvents(3) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(3) {
		t.Fatalf("expected len of assigned identities to be 3")
	}

	if !cloudClient.CompareMSI("testvmss1", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}

	podClient.DeletePod("test-pod1", "default")
	eventCh <- internalaadpodid.PodDeleted

	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}
	if !cloudClient.CompareMSI("testvmss1", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}

	podClient.DeletePod("test-pod2", "default")
	eventCh <- internalaadpodid.PodDeleted

	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	if !cloudClient.CompareMSI("testvmss1", []string{}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}
}

func TestMICStateFlow(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	nodeClient.AddNode("test-node1")
	podClient.AddPod("test-pod1", "default", "test-node1", "test-select1")

	eventCh <- internalaadpodid.PodCreated
	defer micClient.testRunSync()(t)

	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !((*listAssignedIDs)[0].Status.Status == aadpodid.AssignedIDAssigned) {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
	}

	// delete the pod, simulate failure in cloud calls on trying to un-assign identity from node
	podClient.DeletePod("test-pod1", "default")
	// SetError sets error in crd client only for remove assigned identity
	cloudClient.SetError(errors.New("error removing identity from node"))
	cloudClient.testVMClient.identity = &compute.VirtualMachineIdentity{
		UserAssignedIdentities: map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{
			testResourceID: {},
		},
	}

	eventCh <- internalaadpodid.PodDeleted
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !((*listAssignedIDs)[0].Status.Status == aadpodid.AssignedIDAssigned) {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
	}

	crdClient.SetError(errors.New("error from crd client"))

	// add new pod, this time the old assigned identity which is in Assigned state should be tried to delete
	// simulate failure on kube api call to delete crd
	crdClient.CreateID("test-id2", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid2", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding2", "default", "test-id2", "test-select2", "")

	nodeClient.AddNode("test-node2")
	podClient.AddPod("test-pod2", "default", "test-node2", "test-select2")

	eventCh <- internalaadpodid.PodCreated
	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	for _, assignedID := range *listAssignedIDs {
		if assignedID.Spec.Pod == "test-pod1" {
			if assignedID.Status.Status != aadpodid.AssignedIDUnAssigned {
				t.Fatalf("Expected status to be: %s. Got: %s", aadpodid.AssignedIDUnAssigned, assignedID.Status.Status)
			}
		}
		if assignedID.Spec.Pod == "test-pod2" {
			if assignedID.Status.Status != aadpodid.AssignedIDAssigned {
				t.Fatalf("Expected status to be: %s. Got: %s", aadpodid.AssignedIDAssigned, assignedID.Status.Status)
			}
		}
	}
	crdClient.UnsetError()

	// delete pod2 and everything should be cleaned up now
	podClient.DeletePod("test-pod2", "default")
	eventCh <- internalaadpodid.PodDeleted
	if !crdClient.waitForAssignedIDs(0) {
		t.Fatalf("expected len of assigned identities to be 0")
	}
}

func TestForceNamespaced(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, true, 4, nil)

	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "idrv1")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "bindingrv1")

	nodeClient.AddNode("test-node1")
	podClient.AddPod("test-pod1", "default", "test-node1", "test-select1")

	eventCh <- internalaadpodid.PodCreated
	defer micClient.testRunSync()(t)

	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !((*listAssignedIDs)[0].Status.Status == aadpodid.AssignedIDAssigned) {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
	}

	crdClient.CreateID("test-id1", "default2", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "idrv2")
	crdClient.CreateBinding("testbinding1", "default2", "test-id1", "test-select1", "bindingrv2")
	podClient.AddPod("test-pod2", "default2", "test-node1", "test-select1")

	eventCh <- internalaadpodid.IdentityCreated
	eventCh <- internalaadpodid.BindingCreated
	eventCh <- internalaadpodid.PodCreated

	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}

	for _, assignedID := range *listAssignedIDs {
		if !(assignedID.Status.Status == aadpodid.AssignedIDAssigned) {
			t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
		}
	}
}

func TestSyncRetryLoop(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)
	syncRetryInterval, err := time.ParseDuration("5s")
	if err != nil {
		t.Fatalf("error parsing duration: %v", err)
	}
	micClient.syncRetryInterval = syncRetryInterval

	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	nodeClient.AddNode("test-node1")
	podClient.AddPod("test-pod1", "default", "test-node1", "test-select1")

	eventCh <- internalaadpodid.PodCreated
	defer micClient.testRunSync()(t)

	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !((*listAssignedIDs)[0].Status.Status == aadpodid.AssignedIDAssigned) {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
	}

	// delete the pod, simulate failure in cloud calls on trying to un-assign identity from node
	podClient.DeletePod("test-pod1", "default")
	cloudClient.SetError(errors.New("error removing identity from node"))
	cloudClient.testVMClient.identity = &compute.VirtualMachineIdentity{
		UserAssignedIdentities: map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{
			testResourceID: {},
		},
	}

	eventCh <- internalaadpodid.PodDeleted
	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}

	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !((*listAssignedIDs)[0].Status.Status == aadpodid.AssignedIDAssigned) {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[0].Status.Status)
	}

	// mic should automatically retry and delete assigned identity
	if !crdClient.waitForAssignedIDs(0) {
		t.Fatalf("expected len of assigned identities to be 0")
	}
}

func TestSyncNodeNotFound(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	for i := 0; i < 10; i++ {
		nodeClient.AddNode(fmt.Sprintf("test-node%d", i))
		podClient.AddPod(fmt.Sprintf("test-pod%d", i), "default", fmt.Sprintf("test-node%d", i), "test-select1")
		eventCh <- internalaadpodid.PodCreated
	}

	defer micClient.testRunSync()(t)

	if !evtRecorder.WaitForEvents(10) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(10) {
		t.Fatalf("expected len of assigned identities to be 10")
	}
	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	for i := range *listAssignedIDs {
		if !((*listAssignedIDs)[i].Status.Status == aadpodid.AssignedIDAssigned) {
			t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[i].Status.Status)
		}
	}

	// delete 5 nodes
	for i := 5; i < 10; i++ {
		nodeClient.Delete(fmt.Sprintf("test-node%d", i))
		podClient.DeletePod(fmt.Sprintf("test-pod%d", i), "default")
		eventCh <- internalaadpodid.PodDeleted
	}

	nodeClient.AddNode("test-nodex")
	podClient.AddPod("test-podx", "default", "test-node1", "test-select1")
	eventCh <- internalaadpodid.PodCreated

	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(6) {
		t.Fatalf("expected len of assigned identities to be 6")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	for i := range *listAssignedIDs {
		if !((*listAssignedIDs)[i].Status.Status == aadpodid.AssignedIDAssigned) {
			t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, (*listAssignedIDs)[i].Status.Status)
		}
	}
}

func TestProcessingTimeForScale(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 20000)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 20000)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	nodeClient.AddNode("test-node1")
	for i := 0; i < 20000; i++ {
		podClient.AddPod(fmt.Sprintf("test-pod%d", i), "default", "test-node1", "test-select1")
	}
	eventCh <- internalaadpodid.PodCreated

	defer micClient.testRunSync()(t)

	if !evtRecorder.WaitForEvents(20000) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}

	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !(len(*listAssignedIDs) == 20000) {
		t.Fatalf("expected assigned identities len: %d, got: %d", 20000, len(*listAssignedIDs))
	}

	for i := 10000; i < 20000; i++ {
		podClient.DeletePod(fmt.Sprintf("test-pod%d", i), "default")
	}
	eventCh <- internalaadpodid.PodDeleted

	if !crdClient.waitForAssignedIDs(10000) {
		t.Fatalf("expected len of assigned identities to be 10000")
	}
	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}
	if !(len(*listAssignedIDs) == 10000) {
		t.Fatalf("expected assigned identities len: %d, got: %d", 10000, len(*listAssignedIDs))
	}
}

func TestSyncExit(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType)
	cloudClient := NewTestCloudClient(config.AzureConfig{VMType: "vmss"})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)

	micClient.testRunSync()(t)
}

func TestMicAddDelVMSSwithImmutableIdentities(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{VMType: "vmss"})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)
	var immutableUserMSIs = map[string]bool{
		"zero-test":              true,
		"test-user-msi-clientid": true,
	}

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, immutableUserMSIs)

	// Test to add and delete at the same time.
	// Add a pod, identity and binding.
	crdClient.CreateID("test-id1", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid", nil, "", "", "", "")
	crdClient.CreateBinding("testbinding1", "default", "test-id1", "test-select1", "")

	nodeClient.AddNode("test-node1", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss1/virtualMachines/0"
	})

	nodeClient.AddNode("test-node2", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss1/virtualMachines/1"
	})

	nodeClient.AddNode("test-node3", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/fakeSub/resourceGroups/fakeGroup/providers/Microsoft.Compute/virtualMachineScaleSets/testvmss2/virtualMachines/0"
	})

	podClient.AddPod("test-pod1", "default", "test-node1", "test-select1")
	podClient.AddPod("test-pod2", "default", "test-node2", "test-select1")
	podClient.AddPod("test-pod3", "default", "test-node3", "test-select1")

	defer micClient.testRunSync()(t)

	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated
	eventCh <- internalaadpodid.PodCreated
	if !evtRecorder.WaitForEvents(3) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}
	if !crdClient.waitForAssignedIDs(3) {
		t.Fatalf("expected len of assigned identities to be 3")
	}
	if !cloudClient.CompareMSI("testvmss1", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}

	podClient.DeletePod("test-pod1", "default")
	eventCh <- internalaadpodid.PodDeleted

	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}
	if !cloudClient.CompareMSI("testvmss1", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}

	podClient.DeletePod("test-pod2", "default")
	eventCh <- internalaadpodid.PodDeleted

	if !crdClient.waitForAssignedIDs(1) {
		t.Fatalf("expected len of assigned identities to be 1")
	}
	if !cloudClient.CompareMSI("testvmss1", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss1"])
	}
	if !cloudClient.CompareMSI("testvmss2", []string{testResourceID}) {
		t.Fatalf("missing identity: %+v", cloudClient.ListMSI()["testvmss2"])
	}
}

func TestCloudProviderRetryLoop(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType, 100)
	cloudClient := NewTestCloudClient(config.AzureConfig{})
	cloudClient.RetryClient.RegisterRetriableErrors("KnownError")
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool, 100)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)
	defer micClient.testRunSync()(t)

	erroneousTestResourceID := strings.Replace(testResourceID, "identity1", "erroneousIdentity", -1)
	cloudClient.SetError(fmt.Errorf("KnownError: '%s' is erroneous", erroneousTestResourceID))
	crdClient.CreateID("test-id-1", "default", aadpodid.UserAssignedMSI, erroneousTestResourceID, "test-user-msi-clientid-1", nil, "", "", "", "")
	crdClient.CreateBinding("test-binding-1", "default", "test-id-1", "test-select-1", "")
	crdClient.CreateID("test-id-2", "default", aadpodid.UserAssignedMSI, testResourceID, "test-user-msi-clientid-2", nil, "", "", "", "")
	crdClient.CreateBinding("test-binding-2", "default", "test-id-2", "test-select-2", "")

	nodeClient.AddNode("test-node-1")
	podClient.AddPod("test-pod-1", "default", "test-node-1", "test-select-1")
	podClient.AddPod("test-pod-2", "default", "test-node-1", "test-select-2")

	eventCh <- internalaadpodid.PodCreated
	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}

	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}

	listAssignedIDs, err := crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}

	assignedID := findAssignedIDByName("test-pod-1-default-test-id-1", listAssignedIDs)
	// Not in assigned state since the identity is erroneous
	if assignedID.Status.Status != aadpodid.AssignedIDCreated {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDCreated, assignedID.Status.Status)
	}

	assignedID = findAssignedIDByName("test-pod-2-default-test-id-2", listAssignedIDs)
	if assignedID.Status.Status != aadpodid.AssignedIDAssigned {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, assignedID.Status.Status)
	}

	podClient.DeletePod("test-pod-2", "default")
	cloudClient.SetError(fmt.Errorf("KnownError: '%s' is erroneous", testResourceID))

	eventCh <- internalaadpodid.PodDeleted
	if !evtRecorder.WaitForEvents(1) {
		t.Fatalf("Timeout waiting for mic sync cycles")
	}

	if !crdClient.waitForAssignedIDs(2) {
		t.Fatalf("expected len of assigned identities to be 2")
	}

	listAssignedIDs, err = crdClient.ListAssignedIDs()
	if err != nil {
		t.Fatalf("list assigned ids failed , error: %+v", err)
	}

	assignedID = findAssignedIDByName("test-pod-1-default-test-id-1", listAssignedIDs)
	if assignedID.Status.Status != aadpodid.AssignedIDAssigned {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, assignedID.Status.Status)
	}

	assignedID = findAssignedIDByName("test-pod-2-default-test-id-2", listAssignedIDs)
	// Should still be assigned since the cloud client encountered an error
	// when unassigning the identity from the underlying node
	if assignedID.Status.Status != aadpodid.AssignedIDAssigned {
		t.Fatalf("expected status to be %s, got: %s", aadpodid.AssignedIDAssigned, assignedID.Status.Status)
	}
}

func TestGenerateIdentityAssignmentStateVM(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType)
	cloudClient := NewTestCloudClient(config.AzureConfig{VMType: "vmss"})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)
	currentState, desiredState, isVMSSMap, err := micClient.generateIdentityAssignmentState()
	assert.Empty(t, currentState)
	assert.Empty(t, desiredState)
	assert.Empty(t, isVMSSMap)
	assert.NoError(t, err)

	nodeClient.AddNode("node-0", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Compute/virtualMachines/node-0"
	})

	_ = crdClient.CreateAssignedIdentity(&internalaadpodid.AzureAssignedIdentity{
		Spec: internalaadpodid.AzureAssignedIdentitySpec{
			NodeName: "node-0",
			AzureIdentityRef: &internalaadpodid.AzureIdentity{
				Spec: internalaadpodid.AzureIdentitySpec{
					ResourceID: testResourceID,
				},
			},
		},
		Status: internalaadpodid.AzureAssignedIdentityStatus{
			Status: aadpodid.AssignedIDAssigned,
		},
	})

	// the user-assigned identity isn't assigned to a VMSS instance on Azure
	currentState, desiredState, isVMSSMap, err = micClient.generateIdentityAssignmentState()
	assert.Equal(t, currentState, map[string]map[string]bool{
		"node-0": {},
	})
	assert.Equal(t, desiredState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, isVMSSMap, map[string]bool{
		"node-0": false,
	})
	assert.NoError(t, err)

	// the user-assigned identity is now assigned to a VM instance on Azure
	vm, _ := cloudClient.testVMClient.Get("", "node-0")
	vm.Identity = &compute.VirtualMachineIdentity{
		UserAssignedIdentities: map[string]*compute.VirtualMachineIdentityUserAssignedIdentitiesValue{
			testResourceID: {},
		},
	}
	_ = cloudClient.testVMClient.UpdateIdentities("", "node-0", vm)

	currentState, desiredState, isVMSSMap, err = micClient.generateIdentityAssignmentState()
	assert.Equal(t, currentState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, desiredState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, isVMSSMap, map[string]bool{
		"node-0": false,
	})
	assert.NoError(t, err)
}

func TestGenerateIdentityAssignmentStateVMSS(t *testing.T) {
	eventCh := make(chan internalaadpodid.EventType)
	cloudClient := NewTestCloudClient(config.AzureConfig{VMType: "vmss"})
	crdClient := NewTestCrdClient(nil)
	podClient := NewTestPodClient()
	nodeClient := NewTestNodeClient()
	var evtRecorder TestEventRecorder
	evtRecorder.lastEvent = new(LastEvent)
	evtRecorder.eventChannel = make(chan bool)

	micClient := NewMICTestClient(eventCh, cloudClient, crdClient, podClient, nodeClient, &evtRecorder, false, 4, nil)
	currentState, desiredState, isVMSSMap, err := micClient.generateIdentityAssignmentState()
	assert.Empty(t, currentState)
	assert.Empty(t, desiredState)
	assert.Empty(t, isVMSSMap)
	assert.NoError(t, err)

	nodeClient.AddNode("node-0", func(n *corev1.Node) {
		n.Spec.ProviderID = "azure:///subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Compute/virtualMachineScaleSets/node-0/virtualMachines/0"
	})

	_ = crdClient.CreateAssignedIdentity(&internalaadpodid.AzureAssignedIdentity{
		Spec: internalaadpodid.AzureAssignedIdentitySpec{
			NodeName: "node-0",
			AzureIdentityRef: &internalaadpodid.AzureIdentity{
				Spec: internalaadpodid.AzureIdentitySpec{
					Type:       internalaadpodid.UserAssignedMSI,
					ResourceID: testResourceID,
				},
			},
		},
		Status: internalaadpodid.AzureAssignedIdentityStatus{
			Status: aadpodid.AssignedIDAssigned,
		},
	})

	// the user-assigned identity isn't assigned to a VMSS instance on Azure
	currentState, desiredState, isVMSSMap, err = micClient.generateIdentityAssignmentState()
	assert.Equal(t, currentState, map[string]map[string]bool{
		"node-0": {},
	})
	assert.Equal(t, desiredState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, isVMSSMap, map[string]bool{
		"node-0": true,
	})
	assert.NoError(t, err)

	// the user-assigned identity is now assigned to a VMSS instance on Azure
	vmss, _ := cloudClient.testVMSSClient.Get("", "node-0")
	vmss.Identity = &compute.VirtualMachineScaleSetIdentity{
		UserAssignedIdentities: map[string]*compute.VirtualMachineScaleSetIdentityUserAssignedIdentitiesValue{
			testResourceID: {},
		},
	}
	_ = cloudClient.testVMSSClient.UpdateIdentities("", "node-0", vmss)

	currentState, desiredState, isVMSSMap, err = micClient.generateIdentityAssignmentState()
	assert.Equal(t, currentState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, desiredState, map[string]map[string]bool{
		"node-0": {
			testResourceID: true,
		},
	})
	assert.Equal(t, isVMSSMap, map[string]bool{
		"node-0": true,
	})
	assert.NoError(t, err)
}

func TestGenerateIdentityAssignmentDiff(t *testing.T) {
	testCases := []struct {
		currentState map[string]map[string]bool
		desiredState map[string]map[string]bool
		expectedDiff map[string][]string
	}{
		{
			currentState: map[string]map[string]bool{
				"node-0": {
					"id-0": true,
				},
			},
			desiredState: map[string]map[string]bool{
				"node-0": {
					"id-0": true,
				},
			},
			expectedDiff: map[string][]string{},
		},
		{
			currentState: map[string]map[string]bool{
				"node-1": {
					"id-1": true,
				},
			},
			desiredState: map[string]map[string]bool{
				"node-0": {
					"id-0": true,
				},
				"node-1": {
					"id-0": true,
					"id-1": true,
				},
			},
			expectedDiff: map[string][]string{
				"node-0": {
					"id-0",
				},
				"node-1": {
					"id-0",
				},
			},
		},
		{
			currentState: nil,
			desiredState: map[string]map[string]bool{
				"node-0": {
					"id-0": true,
				},
			},
			expectedDiff: map[string][]string{
				"node-0": {
					"id-0",
				},
			},
		},
		{
			currentState: map[string]map[string]bool{
				"node-0": {
					"id-0": true,
				},
			},
			desiredState: nil,
			expectedDiff: map[string][]string{},
		},
	}

	for _, tc := range testCases {
		assert.Equal(t, tc.expectedDiff, generateIdentityAssignmentDiff(tc.currentState, tc.desiredState))
	}
}

func findAssignedIDByName(name string, assignedIDs *[]internalaadpodid.AzureAssignedIdentity) *internalaadpodid.AzureAssignedIdentity {
	for _, assignedID := range *assignedIDs {
		if assignedID.Name == name {
			return &assignedID
		}
	}
	return nil
}
