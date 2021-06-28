package k8s

import (
	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// FakeClient implements Interface
type FakeClient struct {
}

// NewFakeClient new fake kubernetes api client
func NewFakeClient() (Client, error) {

	fakeClient := &FakeClient{}

	return fakeClient, nil
}

// GetPodInfo returns fake pod name, namespace and replicaset
func (c *FakeClient) GetPodInfo(podip string) (podns, podname, rsName string, selectors *metav1.LabelSelector, err error) {
	return "ns", "podname", "rsName", nil, nil
}

// GetPod returns fake pod object and nil error
func (c *FakeClient) GetPod(podns, podname string) (v1.Pod, error) {
	return v1.Pod{}, nil
}

// ListPodIds for pod
func (c *FakeClient) ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error) {
	return nil, nil
}

// ListPodIdsWithBinding for pod
func (c *FakeClient) ListPodIdsWithBinding(podns string, labels map[string]string) ([]aadpodid.AzureIdentity, error) {
	return nil, nil
}

// ListPodIdentityExceptions for pod
func (c *FakeClient) ListPodIdentityExceptions(ns string) (*[]aadpodid.AzurePodIdentityException, error) {
	return nil, nil
}

// GetSecret returns secret the secretRef represents
func (c *FakeClient) GetSecret(secretRef *v1.SecretReference) (*v1.Secret, error) {
	return nil, nil
}

// Start - for starting informer clients in the fake Client
func (c *FakeClient) Start(exit <-chan struct{}) {

}
