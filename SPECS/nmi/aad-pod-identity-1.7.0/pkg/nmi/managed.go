package nmi

import (
	"context"
	"fmt"
	"strings"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	auth "github.com/Azure/aad-pod-identity/pkg/auth"
	k8s "github.com/Azure/aad-pod-identity/pkg/k8s"
	utils "github.com/Azure/aad-pod-identity/pkg/utils"

	"github.com/Azure/go-autorest/autorest/adal"
	"k8s.io/klog/v2"
)

// ManagedClient implements the TokenClient interface
type ManagedClient struct {
	TokenClient
	KubeClient   k8s.Client
	IsNamespaced bool
}

// NewManagedTokenClient creates new managed token client
func NewManagedTokenClient(client k8s.Client, config Config) (*ManagedClient, error) {
	// managed mode supported only in force namespaced mode
	if !config.Namespaced {
		return nil, fmt.Errorf("managed mode not intialized in force namespaced mode")
	}
	return &ManagedClient{
		KubeClient:   client,
		IsNamespaced: config.Namespaced,
	}, nil
}

// GetIdentities gets the azure identity that matches the podns/podname and client id
func (mc *ManagedClient) GetIdentities(ctx context.Context, podns, podname, clientID, resourceID string) (*aadpodid.AzureIdentity, error) {
	// get pod object to retrieve labels
	pod, err := mc.KubeClient.GetPod(podns, podname)
	if err != nil {
		return nil, fmt.Errorf("failed to get pod %s/%s, error: %+v", podns, podname, err)
	}
	// get all the azure identities based on azure identity bindings
	azureIdentities, err := mc.KubeClient.ListPodIdsWithBinding(podns, pod.Labels)
	if err != nil {
		return nil, fmt.Errorf("failed to get AzureIdentities for pod %s/%s, error: %+v", podns, podname, err)
	}
	identityUnspecified := len(clientID) == 0 && len(resourceID) == 0
	for _, id := range azureIdentities {
		// if client id exists in the request, then send the first identity that matched the client id
		if len(clientID) != 0 && id.Spec.ClientID == clientID {
			klog.Infof("clientID in request: %s, %s/%s has been matched with azure identity %s/%s", utils.RedactClientID(clientID), podns, podname, id.Namespace, id.Name)
			return &id, nil
		}

		// if resource id exists in the request, then send the first identity that matched the resource id
		if len(resourceID) != 0 && id.Spec.ResourceID == resourceID {
			return &id, nil
		}

		// if client doesn't exist in the request, then return the first identity in the same namespace as the pod
		if identityUnspecified && strings.EqualFold(id.Namespace, podns) {
			klog.Infof("no clientID or resourceID in request. %s/%s has been matched with azure identity %s/%s", podns, podname, id.Namespace, id.Name)
			return &id, nil
		}
	}
	return nil, fmt.Errorf("no azure identity found for request clientID %s", utils.RedactClientID(clientID))
}

// GetTokens returns ADAL tokens based on the request and its pod identity.
func (mc *ManagedClient) GetTokens(ctx context.Context, rqClientID, rqResource string, azureID aadpodid.AzureIdentity) (tokens []*adal.Token, err error) {
	rqHasClientID := len(rqClientID) != 0
	clientID := azureID.Spec.ClientID

	idType := azureID.Spec.Type
	switch idType {
	case aadpodid.UserAssignedMSI:
		if rqHasClientID && !strings.EqualFold(rqClientID, clientID) {
			klog.Warningf("client ID mismatch, requested:%s available:%s", rqClientID, clientID)
		}
		klog.Infof("matched identityType:%v clientid:%s resource:%s", idType, utils.RedactClientID(clientID), rqResource)
		token, err := auth.GetServicePrincipalTokenFromMSIWithUserAssignedID(clientID, rqResource)
		return []*adal.Token{token}, err
	case aadpodid.ServicePrincipal:
		tenantID := azureID.Spec.TenantID
		auxiliaryTenantIDs := azureID.Spec.AuxiliaryTenantIDs
		adEndpoint := azureID.Spec.ADEndpoint
		secretRef := &azureID.Spec.ClientPassword
		klog.Infof("matched identityType:%v adendpoint:%s tenantid:%s auxiliaryTenantIDs:%v clientid:%s resource:%s",
			idType, adEndpoint, tenantID, auxiliaryTenantIDs, utils.RedactClientID(clientID), rqResource)
		secret, err := mc.KubeClient.GetSecret(secretRef)
		if err != nil {
			return nil, fmt.Errorf("failed to get Kubernetes secret %s/%s, err: %v", secretRef.Namespace, secretRef.Name, err)
		}
		clientSecret := ""
		for _, v := range secret.Data {
			clientSecret = string(v)
			break
		}
		tokens, err := auth.GetServicePrincipalToken(adEndpoint, tenantID, clientID, clientSecret, rqResource, auxiliaryTenantIDs)
		return tokens, err
	case aadpodid.ServicePrincipalCertificate:
		tenantID := azureID.Spec.TenantID
		adEndpoint := azureID.Spec.ADEndpoint
		secretRef := &azureID.Spec.ClientPassword
		klog.Infof("matched identityType:%v adendpoint:%s tenantid:%s clientid:%s resource:%s",
			idType, adEndpoint, tenantID, utils.RedactClientID(clientID), rqResource)
		secret, err := mc.KubeClient.GetSecret(secretRef)
		if err != nil {
			return nil, fmt.Errorf("failed to get Kubernetes secret %s/%s, err: %v", secretRef.Namespace, secretRef.Name, err)
		}
		certificate, password := secret.Data["certificate"], secret.Data["password"]
		token, err := auth.GetServicePrincipalTokenWithCertificate(adEndpoint, tenantID, clientID,
			certificate, string(password), rqResource)
		return []*adal.Token{token}, err
	default:
		return nil, fmt.Errorf("unsupported identity type %+v", idType)
	}
}
