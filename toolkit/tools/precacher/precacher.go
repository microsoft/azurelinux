// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/randomization"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"

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
	donwloadResultTypeUnavailable
)

type downloadResult struct {
	pkgName    string
	resultType downloadResultType
}

var (
	app = kingpin.New("precacher", "Pre-hydrate RPM caches for a given set of repo URLs.")

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()

	outDir            = exe.OutputDirFlag(app, "Directory to download packages into.")
	snapshot          = app.Flag("snapshot", "Path to the rpm snapshot .json file.").ExistingFile()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages downloaded").String()
	repoUrls          = app.Flag("repo-url", "URLs of the repos to download from.").Strings()

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

	// Get the state of the current repo from a snapshot
	rpmSnapshot, err := rpmSnapshotFromFile(*snapshot)
	if err != nil {
		logger.PanicOnError(err)
	}

	// See what is available online from the upstream repos
	availablePackages, err := getAllRepoData(*repoUrls)
	if err != nil {
		logger.PanicOnError(err)
	}

	logger.Log.Infof("Found %d packages to use for pre-caching", len(availablePackages))
	for _, pkg := range availablePackages {
		logger.Log.Debugf("Found package: %s", pkg)
	}

	// For each package in the snapshot, check if it is available online and try to download it
	downloadedPackages, err := downloadMissingPackages(rpmSnapshot, availablePackages, *outDir, *concurrentNetOps)
	if err != nil {
		logger.PanicOnError(err)
	}

	logger.Log.Infof("Pre-caching complete: Downloaded %d packages into the cache", len(downloadedPackages))
	err = writeSummaryFile(*outputSummaryFile, downloadedPackages)
	if err != nil {
		logger.PanicOnError(err)
	}
}

func rpmSnapshotFromFile(snapshotFile string) (rpmSnapshot *repocloner.RepoContents, err error) {
	err = jsonutils.ReadJSONFile(snapshotFile, &rpmSnapshot)
	return
}

func getAllRepoData(repoUrls []string) (namesToUrls map[string]string, err error) {
	timestamp.StartEvent("pull available package data from repos", nil)
	defer timestamp.StopEvent(nil)
	// repoquery behaves differently on Mariner and Ubuntu
	isMariner := shell.IsMarinerOs()

	namesToUrls = make(map[string]string)
	for _, repoUrl := range repoUrls {
		packages, err := getRepoPackages(repoUrl, isMariner)
		if err != nil {
			return nil, err
		}

		// We will be searching by the name: "<name>-<version>.<distro>.<arch>", the results from the repoquery will be
		// in the form of "(BASE_URL)/<name>-<version>.<distro>.<arch>.rpm"
		for _, pkgUrl := range packages {
			name := path.Base(pkgUrl)
			name = strings.TrimSuffix(name, ".rpm")

			// We need to prepend the repoUrl to the name to get the full url on Mariner
			if isMariner {
				pkgUrl = fmt.Sprintf("%s/%s", repoUrl, pkgUrl)
			}
			namesToUrls[name] = pkgUrl
		}
	}
	return
}

// getRepoPackages returns a list of packages available in the given repoUrl by running repoquery
func getRepoPackages(repoUrl string, isMariner bool) (packages []string, err error) {
	const (
		reqoqueryTool    = "repoquery"
		randomNameLength = 10
	)
	var (
		queryCommonArgList = []string{"-a", "--qf", "%{location}"}
		marinerArgList     = []string{"-y", "-q", "--disablerepo=*"}
		ubuntuArgList      = []string{"--show-duplicates", "--tempcache"}

		finalArgList []string
	)

	logger.Log.Infof("Getting pre-caching package data from %s", repoUrl)
	if isMariner {
		finalArgList = append(marinerArgList, queryCommonArgList...)
	} else {
		finalArgList = append(ubuntuArgList, queryCommonArgList...)
	}

	// We want to avoid using the same repo name for each repoUrl, so we generate a random name
	randomName, err := randomization.RandomString(randomNameLength, randomization.LegalCharactersAlphaNum)
	if err != nil {
		err = fmt.Errorf("failed to generate random string: %w", err)
		return
	}
	repoPathArg := fmt.Sprintf("--repofrompath=mariner-precache-%s,%s", randomName, repoUrl)
	finalArgList = append(finalArgList, repoPathArg)

	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		packages = append(packages, line)
	}

	// Run the repoquery command
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, true, reqoqueryTool, finalArgList...)
	if err != nil {
		err = fmt.Errorf("failed to run repoquery command: %w", err)
		return
	}

	return
}

