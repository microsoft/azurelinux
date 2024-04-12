// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

// DiffType represents the diff file system format
const DiffType = "diff"

// Diff implements Converter interface for Diff partitions
type Diff struct {
}

// Convert simply makes a copy of the RAW image and renames the extension to .diff
func (e *Diff) Convert(input, output string, isInputFile bool) (err error) {
	if !isInputFile {
		return fmt.Errorf("overlay diff conversion requires a RAW file as an input")
	}
	err = file.Copy(input, output)
	return
}

// Extension returns the filetype extension produced by this converter.
func (e *Diff) Extension() string {
	return DiffType
}

// NewDiff returns a new xz format encoder
func NewDiff() *Diff {
	return &Diff{}
}
