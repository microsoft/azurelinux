// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validSELinuxOptions = []SELinux{
		SELinux("permissive"),
		SELinux("enforcing"),
		SELinux("force_enforcing"),
		SELinux(""),
	}
	invalidSELinux     = SELinux("bad_selinux")
	validSELinuxJSON   = `"permissive"`
	invalidSELinuxJSON = `1234`
)

func TestShouldSucceedValidSELinuxMatch_SELinux(t *testing.T) {
	var s SELinux
	assert.Equal(t, len(validSELinuxOptions), len(s.GetValidSELinux()))

	for _, selinux := range validSELinuxOptions {
		found := false
		for _, validSelinux := range s.GetValidSELinux() {
			if selinux == validSelinux {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidSELinux_SELinux(t *testing.T) {
	for _, validSelinux := range validSELinuxOptions {
		var checkedSELinux SELinux

		assert.NoError(t, validSelinux.IsValid())
		err := remarshalJSON(validSelinux, &checkedSELinux)
		assert.NoError(t, err)
		assert.Equal(t, validSelinux, checkedSELinux)
	}
}

func TestShouldFailParsingInvalidSELinux_SELinux(t *testing.T) {
	var checkedSELinux SELinux

	err := invalidSELinux.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for SELinux (bad_selinux)", err.Error())

	err = remarshalJSON(invalidSELinux, &checkedSELinux)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SELinux]: invalid value for SELinux (bad_selinux)", err.Error())
}

func TestShouldSucceedParsingValidJSON_SELinux(t *testing.T) {
	var checkedSELinux SELinux

	err := marshalJSONString(validSELinuxJSON, &checkedSELinux)
	assert.NoError(t, err)
	assert.Equal(t, validSELinuxOptions[0], checkedSELinux)
}

func TestShouldFailParsingInvalidJSON_SELinux(t *testing.T) {
	var checkedSELinux SELinux

	err := marshalJSONString(invalidSELinuxJSON, &checkedSELinux)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SELinux]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeSELinux", err.Error())
}
