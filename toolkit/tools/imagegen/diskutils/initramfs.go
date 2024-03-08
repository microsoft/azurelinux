// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create or modify Initramfs files

package diskutils

import (
	"bytes"
	"fmt"
	"io"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"github.com/cavaliercoder/go-cpio"
	"github.com/klauspost/pgzip"
)

// InitramfsMount represented an editable initramfs
type InitramfsMount struct {
	pgzWriter           *pgzip.Writer
	cpioWriter          *cpio.Writer
	outputBuffer        *bytes.Buffer
	initramfsOutputFile *os.File
}

// CreateInitramfs creates a new initramfs
// Caller is responsible for calling initramfs.Close() when finished
func CreateInitramfs(initramfsPath string) (initramfs InitramfsMount, err error) {
	// Initramfs traditionally is -rw-------
	const initramfsModeBits = os.FileMode(0600)

	initramfs.outputBuffer = new(bytes.Buffer)
	initramfs.pgzWriter = pgzip.NewWriter(initramfs.outputBuffer)
	initramfs.cpioWriter = cpio.NewWriter(initramfs.pgzWriter)

	initramfs.initramfsOutputFile, err = os.OpenFile(initramfsPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, initramfsModeBits)
	if err != nil {
		err = fmt.Errorf("failed to create a new initramfs at (%s):\n%w", initramfsPath, err)
	}

	return
}

// OpenInitramfs makes an existing initramfs editable
// Caller is responsible for calling initramfs.Close() when finished
func OpenInitramfs(initramfsPath string) (initramfs InitramfsMount, err error) {
	logger.Log.Debugf("Opening intramfs (%s)", initramfsPath)
	inputFile, err := os.Open(initramfsPath)
	if err != nil {
		return
	}
	defer inputFile.Close()

	gzReader, err := pgzip.NewReader(inputFile)
	if err != nil {
		return
	}
	defer gzReader.Close()
	cpioReader := cpio.NewReader(gzReader)
	//cpio.Reader has no Close() function to defer

	initramfs.outputBuffer = new(bytes.Buffer)
	initramfs.pgzWriter = pgzip.NewWriter(initramfs.outputBuffer)
	initramfs.cpioWriter = cpio.NewWriter(initramfs.pgzWriter)

	// Read until EOF or other error
	for {
		var (
			bytesIO        int64
			linkPayload    []byte
			nextFileHeader *cpio.Header
		)

		nextFileHeader, err = cpioReader.Next()
		if err == io.EOF {
			// Expected end of archive
			err = nil
			break
		}
		if err != nil {
			return
		}

		// For a given symlink, generate a payload that contains the read value of the link.
		// The payload should be written after the header.
		// e.g. A link from (/bin -> /usr/bin) would have a payload of "/usr/bin".
		// cpio.ModeSymlink is two bits (one of which is reused), need to check for actual
		// equality rather than non-zero after masking
		isLink := ((nextFileHeader.Mode & cpio.ModeType) == cpio.ModeSymlink)
		if isLink {
			linkPayload = []byte(nextFileHeader.Linkname)
			nextFileHeader.Size = int64(len(linkPayload))
		}

		err = initramfs.cpioWriter.WriteHeader(nextFileHeader)
		if err != nil {
			return
		}

		if isLink {
			var bytesWrittenInt int

			// Write returns an int, cast it to an int64 afterwards
			logger.Log.Tracef("Creating link (%s) -> %s", nextFileHeader.Name, nextFileHeader.Linkname)
			bytesWrittenInt, err = initramfs.cpioWriter.Write(linkPayload)
			bytesIO = int64(bytesWrittenInt)
		} else {
			bytesIO, err = io.Copy(initramfs.cpioWriter, cpioReader)
		}

		if err != nil {
			return
		}

		logger.Log.Tracef("File (%s) caused (%d) bytes to be transferred to new archive", nextFileHeader.Name, bytesIO)
		logger.Log.Tracef("Buffer unread length: (%d)", initramfs.outputBuffer.Len())
	}

	inputFile.Close()

	fileInfo, err := os.Stat(initramfsPath)
	if err != nil {
		return
	}

	// We can't edit a CPIO archive in place, completely overwrite the file with truncate
	// The output buffer in memory will be used to re-create the initramfs.
	initramfs.initramfsOutputFile, err = os.OpenFile(initramfsPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, fileInfo.Mode())

	return
}

