// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpmrepocloner

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repomanager/rpmrepomanager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/tdnf"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

const (
	RepoFlagDefaults = uint64(1) << iota
	RepoFlagDownloadedCache
	RepoFlagLocalBuilds
	RepoFlagPreview
	RepoFlagToolchain
	RepoFlagUpstream
	RepoFlagAll = RepoFlagToolchain | RepoFlagLocalBuilds | RepoFlagDownloadedCache | RepoFlagPreview | RepoFlagDefaults | RepoFlagUpstream
)

const (
	chrootCloneDirContainer = "/upstream-cached-rpms"
	chrootCloneDirRegular   = "/outputrpms"

	repoIDAll            = "*"
	repoIDBuilt          = "local-repo"
	repoIDCacheContainer = "upstream-cache-repo"
	repoIDCacheRegular   = "fetcher-cloned-repo"
	repoIDPreview        = "mariner-preview"
	repoIDToolchain      = "toolchain-repo"
)

var (
	// Every valid line pair will be of the form:
	//		<package>-<version>.<arch> : <Description>
	//		Repo	: [repo_name]
	//
	// NOTE: we ignore packages installed in the build environment denoted by "Repo	: @System".
	packageLookupNameMatchRegex = regexp.MustCompile(`([^:\s]+(x86_64|aarch64|noarch))\s*:[^\n]*\nRepo\s+:\s+[^@]`)
	packageNameIndex            = 1

	// Every line containing a repo ID will be of the form:
	//		[<repo_name>]
	// For:
	//
	//		[fetcher-cloned-repo]
	//
	// We'd get:
	//   - repo_name:    fetcher-cloned-repo
	//
	// The non-capturing groups are used to ignore the brackets.
	repoIDRegex = regexp.MustCompile(`(?:\[)([^]]+)(?:\])`)
	repoIDIndex = 1

	// Every valid line will be of the form: <package_name>.<architecture> <version>.<dist> <repo_id>
	// For:
	//
	//		COOL_package2-extended++.aarch64	1.1b.8_X-22~rc1.cm1		fetcher-cloned-repo
	//
	// We'd get:
	//   - package_name:    COOL_package2-extended++
	//   - architecture:    aarch64
	//   - version:         1.1b.8_X-22~rc1
	//   - dist:            cm1
	listedPackageRegex = regexp.MustCompile(`^\s*([[:alnum:]_.+-]+)\.([[:alnum:]_+-]+)\s+([[:alnum:]._+~-]+)\.([[:alpha:]]+[[:digit:]]+)`)
)

const (
	listMatchSubString = iota
	listPackageName    = iota
	listPackageArch    = iota
	listPackageVersion = iota
	listPackageDist    = iota
	listMaxMatchLen    = iota
)

// RpmRepoCloner represents an RPM repository cloner.
type RpmRepoCloner struct {
	chroot          *safechroot.Chroot
	chrootCloneDir  string
	defaultRepoIDs  []string
	externalRepoIDs map[string]bool
	mountedCloneDir string
	repoIDCache     string
	reposArgsList   [][]string
	reposFlags      uint64
}

// ConstructCloner constructs a new RpmRepoCloner.
//   - destinationDir is the directory to save RPMs
//   - tmpDir is the directory to create a chroot
//   - workerTar is the path to the worker tar used to seed the chroot
//   - existingRpmsDir is the directory with prebuilt RPMs
//   - prebuiltRpmsDir is the directory with toolchain RPMs
//   - tlsCert is the path to the TLS certificate, "" if not needed
//   - tlsKey is the path to the TLS key, "" if not needed
//   - repoDefinitions is a list of repo files to use
func ConstructCloner(destinationDir, tmpDir, workerTar, existingRpmsDir, toolchainRpmsDir, tlsCert, tlsKey string, repoDefinitions []string) (r *RpmRepoCloner, err error) {
	timestamp.StartEvent("initialize and configure cloner", nil)
	defer timestamp.StopEvent(nil) // initialize and configure cloner

	r = &RpmRepoCloner{}
	err = r.initialize(destinationDir, tmpDir, workerTar, existingRpmsDir, toolchainRpmsDir, repoDefinitions)
	if err != nil {
		err = fmt.Errorf("failed to prep new rpm cloner:\n%w", err)
	}

	tlsKey, tlsCert = strings.TrimSpace(tlsKey), strings.TrimSpace(tlsCert)
	err = r.addNetworkFiles(tlsCert, tlsKey)
	if err != nil {
		err = fmt.Errorf("failed to customize RPM repo cloner. Error:\n%w", err)
		return
	}

	return
}

