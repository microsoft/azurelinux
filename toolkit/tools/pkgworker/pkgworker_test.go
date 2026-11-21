// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCheckBuildEnvironment(t *testing.T) {
	const indexURL = "https://build:dummy-token@pkgs.dev.azure.com/example/_packaging/feed/pypi/simple/"
	t.Setenv("UNRELATED_SECRET", "must-not-be-forwarded")
	t.Setenv("PIP_EXTRA_INDEX_URL", "https://example.invalid/simple/")

	for _, tc := range []struct {
		name        string
		runCheck    bool
		indexURL    string
		unset       bool
		expectedEnv []string
	}{
		{name: "check with feed", runCheck: true, indexURL: indexURL, expectedEnv: []string{"PIP_INDEX_URL=" + indexURL}},
		{name: "non-check with feed", indexURL: indexURL},
		{name: "check with empty feed", runCheck: true},
		{name: "check without feed", runCheck: true, unset: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			t.Setenv("PIP_INDEX_URL", tc.indexURL)
			if tc.unset {
				assert.NoError(t, os.Unsetenv("PIP_INDEX_URL"))
			}
			assert.Equal(t, tc.expectedEnv, checkBuildEnvironment(tc.runCheck))
		})
	}
}
