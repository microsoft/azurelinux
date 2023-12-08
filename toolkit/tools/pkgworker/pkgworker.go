// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A worker for building packages locally

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ccachemanager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repomanager/rpmrepomanager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/tdnf"
	"golang.org/x/sys/unix"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	chrootLocalRpmsDir      = "/localrpms"
	chrootLocalToolchainDir = "/toolchainrpms"
	chrootLocalRpmsCacheDir = "/upstream-cached-rpms"
	chrootCcacheDir         = "/ccache-dir"
)

var (
	app                  = kingpin.New("pkgworker", "A worker for building packages locally")
	srpmFile             = exe.InputFlag(app, "Full path to the SRPM to build")
	workDir              = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar            = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile             = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmsDirPath          = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	srpmsDirPath         = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	toolchainDirPath     = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain a top level directory for each architecture.").Required().ExistingDir()
	cacheDir             = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from CBL-Mariner Base").Required().ExistingDir()
	basePackageName      = app.Flag("base-package-name", "The name of the spec file used to build this package without the extension.").Required().String()
	noCleanup            = app.Flag("no-cleanup", "Whether or not to delete the chroot folder after the build is done").Bool()
	distTag              = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with").Required().String()
	rpmmacrosFile        = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use").ExistingFile()
	runCheck             = app.Flag("run-check", "Run the check during package build").Bool()
	packagesToInstall    = app.Flag("install-package", "Filepaths to RPM packages that should be installed before building.").Strings()
	outArch              = app.Flag("out-arch", "Architecture of resulting package").String()
	useCcache            = app.Flag("use-ccache", "Automatically install and use ccache during package builds").Bool()
	ccacheRootDir        = app.Flag("ccache-root-dir", "The directory used to store ccache outputs").String()
	ccachConfig          = app.Flag("ccache-config", "The configuration file for ccache.").String()
	maxCPU               = app.Flag("max-cpu", "Max number of CPUs used for package building").Default("").String()
	timeout              = app.Flag("timeout", "Timeout for package building").Required().Duration()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

var (
	packageUnavailableRegex = regexp.MustCompile(`^No package \\x1b\[1m\\x1b\[30m(.+) \\x1b\[0mavailable`)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	rpmsDirAbsPath, err := filepath.Abs(*rpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for RPMs directory '%s'", *rpmsDirPath)

	toolchainDirAbsPath, err := filepath.Abs(*toolchainDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for toolchain RPMs directory '%s'", *toolchainDirPath)

	srpmsDirAbsPath, err := filepath.Abs(*srpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for SRPMs directory '%s'", *srpmsDirPath)

	chrootDir := buildChrootDirPath(*workDir, *srpmFile, *runCheck)

	defines := rpm.DefaultDefinesWithDist(*runCheck, *distTag)
	defines[rpm.DistroReleaseVersionDefine] = *distroReleaseVersion
	defines[rpm.DistroBuildNumberDefine] = *distroBuildNumber
	defines[rpm.MarinerModuleLdflagsDefine] = "-Wl,-dT,%{_topdir}/BUILD/module_info.ld"

	ccacheManager, ccacheErr := ccachemanager.CreateManager(*ccacheRootDir, *ccachConfig)
	if ccacheErr == nil {
		if *useCcache {
			buildArch, ccacheErr := rpm.GetRpmArch(runtime.GOARCH)
			if ccacheErr == nil {
				ccacheErr = ccacheManager.SetCurrentPkgGroup(*basePackageName, buildArch)
				if ccacheErr == nil {
					if ccacheManager.CurrentPkgGroup.Enabled {
						defines[rpm.MarinerCCacheDefine] = "true"
					}
				} else {
					logger.Log.Warnf("Failed to set package ccache configuration:\n%v", ccacheErr)
					ccacheManager = nil
				}
			} else {
				logger.Log.Warnf("Failed to get build architecture:\n%v", ccacheErr)
				ccacheManager = nil
			}
		}
	} else {
		logger.Log.Warnf("Failed to initialize the ccache manager:\n%v", ccacheErr)
		ccacheManager = nil
	}

	if *maxCPU != "" {
		defines[rpm.MaxCPUDefine] = *maxCPU
	}

	builtRPMs, err := buildSRPMInChroot(chrootDir, rpmsDirAbsPath, toolchainDirAbsPath, *workerTar, *srpmFile, *repoFile, *rpmmacrosFile, *outArch, defines, *noCleanup, *runCheck, *packagesToInstall, ccacheManager, *timeout)
	logger.PanicOnError(err, "Failed to build SRPM '%s'. For details see log file: %s .", *srpmFile, *logFile)

	err = copySRPMToOutput(*srpmFile, srpmsDirAbsPath)
	logger.PanicOnError(err, "Failed to copy SRPM '%s' to output directory '%s'.", *srpmFile, rpmsDirAbsPath)

	// On success write a comma-seperated list of RPMs built to stdout that can be parsed by the invoker.
	// Any output from logger will be on stderr so stdout will only contain this output.
	if !*runCheck {
		fmt.Print(strings.Join(builtRPMs, ","))
	}
}

func copySRPMToOutput(srpmFilePath, srpmOutputDirPath string) (err error) {
	srpmFileName := filepath.Base(srpmFilePath)
	srpmOutputFilePath := filepath.Join(srpmOutputDirPath, srpmFileName)

	err = file.Copy(srpmFilePath, srpmOutputFilePath)

	return
}

func buildChrootDirPath(workDir, srpmFilePath string, runCheck bool) (chrootDirPath string) {
	buildDirName := strings.TrimSuffix(filepath.Base(*srpmFile), ".src.rpm")
	if runCheck {
		buildDirName += "_TEST_BUILD"
	}

	return filepath.Join(workDir, buildDirName)
}

func isCCacheEnabled(ccacheManager *ccachemanager.CCacheManager) bool {
	return ccacheManager != nil && ccacheManager.CurrentPkgGroup.Enabled
}

func buildSRPMInChroot(chrootDir, rpmDirPath, toolchainDirPath, workerTar, srpmFile, repoFile, rpmmacrosFile, outArch string, defines map[string]string, noCleanup, runCheck bool, packagesToInstall []string, ccacheManager *ccachemanager.CCacheManager, timeout time.Duration) (builtRPMs []string, err error) {

	const (
		buildHeartbeatTimeout = 30 * time.Minute

		existingChrootDir = false

		overlaySource           = ""
		overlayWorkDirRpms      = "/overlaywork_rpms"
		overlayWorkDirToolchain = "/overlaywork_toolchain"
	)

	srpmBaseName := filepath.Base(srpmFile)

	quit := make(chan bool)
	go func() {
		logger.Log.Infof("Building (%s).", srpmBaseName)

		for {
			select {
			case <-quit:
				if err == nil {
					logger.Log.Infof("Built (%s) -> %v.", srpmBaseName, builtRPMs)
				}
				return
			case <-time.After(buildHeartbeatTimeout):
				logger.Log.Infof("Heartbeat: still building (%s).", srpmBaseName)
			}
		}
	}()
	defer func() {
		quit <- true
	}()

	if isCCacheEnabled(ccacheManager) {
		ccacheErr := ccacheManager.DownloadPkgGroupCCache()
		if ccacheErr != nil {
			logger.Log.Infof("CCache will not be able to use previously generated artifacts:\n%v", ccacheErr)
		}
	}

	// Create the chroot used to build the SRPM
	chroot := safechroot.NewChroot(chrootDir, existingChrootDir)

	outRpmsOverlayMount, outRpmsOverlayExtraDirs := safechroot.NewOverlayMountPoint(chroot.RootDir(), overlaySource, chrootLocalRpmsDir, rpmDirPath, chrootLocalRpmsDir, overlayWorkDirRpms)
	toolchainRpmsOverlayMount, toolchainRpmsOverlayExtraDirs := safechroot.NewOverlayMountPoint(chroot.RootDir(), overlaySource, chrootLocalToolchainDir, toolchainDirPath, chrootLocalToolchainDir, overlayWorkDirToolchain)
	rpmCacheMount := safechroot.NewMountPoint(*cacheDir, chrootLocalRpmsCacheDir, "", safechroot.BindMountPointFlags, "")
	mountPoints := []*safechroot.MountPoint{outRpmsOverlayMount, toolchainRpmsOverlayMount, rpmCacheMount}
	extraDirs := append(outRpmsOverlayExtraDirs, chrootLocalRpmsCacheDir)
	extraDirs = append(extraDirs, toolchainRpmsOverlayExtraDirs...)
	if isCCacheEnabled(ccacheManager) {
		ccacheMount := safechroot.NewMountPoint(ccacheManager.CurrentPkgGroup.CCacheDir, chrootCcacheDir, "", safechroot.BindMountPointFlags, "")
		mountPoints = append(mountPoints, ccacheMount)
		// need to update extraDirs with ccache specific folders to be created
		// inside the container.
		extraDirs = append(extraDirs, chrootCcacheDir)
	}

	err = chroot.Initialize(workerTar, extraDirs, mountPoints)
	if err != nil {
		return
	}
	defer chroot.Close(noCleanup)

	// Place extra files that will be needed to build into the chroot
	srpmFileInChroot, err := copyFilesIntoChroot(chroot, srpmFile, repoFile, rpmmacrosFile, runCheck)
	if err != nil {
		return
	}

	// Run the build in a go routine so we can monitor and kill it if it takes too long.
	results := make(chan error)
	go func() {
		buildErr := chroot.Run(func() (err error) {
			return buildRPMFromSRPMInChroot(srpmFileInChroot, outArch, runCheck, defines, packagesToInstall, isCCacheEnabled(ccacheManager))
		})
		results <- buildErr
	}()

	select {
	case err = <-results:
	case <-time.After(timeout):
		logger.Log.Errorf("Timeout after %v: killing all processes in chroot...", timeout)
		shell.PermanentlyStopAllChildProcesses(unix.SIGKILL)
		err = fmt.Errorf("build timed out after %s", timeout)
	}

	if err != nil {
		return
	}

	if !runCheck {
		builtRPMs, err = moveBuiltRPMs(chroot.RootDir(), rpmDirPath)
	}

	// Only if the groupSize is 1 we can archive since no other packages will
	// re-update this cache.
	if isCCacheEnabled(ccacheManager) && ccacheManager.CurrentPkgGroup.Size == 1 {
		ccacheErr := ccacheManager.UploadPkgGroupCCache()
		if ccacheErr != nil {
			logger.Log.Warnf("Unable to upload ccache archive:\n%v", ccacheErr)
		}
	}

	return
}

func buildRPMFromSRPMInChroot(srpmFile, outArch string, runCheck bool, defines map[string]string, packagesToInstall []string, useCcache bool) (err error) {

	// Convert /localrpms into a repository that a package manager can use.
	err = rpmrepomanager.CreateRepo(chrootLocalRpmsDir)
	if err != nil {
		return
	}

	// Convert /toolchainrpms into a repository that a package manager can use.
	err = rpmrepomanager.CreateRepo(chrootLocalToolchainDir)
	if err != nil {
		return
	}

	// install any additional packages, such as build dependencies.
	err = tdnfInstall(packagesToInstall)
	if err != nil {
		return
	}

	if useCcache {
		ccachePkgName := []string{"ccache"}
		logger.Log.Infof("USE_CCACHE: installing package: %s", ccachePkgName[0])
		err = tdnfInstall(ccachePkgName)
		if err != nil {
			return
		}
	}

	// Remove all libarchive files on the system before issuing a build.
	// If the build environment has libtool archive files present, gnu configure
	// could detect it and create more libtool archive files which can cause
	// build failures.
	err = removeLibArchivesFromSystem()
	if err != nil {
		return
	}

	// Build the SRPM
	if runCheck {
		err = rpm.TestRPMFromSRPM(srpmFile, outArch, defines)
	} else {
		err = rpm.BuildRPMFromSRPM(srpmFile, outArch, defines)
	}

	return
}

func moveBuiltRPMs(chrootRootDir, dstDir string) (builtRPMs []string, err error) {
	const (
		chrootRpmBuildDir = "/usr/src/mariner/RPMS"
		rpmExtension      = ".rpm"
	)

	rpmOutDir := filepath.Join(chrootRootDir, chrootRpmBuildDir)
	err = filepath.Walk(rpmOutDir, func(path string, info os.FileInfo, fileErr error) (err error) {
		if fileErr != nil {
			return fileErr
		}

		// Only copy regular files (not unix sockets, directories, links, ...)
		if !info.Mode().IsRegular() {
			return
		}

		if !strings.HasSuffix(path, rpmExtension) {
			return
		}

		// Get the relative path of the RPM, this will include the architecture directory it lives in.
		// Then join the relative path to the destination directory, this will ensure the RPM gets placed
		// in its correct architecture directory.
		relPath, err := filepath.Rel(rpmOutDir, path)
		if err != nil {
			return
		}

		dstFile := filepath.Join(dstDir, relPath)
		err = file.Move(path, dstFile)
		if err != nil {
			return
		}

		builtRPMs = append(builtRPMs, dstFile)
		return
	})

	return
}

func tdnfInstall(packages []string) (err error) {
	const (
		alreadyInstalledPostfix = "is already installed"
		noMatchingPackagesErr   = "Error(1011) : No matching packages"
		packageMatchGroup       = 1
	)

	var (
		releaseverCliArg string
	)

	if len(packages) == 0 {
		return
	}

	// TDNF supports requesting versioned packages in the form of {name}-{version}.{dist}.{arch}.
	// The packages to install list may contain file paths to rpm files so those will need to be filtered:
	// - Strip any .rpm from packages as TDNF does not support requesting a package with the extension.
	// - Strip any filepath from packages.
	for i := range packages {
		packages[i] = filepath.Base(strings.TrimSuffix(packages[i], ".rpm"))
	}

	releaseverCliArg, err = tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	installArgs := []string{"install", "-y", releaseverCliArg}
	installArgs = append(installArgs, packages...)
	stdout, stderr, err := shell.Execute("tdnf", installArgs...)
	foundNoMatchingPackages := false

	if err != nil {
		logger.Log.Warnf("Failed to install build requirements. stderr: %s\nstdout: %s", stderr, stdout)
		// TDNF will output an error if all packages are already installed.
		// Ignore it iff there is no other error present in stderr.
		splitStderr := strings.Split(stderr, "\n")
		for _, line := range splitStderr {
			trimmedLine := strings.TrimSpace(line)
			if trimmedLine == "" {
				continue
			}

			if strings.Contains(trimmedLine, noMatchingPackagesErr) {
				foundNoMatchingPackages = true
			}

			if !strings.HasSuffix(trimmedLine, alreadyInstalledPostfix) && trimmedLine != noMatchingPackagesErr {
				err = fmt.Errorf(trimmedLine)
				return
			}
		}
		err = nil
	}

	// TDNF will ignore unavailable packages that have been requested to be installed without reporting an error code.
	// Search the stdout of TDNF for such a failure and warn the user.
	// This may happen if a SPEC requires the the path to a tool (e.g. /bin/cp), so mark it as a warning for now.
	var failedToInstall []string
	splitStdout := strings.Split(stdout, "\n")
	for _, line := range splitStdout {
		trimmedLine := strings.TrimSpace(line)
		matches := packageUnavailableRegex.FindStringSubmatch(trimmedLine)
		if len(matches) == 0 {
			continue
		}

		failedToInstall = append(failedToInstall, matches[packageMatchGroup])
	}

	// TDNF will output the error "Error(1011) : No matching packages" if all packages could not be found.
	// In this case it will not print any of the individual packages that failed.
	if foundNoMatchingPackages && len(failedToInstall) == 0 {
		failedToInstall = packages
	}

	if len(failedToInstall) != 0 {
		err = fmt.Errorf("unable to install the following packages: %v", failedToInstall)
	}

	return
}

// removeLibArchivesFromSystem removes all libarchive files on the system. If
// the build environment has libtool archive files present, gnu configure could
// detect it and create more libtool archive files which can cause build failures.
func removeLibArchivesFromSystem() (err error) {
	dirsToExclude := []string{"/proc", "/dev", "/sys", "/run", "/ccache-dir"}

	err = filepath.Walk("/", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip directories that are meant for device files and kernel virtual filesystems.
		// These will not contain .la files and are mounted into the safechroot from the host.
		// Also skip /ccache-dir, which is shared between chroots
		if info.IsDir() && sliceutils.Contains(dirsToExclude, path, sliceutils.StringMatch) {
			return filepath.SkipDir
		}

		if strings.HasSuffix(info.Name(), ".la") {
			return os.Remove(path)
		}

		return nil
	})

	if err != nil {
		logger.Log.Warnf("Unable to remove lib archive file: %s", err)
	}

	return
}

// copyFilesIntoChroot copies several required build specific files into the chroot.
func copyFilesIntoChroot(chroot *safechroot.Chroot, srpmFile, repoFile, rpmmacrosFile string, runCheck bool) (srpmFileInChroot string, err error) {
	const (
		chrootRepoDestDir = "/etc/yum.repos.d"
		chrootSrpmDestDir = "/root/SRPMS"
		resolvFilePath    = "/etc/resolv.conf"
		rpmmacrosDest     = "/usr/lib/rpm/macros.d/macros.override"
	)

	repoFileInChroot := filepath.Join(chrootRepoDestDir, filepath.Base(repoFile))
	srpmFileInChroot = filepath.Join(chrootSrpmDestDir, filepath.Base(srpmFile))

	filesToCopy := []safechroot.FileToCopy{
		safechroot.FileToCopy{
			Src:  repoFile,
			Dest: repoFileInChroot,
		},
		safechroot.FileToCopy{
			Src:  srpmFile,
			Dest: srpmFileInChroot,
		},
	}

	if rpmmacrosFile != "" {
		rpmmacrosCopy := safechroot.FileToCopy{
			Src:  rpmmacrosFile,
			Dest: rpmmacrosDest,
		}
		filesToCopy = append(filesToCopy, rpmmacrosCopy)
	}

	if runCheck {
		logger.Log.Debug("Enabling network access because we're running package tests.")

		resolvFileCopy := safechroot.FileToCopy{
			Src:  resolvFilePath,
			Dest: resolvFilePath,
		}
		filesToCopy = append(filesToCopy, resolvFileCopy)
	}

	err = chroot.AddFiles(filesToCopy...)
	return
}
