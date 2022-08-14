// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validImaPolicies = []ImaPolicy{
		ImaPolicy("tcb"),
		ImaPolicy("appraise_tcb"),
		ImaPolicy("secure_boot"),
		ImaPolicy(""),
	}
	invalidImaPolicy = ImaPolicy("not_a_policy")
	validImaJSON     = `"tcb"`
	invalidImaJSON   = `1234`
)

func TestShouldSucceedValidImaPoliciesMatch_ImaPolicy(t *testing.T) {
	var ima ImaPolicy
	assert.Equal(t, len(validImaPolicies), len(ima.GetValidImaPolicies()))

	for _, imaPolicy := range validImaPolicies {
		found := false
		for _, validImaPolicy := range ima.GetValidImaPolicies() {
			if imaPolicy == validImaPolicy {
				found = true
			}
		}
		assert.True(t, found)
	}
}

func TestShouldSucceedParsingValidPolicies_ImaPolicy(t *testing.T) {
	for _, validPolicy := range validImaPolicies {
		var checkedPolicy ImaPolicy

		assert.NoError(t, validPolicy.IsValid())
		err := remarshalJSON(validPolicy, &checkedPolicy)
		assert.NoError(t, err)
		assert.Equal(t, validPolicy, checkedPolicy)
	}
}

func TestShouldFailParsingInvalidPolicy_ImaPolicy(t *testing.T) {
	var checkedPolicy ImaPolicy

	err := invalidImaPolicy.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for ImaPolicy (not_a_policy)", err.Error())

	err = remarshalJSON(invalidImaPolicy, &checkedPolicy)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ImaPolicy]: invalid value for ImaPolicy (not_a_policy)", err.Error())
}

func TestShouldSucceedParsingValidJSON_ImaPolicy(t *testing.T) {
	var checkedPolicy ImaPolicy

	err := marshalJSONString(validImaJSON, &checkedPolicy)
	assert.NoError(t, err)
	assert.Equal(t, validImaPolicies[0], checkedPolicy)
}

func TestShouldFailParsingInvalidJSON_ImaPolicy(t *testing.T) {
	var checkedPolicy ImaPolicy

	err := marshalJSONString(invalidImaJSON, &checkedPolicy)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ImaPolicy]: json: cannot unmarshal number into Go value of type configuration.IntermediateTypeImaPolicy", err.Error())
}
