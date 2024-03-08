// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import "github.com/microsoft/azurelinux/toolkit/tools/internal/shell"

// TarXzType represents the tar.xz format
const TarXzType = "tar.xz"

// TarXz implements Converter interface to convert a RAW image into a tar.xz file
type TarXz struct {
}

// Convert converts the image in the tar.xz format
func (t *TarXz) Convert(input, output string, isInputFile bool) (err error) {
	const squashErrors = false
	err = shell.ExecuteLive(squashErrors, "tar", "-cJf", output, input)
	return
}

// Extension returns the filetype extension produced by this converter.
func (t *TarXz) Extension() string {
	return TarXzType
}

// NewTarXz returns a new TarXz format encoder
func NewTarXz() *TarXz {
	return &TarXz{}
}