func downloadMissingPackages(rpmSnapshot *repocloner.RepoContents, availablePackages map[string]string, outDir string, concurrentNetOps uint) (downloadedPackages []string, err error) {
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

	// Spawn a worker for each package, they will all do preliminary checks in parrallel before synchronizing on the semaphore.
	// Each worker is responsible for adding and removing itself from the wait group.
	for _, pkg := range rpmSnapshot.Repo {
		go precachePackage(pkg, availablePackages, outDir, wg, results, netOpsSemaphore)
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

func monitorProgress(total int, results chan downloadResult, doneChannel chan struct{}) (downloadedPackages []string) {
	downloaded := 0
	skipped := 0
	failed := 0
	unavailable := 0
	progressIncrement := 5.0
	lastProgressUpdate := progressIncrement * -1

	for done := false; !done; {
		// Wait for a result from a worker, or the done channel to be closed (which means all workers are done)
		select {
		case result := <-results:
			switch result.resultType {
			case downloadResultTypeSkipped:
				skipped++
			case downloadResultTypeSuccess:
				downloadedPackages = append(downloadedPackages, result.pkgName)
				downloaded++
			case downloadResultTypeFailure:
				failed++
			case donwloadResultTypeUnavailable:
				unavailable++
			}
		case <-doneChannel:
			// All workers are done, finish this iteration of the loop and then return
			done = true
		}
		completed := downloaded + skipped + failed + unavailable
		progressPercent := (float64(completed) / float64(total)) * 100
		if progressPercent > lastProgressUpdate+progressIncrement || done {
			logger.Log.Infof("Pre-caching packages: %3d%% (downloaded: %4d, skipped: %4d, unavailable: %4d, failed: %4d)", int(progressPercent), downloaded, skipped, unavailable, failed)
			lastProgressUpdate = progressPercent
		}
	}
	return
}

func precachePackage(pkg *repocloner.RepoPackage, availablePackages map[string]string, outDir string, wg *sync.WaitGroup, results chan<- downloadResult, netOpsSemaphore chan struct{}) {
	const (
		downloadRetryAttempts = 2
		downloadRetryDuration = time.Second
	)

	wg.Add(1)
	defer wg.Done()

	// File names are of the form "<name>-<version>.<distro>.<arch>.rpm"
	pkgName := fmt.Sprintf("%s-%s.%s.%s", pkg.Name, pkg.Version, pkg.Distribution, pkg.Architecture)
	fileName := fmt.Sprintf("%s.rpm", pkgName)
	fullFilePath := path.Join(outDir, fileName)
	result := downloadResult{
		pkgName: fileName,
	}

	// Bail out early if the file already exists
	if exists, _ := file.PathExists(fullFilePath); exists {
		logger.Log.Debugf("Skipping pre-caching '%s'. File already exists", fileName)
		result.resultType = downloadResultTypeSkipped
		results <- result
		return
	}

	// Get the url for the package, or bail out if it is not available
	url, ok := availablePackages[pkgName]
	if !ok {
		logger.Log.Warnf("Pre-caching '%s' failed. Package not found in any repos", fileName)
		result.resultType = donwloadResultTypeUnavailable
		results <- result
		return
	}

	// Limit the number of concurrent network operations to avoid overloading the network
	netOpsSemaphore <- struct{}{}
	defer func() {
		<-netOpsSemaphore
	}()

	logger.Log.Debugf("Pre-caching '%s' from '%s'", fileName, url)
	err := retry.Run(func() error {
		err := network.DownloadFile(url, fullFilePath, nil, nil)
		if err != nil {
			logger.Log.Warnf("Failed to download (%s). Error: %s", url, err)
		}
		return err
	}, downloadRetryAttempts, downloadRetryDuration)

	if err != nil {
		logger.Log.Warnf("Pre-caching '%s' failed. Error: %s", fileName, err)
		result.resultType = downloadResultTypeFailure
		results <- result
		return
	} else {
		logger.Log.Debugf("Pre-caching '%s' succeeded", fileName)
		result.resultType = downloadResultTypeSuccess
		results <- result
	}
}

func writeSummaryFile(summaryFile string, downloadedPackages []string) (err error) {
	logger.Log.Infof("Writing pre-caching summary file to '%s'", summaryFile)
	err = file.WriteLines(downloadedPackages, summaryFile, "\n")
	if err != nil {
		err = fmt.Errorf("failed to write pre-caching summary file: %w", err)
		return
	}
	return
}