// Clone clones the provided list of packages.
// If cloneDeps is set, package dependencies will also be cloned.
// It will automatically resolve packages that describe a provide or file from a package.
// The cloner will mark any package that locally built by setting preBuilt = true
func (r *RpmRepoCloner) Clone(cloneDeps bool, packagesToClone ...*pkgjson.PackageVer) (preBuilt bool, err error) {
	const maxBatchSize = 50

	timestamp.StartEvent("cloning packages", nil)
	defer timestamp.StopEvent(nil)

	if len(packagesToClone) == 0 {
		logger.Log.Debug("No packages to clone.")
		return
	}

	packageNames := make([]string, len(packagesToClone))
	index := 0
	for _, pkg := range packagesToClone {
		packageNames[index] = convertPackageVersionToTdnfArg(pkg)
		index++
	}

	depsSwitch := "--nodeps"
	if cloneDeps {
		depsSwitch = "--alldeps"
	}

	constantArgs := []string{
		"install",
		"-y",
		depsSwitch,
		"--downloadonly",
		"--downloaddir",
		r.chrootCloneDir,
	}

	// Setting install root to a temp directory to prevent TDNF
	// from skipping over packages already installed in the chroot.
	// The 'reinstall' command doesn't support the '--nodeps' flag.

	packagesCount := len(packageNames)
	logger.Log.Debugf("Will clone in total %d packages.", packagesCount)

	for i := 0; i < packagesCount; i += maxBatchSize {
		batchEndIndex := i + maxBatchSize
		if batchEndIndex > packagesCount {
			batchEndIndex = packagesCount
		}

		currentPackageNames := packageNames[i:batchEndIndex]

		finalArgs := make([]string, len(constantArgs)+len(currentPackageNames))
		finalArgs = append(constantArgs, currentPackageNames...)

		logger.Log.Debugf("Cloning batch %d to %d: %v", i, batchEndIndex, currentPackageNames)
		err = r.chroot.Run(func() (err error) {
			var chrootErr error
			// Consider the toolchain RPMs first, then built RPMs, then the already cached, and finally all remote packages.
			preBuilt, chrootErr = r.clonePackage(finalArgs)
			return chrootErr
		})

		if err != nil {
			return
		}
	}

	return
}

// CloneDirectory returns the directory where cloned packages are saved.
func (r *RpmRepoCloner) CloneDirectory() string {
	return r.mountedCloneDir
}

// ClonedRepoContents returns the non-local, downloaded packages.
// This includes the toolchain packages along with other packages downloaded from the upstream repositories.
func (r *RpmRepoCloner) ClonedRepoContents() (repoContents *repocloner.RepoContents, err error) {
	releaseverCliArg, err := tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	// We may hit duplicates between the toolchain packages and the other upstream ones
	// and we don't want to list them twice.
	foundPackages := map[string]bool{}
	repoContents = &repocloner.RepoContents{}
	onStdout := func(args ...interface{}) {
		if len(args) == 0 {
			return
		}

		line := args[0].(string)
		matches := listedPackageRegex.FindStringSubmatch(line)
		if len(matches) != listMaxMatchLen {
			return
		}

		pkg := &repocloner.RepoPackage{
			Name:         matches[listPackageName],
			Version:      matches[listPackageVersion],
			Architecture: matches[listPackageArch],
			Distribution: matches[listPackageDist],
		}

		pkgID := pkg.ID()
		if foundPackages[pkgID] {
			logger.Log.Debugf("Skipping duplicate package: %s", line)
			return
		}
		foundPackages[pkgID] = true

		logger.Log.Debugf("Found package: %s", line)

		repoContents.Repo = append(repoContents.Repo, pkg)
	}

	// We only enable the cache repo, but TDNF will also always list the '@System' packages.
	err = r.chroot.Run(func() (err error) {
		tdnfArgs := []string{
			"list",
			"ALL",
			fmt.Sprintf("--disablerepo=%s", repoIDAll),
			fmt.Sprintf("--enablerepo=%s", r.repoIDCache),
			releaseverCliArg,
		}

		return shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, true, "tdnf", tdnfArgs...)
	})

	return
}

