// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/stretchr/testify/assert"
)

func TestParitionSizeGrow(t *testing.T) {
	var size PartitionSize
	err := UnmarshalYaml([]byte("grow"), &size)
	assert.NoError(t, err)
}

func TestParitionSizeMiB(t *testing.T) {
	var size PartitionSize
	err := UnmarshalYaml([]byte("1M"), &size)
	assert.NoError(t, err)
	assert.Equal(t, PartitionSize{PartitionSizeTypeExplicit, 1 * diskutils.MiB}, size)
}

func TestParitionInvalidNotString(t *testing.T) {
	var size PartitionSize
	err := UnmarshalYaml([]byte("[]"), &size)
	assert.ErrorContains(t, err, "failed to parse partition size")
}

func TestParitionInvalidValue(t *testing.T) {
	var size PartitionSize
	err := UnmarshalYaml([]byte("cat"), &size)
	assert.ErrorContains(t, err, "(cat) has incorrect format")
}
