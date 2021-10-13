// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validMountIdentifiers = []MountIdentifier{
		MountIdentifier("uuid"),
		MountIdentifier("partuuid"),
		MountIdentifier("partlabel"),
		MountIdentifier(""),
	}
	invalidMountIdentifier     = MountIdentifier("not_a_behavior")
	validMountIdentifierJSON   = `"uuid"`
	invalidMountIdentifierJSON = `1234`
)

func TestShouldSucceedValidMountIdentifiersMatch_MountIdentifier(t *testing.T) {
	var identifier MountIdentifier
	assert.Equal(t, len(validMountIdentifiers), len(identifier.GetValidMountIdentifiers()))

	for _, mountIdentifier := range validMountIdentifiers {
		found := false
		for _, validMountIdentifier := range identifier.GetValidMountIdentifiers() {
			if mountIdentifier == validMountIdentifier {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidIdentifiers_MountIdentifier(t *testing.T) {
	for _, validIdentifier := range validMountIdentifiers {
		var checkedIdentifier MountIdentifier

		assert.NoError(t, validIdentifier.IsValid())
		err := remarshalJSON(validIdentifier, &checkedIdentifier)
		assert.NoError(t, err)
		assert.Equal(t, validIdentifier, checkedIdentifier)
	}
}

func TestShouldFailParsingInvalidMountIdentifier_MountIdentifier(t *testing.T) {
	var checkedIdentifier MountIdentifier

	err := invalidMountIdentifier.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Mount Identifier (not_a_behavior)", err.Error())

	err = remarshalJSON(invalidMountIdentifier, &checkedIdentifier)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [MountIdentifier]: invalid value for Mount Identifier (not_a_behavior)", err.Error())
}

func TestShouldSucceedParsingValidJSON_MountIdentifier(t *testing.T) {
	var checkedIdentifier MountIdentifier

	err := marshalJSONString(validMountIdentifierJSON, &checkedIdentifier)
	assert.NoError(t, err)
	assert.Equal(t, validMountIdentifiers[0], checkedIdentifier)
}

func TestShouldFailParsingInvalidJSON_MountIdentifier(t *testing.T) {
	var checkedIdentifier MountIdentifier

	err := marshalJSONString(invalidMountIdentifierJSON, &checkedIdentifier)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [MountIdentifier]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeMountIdentifier", err.Error())
}
