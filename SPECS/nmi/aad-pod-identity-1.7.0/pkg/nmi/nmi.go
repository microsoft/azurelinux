package nmi

import (
	"context"
	"fmt"

	aadpodid "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity"
	"github.com/Azure/aad-pod-identity/pkg/k8s"

	"github.com/Azure/go-autorest/autorest/adal"
	"k8s.io/klog/v2"
)

// OperationMode is the mode in which NMI is operating
// allowed values: standard, managed
type OperationMode string

// Config is the parameters used by token client
type Config struct {
	// Mode is the operation mode for token client
	Mode string
	// RetryAttemptsForCreated number of retries in NMI to find assigned identity in CREATED state for standard mode
	RetryAttemptsForCreated int
	// RetryAttemptsForAssigned number of retries in NMI to find assigned identity in ASSIGNED state for standard mode
	RetryAttemptsForAssigned int
	// FindIdentityRetryIntervalInSeconds Retry interval to find assigned identities in seconds for standard mode
	FindIdentityRetryIntervalInSeconds int
	// NodeName is the node on which NMI is running
	NodeName string
	// Namespaced makes NMI looks for identities in same namespace as pods
	Namespaced bool
}

const (
	// StandardMode is the name of NMI's standard mode.
	StandardMode OperationMode = "standard"

	// ManagedMode is the name of NMI's managed mode.
	ManagedMode OperationMode = "managed"
)

// TokenClient is an abstraction used to retrieve pods' identities and ADAL tokens.
type TokenClient interface {
	// GetIdentities gets the list of identities which match the
	// given pod in the form of AzureIdentity.
	GetIdentities(ctx context.Context, podns, podname, clientID, resourceID string) (*aadpodid.AzureIdentity, error)
	// GetTokens acquires tokens by using the AzureIdentity.
	GetTokens(ctx context.Context, clientID, resource string, podID aadpodid.AzureIdentity) (tokens []*adal.Token, err error)
}

// GetTokenClient returns a token client
func GetTokenClient(client k8s.Client, config Config) (TokenClient, error) {
	klog.Infof("initializing in %s mode", config.Mode)

	switch getOperationMode(config.Mode) {
	case StandardMode:
		return NewStandardTokenClient(client, config)
	case ManagedMode:
		return NewManagedTokenClient(client, config)
	default:
		return nil, fmt.Errorf("operation mode %s not supported", config.Mode)
	}
}

func getOperationMode(mode string) OperationMode {
	return OperationMode(mode)
}

// GetKubeClient returns kube client based on nmi mode
func GetKubeClient(nodeName, mode string, enableScaleFeatures bool) (k8s.Client, error) {
	// StandardMode client doesn't require azure identity and binding informers
	// ManagedMode client doesn't require azure assigned identity informers
	return k8s.NewKubeClient(nodeName, enableScaleFeatures, OperationMode(mode) == StandardMode)
}
