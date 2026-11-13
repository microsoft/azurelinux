// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package buildagents

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestSerializeChrootBuildAgentConfigCheckEnvPassthrough(t *testing.T) {
	config := &BuildAgentConfig{CheckEnvPassthrough: []string{"PIP_INDEX_URL", "NPM_CONFIG_REGISTRY"}}
	t.Setenv("PIP_INDEX_URL", "https://build:token@example.invalid/simple/")

	checkArgs := serializeChrootBuildAgentConfig(config, "pkg", "pkg.src.rpm", "pkg.log", "x86_64", true, nil, time.Hour)
	assert.Contains(t, checkArgs, "--check-env-passthrough=PIP_INDEX_URL")
	assert.Contains(t, checkArgs, "--check-env-passthrough=NPM_CONFIG_REGISTRY")
	for _, arg := range checkArgs {
		// Only names are serialized; values stay in the environment and out of argv.
		assert.NotContains(t, arg, "token")
	}

	buildArgs := serializeChrootBuildAgentConfig(config, "pkg", "pkg.src.rpm", "pkg.log", "x86_64", false, nil, time.Hour)
	for _, arg := range buildArgs {
		assert.NotContains(t, arg, "--check-env-passthrough")
	}
}

func TestValidateEnvVarNames(t *testing.T) {
	assert.NoError(t, ValidateEnvVarNames(nil))
	assert.NoError(t, ValidateEnvVarNames([]string{"PIP_INDEX_URL", "_private", "npm_config_registry2"}))

	for _, invalid := range []string{"", "2NAME", "NAME=value", "NAME WITH SPACE", "NAME,OTHER", "-flag"} {
		assert.Error(t, ValidateEnvVarNames([]string{"PIP_INDEX_URL", invalid}), "expected %q to be rejected", invalid)
	}
}