// Close closes the given RpmRepoCloner.
func (r *RpmRepoCloner) Close() error {
	const leaveChrootFilesOnDisk = false
	return r.chroot.Close(leaveChrootFilesOnDisk)
}

// ConvertDownloadedPackagesIntoRepo initializes the downloaded RPMs into an RPM repository.
// Packages will be placed in a flat directory.
func (r *RpmRepoCloner) ConvertDownloadedPackagesIntoRepo() (err error) {
	logger.Log.Info("Configuring downloaded RPMs as a local repository")
	timestamp.StartEvent("covert packages to repo", nil)
	defer timestamp.StopEvent(nil)

	err = r.initializeMountedChrootRepo(chrootCloneDirRegular)
	if err != nil {
		return
	}

	repoDir := filepath.Join(r.chroot.RootDir(), r.chrootCloneDir)

	// Print warnings for any invalid RPMs
	err = rpmrepomanager.ValidateRpmPaths(repoDir)
	if err != nil {
		logger.Log.Warnf("Failed to validate RPM paths: %s", err)
		// We treat this as just a warning, not a real error.
		err = nil
	}

	if !buildpipeline.IsRegularBuild() {
		// Docker based build doesn't use overlay so cache repo
		// must be explicitly initialized
		err = r.initializeMountedChrootRepo(chrootCloneDirContainer)
	}

	return
}

func (r *RpmRepoCloner) GetEnabledRepos() uint64 {
	return r.reposFlags
}

// SetEnabledRepos tells the cloner which repos it is allowed to use for its queries.
func (r *RpmRepoCloner) SetEnabledRepos(repoFlags uint64) {
	r.reposFlags = repoFlags
	r.reposArgsList = [][]string{}
	previousReposList := []string{fmt.Sprintf("--disablerepo=%s", repoIDAll)}

	defer func() {
		logger.Log.Debugf("Enabled repos: %v.", r.reposArgsList)
	}()

	if RepoFlagToolchain&repoFlags != 0 {
		previousReposList = append(previousReposList, fmt.Sprintf("--enablerepo=%s", repoIDToolchain))
		r.reposArgsList = append(r.reposArgsList, previousReposList)
	}

	if RepoFlagLocalBuilds&repoFlags != 0 {
		previousReposList = append(previousReposList, fmt.Sprintf("--enablerepo=%s", repoIDBuilt))
		r.reposArgsList = append(r.reposArgsList, previousReposList)
	}

	if RepoFlagDownloadedCache&repoFlags != 0 {
		previousReposList = append(previousReposList, fmt.Sprintf("--enablerepo=%s", r.repoIDCache))
		r.reposArgsList = append(r.reposArgsList, previousReposList)
	}

	// Options past this point are only valid if upstream repos are enabled.
	if RepoFlagUpstream&repoFlags == 0 {
		return
	}

	previousReposList = append(previousReposList, fmt.Sprintf("--enablerepo=%s", repoIDAll))

	if RepoFlagPreview&repoFlags == 0 {
		previousReposList = append(previousReposList, fmt.Sprintf("--disablerepo=%s", repoIDPreview))
		r.reposArgsList = append(r.reposArgsList, previousReposList)
	}

	if RepoFlagDefaults&repoFlags == 0 {
		previousReposList = append(previousReposList, r.buildDisabledDefaultReposArgs()...)
		r.reposArgsList = append(r.reposArgsList, previousReposList)
	}
}

