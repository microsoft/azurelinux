// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

// SquashFSType represents the squashfs format
const SquashFSType = "squashfs"

// SquashFS implements Converter interface to convert a RAW image into a squashfs file
type SquashFS struct {
}

// Convert converts the image in the squashfs format
func (t *SquashFS) Convert(input, output string, isInputFile bool) (err error) {
	const (
		squashErrors = false
	)

	if !isInputFile {
		return fmt.Errorf("squashfs conversion requires an input")
	}

	err = shell.ExecuteLive(squashErrors, "mksquashfs", input, output, "-all-root", "-wildcards", "-e", "tmp/*", "-noappend")
	return
}

// Extension returns the filetype extension produced by this converter.
func (t *SquashFS) Extension() string {
	return SquashFSType
}

// NewSquashFS returns a new SquashFS format encoder
func NewSquashFS() *SquashFS {
	return &SquashFS{}
}
