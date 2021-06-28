package pod

import (
	"testing"

	internalaadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/klog/v2"
)

type TestPodClient struct {
	pods []*corev1.Pod
}

func (c TestPodClient) Start(exit <-chan struct{}) {
	klog.Info("start called from the test interface")
}

func (c TestPodClient) GetPods() (pods []*corev1.Pod, err error) {
	// TODO: Add label matching. For now we add only pods which we want to add.
	return c.pods, nil
}

func (c *TestPodClient) AddPod(podName string, podNs string, nodeName string, binding string) {
	labels := make(map[string]string)
	labels[internalaadpodid.CRDLabelKey] = binding
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
	c.pods = append(c.pods, pod)
}

func (c *TestPodClient) DeletePod(podName string, podNs string) {
	var newPods []*corev1.Pod
	changed := false
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

func TestIsPodExcepted(t *testing.T) {
	cases := []struct {
		podLabels        map[string]string
		exceptionList    []internalaadpodid.AzurePodIdentityException
		shouldBeExcepted bool
	}{
		{
			podLabels:        map[string]string{"foo": "bar"},
			exceptionList:    nil,
			shouldBeExcepted: false,
		},
		{
			podLabels: map[string]string{"foo": "except"},
			exceptionList: []internalaadpodid.AzurePodIdentityException{
				{
					ObjectMeta: metav1.ObjectMeta{
						Name: "exception1",
					},
					Spec: internalaadpodid.AzurePodIdentityExceptionSpec{
						PodLabels: map[string]string{"foo": "notexcept"},
					},
				},
			},
			shouldBeExcepted: false,
		},
		{
			podLabels: map[string]string{"foo": "except"},
			exceptionList: []internalaadpodid.AzurePodIdentityException{
				{
					ObjectMeta: metav1.ObjectMeta{
						Name: "exception1",
					},
					Spec: internalaadpodid.AzurePodIdentityExceptionSpec{
						PodLabels: map[string]string{"foo": "notexcept"},
					},
				},
				{
					ObjectMeta: metav1.ObjectMeta{
						Name: "exception2",
					},
					Spec: internalaadpodid.AzurePodIdentityExceptionSpec{
						PodLabels: map[string]string{"foo": "except"},
					},
				},
			},
			shouldBeExcepted: true,
		},
	}

	for _, tc := range cases {
		isExcepted := IsPodExcepted(tc.podLabels, tc.exceptionList)
		if isExcepted != tc.shouldBeExcepted {
			t.Fatalf("expected: %v, got %v", tc.shouldBeExcepted, isExcepted)
		}
	}
}