// WhatProvides attempts to find packages which provide the requested PackageVer.
func (r *RpmRepoCloner) WhatProvides(pkgVer *pkgjson.PackageVer) (packageNames []string, err error) {
	var (
		releaseverCliArg string
	)

	releaseverCliArg, err = tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	provideQuery := convertPackageVersionToTdnfArg(pkgVer)

	baseArgs := []string{
		"provides",
		provideQuery,
		releaseverCliArg,
	}

	// Consider the built (tooolchain, local) RPMs first, then the already cached, and finally all remote packages.
	for _, reposList := range r.reposArgsList {
		logger.Log.Debugf("Using repo args: %v", reposList)

		err = r.chroot.Run(func() (err error) {
			completeArgs := append(baseArgs, reposList...)

			stdout, stderr, err := shell.Execute("tdnf", completeArgs...)
			logger.Log.Debugf("tdnf search for provide '%s':\n%s", pkgVer.Name, stdout)

			if err != nil {
				logger.Log.Debugf("Failed to lookup provide '%s', tdnf error: '%s'", pkgVer.Name, stderr)
				return
			}

			// MUST keep order of packages printed by TDNF.
			// TDNF will print the packages starting from the highest version, which allows us to work around an RPM bug:
			// https://github.com/rpm-software-management/rpm/issues/2359
			for _, matches := range packageLookupNameMatchRegex.FindAllStringSubmatch(stdout, -1) {
				packageName := matches[packageNameIndex]
				packageNames = append(packageNames, packageName)
				logger.Log.Debugf("'%s' is available from package '%s'", pkgVer.Name, packageName)
			}

			return
		})
		if err != nil {
			return
		}

		if len(packageNames) > 0 {
			logger.Log.Debug("Found required package(s), skipping further search in other repos.")
			break
		}
	}

	if len(packageNames) == 0 {
		err = fmt.Errorf("could not resolve %s", pkgVer.Name)
		return
	}

	logger.Log.Debugf("Translated '%s' to package(s): %s", pkgVer.Name, strings.Join(packageNames, " "))
	return
}

// addNetworkFiles adds files needed for networking capabilities into the cloner.
// tlsClientCert and tlsClientKey are optional.
func (r *RpmRepoCloner) addNetworkFiles(tlsClientCert, tlsClientKey string) (err error) {
	files := []safechroot.FileToCopy{
		{Src: "/etc/resolv.conf", Dest: "/etc/resolv.conf"},
	}

	if tlsClientCert != "" && tlsClientKey != "" {
		tlsFiles := []safechroot.FileToCopy{
			{Src: tlsClientCert, Dest: "/etc/tdnf/mariner_user.crt"},
			{Src: tlsClientKey, Dest: "/etc/tdnf/mariner_user.key"},
		}

		files = append(files, tlsFiles...)
	}

	err = r.chroot.AddFiles(files...)
	return
}

func (r *RpmRepoCloner) buildDisabledDefaultReposArgs() (args []string) {
	args = make([]string, len(r.defaultRepoIDs))
	for i, repoID := range r.defaultRepoIDs {
		args[i] = fmt.Sprintf("--disablerepo=%s", repoID)
	}

	return
}

// clonePackage clones a given package using pre-populated arguments.
// It will gradually enable more repos to consider until the package is found.
func (r *RpmRepoCloner) clonePackage(baseArgs []string) (preBuilt bool, err error) {
	const (
		unresolvedOutputPrefix  = "No package"
		toyboxConflictsPrefix   = "toybox conflicts"
		unresolvedOutputPostfix = "available"
	)

	releaseverCliArg, err := tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	baseArgs = append(baseArgs, releaseverCliArg)

	for _, reposArgs := range r.reposArgsList {
		logger.Log.Debugf("Using repo args: %s", reposArgs)

		finalArgs := append(baseArgs, reposArgs...)

		var (
			stdout string
			stderr string
		)
		stdout, stderr, err = shell.Execute("tdnf", finalArgs...)

		logger.Log.Debugf("stdout: %s", stdout)
		logger.Log.Debugf("stderr: %s", stderr)

		if err != nil {
			logger.Log.Debugf("tdnf error (will continue if the only errors are toybox conflicts):\n '%s'", stderr)
		}

		// ============== TDNF SPECIFIC IMPLEMENTATION ==============
		// Check if TDNF could not resolve a given package. If TDNF does not find a requested package,
		// it will not error. Instead it will print a message to stdout. Check for this message.
		//
		// *NOTE*: TDNF will attempt best effort. If N packages are requested, and 1 cannot be found,
		// it will still download N-1 packages while also printing the message.
		splitStdout := strings.Split(stdout, "\n")
		for _, line := range splitStdout {
			trimmedLine := strings.TrimSpace(line)
			// Toybox conflicts are a known issue, reset the err value if encountered
			if strings.HasPrefix(trimmedLine, toyboxConflictsPrefix) {
				logger.Log.Warn("Ignoring known toybox conflict")
				err = nil
				continue
			}
			// If a package was not available, update err
			if strings.HasPrefix(trimmedLine, unresolvedOutputPrefix) && strings.HasSuffix(trimmedLine, unresolvedOutputPostfix) {
				err = fmt.Errorf(trimmedLine)
				break
			}
		}

		if err == nil {
			preBuilt = r.reposArgsUseOnlyLocalSources(reposArgs)
			break
		}
	}

	return
}

