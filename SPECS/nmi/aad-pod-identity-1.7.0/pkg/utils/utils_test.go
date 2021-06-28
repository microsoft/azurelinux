package utils

import (
	"io/ioutil"
	"os"
	"testing"
)

func TestRedactClientID(t *testing.T) {
	tests := []struct {
		name     string
		clientID string
		expected string
	}{
		{
			name:     "should redact client id",
			clientID: "aabc0000-a83v-9h4m-000j-2c0a66b0c1f9",
			expected: "aabc##### REDACTED #####c1f9",
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			actual := RedactClientID(test.clientID)
			if actual != test.expected {
				t.Fatalf("expected: %s, got %s", test.expected, actual)
			}
		})
	}
}

func TestIsValidResourceID(t *testing.T) {
	tests := []struct {
		name        string
		resourceID  string
		expectedErr bool
	}{
		{
			name:        "invalid resource id 0",
			resourceID:  "invalidresid",
			expectedErr: true,
		},
		{
			name:        "invalid resource id 1",
			resourceID:  "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/0000/providers/Microsoft.ManagedIdentity/keyvault-identity-0",
			expectedErr: true,
		},
		{
			name:        "valid resource id",
			resourceID:  "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/0000/providers/Microsoft.ManagedIdentity/userAssignedIdentities/keyvault-identity-0",
			expectedErr: false,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			err := ValidateResourceID(test.resourceID)
			actualErr := err != nil
			if actualErr != test.expectedErr {
				t.Fatalf("expected error: %v, got error: %v", test.expectedErr, err)
			}
		})
	}
}

func TestIsKubenetCNI(t *testing.T) {
	tests := []struct {
		name                 string
		kubeletConfig        string
		expectedIsKubenetCNI bool
	}{
		{
			name: "network plugin cni",
			kubeletConfig: `KUBELET_FLAGS=--address=0.0.0.0 --anonymous-auth=false --authentication-token-webhook=true --authorization-mode=Webhook --azure-container-registry-config=/etc/kubernetes/azure.json --cgroups-per-qos=true --client-ca-file=/etc/kubernetes/certs/ca.crt --cloud-config=/etc/kubernetes/azure.json --cloud-provider=azure --cluster-dns=10.0.0.10 --cluster-domain=cluster.local --dynamic-config-dir=/var/lib/kubelet --enforce-node-allocatable=pods --event-qps=0 --eviction-hard=memory.available<750Mi,nodefs.available<10%,nodefs.inodesFree<5% --feature-gates=RotateKubeletServerCertificate=true --image-gc-high-threshold=85 --image-gc-low-threshold=80 --image-pull-progress-deadline=30m --keep-terminated-pod-volumes=false --kube-reserved=cpu=100m,memory=1638Mi --kubeconfig=/var/lib/kubelet/kubeconfig --max-pods=110 --network-plugin=cni --node-status-update-frequency=10s --non-masquerade-cidr=0.0.0.0/0 --pod-infra-container-image=mcr.microsoft.com/oss/kubernetes/pause:1.3.1 --pod-manifest-path=/etc/kubernetes/manifests --pod-max-pids=-1 --protect-kernel-defaults=true --read-only-port=0 --rotate-certificates=false --streaming-connection-idle-timeout=4h --tls-cert-file=/etc/kubernetes/certs/kubeletserver.crt --tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256 --tls-private-key-file=/etc/kubernetes/certs/kubeletserver.key
KUBELET_REGISTER_SCHEDULABLE=true
NETWORK_POLICY=

KUBELET_NODE_LABELS=kubernetes.azure.com/role=agent,agentpool=agentpool,storageprofile=managed,storagetier=Premium_LRS,kubernetes.azure.com/cluster=MC_aks1016_c00_southcentralus,kubernetes.azure.com/mode=system,kubernetes.azure.com/node-image-version=AKSUbuntu-1604-2020.09.30`,
			expectedIsKubenetCNI: false,
		},
		{
			name: "network plugin kubenet",
			kubeletConfig: `KUBELET_FLAGS=--address=0.0.0.0 --anonymous-auth=false --authentication-token-webhook=true --authorization-mode=Webhook --azure-container-registry-config=/etc/kubernetes/azure.json --cgroups-per-qos=true --client-ca-file=/etc/kubernetes/certs/ca.crt --cloud-config=/etc/kubernetes/azure.json --cloud-provider=azure --cluster-dns=10.0.0.10 --cluster-domain=cluster.local --dynamic-config-dir=/var/lib/kubelet --enforce-node-allocatable=pods --event-qps=0 --eviction-hard=memory.available<750Mi,nodefs.available<10%,nodefs.inodesFree<5% --feature-gates=RotateKubeletServerCertificate=true --image-gc-high-threshold=85 --image-gc-low-threshold=80 --image-pull-progress-deadline=30m --keep-terminated-pod-volumes=false --kube-reserved=cpu=100m,memory=1638Mi --kubeconfig=/var/lib/kubelet/kubeconfig --max-pods=110 --network-plugin=kubenet --node-status-update-frequency=10s --non-masquerade-cidr=0.0.0.0/0 --pod-infra-container-image=mcr.microsoft.com/oss/kubernetes/pause:1.3.1 --pod-manifest-path=/etc/kubernetes/manifests --pod-max-pids=-1 --protect-kernel-defaults=true --read-only-port=0 --rotate-certificates=false --streaming-connection-idle-timeout=4h --tls-cert-file=/etc/kubernetes/certs/kubeletserver.crt --tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256 --tls-private-key-file=/etc/kubernetes/certs/kubeletserver.key
KUBELET_REGISTER_SCHEDULABLE=true
NETWORK_POLICY=

KUBELET_NODE_LABELS=kubernetes.azure.com/role=agent,agentpool=agentpool,storageprofile=managed,storagetier=Premium_LRS,kubernetes.azure.com/cluster=MC_aks1016_c00_southcentralus,kubernetes.azure.com/mode=system,kubernetes.azure.com/node-image-version=AKSUbuntu-1604-2020.09.30`,
			expectedIsKubenetCNI: true,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			tmpFile, err := ioutil.TempFile("", "ut")
			if err != nil {
				t.Fatalf("expected err to be nil, got: %+v", err)
			}
			defer os.Remove(tmpFile.Name())

			_, err = tmpFile.Write([]byte(test.kubeletConfig))
			if err != nil {
				t.Fatalf("expected err to be nil, got: %+v", err)
			}

			isKubenet, err := IsKubenetCNI(tmpFile.Name())
			if err != nil {
				t.Fatalf("expected err to be nil, got: %+v", err)
			}
			if isKubenet != test.expectedIsKubenetCNI {
				t.Fatalf("expected kubenet CNI to be %v, got: %v", test.expectedIsKubenetCNI, isKubenet)
			}
		})
	}
}
