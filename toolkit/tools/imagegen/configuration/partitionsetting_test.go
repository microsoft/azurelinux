// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validPartitionSetting PartitionSetting = PartitionSetting{
		ID:              "testing",
		MountPoint:      "/",
		MountIdentifier: GetDefaultMountIdentifier(),
	}
	invalidvalidPartitionSettingJSON = `{"RemoveDocs": 1234}`
)

func TestShouldSucceedParsingDefaultPartitionSetting_PartitionSetting(t *testing.T) {
	var (
		checkedPartitionSetting PartitionSetting
		defaultPartitionSetting PartitionSetting = PartitionSetting{
			MountIdentifier: GetDefaultMountIdentifier(),
		}
	)
	err := marshalJSONString("{}", &checkedPartitionSetting)
	assert.NoError(t, err)
	assert.Equal(t, defaultPartitionSetting, checkedPartitionSetting)

	// Check the non-standard default values are correct
	assert.Equal(t, "partuuid", checkedPartitionSetting.MountIdentifier.String())
}

func TestShouldSucceedParsingValidPartitionSetting_PartitionSetting(t *testing.T) {
	var checkedPartitionSetting PartitionSetting
	err := remarshalJSON(validPartitionSetting, &checkedPartitionSetting)
	assert.NoError(t, err)
	assert.Equal(t, validPartitionSetting, checkedPartitionSetting)
}

func TestShouldFailParsingInvalidJSON_PartitionSetting(t *testing.T) {
	var checkedPartitionSetting PartitionSetting

	err := marshalJSONString(invalidvalidPartitionSettingJSON, &checkedPartitionSetting)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PartitionSetting]: json: cannot unmarshal number into Go struct field IntermediateTypePartitionSetting.RemoveDocs of type bool", err.Error())
}
