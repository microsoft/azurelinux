// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validReadOnlyVerityRoot ReadOnlyVerityRoot = ReadOnlyVerityRoot{
		Enable:                       true,
		Name:                         "test",
		ErrorCorrectionEnable:        true,
		ErrorCorrectionEncodingRoots: 5,
		VerityErrorBehavior:          "restart",
	}
	validReadOnlyVerityRootWithOverlays = ReadOnlyVerityRoot{
		Enable:           true,
		Name:             "test",
		TmpfsOverlays:    []string{"a/folder", "a/different_folder"},
		TmpfsOverlaySize: "20%",
	}
	invalidReadOnlyVerityRootJSON     = `{"Enable": 1234}`
	invalidReadONlyVerityBehaviorJSON = `{"VerityErrorBehavior": "not_a_behavior"}`
)

func TestShouldSucceedParsingDefaultReadOnlyVerityRoot_ReadOnlyVerityRoot(t *testing.T) {
	var (
		checkedReadOnlyVerityRoot ReadOnlyVerityRoot
		defaultReadOnlyVerityRoot ReadOnlyVerityRoot = ReadOnlyVerityRoot{
			Name:                         "verity_root_fs",
			ErrorCorrectionEncodingRoots: 2,
			ErrorCorrectionEnable:        true,
			VerityErrorBehavior:          VerityErrorBehaviorDefault,
			TmpfsOverlaySize:             "20%",
		}
	)
	err := marshalJSONString("{}", &checkedReadOnlyVerityRoot)
	assert.NoError(t, err)

	// We set non-standard default values
	assert.Equal(t, defaultReadOnlyVerityRoot, checkedReadOnlyVerityRoot)

	assert.Equal(t, false, checkedReadOnlyVerityRoot.Enable)
	assert.Equal(t, true, checkedReadOnlyVerityRoot.ErrorCorrectionEnable)
	assert.Equal(t, 2, checkedReadOnlyVerityRoot.ErrorCorrectionEncodingRoots)
	assert.Equal(t, false, checkedReadOnlyVerityRoot.RootHashSignatureEnable)
	assert.Equal(t, 0, len(checkedReadOnlyVerityRoot.TmpfsOverlays))
}

func TestShouldSucceedParsingValidReadOnlyVerityRoot_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	err := remarshalJSON(validReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.NoError(t, err)
	assert.Equal(t, validReadOnlyVerityRoot, checkedReadOnlyVerityRoot)
}

func TestShouldSucceedParsingValidReadOnlyVerityRootWithOverlays_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	err := remarshalJSON(validReadOnlyVerityRootWithOverlays, &checkedReadOnlyVerityRoot)
	assert.NoError(t, err)
	assert.Equal(t, validReadOnlyVerityRootWithOverlays, checkedReadOnlyVerityRoot)
}

func TestShouldFailParsingEmptyName_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidReadOnlyVerityRoot := validReadOnlyVerityRoot

	invalidReadOnlyVerityRoot.Name = ""

	err := invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "[Name] must not be blank", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: [Name] must not be blank", err.Error())

}

func TestShouldFailUnreasonableErrorCorrectionEncodingN_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidReadOnlyVerityRoot := validReadOnlyVerityRoot

	// Test too large
	invalidReadOnlyVerityRoot.ErrorCorrectionEncodingRoots = 25

	err := invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "verity FEC [ErrorCorrectionEncodingRoots] out of bounds ( (2) <= N <= (24)), currently (25)", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: verity FEC [ErrorCorrectionEncodingRoots] out of bounds ( (2) <= N <= (24)), currently (25)", err.Error())

	// Test too small
	invalidReadOnlyVerityRoot.ErrorCorrectionEncodingRoots = 1

	err = invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "verity FEC [ErrorCorrectionEncodingRoots] out of bounds ( (2) <= N <= (24)), currently (1)", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: verity FEC [ErrorCorrectionEncodingRoots] out of bounds ( (2) <= N <= (24)), currently (1)", err.Error())
}

func TestShouldFailInvalidErrorBehavior_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidBehaviorVerityRoot := validReadOnlyVerityRoot

	// Test too large
	invalidBehaviorVerityRoot.VerityErrorBehavior = "not_a_behavior"

	err := invalidBehaviorVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for VerityErrorBehavior (not_a_behavior)", err.Error())

	err = remarshalJSON(invalidBehaviorVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to parse [VerityErrorBehavior]: invalid value for VerityErrorBehavior (not_a_behavior)", err.Error())
}

func TestShouldFailInvalidOverlaySizes_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidReadOnlyVerityRoot := validReadOnlyVerityRootWithOverlays

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "abcd"
	err := invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (abcd), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (abcd), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "1234t"
	err = invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (1234t), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (1234t), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "k1234"
	err = invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (k1234), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (k1234), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "1234kmb"
	err = invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (1234kmb), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (1234kmb), must be of the form '1234, 1234<k,m,g>, 30%", err.Error())
}

func TestShouldFailInvalidOverlaySizePercents_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidReadOnlyVerityRoot := validReadOnlyVerityRootWithOverlays

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "100%"
	err := invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (100%), invalid percentage (100), should be in the range 0 < percentage < 100", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (100%), invalid percentage (100), should be in the range 0 < percentage < 100", err.Error())

	invalidReadOnlyVerityRoot.TmpfsOverlaySize = "0%"
	err = invalidReadOnlyVerityRoot.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "failed to validate [TmpfsOverlaySize] (0%), invalid percentage (0), should be in the range 0 < percentage < 100", err.Error())

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlaySize] (0%), invalid percentage (0), should be in the range 0 < percentage < 100", err.Error())
}

func TestShouldFailNestedVerityOverlays_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot
	invalidReadOnlyVerityRoot := validReadOnlyVerityRoot
	invalidReadOnlyVerityRoot.TmpfsOverlays = []string{"/path", "/path/overlaps"}

	err := remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlays], overlays may not overlap each other (/path)(/path/overlaps)", err.Error())

	invalidReadOnlyVerityRoot.TmpfsOverlays = []string{"/path/overlaps", "/path"}

	err = remarshalJSON(invalidReadOnlyVerityRoot, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlays], overlays may not overlap each other (/path)(/path/overlaps)", err.Error())
}

func TestShouldFailParsingInvalidReadOnlyVerityRootJSON_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot

	err := marshalJSONString(invalidReadOnlyVerityRootJSON, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: json: cannot unmarshal number into Go struct field IntermediateTypeReadOnlyVerityRoot.Enable of type bool", err.Error())
}

func TestShouldFailParsingInvalidReadOnlyVerityRootBehaviorJSON_ReadOnlyVerityRoot(t *testing.T) {
	var checkedReadOnlyVerityRoot ReadOnlyVerityRoot

	err := marshalJSONString(invalidReadONlyVerityBehaviorJSON, &checkedReadOnlyVerityRoot)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [ReadOnlyVerityRoot]: failed to parse [VerityErrorBehavior]: invalid value for VerityErrorBehavior (not_a_behavior)", err.Error())
}