// Close flushes the archives and closes all initramfs resources
func (i *InitramfsMount) Close() (err error) {
	var bytesIO int

	logger.Log.Debugf("Closing initramfs file (%s)", i.initramfsOutputFile.Name())

	// Defer close calls to make sure we handle any errors, failing to
	// close the file means we can't close the install root.
	defer i.initramfsOutputFile.Close()
	defer i.pgzWriter.Close()
	defer i.cpioWriter.Close()

	err = i.cpioWriter.Close()
	if err != nil {
		err = fmt.Errorf("failed to close initramfs cpio writer:\n%w", err)
		return
	}
	err = i.pgzWriter.Close()
	if err != nil {
		err = fmt.Errorf("failed to close initramfs pgzip writer:\n%w", err)
		return
	}

	logger.Log.Debugf("Writing (%d) bytes to file", i.outputBuffer.Len())
	bytesIO, err = i.initramfsOutputFile.Write(i.outputBuffer.Bytes())
	if err != nil {
		err = fmt.Errorf("failed to write initramfs file:\n%w", err)
		return
	}
	logger.Log.Infof("Bytes writen to file: (%d)", bytesIO)

	// Explicit call to fsync, archive corruption was occuring occasionally otherwise.
	err = i.initramfsOutputFile.Sync()
	if err != nil {
		err = fmt.Errorf("failed to sync initramfs file:\n%w", err)
		return
	}

	err = i.initramfsOutputFile.Close()
	if err != nil {
		err = fmt.Errorf("failed to close initramfs:\n%w", err)
		return
	}
	return
}

// AddFileToInitramfs places a single file in the initramfs at the destination path.
// - sourcePath: Path to file which is to be added
// - destPath: Final destination in the initramfs
func (i *InitramfsMount) AddFileToInitramfs(sourcePath, destPath string) (err error) {
	var bytesIO int64
	fileInfo, err := os.Lstat(sourcePath)
	if err != nil {
		return
	}
	file, err := os.Open(sourcePath)
	if err != nil {
		return
	}
	defer file.Close()

	// Symlinks need to be resolved to their target file to be added to the cpio archive.
	var linkDestination string
	// This is a Go symlink mode iota, distinct from the cpio symlink mode bits used in OpenInitramfs(),
	// and may be checked directly.
	isSymlink := (fileInfo.Mode() & os.ModeSymlink) != 0
	if isSymlink {
		linkDestination, err = os.Readlink(sourcePath)
		if err != nil {
			return
		}

		logger.Log.Debugf("--> Adding link: (%s) -> (%s)", sourcePath, linkDestination)
	}

	// Convert the OS header into a CPIO header
	// Only symlink files will use the linkDestination parameter, may be "" for other files.
	header, err := cpio.FileInfoHeader(fileInfo, linkDestination)
	if err != nil {
		return
	}
	header.Name = destPath

	err = i.cpioWriter.WriteHeader(header)
	if err != nil {
		return
	}

	if fileInfo.Mode().IsRegular() {
		bytesIO, err = io.Copy(i.cpioWriter, file)
		if err != nil {
			err = fmt.Errorf("failed to add regular file (%s) into initramfs:\n%w", header.Name, err)
			return
		}
		logger.Log.Debugf("New file (%s) caused (%d) bytes to be transferred to new archive", header.Name, bytesIO)
	} else {
		// Special files (unix sockets, directories, symlinks, ...) need to be handled differently
		// since a simple byte transfer of the file's content into the CPIO archive can't be achieved.
		logger.Log.Debugf("Adding special file (%s) to initramfs", header.Name)

		// For a symlink the reported size will be the size (in bytes) of the link's target.
		// Write this data into the archive.
		if isSymlink {
			_, err = i.cpioWriter.Write([]byte(linkDestination))
			if err != nil {
				err = fmt.Errorf("failed to add symlink (%s)->(%s) to initramfs:\n%w", header.Name, linkDestination, err)
				return
			}
		}

		// For all other special files, they will be of size 0 and only contain the header in the archive.
	}

	return
}
