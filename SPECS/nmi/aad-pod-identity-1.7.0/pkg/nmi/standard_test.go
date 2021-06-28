package nmi

import (
	"context"
	"encoding/base64"
	"reflect"
	"testing"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	auth "github.com/Azure/aad-pod-identity/pkg/auth"
	"github.com/Azure/aad-pod-identity/pkg/k8s"
	"github.com/Azure/aad-pod-identity/pkg/metrics"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

type TestKubeClient struct {
	k8s.Client
	azureIdentities interface{}
	err             error
}

func NewTestKubeClient(azids interface{}) *TestKubeClient {
	return &TestKubeClient{
		azureIdentities: azids,
	}
}

func (c *TestKubeClient) ListPodIds(podns, podname string) (map[string][]aadpodid.AzureIdentity, error) {
	identities, _ := c.azureIdentities.(map[string][]aadpodid.AzureIdentity)
	return identities, c.err
}

func TestGetTokenForMatchingIDBySP(t *testing.T) {
	fakeClient := fake.NewSimpleClientset()
	reporter, err := metrics.NewReporter()
	if err != nil {
		t.Fatalf("expected nil error, got: %+v", err)
	}
	auth.InitReporter(reporter)

	secret := &v1.Secret{ObjectMeta: metav1.ObjectMeta{Name: "clientSecret"}, Data: make(map[string][]byte)}
	val, _ := base64.StdEncoding.DecodeString("YWJjZA==")
	secret.Data["key1"] = val
	_, err = fakeClient.CoreV1().Secrets("default").Create(context.TODO(), secret, metav1.CreateOptions{})
	if err != nil {
		t.Fatalf("Error creating secret: %v", err)
	}

	kubeClient := &k8s.KubeClient{ClientSet: fakeClient}
	tokenClient, err := NewStandardTokenClient(kubeClient, Config{})
	if err != nil {
		t.Fatalf("expected err to be nil, got: %v", err)
	}

	secretRef := v1.SecretReference{
		Name:      "clientSecret",
		Namespace: "default",
	}

	podID := aadpodid.AzureIdentity{
		Spec: aadpodid.AzureIdentitySpec{
			Type:           aadpodid.ServicePrincipal,
			TenantID:       "11111111-1111-1111-1111-111111111111",
			ClientID:       "aabc0000-a83v-9h4m-000j-2c0a66b0c1f9",
			ClientPassword: secretRef,
		},
	}
	_, _ = tokenClient.GetTokens(context.Background(), podID.Spec.ClientID, "https://management.azure.com/", podID)
}

func TestGetTokenForMatchingIDBySPCertificate(t *testing.T) {
	fakeClient := fake.NewSimpleClientset()
	reporter, err := metrics.NewReporter()
	if err != nil {
		t.Fatalf("expected nil error, got: %+v", err)
	}
	auth.InitReporter(reporter)

	secret := &v1.Secret{ObjectMeta: metav1.ObjectMeta{Name: "certificate"}, Data: make(map[string][]byte)}
	val, _ := base64.StdEncoding.DecodeString("YWJjZA==")
	secret.Data["certificate"] = val
	secret.Data["password"] = val
	_, err = fakeClient.CoreV1().Secrets("default").Create(context.TODO(), secret, metav1.CreateOptions{})
	if err != nil {
		t.Fatalf("Error creating secret: %v", err)
	}

	kubeClient := &k8s.KubeClient{ClientSet: fakeClient}
	tokenClient, err := NewStandardTokenClient(kubeClient, Config{})
	if err != nil {
		t.Fatalf("expected err to be nil, got: %v", err)
	}

	secretRef := v1.SecretReference{
		Name:      "certificate",
		Namespace: "default",
	}

	podID := aadpodid.AzureIdentity{
		Spec: aadpodid.AzureIdentitySpec{
			Type:           aadpodid.ServicePrincipalCertificate,
			TenantID:       "tid",
			ClientID:       "aabc0000-a83v-9h4m-000j-2c0a66b0c1f9",
			ClientPassword: secretRef,
		},
	}
	_, _ = tokenClient.GetTokens(context.Background(), podID.Spec.ClientID, "https://management.azure.com/", podID)
}

func TestGetIdentitiesStandardClient(t *testing.T) {
	cases := []struct {
		name                  string
		azureIdentities       map[string][]aadpodid.AzureIdentity
		clientID              string
		resourceID            string
		expectedErr           bool
		expectedAzureIdentity *aadpodid.AzureIdentity
		isNamespaced          bool
		podName               string
		podNamespace          string
	}{
		{
			name:                  "no azure identities",
			azureIdentities:       make(map[string][]aadpodid.AzureIdentity),
			expectedErr:           true,
			expectedAzureIdentity: nil,
			podName:               "pod1",
			podNamespace:          "default",
		},
		{
			name: "azure identities with old 1.3/1.4, no request client id",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				"": {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid1",
						},
					},
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid2",
						},
					},
				},
			},
			expectedErr: false,
			expectedAzureIdentity: &aadpodid.AzureIdentity{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "azid1",
					Namespace: "default",
				},
				Spec: aadpodid.AzureIdentitySpec{
					ClientID: "clientid1",
				},
			},
			podName:      "pod2",
			podNamespace: "default",
		},
		{
			name: "no identity requested, found in created state only",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDCreated: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid3",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid3",
						},
					},
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid4",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid4",
						},
					},
				},
			},
			expectedAzureIdentity: &aadpodid.AzureIdentity{},
			expectedErr:           true,
			podName:               "pod3",
			podNamespace:          "default",
		},
		{
			name: "no identity requested, found in assigned state",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid5",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid5",
						},
					},
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid6",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid6",
						},
					},
				},
			},
			expectedErr: false,
			expectedAzureIdentity: &aadpodid.AzureIdentity{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "azid5",
					Namespace: "default",
				},
				Spec: aadpodid.AzureIdentitySpec{
					ClientID: "clientid5",
				},
			},
			podName:      "pod4",
			podNamespace: "default",
		},
		{
			name: "client id in request, no identity with same client id in assigned state",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDCreated: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid1",
						},
					},
				},
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID:   "clientid2",
							ResourceID: "clientid1", // ensure that we are matching against ClientID
						},
					},
				},
			},
			expectedErr:           true,
			expectedAzureIdentity: &aadpodid.AzureIdentity{},
			podName:               "pod5",
			podNamespace:          "default",
			clientID:              "clientid1",
		},
		{
			name: "resource id in request, no identity with same resource id in assigned state",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDCreated: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ResourceID: "resourceid1",
						},
					},
				},
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID:   "resourceid1", // ensure we are matching against ResourceID
							ResourceID: "resourceid2",
						},
					},
				},
			},
			expectedErr:           true,
			expectedAzureIdentity: &aadpodid.AzureIdentity{},
			podName:               "pod5",
			podNamespace:          "default",
			resourceID:            "resourceid1",
		},
		{
			name: "client id in request, found matching identity",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDCreated: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid1",
						},
					},
				},
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID:   "clientid2",
							ResourceID: "resourceid2",
						},
					},
				},
			},
			expectedAzureIdentity: &aadpodid.AzureIdentity{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "azid2",
					Namespace: "default",
				},
				Spec: aadpodid.AzureIdentitySpec{
					ClientID:   "clientid2",
					ResourceID: "resourceid2",
				},
			},
			podName:      "pod5",
			podNamespace: "default",
			clientID:     "clientid2",
		},
		{
			name: "resource id in request, found matching identity",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDCreated: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ResourceID: "resourceid1",
						},
					},
				},
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID:   "resourceid2",
							ResourceID: "resourceid2",
						},
					},
				},
			},
			expectedAzureIdentity: &aadpodid.AzureIdentity{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "azid2",
					Namespace: "default",
				},
				Spec: aadpodid.AzureIdentitySpec{
					ClientID:   "resourceid2",
					ResourceID: "resourceid2",
				},
			},
			podName:      "pod5",
			podNamespace: "default",
			resourceID:   "resourceid2",
		},
		{
			name: "no identity requested, identity in same namespace returned with force namespace mode",
			azureIdentities: map[string][]aadpodid.AzureIdentity{
				aadpodid.AssignedIDAssigned: {
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid2",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid2",
						},
					},
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid1",
							Namespace: "default",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid1",
						},
					},
					{
						ObjectMeta: metav1.ObjectMeta{
							Name:      "azid3",
							Namespace: "testns",
						},
						Spec: aadpodid.AzureIdentitySpec{
							ClientID: "clientid3",
						},
					},
				},
			},
			expectedErr: false,
			expectedAzureIdentity: &aadpodid.AzureIdentity{
				ObjectMeta: metav1.ObjectMeta{
					Name:      "azid3",
					Namespace: "testns",
				},
				Spec: aadpodid.AzureIdentitySpec{
					ClientID: "clientid3",
				},
			},
			podName:      "pod8",
			podNamespace: "testns",
			isNamespaced: true,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			tokenClient, err := NewStandardTokenClient(NewTestKubeClient(tc.azureIdentities), Config{
				Mode:                               "standard",
				RetryAttemptsForCreated:            2,
				RetryAttemptsForAssigned:           1,
				FindIdentityRetryIntervalInSeconds: 1,
				Namespaced:                         tc.isNamespaced,
			})
			if err != nil {
				t.Fatalf("expected err to be nil, got: %v", err)
			}

			azIdentity, err := tokenClient.GetIdentities(context.Background(), tc.podNamespace, tc.podName, tc.clientID, tc.resourceID)
			if tc.expectedErr != (err != nil) {
				t.Fatalf("expected error: %v, got: %v", tc.expectedErr, err)
			}
			if !reflect.DeepEqual(tc.expectedAzureIdentity, azIdentity) {
				t.Fatalf("expected the azure identity to be equal")
			}
		})
	}
}
