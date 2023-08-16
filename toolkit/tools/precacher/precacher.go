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
	donwloadResultTypeUnavailable
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

	outDir            = exe.OutputDirFlag(app, "Directory to download packages into.")
	snapshot          = app.Flag("snapshot", "Path to the rpm snapshot .json file.").ExistingFile()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages downloaded").String()
	repoUrls          = app.Flag("repo-url", "URLs of the repos to download from.").Strings()
	workerTar         = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	buildDir          = app.Flag("worker-dir", "Directory to store chroot while running repo query.").String()

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

	packagesAvailableFromRepos, err := getAllRepoData(*repoUrls, *workerTar, *buildDir)
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
	return
}

// getAllRepoData returns a map of package names to URLs for all packages available in the given repos. It uses
// a chroot to run repoquery.
func getAllRepoData(repoURLs []string, workerTar, buildDir string) (namesToURLs map[string]string, err error) {
	const (
		leaveChrootOnDisk = false
	)
	timestamp.StartEvent("pull available package data from repos", nil)
	defer timestamp.StopEvent(nil)

	// Create a chroot to run repoquery in
	// Create the directory 'buildDir' if it does not exist
	exists, err := file.DirExists(buildDir)
	if err != nil {
		err = fmt.Errorf("failed to check if directory %s exists:\n%w", buildDir, err)
		return nil, err
	}
	if !exists {
		logger.Log.Infof("Creating 1st time chroot directory %s", buildDir)
		err = os.MkdirAll(buildDir, 0755)
		if err != nil {
			err = fmt.Errorf("failed to create directory %s:\n%w", buildDir, err)
			return nil, err
		}
	}
	queryChroot, err := createChroot(workerTar, buildDir, leaveChrootOnDisk)
	if err != nil {
		err = fmt.Errorf("failed to create chroot:\n%w", err)
		return nil, err
	}
	defer queryChroot.Close(leaveChrootOnDisk)

	namesToUrls = make(map[string]string)
	for _, repoURL := range repoURLs {
		// Use the chroot to query each repo for the packages it contains
		var packages []string
		err = queryChroot.Run(func() (chrootErr error) {
			packageRepoPaths, chrootErr = getPackageRepoPaths(repoURL)
			return chrootErr
		})
		if err != nil {
			return nil, err
		}

		// We will be searching by the name: "<name>-<version>.<distro>.<arch>", the results from the repoquery will be
		// in the form of "<PARTIAL_URL>/<name>-<version>.<distro>.<arch>.rpm"
		for _, packageRepoPath := range packageRepoPaths {
			packageName := path.Base(packageRepoPath)
			packageName = strings.TrimSuffix(packageName, ".rpm")

			// We need to prepend the repoURL to the partial URL to get the full URL
			pkgURL = fmt.Sprintf("%s/%s", repoURL, packageRepoPath)
			namesToUrls[name] = pkgURL
		}
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

	queryChroot = safechroot.NewChroot(chrootDir, true)
	err = queryChroot.Initialize(workerTar, nil, nil)
	if err != nil {
		err = fmt.Errorf("failed to initialize chroot: %w", err)
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

	// Install the repoquery package from upstream
	logger.Log.Infof("Installing '%s' package to get 'repoquery' command", dnfUtilsPackageName)
	queryChroot.Run(func() error {
		_, err = installutils.TdnfInstall(dnfUtilsPackageName, rootDir)
		if err != nil {
			err = fmt.Errorf("failed to install '%s':\n%w", dnfUtilsPackageName, err)
		}
		return err
	})
	if err != nil {
		err = fmt.Errorf("failed to install '%s' in chroot:\n%w", dnfUtilsPackageName, err)
		return
	}
	return
}

// getRepoPackages returns a list of packages available in the given repoUrl by running repoquery
func getRepoPackages(repoUrl string) (packages []string, err error) {
	const (
		reqoqueryTool    = "repoquery"
		randomNameLength = 10
		printErrorOutput = true
	)
	var queryCommonArgList = []string{"-y", "-q", "--disablerepo=*", "-a", "--qf", "%{location}"}

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
		packages = append(packages, line)
	}

	// Run the repoquery command
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, printErrorOutput, reqoqueryTool, finalArgList...)
	if err != nil {
		err = fmt.Errorf("failed to run repoquery command:\n%w", err)
		return
	}

	return
}

// downloadMissingPackages will attemp to download each package listed in rpmSnapshot that is not already present in the
// outDir. It will return a list of the packages that were downloaded. It will use concurrentNetOps to limit the number of
// concurrent network operations used to download the missing packages. It will also monitor the results and print periodic
// progress updates to the console.
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

	// Spawn a worker for each package, they will all do preliminary checks in parallel before synchronizing on the semaphore.
	// Each worker is responsible for removing itself from the wait group once done.
	for _, pkg := range rpmSnapshot.Repo {
		wg.Add(1)
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
				failed++
			case donwloadResultTypeUnavailable:
				logger.Log.Warnf("'%s' failed, not found in any repos", result.pkgName)
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
// This function runs with best effort, so it will return a result (of type downloadResultTypeFailure) if any error occurs
// rather than returning an error. The caller is expected to have added to the provided wait group, while this function is
// responsible for removing itself from the wait group. As much processing as possible is done before acquiring the
// network operations semaphore to minimize the time spent holding it.
func precachePackage(pkg *repocloner.RepoPackage, availablePackages map[string]string, outDir string, wg *sync.WaitGroup, results chan<- downloadResult, netOpsSemaphore chan struct{}) {
	const (
		downloadRetryAttempts = 2
		downloadRetryDuration = time.Second
	)

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
		result.resultType = downloadResultTypeSkipped
		results <- result
		return
	}

	// Get the url for the package, or bail out if it is not available
	url, ok := availablePackages[pkgName]
	if !ok {
		result.resultType = donwloadResultTypeUnavailable
		results <- result
		return
	}

	// Limit the number of concurrent network operations to avoid overloading the network. All work past this point
	// is either network related, or trivial, so we can safely hold the semaphore until we are done.
	netOpsSemaphore <- struct{}{}
	defer func() {
		<-netOpsSemaphore
	}()

	logger.Log.Debugf("Pre-caching '%s' from '%s'", fileName, url)
	err := retry.Run(func() error {
		err := network.DownloadFile(url, fullFilePath, nil, nil)
		if err != nil {
			logger.Log.Warnf("Attempt to download (%s) failed. Error: %s", url, err)
		}
		return err
	}, downloadRetryAttempts, downloadRetryDuration)

	if err != nil {
		result.resultType = downloadResultTypeFailure
		results <- result
		return
	}

	result.resultType = downloadResultTypeSuccess
	results <- result
}

func writeSummaryFile(summaryFile string, downloadedPackages []string) (err error) {
	logger.Log.Infof("Writing summary file to '%s'", summaryFile)
	err = file.WriteLines(downloadedPackages, "\n", summaryFile)
	if err != nil {
		err = fmt.Errorf("failed to write pre-caching summary file:\n%w", err)
		return
	}
	return
}
