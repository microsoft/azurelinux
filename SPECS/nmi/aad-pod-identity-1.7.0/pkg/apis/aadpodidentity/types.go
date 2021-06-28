package aadpodidentity

import (
	api "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EventType is a type that represents critical events that are sent to MIC.
type EventType int

const (
	// PodCreated is an event that is sent to the event channel when a pod is created.
	PodCreated EventType = 0

	// PodDeleted is an event that is sent to the event channel when a pod is deleted.
	PodDeleted EventType = 1

	// PodUpdated is an event that is sent to the event channel when a pod is updated.
	PodUpdated EventType = 2

	// IdentityCreated is an event that is sent to the event channel when an AzureIdentity is created.
	IdentityCreated EventType = 3

	// IdentityDeleted is an event that is sent to the event channel when an AzureIdentity is deleted.
	IdentityDeleted EventType = 4

	// IdentityUpdated is an event that is sent to the event channel when an AzureIdentity is updated.
	IdentityUpdated EventType = 5

	// BindingCreated is an event that is sent to the event channel when an AzureIdentityBinding is created.
	BindingCreated EventType = 6

	// BindingDeleted is an event that is sent to the event channel when an AzureIdentityBinding is deleted.
	BindingDeleted EventType = 7

	// BindingUpdated is an event that is sent to the event channel when an AzureIdentityBinding is updated.
	BindingUpdated EventType = 8

	// Exit is an event that is sent to the event channel when the program exits.
	Exit EventType = 9
)

const (
	// CRDGroup is the group name of aad-pod-identity CRDs.
	CRDGroup = "aadpodidentity.k8s.io"

	// CRDVersion is the version of the CRD group.
	CRDVersion = "v1"

	// CRDLabelKey is the static label that is used in pods.
	CRDLabelKey = "aadpodidbinding"

	// BehaviorKey is the key that describes the behavior of aad-pod-identity.
	// Supported values:
	// namespaced - used for running in namespaced mode. AzureIdentity,
	//              AzureIdentityBinding and pod in the same namespace
	//              will only be matched for this behavior.
	BehaviorKey = "aadpodidentity.k8s.io/Behavior"

	// BehaviorNamespaced indicates that aad-pod-identity is behaving in namespaced mode.
	BehaviorNamespaced = "namespaced"

	// AssignedIDCreated indicates that an AzureAssignedIdentity is created.
	AssignedIDCreated = "Created"

	// AssignedIDAssigned indicates that an identity has been assigned to the node.
	AssignedIDAssigned = "Assigned"

	// AssignedIDUnAssigned indicates that an identity has been unassigned from the node.
	AssignedIDUnAssigned = "Unassigned"
)

// AzureIdentity is the specification of the identity data structure.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureIdentity struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   AzureIdentitySpec   `json:"spec"`
	Status AzureIdentityStatus `json:"status"`
}

// AzureIdentityBinding brings together the spec of matching pods and the identity which they can use.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureIdentityBinding struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   AzureIdentityBindingSpec   `json:"spec"`
	Status AzureIdentityBindingStatus `json:"status"`
}

// AzureAssignedIdentity contains the identity <-> pod mapping which is matched.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureAssignedIdentity struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   AzureAssignedIdentitySpec   `json:"spec"`
	Status AzureAssignedIdentityStatus `json:"Status"`
}

// AzurePodIdentityException contains the pod selectors for all pods that don't require
// NMI to process and request token on their behalf.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzurePodIdentityException struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   AzurePodIdentityExceptionSpec   `json:"spec"`
	Status AzurePodIdentityExceptionStatus `json:"Status"`
}

// AzureIdentityList contains a list of AzureIdentities.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureIdentityList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []AzureIdentity `json:"items"`
}

// AzureIdentityBindingList contains a list of AzureIdentityBindings.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureIdentityBindingList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []AzureIdentityBinding `json:"items"`
}

// AzureAssignedIdentityList contains a list of AzureAssignedIdentities.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzureAssignedIdentityList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []AzureAssignedIdentity `json:"items"`
}

// AzurePodIdentityExceptionList contains a list of AzurePodIdentityExceptions.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type AzurePodIdentityExceptionList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []AzurePodIdentityException `json:"items"`
}

