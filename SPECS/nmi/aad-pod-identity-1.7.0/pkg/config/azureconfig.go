package config

// AzureConfig is representing /etc/kubernetes/azure.json
type AzureConfig struct {
	Cloud                       string `json:"cloud" yaml:"cloud"`
	TenantID                    string `json:"tenantId" yaml:"tenantId"`
	ClientID                    string `json:"aadClientId" yaml:"aadClientId"`
	ClientSecret                string `json:"aadClientSecret" yaml:"aadClientSecret"`
	SubscriptionID              string `json:"subscriptionId" yaml:"subscriptionId"`
	ResourceGroupName           string `json:"resourceGroup" yaml:"resourceGroup"`
	SecurityGroupName           string `json:"securityGroupName" yaml:"securityGroupName"`
	VMType                      string `json:"vmType" yaml:"vmType"`
	UseManagedIdentityExtension bool   `json:"useManagedIdentityExtension,omitempty" yaml:"useManagedIdentityExtension,omitempty"`
	UserAssignedIdentityID      string `json:"userAssignedIdentityID,omitempty" yaml:"userAssignedIdentityID,omitempty"`
}
