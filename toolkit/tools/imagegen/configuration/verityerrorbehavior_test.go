// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validVerityErrorBehaviors = []VerityErrorBehavior{
		VerityErrorBehavior("ignore"),
		VerityErrorBehavior("restart"),
		VerityErrorBehavior("panic"),
		VerityErrorBehavior(""),
	}
	invalidVerityErrorBehavior     = VerityErrorBehavior("not_a_behavior")
	validVerityErrorBehaviorJSON   = `"ignore"`
	invalidVerityErrorBehaviorJSON = `1234`
)

func TestShouldSucceedValidImaPoliciesMatch_VerityErrorBehavior(t *testing.T) {
	var behavior VerityErrorBehavior
	assert.Equal(t, len(validVerityErrorBehaviors), len(behavior.GetValidVerityErrorBehaviors()))

	for _, errorBehavior := range validVerityErrorBehaviors {
		found := false
		for _, validErrorBehavior := range behavior.GetValidVerityErrorBehaviors() {
			if errorBehavior == validErrorBehavior {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidPolicies_VerityErrorBehavior(t *testing.T) {
	for _, validErrorBehavior := range validVerityErrorBehaviors {
		var checkedBehavior VerityErrorBehavior

		assert.NoError(t, validErrorBehavior.IsValid())
		err := remarshalJSON(validErrorBehavior, &checkedBehavior)
		assert.NoError(t, err)
		assert.Equal(t, validErrorBehavior, checkedBehavior)
	}
}

func TestShouldFailParsingInvalidErrorBehavoir_VerityErrorBehavior(t *testing.T) {
	var checkedBehavior VerityErrorBehavior

	err := invalidVerityErrorBehavior.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for VerityErrorBehavior (not_a_behavior)", err.Error())

	err = remarshalJSON(invalidVerityErrorBehavior, &checkedBehavior)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [VerityErrorBehavior]: invalid value for VerityErrorBehavior (not_a_behavior)", err.Error())
}

func TestShouldSucceedParsingValidJSON_VerityErrorBehavior(t *testing.T) {
	var checkedBehavior VerityErrorBehavior

	err := marshalJSONString(validVerityErrorBehaviorJSON, &checkedBehavior)
	assert.NoError(t, err)
	assert.Equal(t, validVerityErrorBehaviors[0], checkedBehavior)
}

func TestShouldFailParsingInvalidJSON_VerityErrorBehavior(t *testing.T) {
	var checkedBehavior VerityErrorBehavior

	err := marshalJSONString(invalidVerityErrorBehaviorJSON, &checkedBehavior)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [VerityErrorBehavior]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeVerityErrorBehavior", err.Error())
}
