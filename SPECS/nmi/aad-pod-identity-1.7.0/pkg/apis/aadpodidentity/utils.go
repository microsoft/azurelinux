package aadpodidentity

// IsNamespacedIdentity returns true if azureID is a namespaced identity.
func IsNamespacedIdentity(azureID *AzureIdentity) bool {
	if val, ok := azureID.Annotations[BehaviorKey]; ok {
		if val == BehaviorNamespaced {
			return true
		}
	}
	return false
}
