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
	for _, validTargetDiskType := range validTargetDiskTypes {
		var checkedTargetDiskType TargetDiskType

		assert.NoError(t, validTargetDiskType.IsValid())
		err := remarshalJSON(validTargetDiskType, &checkedTargetDiskType)
		assert.NoError(t, err)
		assert.Equal(t, validTargetDiskType, checkedTargetDiskType)
	}
}

func TestShouldFailParsingInvalidTargetDiskType_TargetDiskType(t *testing.T) {
	var checkedTargetDiskType TargetDiskType

	err := invalidTargetDiskType.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for TargetDiskType (not_a_disk_type)", err.Error())

	err = remarshalJSON(invalidTargetDiskType, &checkedTargetDiskType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: invalid value for TargetDiskType (not_a_disk_type)", err.Error())
}

func TestShouldSucceedParsingValidJSON_TargetDiskType(t *testing.T) {
	var checkedTargetDiskType TargetDiskType

	err := marshalJSONString(validTargetDiskTypeJSON, &checkedTargetDiskType)
	assert.NoError(t, err)
	assert.Equal(t, validTargetDiskTypes[0], checkedTargetDiskType)
}

func TestShouldFailParsingInvalidJSON_TargetDiskType(t *testing.T) {
	var checkedTargetDiskType TargetDiskType

	err := marshalJSONString(invalidTargetDiskTypeJSON, &checkedTargetDiskType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeTargetDiskType", err.Error())
}
