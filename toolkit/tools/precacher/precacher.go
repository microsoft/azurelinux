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

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/sirupsen/logrus"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultNetOpsCount = "20"
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
	packagesAvailableFromRepos, err := repoutils.GetAllRepoData(*repoUrls, *repoFiles, *workerTar, *buildDir, *repoUrlsFile)
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
	_, err = retry.RunWithDefaultDownloadBackoff(func() error {
		err := network.DownloadFile(url, fullFilePath, nil, nil)
		if err != nil {
			logger.Log.Warnf("Attempt to download (%s) failed. Error: %s", url, err)
		}
		return err
	}, noCancel)
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