func convertPackageVersionToTdnfArg(pkgVer *pkgjson.PackageVer) (tdnfArg string) {
	tdnfArg = pkgVer.Name

	// TDNF does not accept versioning information on implicit provides.
	if pkgVer.IsImplicitPackage() {
		if pkgVer.Condition != "" {
			logger.Log.Warnf("Discarding version constraint for implicit package: %v", pkgVer)
		}
		return
	}

	// To avoid significant overhead we only download the latest version of a package
	// for ">" and ">=" constraints (ie remove constraints).
	switch pkgVer.Condition {
	case "":
	case "=":
		tdnfArg = fmt.Sprintf("%s-%s", pkgVer.Name, pkgVer.Version)
	case "<=", "<":
		tdnfArg = fmt.Sprintf("%s %s %s", pkgVer.Name, pkgVer.Condition, pkgVer.Version)
	case ">", ">=":
		logger.Log.Warnf("Discarding '%s' version constraint for: %v", pkgVer.Condition, pkgVer)
	default:
		logger.Log.Errorf("Unsupported version constraint: %s", pkgVer.Condition)
	}

	return
}

// initializeMountedChrootRepo will initialize a local RPM repository inside the chroot.
func (r *RpmRepoCloner) initializeMountedChrootRepo(repoDir string) (err error) {
	return r.chroot.Run(func() (err error) {
		err = os.MkdirAll(repoDir, os.ModePerm)
		if err != nil {
			logger.Log.Errorf("Failed to create repo directory '%s'.", repoDir)
			return
		}
		err = rpmrepomanager.CreateRepo(repoDir)
		if err != nil {
			logger.Log.Errorf("Failed to create an RPM repository under '%s'.", repoDir)
			return
		}

		return r.refreshPackagesCache()
	})
}

