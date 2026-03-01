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
	"regexp"
	"runtime"
	"strconv"
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

// packageVersionRe matches lines of the form "NAME: EPOCHNUM|VERSION-RELEASE"
// as produced by the rpm query format "%{NAME}: %{EPOCHNUM}|%{VERSION}-%{RELEASE}".
var packageVersionRe = regexp.MustCompile(`^([^:]+): (\d+)\|(.+)-(.+)$`)

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
	const (
		prefix = "azl"
	)

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
			logger.PanicOnError(err)
		}
		if err != nil {
			logger.Log.Errorf("Failed to determine RPM architecture for runtime architecture %q: %v", runtime.GOARCH, err)
		}
	}

	if *workerTar == "" {
		logger.Log.Error("No worker tar provided, parsing specs in host environment. This may cause issues if the host environment is different from the target build environment.")
		return
	}

	const leaveFilesOnDisk = false
	chroot, err = specreaderutils.CreateChroot("versionprocessor_chroot", *workerTar, *buildDir,
		specreaderutils.WithSpecsDir(*specsDir))
	if err != nil {
		logger.Log.Errorf("Failed to create chroot: %s", err)
		os.Exit(1)
	}
	defer chroot.Close(leaveFilesOnDisk)

	doParse := func() error {
		// Find all spec files
		allSpecFiles, err := specreaderutils.FindSpecFiles(*specsDir, nil)
		if err != nil {
			logger.Log.Errorf("Error finding spec files: %s", err)
			return err
		}

		logger.Log.Infof("Processing version and release for %d spec files into %s", len(allSpecFiles), *output)

		// Get spec file version-release
		for _, specFile := range allSpecFiles {
			macrosOutput, err = processSpecFile(specFile, buildArch, prefix, macrosOutput)
			if err != nil {
				return fmt.Errorf("error processing spec file (%s): %w", specFile, err)
			}
		}

		return err
	}

	if chroot != nil {
		err = chroot.Run(doParse)
	} else {
		err = doParse()
	}

	if err != nil {
		logger.Log.Errorf("Failed to generate versions macros: %s", err)
		os.Exit(1)
	}

	err = writeExtraFilesToOutput(*extraFiles, macrosOutput, *output)
	if err != nil {
		logger.Log.Errorf("Failed to write extra files to output: %s", err)
		os.Exit(1)
	}
}

func processSpecFile(specFile string, buildArch string, prefix string, macrosOutput []string) (newMacrosOutput []string, err error) {
	specFileName := filepath.Base(specFile)

	sourceDir := filepath.Dir(specFile)
	defines := rpm.DefaultDistroDefines(false, *distTag)

	packages, err := rpm.QuerySPEC(specFile, sourceDir, `%{NAME}: %{EPOCHNUM}|%{VERSION}-%{RELEASE}\n`, buildArch, defines, rpm.QueryHeaderArgument)

	if err != nil {
		logger.Log.Errorf("Failed to query spec file (%s). Error: %s", specFileName, err)
		return nil, err
	}

	for _, packageVersionString := range packages {

		packageMacros, err := processPackageVersionString(packageVersionString, specFileName, prefix)
		if err != nil {
			logger.Log.Errorf("Error processing package version string: %s", err)
			continue
		}

		macrosOutput = append(macrosOutput, packageMacros...)
	}

	return macrosOutput, nil
}

func processPackageVersionString(packageVersionString string, specFileName string, prefix string) (macros []string, err error) {
	// The output of the rpm query is in the format "NAME: EPOCHNUM|VERSION-RELEASE".
	match := packageVersionRe.FindStringSubmatch(packageVersionString)

	if len(match) != 5 {
		err = fmt.Errorf("unexpected version format retrieved from spec file (%s): %q", specFileName, packageVersionString)
		logger.Log.Errorf("%s", err)
		return nil, err
	}

	packageName := match[1]
	epochStr := match[2]
	version := match[3]
	release := match[4]

	// Remove the dist tag from the release. The release macro does not include the distro suffix
	// so that it can be compared across different distros.
	releaseClean := strings.Replace(release, *distTag, "", 1)

	// Replace '-' with '_' as RPM macros cannot contain '-'.
	packageNameMacroFormat := strings.ReplaceAll(packageName, "-", "_")

	versionMacroString := prefix + "_" + packageNameMacroFormat + "_version"
	releaseMacroString := prefix + "_" + packageNameMacroFormat + "_release"

	epochNum, convErr := strconv.Atoi(epochStr)
	if convErr == nil && epochNum > 0 {
		epochMacroString := prefix + "_" + packageNameMacroFormat + "_epoch"
		macros = append(macros, fmt.Sprintf("%%%s %s", epochMacroString, epochStr))
	}

	macros = append(macros, fmt.Sprintf("%%%s %s", versionMacroString, version))
	macros = append(macros, fmt.Sprintf("%%%s %s", releaseMacroString, releaseClean))

	return macros, nil
}

func writeExtraFilesToOutput(extraFiles []string, macrosOutput []string, output string) (err error) {
	// If extra files were provided, append their contents to the output as well.
	for _, extraPath := range extraFiles {
		if strings.TrimSpace(extraPath) == "" {
			continue
		}

		contents, readErr := file.Read(extraPath)
		if readErr != nil {
			logger.Log.Errorf("Failed to read extra macros file (%s): %s", extraPath, readErr)
			continue
		}

		macrosOutput = append(macrosOutput, contents)
		logger.Log.Infof("Appended contents of provided extra macros file (%s) to %s", extraPath, output)
	}

	err = file.WriteLines(macrosOutput, output)
	if err != nil {
		logger.Log.Errorf("Failed to write file (%s)", output)
		return err
	}

	return nil
}
