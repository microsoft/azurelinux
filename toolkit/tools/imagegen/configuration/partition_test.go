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

func TestShouldPassEmptyName_Partition(t *testing.T) {
	var checkedPartition Partition
	emptyNamePartition := validPartition

	emptyNamePartition.Name = ""

	err := remarshalJSON(emptyNamePartition, &checkedPartition)
	assert.NoError(t, err)
}

func TestShouldPassMaxLengthName_Partition(t *testing.T) {
	var checkedPartition Partition
	maxNamePartition := validPartition

	maxNamePartition.Name = "abcdefghijklmnopqrstuvwxyz012345678"

	err := remarshalJSON(maxNamePartition, &checkedPartition)
	assert.NoError(t, err)
}

func TestShouldFailLongNormalName_Partition(t *testing.T) {
	var checkedPartition Partition
	longNamePartition := validPartition

	longNamePartition.Name = "abcdefghijklmnopqrstuvwxyz0123456789"

	err := longNamePartition.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "[Name] is too long, GPT header can hold only 72 bytes of UTF-16 (35 normal characters + null) while (abcdefghijklmnopqrstuvwxyz0123456789) needs 74 bytes", err.Error())

	err = remarshalJSON(longNamePartition, &checkedPartition)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Partition]: [Name] is too long, GPT header can hold only 72 bytes of UTF-16 (35 normal characters + null) while (abcdefghijklmnopqrstuvwxyz0123456789) needs 74 bytes", err.Error())
}

func TestShouldPassShortSymbolName_Partition(t *testing.T) {
	var checkedPartition Partition
	shortSymbolNamePartition := validPartition
	shortSymbolNamePartition.Name = "1👌2🤣3🤢ab~52*^&%$6"

	err := remarshalJSON(shortSymbolNamePartition, &checkedPartition)
	assert.NoError(t, err)
}

func TestShouldFailLongSymbolName_Partition(t *testing.T) {
	var checkedPartition Partition
	longSymbolNamePartition := validPartition

	longSymbolNamePartition.Name = "1🤷‍♂️2@3( •_•)>⌐■~■ab~52(⌐■_■)67👩‍💻"

	err := longSymbolNamePartition.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "[Name] is too long, GPT header can hold only 72 bytes of UTF-16 (35 normal characters + null) while (1🤷\u200d♂️2@3( •_•)>⌐■~■ab~52(⌐■_■)67👩\u200d💻) needs 78 bytes", err.Error())

	err = remarshalJSON(longSymbolNamePartition, &checkedPartition)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Partition]: [Name] is too long, GPT header can hold only 72 bytes of UTF-16 (35 normal characters + null) while (1🤷\u200d♂️2@3( •_•)>⌐■~■ab~52(⌐■_■)67👩\u200d💻) needs 78 bytes", err.Error())
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
