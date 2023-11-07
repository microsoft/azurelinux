// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"archive/tar"
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

type Archive struct {
	ArchivePath string // Path to the generated archive file
}

// Print a table of rpms that are missing from the archive or manifest, interleaving the two lists
func CreateManifestMissmatchReport(missingFromArchive, missingFromManifest []string, archivePath, manifestPath string) (tableLines []string) {
	mergedList := append(missingFromArchive, missingFromManifest...)

	// Format a simple table with two columns:
	// e.g.
	// In Manifest Only 	 In Archive Only
	// ----------------------
	// aPkg-v1
	// 					 aPkg-v2
	// 					 bPkg-v1

	// Get width of longest string.
	header1 := "In Manifest Only"
	header2 := "In Archive Only"

	maxLen := len(header2) + 8 // Assume 2x tab is 8
	for _, s := range mergedList {
		if len(s) > maxLen {
			maxLen = len(s)
		}
	}

	tableLines = append(tableLines, "Missmatched packages between:")
	tableLines = append(tableLines, fmt.Sprintf("Archive: '%s'", archivePath))
	tableLines = append(tableLines, fmt.Sprintf("Manifest: '%s'", manifestPath))
	tableLines = append(tableLines, "")

	// Start table
	tableLines = append(tableLines, header1)
	tableLines = append(tableLines, fmt.Sprintf("\t\t%s", header2))
	tableLines = append(tableLines, strings.Repeat("-", maxLen))

	sort.Strings(mergedList)
	archiveSet := sliceutils.SliceToSet(missingFromArchive)
	for _, pkg := range mergedList {
		if archiveSet[pkg] {
			tableLines = append(tableLines, pkg)
		} else {
			tableLines = append(tableLines, fmt.Sprintf("\t\t%s", pkg))
		}
	}
	tableLines = append(tableLines, "")
	return
}

func (a *Archive) ValidateArchiveContents(expectedRpms []string) (missingFromArchive, missingFromManifest []string, err error) {
	archiveRpms, err := a.getArchiveContents()
	if err != nil {
		return
	}

	missingFromArchive = sliceutils.FindMatches(expectedRpms, func(rpm string) bool {
		return !sliceutils.Contains(archiveRpms, rpm, sliceutils.StringMatch)
	})
	missingFromManifest = sliceutils.FindMatches(archiveRpms, func(rpm string) bool {
		return !sliceutils.Contains(expectedRpms, rpm, sliceutils.StringMatch)
	})
	return
}

func (a *Archive) getArchiveContents() (rpms []string, err error) {
	logger.Log.Infof("Extracting rpms from tar.gz file: %s", a.ArchivePath)
	tarGzFileStream, err := os.Open(a.ArchivePath)
	if err != nil {
		err = fmt.Errorf("failed to open tar.gz file. Error:\n%w", err)
		return
	}
	defer tarGzFileStream.Close()

	tarStream, err := gzip.NewReader(tarGzFileStream)
	if err != nil {
		err = fmt.Errorf("failed to create gzip reader. Error:\n%w", err)
		return
	}
	defer tarStream.Close()

	tarReader := tar.NewReader(tarStream)
	for {
		header, tarErr := tarReader.Next()
		if tarErr != nil {
			if tarErr == io.EOF {
				break
			}
			err = fmt.Errorf("failed to read tar file. Error:\n%w", tarErr)
			return
		}
		filename := header.Name

		switch header.Typeflag {
		case tar.TypeDir:
			// Converting to a flat directory structure, ignore directories
			continue
		case tar.TypeReg:
			rpms = append(rpms, filepath.Base(filename))
		default:
			err = fmt.Errorf("unknown type: %v in tar file", header.Typeflag)
			return
		}
	}
	return
}

func (a *Archive) ExtractToolchainRpms(rpmsDir string) (err error) {
	logger.Log.Infof("Extracting rpms from tar.gz file: %s", a.ArchivePath)
	tarGzFileStream, err := os.Open(a.ArchivePath)
	if err != nil {
		err = fmt.Errorf("failed to open tar.gz file. Error:\n%w", err)
		return
	}
	defer tarGzFileStream.Close()

	tarStream, err := gzip.NewReader(tarGzFileStream)
	if err != nil {
		err = fmt.Errorf("failed to create gzip reader. Error:\n%w", err)
		return
	}
	defer tarStream.Close()

	tarReader := tar.NewReader(tarStream)

	logger.Log.Infof("Extracting rpms from'%s'", a.ArchivePath)
	totalRpms := 0
	extractedRpms := 0
	for {
		header, tarErr := tarReader.Next()
		if tarErr != nil {
			if tarErr == io.EOF {
				logger.Log.Infof("Extracted %d/%d rpms from '%s'", extractedRpms, totalRpms, a.ArchivePath)
				break
			}
			err = fmt.Errorf("failed to read tar file. Error:\n%w", tarErr)
			return
		}

		// get the individual filename and extract to the current directory
		filename := filepath.Join(rpmsDir, header.Name)

		switch header.Typeflag {
		case tar.TypeDir:
			// Converting to a flat directory structure, ignore directories
			continue
		case tar.TypeReg:
			logger.Log.Debugf("Checking toolchain rpm: '%s'", filename)
			totalRpms++
			dstFile := filepath.Join(rpmsDir, filepath.Base(filename))

			tarBytes := make([]byte, header.Size)
			var size int64 = 0
			for size < header.Size {
				var readSize int
				readSize, err = tarReader.Read(tarBytes[size:])
				if err != nil {
					if err != io.EOF {
						err = fmt.Errorf("failed to read file. Error:\n%w", err)
						return
					}
				}
				size += int64(readSize)
			}

			var existingFileOk bool
			existingFileOk, err = file.PathExists(dstFile)
			if err != nil {
				return fmt.Errorf("unable to check if rpm exists: %w", err)
			}
			if existingFileOk {
				logger.Log.Debugf("Checking if file contents are the same: %s", dstFile)
				existingFileBytes, readErr := os.ReadFile(dstFile)
				if err != nil {
					err = fmt.Errorf("unable to read input file:\n%w", readErr)
					return
				}
				existingFileOk = bytes.Equal(existingFileBytes, tarBytes)
				if !existingFileOk {
					logger.Log.Infof("File already exists but has different contents: %s", dstFile)
				}
			} else {
				logger.Log.Infof("File does not exist: %s", dstFile)
			}

			if !existingFileOk {
				extractedRpms++
				var writer *os.File
				writer, err = os.Create(dstFile)
				if err != nil {
					err = fmt.Errorf("failed to create file. Error:\n%w", err)
					return err
				}

				logger.Log.Infof("Extracting toolchain rpm: %s", dstFile)
				byteReader := bytes.NewReader(tarBytes)
				_, err = io.Copy(writer, byteReader)
				writer.Close()

				if err != nil {
					err = fmt.Errorf("failed to copy file. Error:\n%w", err)
					return err
				}
			} else {
				logger.Log.Debugf("File already exists and is the same: %s", dstFile)
			}
		default:
			err = fmt.Errorf("unknown type: %v in tar file '%s'", header.Typeflag, a.ArchivePath)
			return err
		}
	}
	return
}
