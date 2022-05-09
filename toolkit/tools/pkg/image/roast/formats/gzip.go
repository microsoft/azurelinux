// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"
	"io"
	"os"

	"github.com/klauspost/pgzip"
)

// GzipType represents the gzip format
const GzipType = "gz"

// Gzip implements Converter interface to convert a RAW image into a gzipped file
type Gzip struct {
}

// Convert converts the image in the Gzip format
func (g *Gzip) Convert(input, output string, isInputFile bool) (err error) {
	if !isInputFile {
		return fmt.Errorf("gz compression requires a file as an input")
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

	gzipWriter := pgzip.NewWriter(dstFile)
	defer gzipWriter.Close()

	_, err = io.Copy(gzipWriter, srcFile)
	return
}

// Extension returns the filetype extension produced by this converter.
func (g *Gzip) Extension() string {
	return GzipType
}

// NewGzip returns a new Gzip format encoder
func NewGzip() *Gzip {
	return &Gzip{}
}
