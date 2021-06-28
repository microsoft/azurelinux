package cloudprovider

import (
	"testing"

	"github.com/Azure/azure-sdk-for-go/services/compute/mgmt/2019-12-01/compute"
)

func TestGetUpdatedResourceIdentityType(t *testing.T) {
	cases := []struct {
		current  compute.ResourceIdentityType
		expected compute.ResourceIdentityType
	}{
		{
			current:  "",
			expected: compute.ResourceIdentityTypeUserAssigned,
		},
		{
			current:  compute.ResourceIdentityTypeNone,
			expected: compute.ResourceIdentityTypeUserAssigned,
		},
		{
			current:  compute.ResourceIdentityTypeUserAssigned,
			expected: compute.ResourceIdentityTypeUserAssigned,
		},
		{
			current:  compute.ResourceIdentityTypeSystemAssigned,
			expected: compute.ResourceIdentityTypeSystemAssignedUserAssigned,
		},
		{
			current:  compute.ResourceIdentityTypeSystemAssignedUserAssigned,
			expected: compute.ResourceIdentityTypeSystemAssignedUserAssigned,
		},
	}

	for _, tc := range cases {
		actual := getUpdatedResourceIdentityType(tc.current)
		if tc.expected != actual {
			t.Fatalf("expected: %v, got: %v", tc.expected, actual)
		}
	}
}
