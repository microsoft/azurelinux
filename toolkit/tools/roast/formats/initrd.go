// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"
	"io"
	"os"
	"path/filepath"

	"github.com/cavaliercoder/go-cpio"
	"github.com/klauspost/pgzip"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// InitrdType represents the format for a compressed initrd file loaded by the Linux kernel at boot
const InitrdType = "initrd"

// Initrd implements Converter interface to convert a directory into an initrd.
type Initrd struct {
}

// Convert converts the image in the initrd.img format
func (i *Initrd) Convert(input, output string, isInputFile bool) (err error) {
	if isInputFile {
		return fmt.Errorf("initrd conversion requires a directory as an input")
	}

	outputFile, err := os.Create(output)
	if err != nil {
		return
	}
	defer outputFile.Close()

	gzipWriter := pgzip.NewWriter(outputFile)
	defer gzipWriter.Close()

	cpioWriter := cpio.NewWriter(gzipWriter)
	defer func() {
		closeErr := cpioWriter.Close()
		if err != nil {
			err = closeErr
		}
	}()

	err = filepath.Walk(input, func(path string, info os.FileInfo, fileErr error) (err error) {
		if fileErr != nil {
			logger.Log.Warnf("File walk error on path (%s), error: %s", path, fileErr)
			return fileErr
		}
		err = addFileToArchive(input, path, info, cpioWriter)
		if err != nil {
			logger.Log.Warnf("Failed to add (%s), error: %s", path, err)
		}
		return
	})

	return
}

// Extension returns the filetype extension produced by this converter.
func (i *Initrd) Extension() string {
	const extension = "img"
	return extension
}

// NewInitrd returns a new Initrd format encoder
func NewInitrd() *Initrd {
	return &Initrd{}
}

func addFileToArchive(inputDir, path string, info os.FileInfo, cpioWriter *cpio.Writer) (err error) {
	// Get the relative path of the file compared to the input directory.
	// The input directory should be considered the "root" of the cpio archive.
	relPath, err := filepath.Rel(inputDir, path)
	if err != nil {
		return
	}

	logger.Log.Debugf("Adding to initrd: %s", relPath)

	// Symlinks need to be resolved to their target file to be added to the cpio archive.
	var link string
	if info.Mode()&os.ModeSymlink != 0 {
		link, err = os.Readlink(path)
		if err != nil {
			return
		}

		logger.Log.Debugf("--> Adding link: (%s) -> (%s)", relPath, link)
	}

	// Convert the OS header into a CPIO header
	header, err := cpio.FileInfoHeader(info, link)
	if err != nil {
		return
	}

	// The default OS header will only have the filename as "Name".
	// Manually set the CPIO header's Name field to the relative path so it
	// is extracted to the correct directory.
	header.Name = relPath

	err = cpioWriter.WriteHeader(header)
	if err != nil {
		return
	}

	// Special files (unix sockets, directories, symlinks, ...) need to be handled differently
	// since a simple byte transfer of the file's content into the CPIO archive can't be achieved.
	if !info.Mode().IsRegular() {
		// For a symlink the reported size will be the size (in bytes) of the link's target.
		// Write this data into the archive.
		if info.Mode()&os.ModeSymlink != 0 {
			_, err = cpioWriter.Write([]byte(link))
		}

		// For all other special files, they will be of size 0 and only contain the header in the archive.
		return
	}

	// For regular files, open the actual file and copy its content into the archive.
	fileToAdd, err := os.Open(path)
	if err != nil {
		return
	}
	defer fileToAdd.Close()

	_, err = io.Copy(cpioWriter, fileToAdd)
	return
}
