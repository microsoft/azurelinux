// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	// QcowType represents the qcow2 virtual drive format
	QcowType = "qcow2"
)

// Qcow implements Converter interface to convert a RAW image into a qcow2 file
type Qcow struct {
}

// Convert converts the image in the qcow2 format
func (v *Qcow) Convert(input, output string, isInputFile bool) (err error) {
	const (
		outputFormat = "qcow2"
		squashErrors = false
	)

	if !isInputFile {
		return fmt.Errorf("qcow2 conversion requires a RAW file as an input")
	}

	err = shell.ExecuteLive(squashErrors, "qemu-img", "convert", "-O", outputFormat, input, output)
	return
}

// Extension returns the filetype extension produced by this converter.
func (v *Qcow) Extension() string {
	return QcowType
}

// NewQcow returns a new qcow format encoder
func NewQcow() *Qcow {
	return &Qcow{}
}
