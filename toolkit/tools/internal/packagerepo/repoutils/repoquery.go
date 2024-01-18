// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repoutils

import (
	"fmt"
	"os"
	"path"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/randomization"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

const (
	chrootRepoDir = "/etc/yum.repos.d/"
)

// GetAllRepoData returns a map of package names to URLs for all packages
// available in the given repos. It uses a chroot to run repoquery.
func GetAllRepoData(repoURLs, repoFiles []string, workerTar, buildDir, repoUrlsFile string) (namesToURLs map[string]string, err error) {
	const (
		leaveChrootOnDisk = false
	)
	timestamp.StartEvent("pull available package data from repos", nil)
	defer timestamp.StopEvent(nil)

	queryChroot, err := createChroot(workerTar, buildDir, leaveChrootOnDisk)
	if err != nil {
		err = fmt.Errorf("failed to create chroot:\n%w", err)
		return nil, err
	}
	defer queryChroot.Close(leaveChrootOnDisk)

	namesToURLs = make(map[string]string)
	allPackageURLs := []string{}
	for _, repoURL := range repoURLs {
		// Use the chroot to query each repo for the packages it contains
		var packageRepoURLs []string
		err = queryChroot.Run(func() (chrootErr error) {
			packageRepoURLs, chrootErr = getPackageRepoPathsFromUrl(repoURL)
			return chrootErr
		})
		if err != nil {
			return nil, err
		}
		allPackageURLs = append(allPackageURLs, packageRepoURLs...)
	}

	// Use the chroot to query each repo for the packages it contains
	for _, repoFile := range repoFiles {
		// Replace the existing repo file (if it exists) with the one that we want to query
		logger.Log.Infof("Will query package data from %s", repoFile)
		destFile := path.Join(chrootRepoDir, path.Base(repoFile))
		chrootRepoFile := []safechroot.FileToCopy{
			{Src: repoFile, Dest: destFile},
		}
		err = queryChroot.AddFiles(chrootRepoFile...)
		if err != nil {
			err = fmt.Errorf("failed to add files to chroot:\n%w", err)
			return
		}
	}

	var packageRepoUrls []string
	// Only run repoquery if we have repo files to query. --enablerepo=* will not work if there are no repo files
	// and will return "Error: Unknown repo: '*'"
	if len(repoFiles) > 0 {
		err = queryChroot.Run(func() (chrootErr error) {
			packageRepoUrls, chrootErr = getPackageRepoUrlsFromRepoFiles()
			return chrootErr
		})
		if err != nil {
			return nil, err
		}
	}
	allPackageURLs = append(allPackageURLs, packageRepoUrls...)

	// We will be searching by the name: "<name>-<version>.<distro>.<arch>", the results from the repoquery will be
	// in the form of "<PARTIAL_URL>/<name>-<version>.<distro>.<arch>.rpm"
	allPackageURLs = sliceutils.RemoveDuplicatesFromSlice(allPackageURLs)
	for _, packageURL := range allPackageURLs {
		packageName := path.Base(packageURL)
		packageName = strings.TrimSuffix(packageName, ".rpm")

		namesToURLs[packageName] = packageURL
	}

	if repoUrlsFile != "" {
		err = file.WriteLines(allPackageURLs, repoUrlsFile)
	}

	return
}

// createChroot creates a network-enabled chroot to run repoquery in. The caller is expected to call Close() on the
// returned chroot unless an error is returned, in which case the chroot will be closed by this function.
func createChroot(workerTar, chrootDir string, leaveChrootOnDisk bool) (queryChroot *safechroot.Chroot, err error) {
	const (
		dnfUtilsPackageName = "dnf-utils"
		rootDir             = "/"
	)
	timestamp.StartEvent("creating repoquery chroot", nil)
	defer timestamp.StopEvent(nil)
	logger.Log.Info("Creating chroot for repoquery")

	queryChroot = safechroot.NewChroot(chrootDir, false)
	err = queryChroot.Initialize(workerTar, nil, nil, true)
	if err != nil {
		err = fmt.Errorf("failed to initialize chroot:\n%w", err)
		return
	}

	defer func() {
		if err != nil {
			closeErr := queryChroot.Close(leaveChrootOnDisk)
			if closeErr != nil {
				logger.Log.Errorf("Failed to close chroot, err: %s", closeErr)
			}
		}
	}()

	// We will need network to install the repoquery package
	files := []safechroot.FileToCopy{
		{Src: "/etc/resolv.conf", Dest: "/etc/resolv.conf"},
	}
	err = queryChroot.AddFiles(files...)
	if err != nil {
		err = fmt.Errorf("failed to add files to chroot:\n%w", err)
		return
	}

	// Install the repoquery package from upstream, then clean up any existing repos
	logger.Log.Infof("Installing '%s' package to get 'repoquery' command", dnfUtilsPackageName)
	err = queryChroot.Run(func() error {
		_, chrootErr := installutils.TdnfInstall(dnfUtilsPackageName, rootDir)
		if chrootErr != nil {
			chrootErr = fmt.Errorf("failed to install '%s':\n%w", dnfUtilsPackageName, err)
			return chrootErr
		}

		// Remove all existing repos, we will be adding the repo files we want to query later
		chrootErr = os.RemoveAll("/etc/yum.repos.d")
		return chrootErr
	})
	if err != nil {
		err = fmt.Errorf("failed to install '%s' in chroot:\n%w", dnfUtilsPackageName, err)
		return
	}
	return
}

// getPackageRepoPathsFromUrl returns a list of packages available in the given repoUrl by running repoquery
func getPackageRepoPathsFromUrl(repoUrl string) (packageURLs []string, err error) {
	const (
		reqoqueryTool    = "repoquery"
		randomNameLength = 10
		printErrorOutput = true
	)
	var queryCommonArgList = []string{"-y", "-q", "--disablerepo=*", "-a", "--location"}

	logger.Log.Infof("Getting package data from %s", repoUrl)

	// We want to avoid using the same repo name for each repoUrl, so we generate a random name
	randomName, err := randomization.RandomString(randomNameLength, randomization.LegalCharactersAlphaNum)
	if err != nil {
		err = fmt.Errorf("failed to generate random string:\n%w", err)
		return
	}
	repoPathArg := fmt.Sprintf("--repofrompath=mariner-precache-%s,%s", randomName, repoUrl)
	finalArgList := append(queryCommonArgList, repoPathArg)

	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		packageURLs = append(packageURLs, line)
	}

	// Run the repoquery command
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, printErrorOutput, reqoqueryTool, finalArgList...)
	if err != nil {
		err = fmt.Errorf("failed to run repoquery command:\n%w", err)
		return
	}

	return
}

// getPackageRepoUrlsFromRepoFiles returns a list of packages available in all RPM repos listed in the system's .repo files.
func getPackageRepoUrlsFromRepoFiles() (packageURLs []string, err error) {
	const (
		reqoqueryTool    = "repoquery"
		randomNameLength = 10
		printErrorOutput = true
	)
	// We have removed all other repo files from the chroot, so we can blindly enable all repos to get the full list of packages
	var queryCommonArgList = []string{"-y", "-q", "--enablerepo=*", "-a", "--location"}

	logger.Log.Info("Getting package data from repo files")

	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		packageURLs = append(packageURLs, line)
	}

	// Run the repoquery command
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, printErrorOutput, reqoqueryTool, queryCommonArgList...)
	if err != nil {
		err = fmt.Errorf("failed to run repoquery command:\n%w", err)
		return
	}

	return
}
