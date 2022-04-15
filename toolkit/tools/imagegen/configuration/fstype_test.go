// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validFsTypeOptions = []FsType{
		FsType("fat32"),
		FsType("fat16"),
		FsType("vfat"),
		FsType("ext2"),
		FsType("ext3"),
		FsType("ext4"),
		FsType("linux-swap"),
	}
	invalidFsType    = FsType("bad_FsType")
	validFsTypeJSON   = `"fat32"`
	invalidFsTypeJSON = `1234`
)

func TestShouldSucceedValidFstypeMatch_FsType (t *testing.T) {
	var f FsType
	assert.Equal(t, len(validFsTypeOptions), len(f.GetValidFsType()))

	for _, fstype := range validFsTypeOptions {
		found := false
		for _, validFsType := range f.GetValidFsType() {
			if fstype == validFsType {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidFsType_FsType(t *testing.T) {
	for _, validFsType := range validFsTypeOptions {
		var checkedFsType FsType

		assert.NoError(t, validFsType.IsValid())
		err := remarshalJSON(validFsType, &checkedFsType)
		assert.NoError(t, err)
		assert.Equal(t, validFsType, checkedFsType)
	}
}

func TestShouldFailParsingInvalidFsType_FsType(t *testing.T) {
	var checkedFsType FsType

	err := invalidFsType.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for FsType (bad_FsType)", err.Error())

	err = remarshalJSON(invalidFsType, &checkedFsType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [FsType]: invalid value for FsType (bad_FsType)", err.Error())
}

func TestShouldSucceedParsingValidJSON_FsType(t *testing.T) {
	var checkedFsType FsType

	err := marshalJSONString(validFsTypeJSON, &checkedFsType)
	assert.NoError(t, err)
	assert.Equal(t, validFsTypeOptions[0], checkedFsType)
}

func TestShouldFailParsingInvalidJSON_FsType(t *testing.T) {
	var checkedFsType FsType

	err := marshalJSONString(invalidFsTypeJSON, &checkedFsType)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [FsType]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeFsType", err.Error())
}
