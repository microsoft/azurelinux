// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	// VhdType represents the vhd virtual drive format
	VhdType = "vhd"

	// VhdxType represents the vhdx virtual drive format
	VhdxType = "vhdx"
)

// Vhd implements Converter interface to convert a RAW image into a VHD(x) file
type Vhd struct {
	generation2 bool
}

// Convert converts the image in the VHD(x) format
func (v *Vhd) Convert(input, output string, isInputFile bool) (err error) {
	const (
		qemuVhdType  = "vpc"
		squashErrors = false
	)

	if !isInputFile {
		return fmt.Errorf("vhd conversion requires a RAW file as an input")
	}

	var format string
	args := []string{"convert", input, output}

	if v.generation2 {
		format = VhdxType
	} else {
		format = qemuVhdType
		args = append(args, "-o", "subformat=fixed,force_size")
	}

	args = append(args, "-O", format)

	err = shell.ExecuteLive(squashErrors, "qemu-img", args...)
	return
}

// Extension returns the filetype extension produced by this converter.
func (v *Vhd) Extension() string {
	if v.generation2 {
		return VhdxType
	}

	return VhdType
}

// NewVhd returns a new Vhd(x) format encoder
func NewVhd(generation2 bool) *Vhd {
	return &Vhd{
		generation2: generation2,
	}
}
