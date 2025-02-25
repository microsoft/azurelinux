// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validRaidConfig       RaidConfig = RaidConfig{RaidID: "MyRaidID", ComponentPartIDs: []string{"MyPartID1", "MyPartID2"}}
	validRaidConfigJSON              = `{"RaidID": "MyRaidID", "ComponentPartIDs": ["MyPartID1", "MyPartID2"]}`
	invalidRaidConfigJSON            = `{"RaidID": 0}`
)

func TestShouldSucceedParsingDefaultRaidConfig_RaidConfig(t *testing.T) {
	var checkedRaidConfig RaidConfig
	err := marshalJSONString("{}", &checkedRaidConfig)
	assert.NoError(t, err)
	assert.Equal(t, RaidConfig{}, checkedRaidConfig)
}

func TestShouldSucceedParsingValidRaidConfig_RaidConfig(t *testing.T) {
	var checkedRaidConfig RaidConfig
	err := remarshalJSON(validRaidConfig, &checkedRaidConfig)
	assert.NoError(t, err)
	assert.Equal(t, validRaidConfig, checkedRaidConfig)
}

func TestShouldSucceedParsingValidJSON_RaidConfig(t *testing.T) {
	var checkedRaidConfig RaidConfig

	err := marshalJSONString(validRaidConfigJSON, &checkedRaidConfig)
	assert.NoError(t, err)
	assert.Equal(t, validRaidConfig, checkedRaidConfig)
}

func TestShouldFailParsingInvalidJSON_RaidConfig(t *testing.T) {
	var checkedRaidConfig RaidConfig

	err := marshalJSONString(invalidRaidConfigJSON, &checkedRaidConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [RaidConfig]: json: cannot unmarshal number into Go struct field IntermediateTypeRaidConfig.RaidID of type string", err.Error())
}

func TestShouldFailInvalidLevel_RaidConfig(t *testing.T) {
	var checkedRaidConfig RaidConfig
	invalidRaidConfig := validRaidConfig

	invalidRaidConfig.Level = -1

	err := invalidRaidConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [RaidConfig]: Level must be one of 0, 1, 4, 5, 6, 10", err.Error())

	err = remarshalJSON(invalidRaidConfig, &checkedRaidConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [RaidConfig]: invalid [RaidConfig]: Level must be one of 0, 1, 4, 5, 6, 10", err.Error())
}
