// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

// RdiffType represents the rdiff file system format
const RdiffType = "rdiff"

// Rdiff implements Converter interface for Rdiff partitions
type Rdiff struct {
}

// Convert simply makes a copy of the RAW image and renames the extension to .diff
func (e *Rdiff) Convert(input, output string, isInputFile bool) (err error) {
	if !isInputFile {
		return fmt.Errorf("rdiff conversion requires a RAW file as an input")
	}
	err = file.Copy(input, output)
	return
}

// Extension returns the filetype extension produced by this converter.
func (e *Rdiff) Extension() string {
	return RdiffType
}

// NewRdiff returns a new xz format encoder
func NewRdiff() *Rdiff {
	return &Rdiff{}
}