// IdentityType represents different types of identities.
//+k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
type IdentityType int

const (
	// UserAssignedMSI represents a user-assigned identity.
	UserAssignedMSI IdentityType = 0

	// ServicePrincipal represents a service principal.
	ServicePrincipal IdentityType = 1

	// ServicePrincipalCertificate represents a service principal certificate.
	ServicePrincipalCertificate IdentityType = 2
)

// AzureIdentitySpec describes the credential specifications of an identity on Azure.
type AzureIdentitySpec struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	// UserAssignedMSI or Service Principal
	Type IdentityType `json:"type"`

	// User assigned MSI resource id.
	ResourceID string `json:"resourceid"`
	// Both User Assigned MSI and SP can use this field.
	ClientID string `json:"clientid"`

	// Used for service principal
	ClientPassword api.SecretReference `json:"clientpassword"`
	// Service principal primary tenant id.
	TenantID string `json:"tenantid"`
	// Service principal auxiliary tenant ids
	AuxiliaryTenantIDs []string `json:"auxiliarytenantids"`
	// For service principal. Option param for specifying the  AD details.
	ADResourceID string `json:"adresourceid"`
	ADEndpoint   string `json:"adendpoint"`

	Replicas *int32 `json:"replicas"`
}

// AzureIdentityStatus contains the replica status of the resource.
type AzureIdentityStatus struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	AvailableReplicas int32 `json:"availableReplicas"`
}

// AssignedIDState represents the state of an AzureAssignedIdentity
type AssignedIDState int

const (
	// Created - Default state of the assigned identity
	Created AssignedIDState = 0

	// Assigned - When the underlying platform assignment of
	// managed identity is complete, the state moves to assigned
	Assigned AssignedIDState = 1
)

const (
	// AzureIDResource is the name of AzureIdentity.
	AzureIDResource = "azureidentities"

	// AzureIDBindingResource is the name of AzureIdentityBinding.
	AzureIDBindingResource = "azureidentitybindings"

	// AzureAssignedIDResource is the name of AzureAssignedIdentity.
	AzureAssignedIDResource = "azureassignedidentities"

	// AzurePodIdentityExceptionResource is the name of AzureIdentityException.
	AzurePodIdentityExceptionResource = "azurepodidentityexceptions"
)

// AzureIdentityBindingSpec matches the pod with the Identity.
// Used to indicate the potential matches to look for between the pod/deployment
// and the identities present.
type AzureIdentityBindingSpec struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	AzureIdentity     string `json:"azureidentity"`
	Selector          string `json:"selector"`
	// Weight is used to figure out which of the matching identities would be selected.
	Weight int `json:"weight"`
}

// AzureIdentityBindingStatus contains the status of an AzureIdentityBinding.
type AzureIdentityBindingStatus struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	AvailableReplicas int32 `json:"availableReplicas"`
}

// AzureAssignedIdentitySpec contains the relationship
// between an AzureIdentity and an AzureIdentityBinding.
type AzureAssignedIdentitySpec struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	AzureIdentityRef  *AzureIdentity        `json:"azureidentityref"`
	AzureBindingRef   *AzureIdentityBinding `json:"azurebindingref"`
	Pod               string                `json:"pod"`
	PodNamespace      string                `json:"podnamespace"`
	NodeName          string                `json:"nodename"`

	Replicas *int32 `json:"replicas"`
}

// AzureAssignedIdentityStatus contains the replica status of the resource.
type AzureAssignedIdentityStatus struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	Status            string `json:"status"`
	AvailableReplicas int32  `json:"availableReplicas"`
}

// AzurePodIdentityExceptionSpec matches pods with the selector defined.
// If request originates from a pod that matches the selector, nmi will
// proxy the request and send response back without any validation.
type AzurePodIdentityExceptionSpec struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	PodLabels         map[string]string `json:"podLabels"`
}

// AzurePodIdentityExceptionStatus contains the status of an AzurePodIdentityException.
type AzurePodIdentityExceptionStatus struct {
	metav1.ObjectMeta `json:"metadata,omitempty"`
	Status            string `json:"status"`
}
