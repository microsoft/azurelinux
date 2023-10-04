// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"math/rand"
	"os"
	"path"
	"strings"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/randomization"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/sirupsen/logrus"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultNetOpsCount = "20"
	chrootRepoDir      = "/etc/yum.repos.d/"
)

type downloadResultType int

const (
	downloadResultTypeSuccess downloadResultType = iota
	downloadResultTypeFailure
	downloadResultTypeSkipped
	downloadResultTypeUnavailable
)

type downloadResult struct {
	pkgName    string
	resultType downloadResultType
}

var (
	app = kingpin.New("precacher", "Pre-hydrate RPM cache for a given set of repo URLs and a RPM snapshot file.")

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()

	outDir            = app.Flag("output-dir", "Directory to download packages into.").Required().ExistingDir()
	snapshot          = app.Flag("snapshot", "Path to the rpm snapshot .json file.").ExistingFile()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages downloaded").String()
	repoUrlsFile      = app.Flag("repo-urls-file", "Path to save the list of package URLs available in the repos").String()
	repoUrls          = app.Flag("repo-url", "URLs of the repos to download from.").Strings()
	repoFiles         = app.Flag("repo-file", "Files containing URLs of the repos to download from.").ExistingFiles()
	workerTar         = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	buildDir          = app.Flag("worker-dir", "Directory to store chroot while running repo query.").Required().String()

	concurrentNetOps = app.Flag("concurrent-net-ops", "Number of concurrent network operations to perform.").Default(defaultNetOpsCount).Uint()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("precacher", *timestampFile)
	defer timestamp.CompleteTiming()

	rpmSnapshot, err := rpmSnapshotFromFile(*snapshot)
	if err != nil {
		logger.PanicOnError(err)
	}

	packagesAvailableFromRepos, err := getAllRepoData(*repoUrls, *repoFiles, *workerTar, *buildDir, *repoUrlsFile)
	if err != nil {
		logger.PanicOnError(err)
	}

	logger.Log.Infof("Found %d available packages", len(packagesAvailableFromRepos))
	if logger.Log.IsLevelEnabled(logrus.DebugLevel) {
		for _, pkg := range packagesAvailableFromRepos {
			logger.Log.Debugf("Found package: %s", pkg)
		}
	}

	downloadedPackages, err := downloadMissingPackages(rpmSnapshot, packagesAvailableFromRepos, *outDir, *concurrentNetOps)
	if err != nil {
		logger.PanicOnError(err)
	}

	logger.Log.Infof("Downloaded %d packages into the cache", len(downloadedPackages))
	err = writeSummaryFile(*outputSummaryFile, downloadedPackages)
	if err != nil {
		logger.PanicOnError(err)
	}
}

func rpmSnapshotFromFile(snapshotFile string) (rpmSnapshot *repocloner.RepoContents, err error) {
	err = jsonutils.ReadJSONFile(snapshotFile, &rpmSnapshot)

	// Randomize the order of the packages to average out the package sizes to optimize the download speed. Lots of small
	// packages will be slow to download because of the overhead of the network operations, so mix in some large packages
	// to average out the download time. We have a better chance of maximizing the network bandwidth this way.
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(rpmSnapshot.Repo), func(i, j int) {
		rpmSnapshot.Repo[i], rpmSnapshot.Repo[j] = rpmSnapshot.Repo[j], rpmSnapshot.Repo[i]
	})

	return
}

