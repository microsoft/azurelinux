// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestCheckBuildEnvironment(t *testing.T) {
	const indexURL = "https://build:token@pkgs.dev.azure.com/example/_packaging/feed/pypi/simple/"
	t.Setenv("PIP_INDEX_URL", indexURL)
	t.Setenv("NPM_CONFIG_REGISTRY", "https://pkgs.dev.azure.com/example/_packaging/feed/npm/registry/")
	t.Setenv("EMPTY_VALUE", "")
	t.Setenv("UNRELATED_SECRET", "must-not-be-forwarded")

	for _, tc := range []struct {
		name        string
		runCheck    bool
		names       []string
		expectedEnv []string
	}{
		{name: "check forwards only listed variables", runCheck: true, names: []string{"PIP_INDEX_URL"}, expectedEnv: []string{"PIP_INDEX_URL=" + indexURL}},
		{
			name:     "check forwards several variables in order",
			runCheck: true,
			names:    []string{"NPM_CONFIG_REGISTRY", "PIP_INDEX_URL"},
			expectedEnv: []string{
				"NPM_CONFIG_REGISTRY=https://pkgs.dev.azure.com/example/_packaging/feed/npm/registry/",
				"PIP_INDEX_URL=" + indexURL,
			},
		},
		{name: "check skips empty and unset variables", runCheck: true, names: []string{"EMPTY_VALUE", "NOT_SET_ANYWHERE"}},
		{name: "check without names forwards nothing", runCheck: true},
		{name: "non-check forwards nothing", names: []string{"PIP_INDEX_URL"}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			assert.Equal(t, tc.expectedEnv, checkBuildEnvironment(tc.runCheck, tc.names))
		})
	}
}
