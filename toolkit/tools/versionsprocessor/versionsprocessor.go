// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// versionsprocessor is a tool to generate a macro file of all specs version and release.
// It iterates ove all of the SPEC files in the provided directory, gets the version and release for each SPEC,
// and then writes that information to an output file as RPM macros file.\
// The output file is then provided to other tools and passed into their respective rpm macros folder so that rpmbuild command automatically recognize it.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/directory"
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
	extraFiles    = app.Flag("extra-macros-files", "Additional files whose contents will be appended to the output; may be specified multiple times.").ExistingFiles()
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

	logger.PanicOnError(err)

	var buildArch string = *targetArch

	if *targetArch == "" {
		buildArch, err = rpm.GetRpmArch(runtime.GOARCH)
		if err != nil {
			return
		}
	}

	if *workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, err = createChroot(*workerTar, *buildDir, *specsDir)
		if err != nil {
			return
		}
		defer chroot.Close(leaveFilesOnDisk)
	}

	doParse := func() error {
		// Find all spec files
		allSpecFiles, err := specreaderutils.FindSpecFiles(*specsDir, nil)
		if err != nil {
			logger.Log.Panicf("Error finding spec files: %s", err)
			return err
		}

		logger.Log.Infof("Processing version and release for %d spec files into %s", len(allSpecFiles), *output)

		// Process all specs files
		for _, specFile := range allSpecFiles {

			// Get spec file version-release

			specFileName := filepath.Base(specFile)

			sourceDir := filepath.Dir(specFile)
			defines := rpm.DefaultDistroDefines(false, *distTag)

			packages, err := rpm.QuerySPEC(specFile, sourceDir, `%{NAME}: %{evr}\n`, buildArch, defines, rpm.QueryHeaderArgument)

			if err != nil {
				logger.Log.Errorf("Failed to query spec file (%s). Error: %s", specFileName, err)
				continue
			}

			for _, packageVersionString := range packages {

				// the output of the above query is in the format of "packagename: version-release",
				// so split by ": " to get the version-release portion we want the second part
				releaseVerSplit := regexp.MustCompile(`^[^:]+: (.+)-(.+)$`).FindStringSubmatch(packageVersionString)[1:]

				if len(releaseVerSplit) != 2 {
					logger.Log.Errorf("Empty version-release format retrieved from spec file (%s)", specFileName)
					continue
				}

				version := releaseVerSplit[0]
				release := releaseVerSplit[1]
				releaseClean := strings.Replace(release, *distTag, "", 1) // targetting azl3 specifically since this won't go into above 3.0 toolkit

				// strip out the .spec suffix and replace '-' with '_' as RPM macros cannot have '-'
				specFileNameMacroFormat := strings.Replace(specFileName, ".spec", "", 1)
				specFileNameMacroFormat = strings.ReplaceAll(specFileNameMacroFormat, "-", "_")

				versionMacroString := prefix + "_" + specFileNameMacroFormat + "_version"
				releaseMacroString := prefix + "_" + specFileNameMacroFormat + "_release"

				// Generate RPM macro definitions instead of modifying spec files directly.
				macros := fmt.Sprintf("%%%s %s\n%%%s %s",
					versionMacroString, version,
					releaseMacroString, releaseClean,
				)

				macrosOutput = append(macrosOutput, macros)
			}
		}

		return err
	}

	if chroot != nil {
		err = chroot.Run(doParse)
	} else {
		err = doParse()
	}

	// If extra files were provided, append their contents to the output as well.
	for _, extraPath := range *extraFiles {
		if strings.TrimSpace(extraPath) == "" {
			continue
		}

		contents, readErr := file.Read(extraPath)
		if readErr != nil {
			logger.Log.Errorf("Failed to read extra macros file (%s): %s", extraPath, readErr)
			continue
		}

		macrosOutput = append(macrosOutput, contents)
		logger.Log.Infof("Appended contents of provided extra macros file (%s) to %s", extraPath, *output)
	}

	err = file.WriteLines(macrosOutput, *output)
	if err != nil {
		logger.Log.Errorf("Failed to write file (%s)", *output)
		return
	}
}

// createChroot creates a chroot to parse SPECs inside of.
func createChroot(workerTar, buildDir, specsDir string) (chroot *safechroot.Chroot, err error) {
	const (
		chrootName       = "versionprocessor_chroot"
		existingDir      = false
		leaveFilesOnDisk = false
	)

	// Mount the specs and srpms directories to an identical path inside the chroot.
	// Since versionsprocessor saves the full paths to specs in its output that grapher will then consume,
	// the pathing needs to be preserved from the host system.
	var extraDirectories []string

	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDir, specsDir, "", safechroot.BindMountPointFlags, ""),
	}

	chrootDir := filepath.Join(buildDir, chrootName)
	chroot = safechroot.NewChroot(chrootDir, existingDir)

	err = chroot.Initialize(workerTar, extraDirectories, extraMountPoints, true)
	if err != nil {
		return
	}

	// If this is not a regular build then copy in all of the SPECs since there are no bind mounts.
	if !buildpipeline.IsRegularBuild() {
		dirsToCopy := []string{specsDir}
		for _, dir := range dirsToCopy {
			dirInChroot := filepath.Join(chroot.RootDir(), dir)
			err = directory.CopyContents(dir, dirInChroot)
			if err != nil {
				closeErr := chroot.Close(leaveFilesOnDisk)
				if closeErr != nil {
					logger.Log.Errorf("Failed to close chroot, err: %s", err)
				}
				return
			}
		}
	}

	return
}