// getAllRepoData returns a map of package names to URLs for all packages available in the given repos. It uses
// a chroot to run repoquery.
func getAllRepoData(repoURLs, repoFiles []string, workerTar, buildDir, repoUrlsFile string) (namesToURLs map[string]string, err error) {
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
	err = queryChroot.Run(func() (chrootErr error) {
		packageRepoUrls, chrootErr = getPackageRepoUrlsFromRepoFiles()
		return chrootErr
	})
	if err != nil {
		return nil, err
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

	err = file.WriteLines(allPackageURLs, repoUrlsFile)

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
	err = queryChroot.Initialize(workerTar, nil, nil)
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

// downloadMissingPackages will attempt to download each package listed in rpmSnapshot that is not already present in the
// outDir. It will return a list of the packages that were downloaded. It will use concurrentNetOps to limit the number of
// concurrent network operations used to download the missing packages. It will also monitor the results and print periodic
// progress updates to the console.
func downloadMissingPackages(rpmSnapshot *repocloner.RepoContents, packagesAvailableFromRepos map[string]string, outDir string, concurrentNetOps uint) (downloadedPackages []string, err error) {
	timestamp.StartEvent("download missing packages", nil)
	defer timestamp.StopEvent(nil)

	// We will be downloading packages concurrently, so we need to keep track of when they are all done via a wait group. To
	// simplify the code just use goroutines with a semaphore channel to limit the number of concurrent network operations. Each
	// goroutine will handle a single package and will send the result of the download to a results channel. The main thread will
	// monitor the results channel and update the progress counter accordingly.
	wg := new(sync.WaitGroup)
	netOpsSemaphore := make(chan struct{}, concurrentNetOps)
	results := make(chan downloadResult)
	doneChannel := make(chan struct{})

	// Spawn a worker for each package, they will all do preliminary checks in parallel before synchronizing on the semaphore.
	// Each worker is responsible for removing itself from the wait group once done.
	for _, pkg := range rpmSnapshot.Repo {
		wg.Add(1)
		go precachePackage(pkg, packagesAvailableFromRepos, outDir, wg, results, netOpsSemaphore)
	}

	// Wait for all the workers to finish and signal the main thread when we are done
	go func() {
		wg.Wait()
		close(doneChannel)
	}()

	// Monitor the results channel and update the progress counter accordingly. Return once the done channel is closed.
	downloadedPackages = monitorProgress(len(rpmSnapshot.Repo), results, doneChannel)

	return
}

// monitorProgress will wait for results from the downloadResult channel and update the progress counter accordingly. If
// no more results are available we expect the done channel to be closed, at which point we will return.
func monitorProgress(total int, results chan downloadResult, doneChannel chan struct{}) (downloadedPackages []string) {
	const progressIncrement = 10.0

	downloaded := 0
	skipped := 0
	failed := 0
	unavailable := 0
	lastProgressUpdate := progressIncrement * -1

	for done := false; !done; {
		// Wait for a result from a worker, or the done channel to be closed (which means all workers are done)
		select {
		case result := <-results:
			switch result.resultType {
			case downloadResultTypeSkipped:
				logger.Log.Debugf("Skipping pre-caching '%s'. File already exists", result.pkgName)
				skipped++
			case downloadResultTypeSuccess:
				logger.Log.Debugf("Pre-caching '%s' succeeded", result.pkgName)
				downloadedPackages = append(downloadedPackages, result.pkgName)
				downloaded++
			case downloadResultTypeFailure:
				logger.Log.Warnf("Failed to download: %s", result.pkgName)
				failed++
			case downloadResultTypeUnavailable:
				logger.Log.Warnf("Could not find '%s' in any repos", result.pkgName)
				unavailable++
			}
		case <-doneChannel:
			// All workers are done, finish this iteration of the loop and then return
			done = true
		}

		// Calculate the progress percentage and update the progress counter if needed (update every 'progressIncrement' percent)
		completed := downloaded + skipped + failed + unavailable
		progressPercent := (float64(completed) / float64(total)) * 100
		if progressPercent > lastProgressUpdate+progressIncrement || done {
			logger.Log.Infof("Pre-caching: %3d%% ( downloaded: %4d, skipped: %4d, unavailable: %4d, failed: %4d )", int(progressPercent), downloaded, skipped, unavailable, failed)
			lastProgressUpdate = progressPercent
		}
	}
	return
}

// precachePackage will attempt to download the specified package. It will return a downloadResult struct via the results.
// This function runs with best effort, so it will return all errors via the results channel. rather than returning an error.
// The results may be one of:
//   - downloadResultTypeSuccess: The package was downloaded successfully
//   - downloadResultTypeFailure: The package failed to download (ie error occurred)
//   - downloadResultTypeSkipped: The package was not downloaded because it already exists
//   - downloadResultTypeUnavailable: The package was not downloaded because it was not found in any of the repos
//
// The caller is expected to have added to the provided wait group, while this function is
// responsible for removing itself from the wait group. As much processing as possible is done before acquiring the
// network operations semaphore to minimize the time spent holding it.
func precachePackage(pkg *repocloner.RepoPackage, packagesAvailableFromRepos map[string]string, outDir string, wg *sync.WaitGroup, results chan<- downloadResult, netOpsSemaphore chan struct{}) {
	const (
		// With 5 attempts, initial delay of 1 second, and a backoff factor of 2.0 the total time spent retrying will be
		// ~30 seconds.
		downloadRetryAttempts = 5
		failureBackoffBase    = 2.0
		downloadRetryDuration = time.Second
	)
	var noCancel chan struct{} = nil

	// File names are of the form "<name>-<version>.<distro>.<arch>.rpm"
	pkgName, fileName := formatName(pkg)
	fullFilePath := path.Join(outDir, fileName)
	result := downloadResult{
		pkgName:    fileName,
		resultType: downloadResultTypeFailure,
	}

	defer func() {
		results <- result
		wg.Done()
	}()

	// Bail out early if the file already exists
	exists, err := file.PathExists(fullFilePath)
	if err != nil {
		logger.Log.Warnf("Failed to check if file exists: %s", err)
		return
	}
	if exists {
		result.resultType = downloadResultTypeSkipped
		return
	}

	// Get the URL for the package, or bail out if it is not available.
	url, ok := packagesAvailableFromRepos[pkgName]
	if !ok {
		result.resultType = downloadResultTypeUnavailable
		return
	}

	// Limit the number of concurrent network operations to avoid overloading the network. All work past this point
	// is either network related, or trivial, so we can safely hold the semaphore until we are done.
	netOpsSemaphore <- struct{}{}
	defer func() {
		<-netOpsSemaphore
	}()

	logger.Log.Debugf("Pre-caching '%s' from '%s'", fileName, url)
	_, err = retry.RunWithExpBackoff(func() error {
		err := network.DownloadFile(url, fullFilePath, nil, nil)
		if err != nil {
			logger.Log.Warnf("Attempt to download (%s) failed. Error: %s", url, err)
		}
		return err
	}, downloadRetryAttempts, downloadRetryDuration, failureBackoffBase, noCancel)
	if err != nil {
		return
	}

	result.resultType = downloadResultTypeSuccess
}

func formatName(pkg *repocloner.RepoPackage) (pkgName, fileName string) {
	// Names should not contain the epoch, strip everything before the ":"" in the string. "Version": "0:1.2-3", becomes "1.2-3"
	version := pkg.Version
	if strings.Contains(version, ":") {
		version = strings.Split(version, ":")[1]
	}

	pkgName = fmt.Sprintf("%s-%s.%s.%s", pkg.Name, version, pkg.Distribution, pkg.Architecture)
	fileName = fmt.Sprintf("%s.rpm", pkgName)
	return
}

func writeSummaryFile(summaryFile string, downloadedPackages []string) (err error) {
	logger.Log.Infof("Writing summary file to '%s'", summaryFile)
	err = file.WriteLines(downloadedPackages, summaryFile)
	if err != nil {
		err = fmt.Errorf("failed to write pre-caching summary file:\n%w", err)
		return
	}
	return
}
