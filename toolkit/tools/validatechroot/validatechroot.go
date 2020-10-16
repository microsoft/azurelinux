// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path"
	"regexp"
	"strings"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/safechroot"
	"microsoft.com/pkggen/internal/shell"
)

var (
	app = kingpin.New("validatechroot", "A tool to validate that the worker chroot is well configured and all dependencies are satisfied.")

	toolchainRpmsDir = app.Flag("rpm-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir           = app.Flag("tmp-dir", "Temporary chroot directory.").String()

	workerTar      = app.Flag("worker-chroot", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	workerManifest = app.Flag("worker-manifest", "Full path to the worker manifest file").Required().ExistingFile()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	leaveChrootFilesOnDisk = false
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	err := validateWorker()

	if err != nil {
		logger.Log.Fatalf("Failed to validate worker. Error: %s", err)
	}
}

func validateWorker() (err error) {
	const (
		chrootToolchainRpmsDir = "/toolchainrpms"
		isExistingDir          = false
	)

	var (
		chroot *safechroot.Chroot
		// Every valid line will be of the form: <package>-<version>.<arch>.rpm
		packageArchLookupRegex = regexp.MustCompile(`^.+(?P<arch>x86_64|aarch64|noarch)\.rpm$`)
	)

	// Ensure that if initialization fails, the chroot is closed
	defer func() {
		if chroot != nil {
			closeErr := chroot.Close(leaveChrootFilesOnDisk)
			if closeErr != nil {
				logger.Log.Panicf("Unable to close chroot on failed initialization. Error: %s", closeErr)
			}
		}
	}()

	logger.Log.Infof("Creating chroot environment to validate '%s' against '%s'", *workerTar, *workerManifest)

	chroot = safechroot.NewChroot(*tmpDir, isExistingDir)
	rpmMount := safechroot.NewMountPoint(*toolchainRpmsDir, chrootToolchainRpmsDir, "", safechroot.BindMountPointFlags, "")
	extraDirectories := []string{chrootToolchainRpmsDir}
	rpmMounts := []*safechroot.MountPoint{rpmMount}
	err = chroot.Initialize(*workerTar, extraDirectories, rpmMounts)
	if err != nil {
		chroot = nil
		return
	}

	manifestEntires, err := file.ReadLines(*workerManifest)
	badEntries := make(map[string]string)

	err = chroot.Run(func() (err error) {
		for _, rpm := range manifestEntires {
			archMatches := packageArchLookupRegex.FindStringSubmatch(rpm)
			if len(archMatches) != 2 {
				logger.Log.Errorf("%v", archMatches)
				return fmt.Errorf("'%s' is an invalid rpm file path", rpm)
			}
			arch := archMatches[1]
			rpmPath := path.Join(chrootToolchainRpmsDir, arch, rpm)

			// --replacepkgs instructs RPM to gracefully re-install a package, including checking dependencies
			args := []string{
				"-ihv",
				"--replacepkgs",
				"--nosignature",
				rpmPath,
			}
			logger.Log.Infof("Running rpm %s", strings.Join(args, " "))
			stdout, stderr, err := shell.Execute("rpm", args...)

			logger.Log.Debug(stdout)

			if err != nil || len(stderr) > 0 {
				logger.Log.Warn(stderr)
				badEntries[rpm] = stderr
			}
		}
		return
	})

	if len(badEntries) > 0 {
		for rpm, stderr := range badEntries {
			logger.Log.Errorf("%s:\n %s", rpm, stderr)
		}
		err = fmt.Errorf("found invalid packages in the worker chroot")
	}
	return
}
