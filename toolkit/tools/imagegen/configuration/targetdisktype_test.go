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
		var checkedTargetDiskTyp TargetDiskType

		assert.NoError(t, validTargetDiskType.IsValid())
		err := remarshalJSON(validTargetDiskType, &checkedTargetDiskTyp)
		assert.NoError(t, err)
		assert.Equal(t, validTargetDiskType, checkedTargetDiskTyp)
	}
}

func TestShouldFailParsingInvalidTargetDiskType_TargetDiskType(t *testing.T) {
	var checkedTargetDiskTyp TargetDiskType

	err := invalidTargetDiskType.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for TargetDiskType (not_a_disk_type)", err.Error())

	err = remarshalJSON(invalidTargetDiskType, &checkedTargetDiskTyp)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: invalid value for TargetDiskType (not_a_disk_type)", err.Error())
}

func TestShouldSucceedParsingValidJSON_TargetDiskType(t *testing.T) {
	var checkedTargetDiskTyp TargetDiskType

	err := marshalJSONString(validTargetDiskTypeJSON, &checkedTargetDiskTyp)
	assert.NoError(t, err)
	assert.Equal(t, validTargetDiskTypes[0], checkedTargetDiskTyp)
}

func TestShouldFailParsingInvalidJSON_TargetDiskType(t *testing.T) {
	var checkedTargetDiskTyp TargetDiskType

	err := marshalJSONString(invalidTargetDiskTypeJSON, &checkedTargetDiskTyp)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [TargetDiskType]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeTargetDiskType", err.Error())
}
