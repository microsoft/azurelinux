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