// initialize initializes rpmrepocloner, enabling Clone() to be called.
//   - destinationDir is the directory to save RPMs
//   - tmpDir is the directory to create a chroot
//   - workerTar is the path to the worker tar used to seed the chroot
//   - existingRpmsDir is the directory with prebuilt RPMs
//   - prebuiltRpmsDir is the directory with toolchain RPMs
//   - repoDefinitions is a list of repo files to use when cloning RPMs
func (r *RpmRepoCloner) initialize(destinationDir, tmpDir, workerTar, existingRpmsDir, toolchainRpmsDir string, repoDefinitions []string) (err error) {
	const (
		isExistingDir          = false
		leaveChrootFilesOnDisk = false

		bindFsType = ""
		bindData   = ""

		chrootLocalRpmsDir      = "/localrpms"
		chrootLocalToolchainDir = "/toolchainrpms"

		overlaySource                  = "overlay"
		overlayUpperDirectoryRpms      = "/overlaywork/upper_rpms"
		overlayWorkDirectoryRpms       = "/overlaywork/workdir_rpms"
		overlayUpperDirectoryToolchain = "/overlaywork/upper_toolchain"
		overlayWorkDirectoryToolchain  = "/overlaywork/workdir_toolchain"
	)

	// Ensure that if initialization fails, the chroot is closed
	defer func() {
		if err != nil {
			logger.Log.Warnf("Failed to initialize cloner. Error: %s", err)
			if r.chroot != nil {
				closeErr := r.chroot.Close(leaveChrootFilesOnDisk)
				if closeErr != nil {
					logger.Log.Panicf("Unable to close chroot on failed initialization. Error: %s", closeErr)
				}
			}
		}
	}()

	// Create the directory to download into
	err = os.MkdirAll(destinationDir, os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Could not create download directory (%s)", destinationDir)
		return
	}

	// Setup the chroot
	logger.Log.Infof("Creating cloning environment to populate (%s)", destinationDir)
	r.chroot = safechroot.NewChroot(tmpDir, isExistingDir)

	r.mountedCloneDir = destinationDir

	// Setup mount points for the chroot.
	//
	// 1) Mount the provided directory of existing RPMs into the chroot as an overlay,
	// ensuring the chroot can read the files, but not alter the actual directory outside
	// the chroot.
	//
	// 2) Mount the directory to download RPMs into as a bind, allowing the chroot to write
	// files into it.
	outRpmsOverlayMount, overlayExtraDirs := safechroot.NewOverlayMountPoint(r.chroot.RootDir(), overlaySource, chrootLocalRpmsDir, existingRpmsDir, overlayUpperDirectoryRpms, overlayWorkDirectoryRpms)
	extraMountPoints := []*safechroot.MountPoint{
		outRpmsOverlayMount,
		safechroot.NewMountPoint(destinationDir, chrootCloneDirRegular, bindFsType, safechroot.BindMountPointFlags, bindData),
	}

	// Include the special toolchain packages directory.
	toolchainRpmsOverlayMount, toolchainRpmsOverlayExtraDirs := safechroot.NewOverlayMountPoint(r.chroot.RootDir(), overlaySource, chrootLocalToolchainDir, toolchainRpmsDir, overlayUpperDirectoryToolchain, overlayWorkDirectoryToolchain)
	extraMountPoints = append(extraMountPoints, toolchainRpmsOverlayMount)
	overlayExtraDirs = append(overlayExtraDirs, toolchainRpmsOverlayExtraDirs...)

	// Also request that /overlaywork is created before any chroot mounts happen so the overlay can
	// be created successfully
	err = r.chroot.Initialize(workerTar, overlayExtraDirs, extraMountPoints)
	if err != nil {
		r.chroot = nil
		return
	}

	// The 'cacheRepoDir' repo is only used during Docker based builds, which don't
	// use overlay so cache repo must be explicitly initialized.
	// We make sure it's present during all builds to avoid noisy TDNF error messages in the logs.
	reposToInitialize := []string{chrootLocalRpmsDir, chrootCloneDirRegular, chrootCloneDirContainer, chrootLocalToolchainDir}
	for _, repoToInitialize := range reposToInitialize {
		logger.Log.Debugf("Initializing the '%s' repository.", repoToInitialize)
		err = r.initializeMountedChrootRepo(repoToInitialize)
		if err != nil {
			logger.Log.Errorf("Failed while trying to initialize the '%s' repository.", repoToInitialize)
			return
		}
	}

	logger.Log.Info("Initializing repository configurations")
	err = r.initializeRepoDefinitions(repoDefinitions)
	if err != nil {
		return
	}

	r.SetEnabledRepos(RepoFlagAll)

	// Docker-based build doesn't use overlay so repo folder
	// must be explicitly set to the RPMs cache folder.
	r.chrootCloneDir = chrootCloneDirContainer
	r.repoIDCache = repoIDCacheContainer
	if buildpipeline.IsRegularBuild() {
		r.chrootCloneDir = chrootCloneDirRegular
		r.repoIDCache = repoIDCacheRegular
	}

	r.externalRepoIDs = map[string]bool{
		r.repoIDCache: true,
		repoIDAll:     true,
	}

	return
}

