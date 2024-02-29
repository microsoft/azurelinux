// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

// Ext4Type represents the ext4 file system format
const Ext4Type = "ext4"

// Ext4 implements Converter interface for Ext4 partitions
type Ext4 struct {
}

// Convert simply makes a copy of the RAW image and renames the extension to ext4
func (e *Ext4) Convert(input, output string, isInputFile bool) (err error) {
	if !isInputFile {
		return fmt.Errorf("ext4 conversion requires a RAW file as an input")
	}
	err = file.Copy(input, output)
	return
}

// Extension returns the filetype extension produced by this converter.
func (e *Ext4) Extension() string {
	return Ext4Type
}

// NewExt4 returns a new xz format encoder
func NewExt4() *Ext4 {
	return &Ext4{}
}
