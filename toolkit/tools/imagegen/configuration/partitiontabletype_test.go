// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validPartitionTableTypes = []PartitionTableType{
		PartitionTableType("gpt"),
		PartitionTableType("mbr"),
		PartitionTableType(""),
	}
	invalidPartitionTableType                 = PartitionTableType("not_a_partition_type")
	validPartitionTableTypeJSON               = `"gpt"`
	invalidPartitionTableTypeJSON             = `1234`
	validPartitionTableTypesToPartedArguments = map[PartitionTableType]string{
		PartitionTableType("gpt"): "gpt",
		PartitionTableType("mbr"): "msdos",
		PartitionTableType(""):    "",
	}
)

func TestShouldSucceedValidPartitionsMatch_PartitionTableType(t *testing.T) {
	var ptt PartitionTableType
	assert.Equal(t, len(validPartitionTableTypes), len(ptt.GetValidPartitionTableTypes()))

	for _, partitionType := range validPartitionTableTypes {
		found := false
		for _, validPartitionType := range ptt.GetValidPartitionTableTypes() {
			if partitionType == validPartitionType {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidPartitionTableType_PartitionTableType(t *testing.T) {
	for _, validPartitionType := range validPartitionTableTypes {
		var checkedPartitionType PartitionTableType

		assert.NoError(t, validPartitionType.IsValid())
		err := remarshalJSON(validPartitionType, &checkedPartitionType)
		assert.NoError(t, err)
		assert.Equal(t, validPartitionType, checkedPartitionType)
	}
}

func TestShouldFailParsingInvalidPartitionTableType_PartitionTableType(t *testing.T) {
	var checkedPartitionType PartitionTableType

	err := invalidPartitionTableType.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PartitionTableType (not_a_partition_type)", err.Error())

	err = remarshalJSON(invalidPartitionTableType, &checkedPartitionType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PartitionTableType]: invalid value for PartitionTableType (not_a_partition_type)", err.Error())
}

func TestShouldSucceedParsingValidJSON_PartitionTableType(t *testing.T) {
	var checkedPartitionType PartitionTableType

	err := marshalJSONString(validPartitionTableTypeJSON, &checkedPartitionType)
	assert.NoError(t, err)
	assert.Equal(t, validPartitionTableTypes[0], checkedPartitionType)
}

func TestShouldFailParsingInvalidJSON_PartitionTableType(t *testing.T) {
	var checkedPartitionType PartitionTableType

	err := marshalJSONString(invalidPartitionTableTypeJSON, &checkedPartitionType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PartitionTableType]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypePartitionTableType", err.Error())
}

func TestShouldSucceedConvertToPartedArgument_PartitionTableType(t *testing.T) {
	var ptt PartitionTableType
	assert.Equal(t, len(validPartitionTableTypes), len(ptt.GetValidPartitionTableTypes()))

	for _, partitionType := range validPartitionTableTypes {
		partedArgument, err := partitionType.ConvertToPartedArgument()
		assert.NoError(t, err)
		assert.Equal(t, partedArgument, validPartitionTableTypesToPartedArguments[partitionType])
	}
}

func TestShouldFailConvertToPartedArgument_PartitionTableType(t *testing.T) {
	_, err := invalidPartitionTableType.ConvertToPartedArgument()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PartitionTableType (not_a_partition_type)", err.Error())
}
