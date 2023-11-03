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

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/systemdependency"
)

const officialName = "official"

type OfficialScript struct {
	OutputFile           string   // Path to the generated bootstrap file
	ScriptPath           string   // Path to the bootstrap script
	WorkingDir           string   // Path to the working directory
	DistTag              string   // Dist tag for the rpms
	BuildNumber          string   // Build number for the rpms
	ReleaseVersion       string   // Release version for the rpms
	BuildDir             string   // Path to the build directory
	RpmsDir              string   // Path to the rpms directory
	SpecsDir             string   // Path to the specs directory
	RunCheck             bool     // Run check
	UseIncremental       bool     // Use incremental build mode
	IntermediateSrpmsDir string   // Path to the intermediate srpms directory
	OutputSrpmsDir       string   // Path to the output srpms directory
	ToolchainFromRepos   string   // Path to the toolchain from repos
	ToolchainManifest    string   // Path to the toolchain manifest
	BldTracker           string   // Path to the bld tracker
	TimestampFile        string   // Path to the timestamp file
	InputFiles           []string // List of input files to hash for validating the cache
}

func (o *OfficialScript) CheckCache(cacheDir string) (string, bool, error) {
	return checkCache(officialName, o.InputFiles, cacheDir)
}

func (o *OfficialScript) RestoreFromCache(cacheDir string) error {
	return restoreFromCache(officialName, o.InputFiles, o.OutputFile, cacheDir)
}

func (o *OfficialScript) AddToCache(cacheDir string) (string, error) {
	return addToCache(officialName, o.InputFiles, o.OutputFile, cacheDir)
}

func (o *OfficialScript) PrepIncrementalRpms(downloadDir string, toolchainRPMs []string) (err error) {
	for _, rpm := range toolchainRPMs {
		var fileExists bool
		srcPath := filepath.Join(downloadDir, rpm)
		dstPath := filepath.Join(o.ToolchainFromRepos, rpm)
		fileExists, err = file.PathExists(srcPath)

		if err != nil {
			return fmt.Errorf("unable to check if rpm exists: %w", err)
		}
		if !fileExists {
			// Just touch an empty file in the delta directory
			dstFile, fileErr := os.Create(dstPath)
			if fileErr != nil {
				err = fmt.Errorf("unable to create delta rpm file: %w", fileErr)
				return
			}
			dstFile.Close()
		} else {
			err = file.Copy(srcPath, dstPath)
			if err != nil {
				err = fmt.Errorf("unable to restore from cache:\n%w", err)
				return
			}
		}
	}
	return
}

func (o *OfficialScript) BuildOfficialToolchainRpms() (err error) {
	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Infof("Official Toolchain: %s", line)
	}
	onStdErr := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Debugf("Official Toolchain: %s", line)
	}

	script := o.ScriptPath
	incrementalArg := "n"
	if o.UseIncremental {
		incrementalArg = "y"
	}
	gzipTool, err := systemdependency.GzipTool()
	if err != nil {
		err = fmt.Errorf("failed to get gzip tool. Error:\n%w", err)
		return
	}
	runCheckArg := "n"
	if o.RunCheck {
		runCheckArg = "y"
	}
	args := []string{
		o.DistTag,
		o.BuildNumber,
		o.ReleaseVersion,
		o.BuildDir,
		o.RpmsDir,
		o.SpecsDir,
		runCheckArg,
		filepath.Dir(o.ToolchainManifest),
		incrementalArg,
		gzipTool,
		o.IntermediateSrpmsDir,
		o.OutputSrpmsDir,
		o.ToolchainFromRepos,
		o.ToolchainManifest,
		o.BldTracker,
		o.TimestampFile,
	}

	err = shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, o.WorkingDir, args...)
	if err != nil {
		err = fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
		return
	}

	return nil
}

func (o *OfficialScript) ExtractToolchainRpms(rpmsDir string) (err error) {
	logger.Log.Infof("Extracting rpms from tar.gz file: %s", o.OutputFile)
	tarGzFileStream, err := os.Open(o.OutputFile)
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

	logger.Log.Infof("Extracting rpms from'%s'", o.OutputFile)
	totalRpms := 0
	extractedRpms := 0
	for {
		header, tarErr := tarReader.Next()
		if tarErr != nil {
			if tarErr == io.EOF {
				logger.Log.Infof("Extracted %d/%d rpms from '%s'", extractedRpms, totalRpms, o.OutputFile)
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
				logger.Log.Debugf("Checking if file contents are the same: %s", filename)
				existingFileBytes, readErr := os.ReadFile(dstFile)
				if err != nil {
					err = fmt.Errorf("unable to read input file:\n%w", readErr)
					return
				}
				existingFileOk = bytes.Equal(existingFileBytes, tarBytes)
				if !existingFileOk {
					logger.Log.Infof("File already exists but has different contents: %s", filename)
				}
			}

			if !existingFileOk {
				extractedRpms++
				var writer *os.File
				writer, err = os.Create(dstFile)
				if err != nil {
					err = fmt.Errorf("failed to create file. Error:\n%w", err)
					return err
				}

				logger.Log.Infof("Extracting toolchain rpm: %s", filename)
				byteReader := bytes.NewReader(tarBytes)
				_, err = io.Copy(writer, byteReader)
				writer.Close()

				if err != nil {
					err = fmt.Errorf("failed to copy file. Error:\n%w", err)
					return err
				}
			} else {
				logger.Log.Debugf("File already exists and is the same: %s", filename)
			}
		default:
			err = fmt.Errorf("unknown type: %v in tar file", header.Typeflag)
			return err
		}
	}
	return
}
