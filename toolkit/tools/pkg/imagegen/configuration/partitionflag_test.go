// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validPartitionFlags = []PartitionFlag{
		PartitionFlag("esp"),
		PartitionFlag("grub"),
		PartitionFlag("bios_grub"),
		PartitionFlag("bios-grub"),
		PartitionFlag("boot"),
		PartitionFlag("dmroot"),
	}
	invalidPartitionFlag     = PartitionFlag("not_a_partition_flag")
	validPartitionFlagJSON   = `"esp"`
	invalidPartitionFlagJSON = `1234`
)

func TestShouldSucceedValidFlagsMatch_PartitionFlag(t *testing.T) {
	var pf PartitionFlag
	assert.Equal(t, len(validPartitionFlags), len(pf.GetValidPartitionFlags()))

	for _, partitionFlag := range validPartitionFlags {
		found := false
		for _, validPartitionType := range pf.GetValidPartitionFlags() {
			if partitionFlag == validPartitionType {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidPartitionFlag_PartitionFlag(t *testing.T) {
	for _, validPartitionFlag := range validPartitionFlags {
		var checkedPartitionFlag PartitionFlag

		assert.NoError(t, validPartitionFlag.IsValid())
		err := remarshalJSON(validPartitionFlag, &checkedPartitionFlag)
		assert.NoError(t, err)
		assert.Equal(t, validPartitionFlag, checkedPartitionFlag)
	}
}

func TestShouldFailParsingInvalidPartitionFlag_PartitionFlag(t *testing.T) {
	var checkedPartitionFlag PartitionFlag

	err := invalidPartitionFlag.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Flag (not_a_partition_flag)", err.Error())

	err = remarshalJSON(invalidPartitionFlag, &checkedPartitionFlag)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Flag]: invalid value for Flag (not_a_partition_flag)", err.Error())
}

func TestShouldSucceedParsingValidJSON_PartitionFlag(t *testing.T) {
	var checkedPartitionFlag PartitionFlag

	err := marshalJSONString(validPartitionFlagJSON, &checkedPartitionFlag)
	assert.NoError(t, err)
	assert.Equal(t, validPartitionFlags[0], checkedPartitionFlag)
}

func TestShouldFailParsingInvalidJSON_PartitionFlag(t *testing.T) {
	var checkedPartitionFlag PartitionFlag

	err := marshalJSONString(invalidPartitionFlagJSON, &checkedPartitionFlag)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Flag]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypePartitionFlag", err.Error())
}
