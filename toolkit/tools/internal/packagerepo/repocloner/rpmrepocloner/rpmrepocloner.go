// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpmrepocloner

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"microsoft.com/pkggen/internal/buildpipeline"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/packagerepo/repocloner"
	"microsoft.com/pkggen/internal/packagerepo/repomanager/rpmrepomanager"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/safechroot"
	"microsoft.com/pkggen/internal/shell"
)

const (
	allRepoIDs             = "*"
	builtRepoID            = "local-repo"
	cacheRepoID            = "upstream-cache-repo"
	squashChrootRunErrors  = false
	chrootDownloadDir      = "/outputrpms"
	leaveChrootFilesOnDisk = false
	updateRepoID           = "mariner-official-update"
	previewRepoID          = "mariner-preview"
	fetcherRepoID          = "fetcher-cloned-repo"
	cacheRepoDir           = "/upstream-cached-rpms"
)

var (
	// Every valid line pair will be of the form:
	//		<package>-<version>.<arch> : <Description>
	//		Repo	: [repo_name]
	//
	// NOTE: we ignore packages installed in the build environment denoted by "Repo	: @System".
	packageLookupNameMatchRegex = regexp.MustCompile(`([^:\s]+(x86_64|aarch64|noarch))\s*:[^\n]*\nRepo\s+:\s+[^@]`)
	packageNameIndex            = 1

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
	listedPackageRegex = regexp.MustCompile(`^\s*([[:alnum:]_+-]+)\.([[:alnum:]_+-]+)\s+([[:alnum:]._+~-]+)\.([[:alnum:]_+-]+)`)
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
	chroot         *safechroot.Chroot
	usePreviewRepo bool
	cloneDir       string
}

// New creates a new RpmRepoCloner
func New() *RpmRepoCloner {
	return &RpmRepoCloner{}
}

// Initialize initializes rpmrepocloner, enabling Clone() to be called.
//  - destinationDir is the directory to save RPMs
//  - tmpDir is the directory to create a chroot
//  - workerTar is the path to the worker tar used to seed the chroot
//  - existingRpmsDir is the directory with prebuilt RPMs
//  - usePreviewRepo if set, the upstream preview repository will be used.
//  - repoDefinitions is a list of repo files to use when cloning RPMs
func (r *RpmRepoCloner) Initialize(destinationDir, tmpDir, workerTar, existingRpmsDir string, usePreviewRepo bool, repoDefinitions []string) (err error) {
	const (
		isExistingDir = false

		bindFsType = ""
		bindData   = ""

		chrootLocalRpmsDir = "/localrpms"

		overlayWorkDirectory  = "/overlaywork/workdir"
		overlayUpperDirectory = "/overlaywork/upper"
		overlaySource         = "overlay"
	)

	r.usePreviewRepo = usePreviewRepo
	if usePreviewRepo {
		logger.Log.Info("Enabling preview repo")
	}

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

	r.cloneDir = destinationDir

	// Setup mount points for the chroot.
	//
	// 1) Mount the provided directory of existing RPMs into the chroot as an overlay,
	// ensuring the chroot can read the files, but not alter the actual directory outside
	// the chroot.
	//
	// 2) Mount the directory to download RPMs into as a bind, allowing the chroot to write
	// files into it.
	overlayMount, overlayExtraDirs := safechroot.NewOverlayMountPoint(r.chroot.RootDir(), overlaySource, chrootLocalRpmsDir, existingRpmsDir, overlayUpperDirectory, overlayWorkDirectory)
	extraMountPoints := []*safechroot.MountPoint{
		overlayMount,
		safechroot.NewMountPoint(destinationDir, chrootDownloadDir, bindFsType, safechroot.BindMountPointFlags, bindData),
	}

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
	reposToInitialize := []string{chrootLocalRpmsDir, chrootDownloadDir, cacheRepoDir}
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

	return
}

