// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultWorkerCount = "100"
)

var (
	app           = kingpin.New("kernelverprocessor", "A tool to determine dynamic kernel version")
	specsDir      = exe.InputDirFlag(app, "Directory to scan for SPECS")
	output        = exe.OutputFlag(app, "Output file to export the JSON")
	workers       = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	distTag       = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	targetArch    = app.Flag("target-arch", "The architecture of the machine the RPM binaries run on").String()
	logFlags      = exe.SetupLogFlags(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	const (
		querySrpm             = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		queryProvidedPackages = `rpm %{ARCH}/%{nvra}.rpm\n[provides %{PROVIDENEVRS}\n][requires %{REQUIRENEVRS}\n][arch %{ARCH}\n]`
		prefix                = "azl"
	)

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("kernelverprocessor", *timestampFile)
	defer timestamp.CompleteTiming()

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	logger.PanicOnError(err)

	var buildArch string = *targetArch

	if *targetArch == "" {
		buildArch, err = rpm.GetRpmArch(runtime.GOARCH)
		if err != nil {
			return
		}
	}

	// Find all spec files
	allSpecFiles, err := specreaderutils.FindSpecFiles(*specsDir, nil)
	if err != nil {
		logger.Log.Panicf("Error finding spec files: %s", err)
		return
	}

	logger.Log.Infof("Processing version and release for %d spec files into %s", len(allSpecFiles), *output)

	macros_output := []byte{}

	// Process each kernel flavour/type
	for _, specFile := range allSpecFiles {

		// Get kernel version-release from spec file

		specFileName := filepath.Base(specFile)

		sourceDir := filepath.Dir(specFile)
		noCheckDefines := rpm.DefaultDistroDefines(false, *distTag)

		versionRelease, err := rpm.QuerySPEC(specFile, sourceDir, `%{VERSION}-%{RELEASE}`, buildArch, noCheckDefines, rpm.QueryHeaderArgument)
		if err != nil {
			logger.Log.Errorf("Failed to query spec file (%s). Error: %s", specFileName, err)
			continue
		}

		logger.PanicOnError(err)

		if len(versionRelease) == 0 {
			logger.Log.Errorf("Invalid version-release retrieved from spec file (%s): %s", specFileName, versionRelease)
			continue
		}

		releaseVerSplit := strings.Split(versionRelease[0], "-")

		if len(releaseVerSplit) < 2 {
			logger.Log.Errorf("Invalid version-release format retrieved from spec file (%s): %s", specFileName, versionRelease[0])
			continue
		}

		version := releaseVerSplit[0]
		release := releaseVerSplit[1]
		releaseClean := strings.SplitN(release, ".", 2)[0] // Includes distribution tag suffixes

		// strip out the .spec suffix and replace '-' with '_' as RPM macros cannot have '-'
		specFileNameMacroFormat := strings.Replace(specFileName, ".spec", "", 1)
		specFileNameMacroFormat = strings.ReplaceAll(specFileNameMacroFormat, "-", "_")
		specFileNameMacroFormat = strings.ToLower(specFileNameMacroFormat)

		versionMacroString := prefix + "_" + specFileNameMacroFormat + "_version"
		releaseMacroString := prefix + "_" + specFileNameMacroFormat + "_release"

		// Generate RPM macro definitions instead of modifying spec files directly.
		macros := fmt.Sprintf("%%%s %s\n%%%s %s\n",
			versionMacroString, version,
			releaseMacroString, releaseClean,
		)

		macros_output = append(macros_output, []byte(macros)...)
	}

	err = file.Write(string(macros_output), *output)
	if err != nil {
		logger.Log.Errorf("Failed to write file (%s)", *output)
		return
	}

}
