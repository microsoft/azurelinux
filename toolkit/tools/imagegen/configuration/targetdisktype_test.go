// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validTargetDiskTypes = []TargetDiskType{
		TargetDiskType("path"),
		TargetDiskType(""),
	}
	invalidTargetDiskType     = TargetDiskType("not_a_disk_type")
	validTargetDiskTypeJSON   = `"path"`
	invalidTargetDiskTypeJSON = `1234`
)

func TestShouldSucceedValidTargetDiskTypesMatch_TargetDiskType(t *testing.T) {
	var vdt TargetDiskType
	assert.Equal(t, len(validTargetDiskTypes), len(vdt.GetValidTargetDiskTypes()))

	for _, TargetDiskType := range validTargetDiskTypes {
		found := false
		for _, validTargetDiskType := range vdt.GetValidTargetDiskTypes() {
			if TargetDiskType == validTargetDiskType {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidPolicies_TargetDiskType(t *testing.T) {
	for _, validPolicy := range validTargetDiskTypes {
		var checkedPolicy TargetDiskType

		assert.NoError(t, validPolicy.IsValid())
		err := remarshalJSON(validPolicy, &checkedPolicy)
		assert.NoError(t, err)
		assert.Equal(t, validPolicy, checkedPolicy)
	}
}

func TestShouldFailParsingInvalidPolicy_TargetDiskType(t *testing.T) {
	var checkedPolicy TargetDiskType

	err := invalidTargetDiskType.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for TargetDiskType (not_a_disk_type)", err.Error())

	err = remarshalJSON(invalidTargetDiskType, &checkedPolicy)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: invalid value for TargetDiskType (not_a_disk_type)", err.Error())
}

func TestShouldSucceedParsingValidJSON_TargetDiskType(t *testing.T) {
	var checkedPolicy TargetDiskType

	err := marshalJSONString(validTargetDiskTypeJSON, &checkedPolicy)
	assert.NoError(t, err)
	assert.Equal(t, validTargetDiskTypes[0], checkedPolicy)
}

func TestShouldFailParsingInvalidJSON_TargetDiskType(t *testing.T) {
	var checkedPolicy TargetDiskType

	err := marshalJSONString(invalidTargetDiskTypeJSON, &checkedPolicy)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeTargetDiskType", err.Error())
}