// AddNetworkFiles adds files needed for networking capabilities into the cloner.
// tlsClientCert and tlsClientKey are optional.
func (r *RpmRepoCloner) AddNetworkFiles(tlsClientCert, tlsClientKey string) (err error) {
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
	const chrootRepoFile = "/etc/yum.repos.d/allrepos.repo"

	fullRepoFilePath := filepath.Join(r.chroot.RootDir(), chrootRepoFile)

	// Create the directory for the repo file
	err = os.MkdirAll(filepath.Dir(fullRepoFilePath), os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Could not create directory for chroot repo file (%s)", fullRepoFilePath)
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

// initializeMountedChrootRepo will initialize a local RPM repository inside the chroot.
func (r *RpmRepoCloner) initializeMountedChrootRepo(repoDir string) (err error) {
	return r.chroot.Run(func() (err error) {
		err = os.MkdirAll(repoDir, os.ModePerm)
		if err != nil {
			logger.Log.Errorf("Failed to create repo directory '%s'.", repoDir)
			return
		}
		return rpmrepomanager.CreateRepo(repoDir)
	})
}

// Clone clones the provided list of packages.
// If cloneDeps is set, package dependencies will also be cloned.
// It will automatically resolve packages that describe a provide or file from a package.
// The cloner will mark any package that locally built by setting preBuilt = true
func (r *RpmRepoCloner) Clone(cloneDeps bool, packagesToClone ...*pkgjson.PackageVer) (preBuilt bool, err error) {
	for _, pkg := range packagesToClone {
		pkgName := convertPackageVersionToTdnfArg(pkg)

		logger.Log.Debugf("Cloning: %s", pkgName)
		args := []string{
			"--destdir",
			chrootDownloadDir,
			pkgName,
		}

		if cloneDeps {
			args = append([]string{"download", "--alldeps"}, args...)
		} else {
			args = append([]string{"download-nodeps"}, args...)
		}

		err = r.chroot.Run(func() (err error) {
			var chrootErr error
			// Consider the built RPMs first, then the already cached (e.g. tooolchain), and finally all remote packages.
			repoOrderList := []string{builtRepoID, cacheRepoID, allRepoIDs}
			preBuilt, chrootErr = r.clonePackage(args, repoOrderList...)
			return chrootErr
		})

		if err != nil {
			return
		}
	}

	return
}

// WhatProvides attempts to find packages which provide the requested PackageVer.
func (r *RpmRepoCloner) WhatProvides(pkgVer *pkgjson.PackageVer) (packageNames []string, err error) {
	provideQuery := convertPackageVersionToTdnfArg(pkgVer)

	baseArgs := []string{
		"provides",
		provideQuery,
		fmt.Sprintf("--disablerepo=%s", allRepoIDs),
	}

	foundPackages := make(map[string]bool)
	// Consider the built (local) RPMs first, then the already cached (e.g. tooolchain), and finally all remote packages.
	repoOrderList := []string{builtRepoID, cacheRepoID, allRepoIDs}
	for _, repoID := range repoOrderList {
		logger.Log.Debugf("Enabling repo ID: %s", repoID)

		err = r.chroot.Run(func() (err error) {
			completeArgs := append(baseArgs, fmt.Sprintf("--enablerepo=%s", repoID))

			if !r.usePreviewRepo {
				completeArgs = append(completeArgs, fmt.Sprintf("--disablerepo=%s", previewRepoID))
			}

			stdout, stderr, err := shell.Execute("tdnf", completeArgs...)
			logger.Log.Debugf("tdnf search for provide '%s':\n%s", pkgVer.Name, stdout)

			if err != nil {
				logger.Log.Debugf("Failed to lookup provide '%s', tdnf error: '%s'", pkgVer.Name, stderr)
				return
			}

			for _, matches := range packageLookupNameMatchRegex.FindAllStringSubmatch(stdout, -1) {
				packageName := matches[packageNameIndex]
				if _, found := foundPackages[packageName]; !found {
					foundPackages[packageName] = true
					logger.Log.Debugf("'%s' is available from package '%s'", pkgVer.Name, packageName)
				}
			}

			return
		})
		if err != nil {
			return
		}

		if len(foundPackages) > 0 {
			logger.Log.Debug("Found required package(s), skipping further search in other repos.")
			break
		}
	}

	if len(foundPackages) == 0 {
		err = fmt.Errorf("could not resolve %s", pkgVer.Name)
		return
	}

	for packageName := range foundPackages {
		packageNames = append(packageNames, packageName)
	}

	logger.Log.Debugf("Translated '%s' to package(s): %s", pkgVer.Name, strings.Join(packageNames, " "))
	return
}

// ConvertDownloadedPackagesIntoRepo initializes the downloaded RPMs into an RPM repository.
func (r *RpmRepoCloner) ConvertDownloadedPackagesIntoRepo() (err error) {
	srcDir := filepath.Join(r.chroot.RootDir(), chrootDownloadDir)
	repoDir := srcDir

	if !buildpipeline.IsRegularBuild() {
		// Docker based build doesn't use overlay so repo folder
		// must be explicitely set to the RPMs cache folder
		repoDir = filepath.Join(r.chroot.RootDir(), cacheRepoDir)
	}

	err = rpmrepomanager.OrganizePackagesByArch(srcDir, repoDir)
	if err != nil {
		return
	}

	err = r.initializeMountedChrootRepo(chrootDownloadDir)
	if err != nil {
		return
	}

	if !buildpipeline.IsRegularBuild() {
		// Docker based build doesn't use overlay so cache repo
		// must be explicitly initialized
		err = r.initializeMountedChrootRepo(cacheRepoDir)
	}

	return
}

// ClonedRepoContents returns the packages contained in the cloned repository.
func (r *RpmRepoCloner) ClonedRepoContents() (repoContents *repocloner.RepoContents, err error) {
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

		repoContents.Repo = append(repoContents.Repo, pkg)
	}

	checkedRepoID := fetcherRepoID
	// Docker based build doesn't use overlay so cache repo was explicitely initialized
	if !buildpipeline.IsRegularBuild() {
		checkedRepoID = cacheRepoID
	}

	err = r.chroot.Run(func() (err error) {
		// Disable all repositories except the fetcher repository (the repository with the cloned packages)
		tdnfArgs := []string{
			"list",
			"ALL",
			fmt.Sprintf("--disablerepo=%s", allRepoIDs),
			fmt.Sprintf("--enablerepo=%s", checkedRepoID),
		}
		return shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, true, "tdnf", tdnfArgs...)
	})

	return
}

