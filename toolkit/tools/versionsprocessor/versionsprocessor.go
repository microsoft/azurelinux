// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// versionsprocessor is a tool to generate a macro file of all specs version and release.
// It iterates over all of the SPEC files in the provided directory, gets the version and release for each SPEC,
// and then writes that information to an output file as RPM macros file.
// The output file is then provided to other tools and passed into their respective rpm macros folder so that rpmbuild command automatically recognize it.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app           = kingpin.New("versionsprocessor", "A tool to generate a macro file of all specs version and release")
	specsDir      = exe.InputDirFlag(app, "Directory to scan for SPECS")
	output        = exe.OutputFlag(app, "Output file to export the JSON")
	distTag       = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	targetArch    = app.Flag("target-arch", "The architecture of the machine the RPM binaries run on").String()
	buildDir      = app.Flag("build-dir", "Directory to store temporary files while parsing.").String()
	logFlags      = exe.SetupLogFlags(app)
	profFlags     = exe.SetupProfileFlags(app)
	workerTar     = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.  If this argument is empty, specs will be parsed in the host environment.").ExistingFile()
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
	extraFiles    = app.Flag("extra-macros-file", "Additional files whose contents will be appended to the output; may be specified multiple times.").ExistingFiles()
)

func main() {
	var (
		chroot       *safechroot.Chroot
		macrosOutput []string
	)

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("versionsprocessor", *timestampFile)
	defer timestamp.CompleteTiming()

	var buildArch string = *targetArch

	if *targetArch == "" {
		buildArch, err = rpm.GetRpmArch(runtime.GOARCH)
		if err != nil {
			logger.Log.Errorf("Failed to get RPM architecture for GOARCH %s: %s", runtime.GOARCH, err)
			return
		}
	}

	if *workerTar == "" {
		logger.Log.Error("No worker tar provided, please provide a worker tar to parse specs in the chroot environment.")
		return
	}

	const leaveFilesOnDisk = false
	chroot, err = specreaderutils.CreateChroot("versionprocessor_chroot", *workerTar, *buildDir, *specsDir)
	if err != nil {
		logger.PanicOnError("Failed to create chroot")
	}
	defer chroot.Close(leaveFilesOnDisk)

	doParse := func() error {
		// Find all spec files in provided specs dir
		allSpecFiles, err := specreaderutils.FindSpecFiles(*specsDir, nil)
		if err != nil {
			logger.Log.Errorf("Error finding spec files: %s", err)
			return err
		}

		logger.Log.Infof("Processing version and release for %d spec files into %s", len(allSpecFiles), *output)

		type ProcessResult struct {
			macros []string
			err    error
		}
		resultsChannel := make(chan ProcessResult, len(allSpecFiles))

		for _, specFile := range allSpecFiles {
			go func(sf string) {
				macros, processErr := processSpecFile(sf, buildArch, *distTag, nil)
				if processErr != nil {
					processErr = fmt.Errorf("error processing spec file (%s): %w", sf, processErr)
				}
				resultsChannel <- ProcessResult{
					macros: macros,
					err:    processErr,
				}
			}(specFile)
		}

		for i := 0; i < len(allSpecFiles); i++ {
			result := <-resultsChannel
			if result.err != nil {
				logger.Log.Errorf("%s", result.err)
				return result.err
			}
			macrosOutput = append(macrosOutput, result.macros...)
		}

		return err
	}

	err = chroot.Run(doParse)

	if err != nil {
		logger.Log.Fatalf("Error processing spec files: %s", err)
	}

	err = writeExtraFilesToOutput(*extraFiles, macrosOutput, *output)
	if err != nil {
		logger.Log.Errorf("Failed to write extra files to output: %s", err)
		os.Exit(1)
	}
}

func processSpecFile(specFile string, buildArch string, distTag string, macrosOutput []string) (newMacrosOutput []string, err error) {
	specFileName := filepath.Base(specFile)

	sourceDir := filepath.Dir(specFile)
	defines := rpm.DefaultDistroDefines(false, distTag)

	packages, err := rpm.QuerySPECForBuiltRPMs(specFile, sourceDir, buildArch, defines)
	if err != nil {
		logger.Log.Errorf("Failed to query spec file (%s). Error: %s", specFileName, err)
		return nil, err
	}

	for _, packageNEVRA := range packages {
		macros, processErr := processPackageVersionString(packageNEVRA)
		if processErr != nil {
			logger.Log.Errorf("Failed to process package (%s) from spec file (%s): %s", packageNEVRA, specFileName, processErr)
			continue
		}

		macrosOutput = append(macrosOutput, macros...)
	}

	return macrosOutput, nil
}

func processPackageVersionString(packageNEVRA string) (macros []string, err error) {
	const prefix = "azl"

	matches := rpm.RpmSpecBuiltRPMRegex.FindStringSubmatch(packageNEVRA)
	if len(matches) != rpm.RpmSpecBuiltRPMRegexMatchesCount {
		return nil, fmt.Errorf("invalid package NEVRA format: %q", packageNEVRA)
	}

	name := matches[rpm.RpmSpecBuiltRPMRegexNameIndex]
	epoch := matches[rpm.RpmSpecBuiltRPMRegexEpochIndex]
	version := matches[rpm.RpmSpecBuiltRPMRegexVersionIndex]
	release := matches[rpm.RpmSpecBuiltRPMRegexReleaseIndex]

	// Replace '-' with '_' as RPM macros cannot have '-'.
	nameMacroFormat := strings.ReplaceAll(name, "-", "_")

	epochMacroString := prefix + "_" + nameMacroFormat + "_epoch"
	versionMacroString := prefix + "_" + nameMacroFormat + "_version"
	releaseMacroString := prefix + "_" + nameMacroFormat + "_release"

	// Generate RPM macro definitions instead of modifying spec files directly.
	macros = []string{
		fmt.Sprintf("%%%s %s", versionMacroString, version),
		fmt.Sprintf("%%%s %s", releaseMacroString, release),
	}

	// Only append (to the front of the list) if we have an epoch
	if epoch != "" {
		macros = append([]string{fmt.Sprintf("%%%s %s", epochMacroString, epoch)}, macros...)
	}

	return macros, nil
}

func writeExtraFilesToOutput(extraFiles []string, macrosOutput []string, output string) (err error) {
	// If extra files were provided, append their contents to the output as well.
	for _, extraPath := range extraFiles {
		if strings.TrimSpace(extraPath) == "" {
			continue
		}

		contents, readErr := file.ReadLines(extraPath)
		if readErr != nil {
			logger.Log.Errorf("Failed to read extra macros file (%s): %s", extraPath, readErr)
			continue
		}

		macrosOutput = append(macrosOutput, contents...)
		logger.Log.Infof("Appended contents of provided extra macros file (%s) to %s", extraPath, output)
	}

	sort.Strings(macrosOutput)

	err = file.WriteLines(macrosOutput, output)
	if err != nil {
		logger.Log.Errorf("Failed to write file (%s)", output)
		return err
	}

	return nil
}
