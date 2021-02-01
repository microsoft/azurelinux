// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validPartition Partition = Partition{
		FsType: "ext4",
		ID:     "MyPartID",
		Name:   "MyPartitionName",
		End:    0,
		Start:  100,
		Flags:  []PartitionFlag{PartitionFlagDeviceMapperRoot},
	}
	invalidvalidPartitionJSON = `{"End": "abc"}`
)

func TestShouldSucceedParsingDefaultPartition_Partition(t *testing.T) {
	var checkedPartition Partition
	err := marshalJSONString("{}", &checkedPartition)
	assert.NoError(t, err)
	assert.Equal(t, Partition{}, checkedPartition)
}

func TestShouldSucceedParsingValidPartition_Partition(t *testing.T) {
	var checkedPartition Partition
	err := remarshalJSON(validPartition, &checkedPartition)
	assert.NoError(t, err)
	assert.Equal(t, validPartition, checkedPartition)
}

func TestShouldSucceedFindingFlag_Partition(t *testing.T) {
	assert.True(t, validPartition.HasFlag(PartitionFlagDeviceMapperRoot))
}

func TestShouldFailFindingBadFlag_Partition(t *testing.T) {
	assert.False(t, validPartition.HasFlag(PartitionFlagBoot))
	assert.False(t, validPartition.HasFlag("notaflag"))
}

func TestShouldFailParsingInvalidFlag_Partition(t *testing.T) {
	var checkedPartition Partition
	invalidPartition := validPartition

	invalidPartition.Flags = []PartitionFlag{"not_a_flag"}

	err := invalidPartition.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Flag (not_a_flag)", err.Error())

	err = remarshalJSON(invalidPartition, &checkedPartition)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Partition]: failed to parse [Flag]: invalid value for Flag (not_a_flag)", err.Error())
}

func TestShouldFailParsingInvalidJSON_Partition(t *testing.T) {
	var checkedPartition Partition

	err := marshalJSONString(invalidvalidPartitionJSON, &checkedPartition)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Partition]: json: cannot unmarshal string into Go struct field IntermediateTypePartition.End of type uint64", err.Error())
}