// CloneDirectory returns the directory where cloned packages are saved.
func (r *RpmRepoCloner) CloneDirectory() string {
	return r.cloneDir
}

// Close closes the given RpmRepoCloner.
func (r *RpmRepoCloner) Close() error {
	return r.chroot.Close(leaveChrootFilesOnDisk)
}

// clonePackage clones a given package using prepopulated arguments.
// It will gradually enable more repos to consider using enabledRepoOrder until the package is found.
func (r *RpmRepoCloner) clonePackage(baseArgs []string, enabledRepoOrder ...string) (preBuilt bool, err error) {
	const (
		unresolvedOutputPrefix  = "No package"
		toyboxConflictsPrefix   = "toybox conflicts"
		unresolvedOutputPostfix = "available"
	)

	if len(enabledRepoOrder) == 0 {
		return false, fmt.Errorf("enabledRepoOrder cannot be empty")
	}

	// Disable all repos first so we can gradually enable them below.
	// TDNF processes enable/disable repo requests in the order that they are passed.
	// So if `--disablerepo=foo` and then `--enablerepo=foo` are passed, `foo` will be enabled.
	baseArgs = append(baseArgs, "--disablerepo=*")

	var enabledRepoArgs []string
	for _, repoID := range enabledRepoOrder {
		logger.Log.Debugf("Enabling repo ID: %s", repoID)
		// Gradually increase the scope of allowed repos. Keep repos already considered enabled
		// as packages from one repo may depend on another.
		// e.g. packages in upstream update repo may require packages in upstream base repo.
		enabledRepoArgs = append(enabledRepoArgs, fmt.Sprintf("--enablerepo=%s", repoID))
		args := append(baseArgs, enabledRepoArgs...)

		if !r.usePreviewRepo {
			args = append(args, fmt.Sprintf("--disablerepo=%s", previewRepoID))
		}

		var (
			stdout string
			stderr string
		)
		stdout, stderr, err = shell.Execute("tdnf", args...)

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
			preBuilt = (repoID == builtRepoID)
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

	// Treat <= as =
	// Treat > and >= as "latest"
	switch pkgVer.Condition {
	case "<=":
		logger.Log.Warnf("Treating '%s' version constraint as '=' for: %v", pkgVer.Condition, pkgVer)
		fallthrough
	case "=":
		tdnfArg = fmt.Sprintf("%s-%s", tdnfArg, pkgVer.Version)
	case "":
		break
	default:
		logger.Log.Warnf("Discarding '%s' version constraint for: %v", pkgVer.Condition, pkgVer)
	}

	return
}
