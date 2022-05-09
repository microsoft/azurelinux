// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"
	"io"
	"os"

	"github.com/ulikunitz/xz"
)

// XzType represents the xz format
const XzType = "xz"

// Xz implements Converter interface to convert a RAW image into a xz file
type Xz struct {
}

// Convert converts the image in the xz format
func (x *Xz) Convert(input, output string, isInputFile bool) (err error) {
	const squashErrors = false

	if !isInputFile {
		return fmt.Errorf("xz compression requires a file as an input")
	}

	srcFile, err := os.Open(input)
	if err != nil {
		return
	}
	defer srcFile.Close()

	dstFile, err := os.Create(output)
	if err != nil {
		return
	}
	defer dstFile.Close()

	xzWriter, err := xz.NewWriter(dstFile)
	if err != nil {
		return
	}
	defer xzWriter.Close()

	_, err = io.Copy(xzWriter, srcFile)

	return
}

// Extension returns the filetype extension produced by this converter.
func (x *Xz) Extension() string {
	return XzType
}

// NewXz returns a new xz format encoder
func NewXz() *Xz {
	return &Xz{}
}
