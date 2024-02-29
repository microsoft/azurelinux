// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

// RawType represents the raw format (no conversion)
const RawType = "raw"

// Raw implements Converter interface for RAW images
type Raw struct {
}

// Convert simply makes a copy of the RAW image
func (r *Raw) Convert(input, output string, isInputFile bool) (err error) {
	if !isInputFile {
		return fmt.Errorf("raw conversion requires a RAW file as an input")
	}
	err = file.Copy(input, output)
	return
}

// Extension returns the filetype extension produced by this converter.
func (r *Raw) Extension() string {
	return RawType
}

// NewRaw returns a new xz format encoder
func NewRaw() *Raw {
	return &Raw{}
}
