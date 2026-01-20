// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	packagelist "github.com/microsoft/azurelinux/toolkit/tools/internal/packlist"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultWorkerCount    = "100"
	kernelHWESpecName     = "kernel-hwe"
	kernelHWEVerMacroName = "KERNEL_HWE_VERSION"
	kernelHWERelMacroName = "KERNEL_HWE_REL"
)

var (
	app                        = kingpin.New("kernelverprocessor", "A tool to determine dynamic kernel version")
	specsDir                   = exe.InputDirFlag(app, "Directory to scan for SPECS")
	specList                   = app.Flag("spec-list", "List of SPECs to parse. If empty will parse all SPECs.").Default("").String()
	output                     = exe.OutputFlag(app, "Output file to export the JSON")
	workers                    = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	buildDir                   = app.Flag("build-dir", "Directory to store temporary files while parsing.").String()
	srpmsDir                   = app.Flag("srpm-dir", "Directory containing SRPMs.").Required().ExistingDir()
	rpmsDir                    = app.Flag("rpm-dir", "Directory containing built RPMs.").Required().ExistingDir()
	toolchainManifest          = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").ExistingFile()
	existingToolchainRpmDir    = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	distTag                    = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	workerTar                  = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.  If this argument is empty, specs will be parsed in the host environment.").ExistingFile()
	targetArch                 = app.Flag("target-arch", "The architecture of the machine the RPM binaries run on").String()
	runCheck                   = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()
	logFlags                   = exe.SetupLogFlags(app)
	profFlags                  = exe.SetupProfileFlags(app)
	timestampFile              = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
	extraKernelVersionsToParse = []string{kernelHWESpecName}
)

func main() {
	const (
		querySrpm             = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		queryProvidedPackages = `rpm %{ARCH}/%{nvra}.rpm\n[provides %{PROVIDENEVRS}\n][requires %{REQUIRENEVRS}\n][arch %{ARCH}\n]`
	)

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("specreader", *timestampFile)
	defer timestamp.CompleteTiming()

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	// A parse list may be provided, if so only parse this subset.
	// If none is provided, parse all specs.
	specListSet, err := packagelist.ParsePackageList(*specList)
	logger.PanicOnError(err)

	// A parse list may be provided, if so only parse this subset.
	// If none is provided, parse all specs.
	kernelSpecListSet, err := packagelist.ParsePackageList(strings.Join(extraKernelVersionsToParse, " "))
	logger.PanicOnError(err)

	//err = specreaderutils.ParseSPECsWrapper(*buildDir, specsAbsDir, *rpmsDir, *srpmsDir, *existingToolchainRpmDir, *distTag, *output, *workerTar, *targetArch, specListSet, toolchainRPMs, *workers, *runCheck)

	var buildArch string = *targetArch

	if *targetArch == "" {
		buildArch, err = rpm.GetRpmArch(runtime.GOARCH)
		if err != nil {
			return
		}
	}

	kernelSpecFiles, err := specreaderutils.FindSpecFiles(*specsDir, kernelSpecListSet)
	if err != nil {
		logger.Log.Panicf("Error finding spec files: %s", err)
		return
	}

	specFiles, err := specreaderutils.FindSpecFiles(*specsDir, specListSet)
	if err != nil {
		logger.Log.Panicf("Error finding spec files: %s", err)
		return
	}

	logger.Log.Infof("Processing kernel HWE spec files: %v", kernelSpecFiles)

	// Process each kernel flavour/type
	for _, specFile := range kernelSpecFiles {

		// Get kernel version-release from spec file

		specFileName := filepath.Base(specFile)

		sourceDir := filepath.Dir(specFile)
		noCheckDefines := rpm.DefaultDistroDefines(false, *distTag)

		logger.Log.Infof("Processing kernel HWE spec files: %v %v", specFileName, sourceDir)

		versionRelease, err := rpm.QuerySPEC(specFile, sourceDir, `%{VERSION}-%{RELEASE}`, buildArch, noCheckDefines, rpm.QueryHeaderArgument)
		if err != nil {
			logger.Log.Errorf("Failed to query kernel-hwe spec file (%s). Error: %s", specFileName, err)
			continue
		}

		logger.Log.Infof("kernel-hwe version-release: %s", versionRelease)
		logger.PanicOnError(err)

		if len(versionRelease) == 0 {
			logger.Log.Errorf("Invalid version-release retrieved from kernel-hwe spec file (%s): %s", specFileName, versionRelease)
			continue
		}

		releaseVerSplit := strings.Split(versionRelease[0], "-")

		if len(releaseVerSplit) < 2 {
			logger.Log.Errorf("Invalid version-release format retrieved from kernel-hwe spec file (%s): %s", specFileName, versionRelease[0])
			continue

		}

		version := releaseVerSplit[0]
		release := releaseVerSplit[1]
		releaseClean := strings.SplitN(release, ".", 2)[0] // Includes distribution tag suffixes

		logger.Log.Infof("Processed kernel-hwe version-release: %s %s", version, release)

		// TODO: Now parse all spec files and update their kernel version/release MACRO accordingly

		for _, OOTspecFile := range specFiles {
			err = sedSPECFile(OOTspecFile, "%{"+kernelHWEVerMacroName+"}", version)

			if err != nil {
				logger.Log.Errorf("Failed to update spec file (%s) with kernel-hwe release version (%s). Error: %s", OOTspecFile, version, err)
				continue
			}

			err = sedSPECFile(OOTspecFile, "%{"+kernelHWERelMacroName+"}", releaseClean)

			if err != nil {
				logger.Log.Errorf("Failed to update spec file (%s) with kernel-hwe release version (%s). Error: %s", OOTspecFile, releaseClean, err)
				continue
			}

			logger.Log.Infof("Updated spec file (%s) with kernel-hwe release version (%s).", OOTspecFile, version)

		}
	}

}

func sedSPECFile(filePath, pattern, replacement string) error {
	expr := fmt.Sprintf("s|%s|%s|g", pattern, replacement)

	cmd := exec.Command("sed", "-i", expr, filePath)
	output, err := cmd.CombinedOutput()
	if err != nil {
		logger.Log.Errorf("sed command failed: %s; output: %s", err, string(output))
		return fmt.Errorf("sed command failed: %w; output: %s", err, string(output))
	}

	return nil
}
