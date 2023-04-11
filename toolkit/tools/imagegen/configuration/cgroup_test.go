// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validCGroupOptions = []CGroup{
		CGroup("version_one"),
		CGroup("version_two"),
		CGroup(""),
	}
	invalidCGroup     = CGroup("bad_cgroup")
	validCGroupJSON   = `"version_two"`
	invalidCGroupJSON = `1234`
)

func TestShouldSucceedValidCGroupMatch_CGroup(t *testing.T) {
	var c CGroup
	assert.Equal(t, len(validCGroupOptions), len(c.GetValidCGroup()))

	for _, cgroup := range validCGroupOptions {
		found := false
		for _, validCGroup := range c.GetValidCGroup() {
			if cgroup == validCGroup {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidCGroup_CGroup(t *testing.T) {
	for _, validCGroup := range validCGroupOptions {
		var checkedCGroup CGroup

		assert.NoError(t, validCGroup.IsValid())
		err := remarshalJSON(validCGroup, &checkedCGroup)
		assert.NoError(t, err)
		assert.Equal(t, validCGroup, checkedCGroup)
	}
}

func TestShouldFailParsingInvalidCGroup_CGroup(t *testing.T) {
	var checkedCGroup CGroup

	err := invalidCGroup.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for CGroup (bad_cgroup)", err.Error())

	err = remarshalJSON(invalidCGroup, &checkedCGroup)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [CGroup]: invalid value for CGroup (bad_cgroup)", err.Error())
}

func TestShouldSucceedParsingValidJSON_CGroup(t *testing.T) {
	var checkedCGroup CGroup

	err := marshalJSONString(validCGroupJSON, &checkedCGroup)
	assert.NoError(t, err)
	assert.Equal(t, validCGroupOptions[1], checkedCGroup)
}

func TestShouldFailParsingInvalidJSON_CGroup(t *testing.T) {
	var checkedCGroup CGroup

	err := marshalJSONString(invalidCGroupJSON, &checkedCGroup)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [CGroup]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeCGroup", err.Error())
}
