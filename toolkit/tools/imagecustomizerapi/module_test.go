// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestModuleIsValidValidValue(t *testing.T) {
	module := Module{
		Name:     "nbd",
		LoadMode: ModuleLoadModeAlways,
	}
	err := module.IsValid()
	assert.NoError(t, err)
}

func TestModuleIsValidEmptyName(t *testing.T) {
	module := Module{
		Name: "",
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "module name cannot be empty")
}

func TestModuleIsValidInvalidName(t *testing.T) {
	module := Module{
		Name: "cat and dogs",
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "module name (cat and dogs) cannot contain spaces or newline characters")
}

func TestModuleIsValidInvalidLoadMode(t *testing.T) {
	module := Module{
		Name:     "nbd",
		LoadMode: "dog",
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "invalid module load mode value (dog)")
}

func TestModuleIsValidValidOptions(t *testing.T) {
	module := Module{
		Name: "nbd",
		Options: map[string]string{
			"nbds_max": "8",
		},
	}
	err := module.IsValid()
	assert.NoError(t, err)
}

func TestModuleIsValidValidEmptyOptionName(t *testing.T) {
	module := Module{
		Name: "nbd",
		Options: map[string]string{
			"": "8",
		},
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "invalid module (nbd)")
	assert.ErrorContains(t, err, "option key cannot be empty")
}

func TestModuleIsValidValidInvalidOptionName(t *testing.T) {
	module := Module{
		Name: "nbd",
		Options: map[string]string{
			" ": "8",
		},
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "invalid module (nbd)")
	assert.ErrorContains(t, err, "option key ( ) cannot contain spaces or newline characters")
}

func TestModuleIsValidValidEmptyOptionValue(t *testing.T) {
	module := Module{
		Name: "nbd",
		Options: map[string]string{
			"nbds_max": "",
		},
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "invalid module (nbd)")
	assert.ErrorContains(t, err, "option value cannot be empty")
}

func TestModuleIsValidValidInvalidOptionValue(t *testing.T) {
	module := Module{
		Name: "nbd",
		Options: map[string]string{
			"nbds_max": " ",
		},
	}
	err := module.IsValid()
	assert.ErrorContains(t, err, "invalid module (nbd)")
	assert.ErrorContains(t, err, "option value ( ) cannot contain spaces or newline characters")
}
