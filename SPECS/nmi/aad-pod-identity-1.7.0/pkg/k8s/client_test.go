package k8s

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"
	"testing"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/kubernetes/fake"
	fakerest "k8s.io/client-go/rest/fake"
)

func TestGetSecret(t *testing.T) {
	secretName := "clientSecret"

	fakeClient := fake.NewSimpleClientset()

	secret := &v1.Secret{ObjectMeta: metav1.ObjectMeta{Name: secretName}}
	_, err := fakeClient.CoreV1().Secrets("default").Create(context.TODO(), secret, metav1.CreateOptions{})
	if err != nil {
		t.Fatalf("Error creating secret: %v", err)
	}

	kubeClient := &KubeClient{ClientSet: fakeClient}

	secretRef := &v1.SecretReference{
		Name:      secretName,
		Namespace: "default",
	}
	retrievedSecret, err := kubeClient.GetSecret(secretRef)
	if err != nil {
		t.Fatalf("Error getting secret: %v", err)
	}
	if retrievedSecret.ObjectMeta.Name != secretName {
		t.Fatalf("Incorrect secret name: %v", retrievedSecret.ObjectMeta.Name)
	}
}

type TestClientSet struct {
	mu      *sync.Mutex
	podList []v1.Pod
}

func (t *TestClientSet) GetTestClientSet() (kubernetes.Interface, *fakerest.RESTClient) {
	TestGroupVersion := schema.GroupVersion{Group: "", Version: "v1"}
	fakeClient := fake.NewSimpleClientset()

	scheme := runtime.NewScheme()
	scheme.AddKnownTypes(TestGroupVersion, &v1.PodList{})

	fakeRestClient := &fakerest.RESTClient{
		NegotiatedSerializer: serializer.WithoutConversionCodecFactory{
			CodecFactory: serializer.NewCodecFactory(scheme)},
		Resp: &http.Response{
			StatusCode: http.StatusOK,
			Body:       t.SerializeObject(&metav1.APIVersions{Versions: []string{"version1"}}),
		},
		Client: fakerest.CreateHTTPClient(func(req *http.Request) (*http.Response, error) {
			header := http.Header{}
			header.Set("Content-Type", runtime.ContentTypeJSON)
			return &http.Response{StatusCode: http.StatusOK, Header: header, Body: t.GetPodList()}, nil
		}),
	}
	return fakeClient, fakeRestClient
}

func (t *TestClientSet) AddPod(name, ns, ip string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	pod := &v1.Pod{
		TypeMeta: metav1.TypeMeta{
			Kind:       "Pod",
			APIVersion: "v1",
		},
		ObjectMeta: metav1.ObjectMeta{
			Name:      name,
			Namespace: ns,
		},
		Status: v1.PodStatus{
			PodIP: ip,
		},
	}
	t.podList = append(t.podList, *pod)
}

func (t *TestClientSet) DeletePod(name, ns string) {
	for i, p := range t.podList {
		if strings.EqualFold(name, p.Name) && strings.EqualFold(ns, p.Namespace) {
			t.podList = append(t.podList[:i], t.podList[i+1:]...)
			break
		}
	}
}

func (t *TestClientSet) SerializeObject(o interface{}) io.ReadCloser {
	output, err := json.MarshalIndent(o, "", "")
	if err != nil {
		panic(err)
	}
	return ioutil.NopCloser(bytes.NewReader([]byte(output)))
}

func (t *TestClientSet) GetPodList() io.ReadCloser {
	t.mu.Lock()
	defer t.mu.Unlock()

	podList := &v1.PodList{}
	podList.Items = append(podList.Items, t.podList...)
	podList.TypeMeta = metav1.TypeMeta{
		Kind:       "PodList",
		APIVersion: "v1",
	}

	return t.SerializeObject(podList)
}

/*
func TestGetPodInfo(t *testing.T) {

	testClientSet := &TestClientSet{mu: &sync.Mutex{}}
	client, restClient := testClientSet.GetTestClientSet()

	optionsModifier := func(options *metav1.ListOptions) {}
	podListWatch := cache.NewFilteredListWatchFromClient(
		restClient,
		"pods",
		v1.NamespaceAll,
		optionsModifier,
	)
	kubeClient := &KubeClient{ClientSet: client, PodListWatch: podListWatch}

	// Test a single pod
	testPodName := "testpodname"
	testPodNs := "default"
	testPodIP := "10.0.0.8"
	testClientSet.AddPod(testPodName, testPodNs, testPodIP)
	podNs, podName, _, _, err := kubeClient.GetPodInfo(testPodIP)
	if err != nil {
		t.Fatalf("Error getting pod: %v", err)
	}
	if podName != testPodName {
		t.Fatalf("Incorrect pod name: %v", podName)
	}
	if podNs != testPodNs {
		t.Fatalf("Incorrect pod ns: %v", podNs)
	}

	// Delete test
	testPodIP = "10.0.0.8"
	testClientSet.DeletePod(testPodName, testPodNs)
	podNs, podName, _, _, err = kubeClient.GetPodInfo(testPodIP)
	if err == nil {
		t.Fatal("Pod still in pod list")
	}
}

func TestPodListRetries(t *testing.T) {
	// this test is to solely test the retry and sleep logic works as expected
	podIP := "10.0.0.8"
	testClientSet := &TestClientSet{mu: &sync.Mutex{}}
	client, restClient := testClientSet.GetTestClientSet()

	testPodName := "testpodname"
	testPodNs := "default"
	testPodIP := "10.0.0.8"

	optionsModifier := func(options *metav1.ListOptions) {}
	podListWatch := cache.NewFilteredListWatchFromClient(
		restClient,
		"pods",
		v1.NamespaceAll,
		optionsModifier,
	)

	kubeClient := &KubeClient{ClientSet: client, PodListWatch: podListWatch}

	time.AfterFunc(time.Duration(1200*time.Millisecond), func() {
		testClientSet.AddPod(testPodName, testPodNs, testPodIP)
	})

	start := time.Now()
	podNs, podName, _, _, err := kubeClient.GetPodInfo(podIP)
	elapsed := time.Since(start)

	if err != nil {
		t.Fatalf("Error getting pod: %v", err)
	}
	if podName != testPodName {
		t.Fatalf("Incorrect pod name: %v", podName)
	}
	if podNs != testPodNs {
		t.Fatalf("Incorrect pod ns: %v", podNs)
	}
	// check the retries actually work as the pod object is created only after 1.2s
	if elapsed < 1200*time.Millisecond {
		t.Fatalf("Retry logic not working as expected. Elapsed time: %v", elapsed)
	}
}
*/
func TestGetReplicaSet(t *testing.T) {
	pod := &v1.Pod{}
	rsIndex := 1
	for i := 0; i < 3; i++ {
		owner := metav1.OwnerReference{}
		owner.Name = "test" + fmt.Sprintf("%d", i)
		if i == rsIndex {
			owner.Kind = "ReplicaSet"
		} else {
			owner.Kind = "Kind" + fmt.Sprintf("%d", i)
		}
		pod.OwnerReferences = append(pod.OwnerReferences, owner)
	}

	c := &KubeClient{}
	rsName := c.getReplicasetName(*pod)
	if rsName != "test1" {
		t.Fatalf("Expected rsName: test1. Got: %s", rsName)
	}
}