// initializeRepoDefinitions will configure the chroot's repo files to match those
// provided by the caller.
func (r *RpmRepoCloner) initializeRepoDefinitions(repoDefinitions []string) (err error) {
	// ============== TDNF SPECIFIC IMPLEMENTATION ==============
	// Unlike some other package managers, TDNF has no notion of repository priority.
	// It reads the repo files using `readdir`, which should be assumed to be random ordering.
	//
	// In order to simulate repository priority, concatenate all requested repofiles into a single file.
	// TDNF will read the file top-down. It will then parse the results into a linked list, meaning
	// the first repo entry in the file is the first to be checked.
	const (
		chrootRepoDir  = "/etc/yum.repos.d/"
		chrootRepoFile = "allrepos.repo"
	)

	fullRepoDirPath := filepath.Join(r.chroot.RootDir(), chrootRepoDir)
	fullRepoFilePath := filepath.Join(fullRepoDirPath, chrootRepoFile)

	// Create the directory for the repo file in case there wasn't already one there
	err = os.MkdirAll(filepath.Dir(fullRepoFilePath), os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Could not create directory for chroot repo file (%s)", fullRepoFilePath)
		return
	}

	// Get a list of the existing repofiles that are part of the chroot, if any
	// We need to capture this list before we add 'allrepos.repo'.
	existingRepoFiles, err := filepath.Glob(filepath.Join(fullRepoDirPath, "*"))
	if err != nil {
		logger.Log.Warnf("Could not list existing repo files (%s)", fullRepoDirPath)
		return
	}

	dstFile, err := os.OpenFile(fullRepoFilePath, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return
	}
	defer dstFile.Close()

	// Append all repo files together into a single repo file.
	// Assume the order of repoDefinitions indicates their relative priority.
	for _, repoFilePath := range repoDefinitions {
		err = appendRepoFile(repoFilePath, dstFile)
		if err != nil {
			return
		}
	}

	// Add each previously existing repofile to the end of the new file, then delete the original.
	// We want to try our custom mounted repos before reaching out to the upstream servers.
	// By default, chroot ships with PMC repositories specified in mariner-repos rpm.
	for _, originalRepoFilePath := range existingRepoFiles {
		repoIDs, err := readRepoIDs(originalRepoFilePath)
		if err != nil {
			return err
		}
		r.defaultRepoIDs = append(r.defaultRepoIDs, repoIDs...)

		err = appendRepoFile(originalRepoFilePath, dstFile)
		if err != nil {
			return err
		}
		err = os.Remove(originalRepoFilePath)
		if err != nil {
			return err
		}
	}

	return
}

func (r *RpmRepoCloner) refreshPackagesCache() (err error) {
	releaseverCliArg, err := tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	args := []string{
		"makecache",
		releaseverCliArg,
		fmt.Sprintf("--enablerepo=%s", repoIDAll),
	}

	stdout, stderr, err := shell.Execute("tdnf", args...)
	if err != nil {
		logger.Log.Errorf("Failed to run 'tdnf makecache'. Stdout:\n%s\nStderr:\n%s\nError: %s.", stdout, stderr, err)
	}

	return
}

func appendRepoFile(repoFilePath string, dstFile *os.File) (err error) {
	repoFile, err := os.Open(repoFilePath)
	if err != nil {
		return
	}
	defer repoFile.Close()

	_, err = io.Copy(dstFile, repoFile)
	if err != nil {
		return
	}

	// Append a new line
	_, err = dstFile.WriteString("\n")
	return
}

func readRepoIDs(repoFilePath string) (repoIDs []string, err error) {
	repoFile, err := os.Open(repoFilePath)
	if err != nil {
		return
	}
	defer repoFile.Close()

	scanner := bufio.NewScanner(repoFile)
	for scanner.Scan() {
		matches := repoIDRegex.FindStringSubmatch(scanner.Text())
		if len(matches) <= repoIDIndex {
			continue
		}

		repoID := matches[repoIDIndex]
		repoIDs = append(repoIDs, repoID)

		logger.Log.Debugf("Found repo ID: %s", repoID)
	}

	err = scanner.Err()
	return

}

func (r *RpmRepoCloner) reposArgsUseOnlyLocalSources(reposArgs []string) bool {
	const repoIDIndex = 1

	for _, repoArg := range reposArgs {
		if strings.Contains(repoArg, "--enablerepo=") {
			repoID := strings.Split(repoArg, "=")[repoIDIndex]
			if r.externalRepoIDs[repoID] {
				return false
			}
		}
	}

	return true
}
