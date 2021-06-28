package utils

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

// RedactClientID redacts client id
func RedactClientID(clientID string) string {
	return redact(clientID, "$1##### REDACTED #####$3")
}

func redact(src, repl string) string {
	r, _ := regexp.Compile(`^(\S{4})(\S|\s)*(\S{4})$`)
	return r.ReplaceAllString(src, repl)
}

// ValidateResourceID validates the resourceID is is of the format
// `/subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>`
func ValidateResourceID(resourceID string) error {
	isValid := regexp.MustCompile(`(?i)/subscriptions/(.+?)/resourcegroups/(.+?)/providers/Microsoft.ManagedIdentity/userAssignedIdentities/(.+)`).MatchString
	if !isValid(resourceID) {
		return fmt.Errorf("invalid resource id: %q, must match /subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>", resourceID)
	}
	return nil
}

func IsKubenetCNI(kubeletConfig string) (bool, error) {
	var isKubenet bool
	// read the kubelet config
	bytes, err := ioutil.ReadFile(kubeletConfig)
	if err != nil {
		return isKubenet, err
	}
	return strings.Contains(string(bytes), "--network-plugin=kubenet"), nil
}
