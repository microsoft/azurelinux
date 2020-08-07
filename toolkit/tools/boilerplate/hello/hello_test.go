// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package hello

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHelloWorld(t *testing.T) {
	want := "Hello, world!"
	assert.Equal(t, want, World())
}
