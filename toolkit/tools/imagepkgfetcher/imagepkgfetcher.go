// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagepkgfetcher", "A tool to download a provided list of packages into a given directory.")

	configFile = exe.InputFlag(app, "Path to the image config file.")
	outDir     = exe.OutputDirFlag(app, "Directory to download packages into.")

	baseDirPath             = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	existingRpmDir          = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	existingToolchainRpmDir = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir                  = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").Required().String()

	workertar            = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles            = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo       = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableDefaultRepos  = app.Flag("disable-default-repos", "Disable pulling packages from PMC repos").Bool()
	disableUpstreamRepos = app.Flag("disable-upstream-repos", "Disables pulling packages from upstream repos").Bool()

	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	externalOnly = app.Flag("external-only", "Only clone packages not provided locally.").Bool()
	inputGraph   = app.Flag("package-graph", "Path to the graph file to read, only needed if external-only is set.").ExistingFile()

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	prof, profErr := profile.StartProfiling(profFlags)
	if profErr != nil {
		logger.Log.Warnf("Could not start profiling: %s", profErr)
		return
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("imagepkgfetcher", *timestampFile)
	defer timestamp.CompleteTiming()

	if *externalOnly && strings.TrimSpace(*inputGraph) == "" {
		logger.Log.Fatal("input-graph must be provided if external-only is set.")
	}

	timestamp.StartEvent("initialize and configure cloner", nil)

	cloner, err := rpmrepocloner.ConstructCloner(*outDir, *tmpDir, *workertar, *existingRpmDir, *existingToolchainRpmDir, *tlsClientCert, *tlsClientKey, *repoFiles)
	if err != nil {
		logger.Log.Panicf("Failed to initialize RPM repo cloner. Error: %s", err)
	}
	defer cloner.Close()

	enabledRepos := rpmrepocloner.RepoFlagAll
	if !*usePreviewRepo {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagPreview
	}
	if *disableUpstreamRepos {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagUpstream
	}
	if *disableDefaultRepos {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagMarinerDefaults
	}
	cloner.SetEnabledRepos(enabledRepos)

	timestamp.StopEvent(nil) // initialize and configure cloner

	if strings.TrimSpace(*inputSummaryFile) != "" {
		timestamp.StartEvent("restore packages", nil)

		// If an input summary file was provided, simply restore the cache using the file.
		err = repoutils.RestoreClonedRepoContents(cloner, *inputSummaryFile)

		timestamp.StopEvent(nil) // restore packages
	} else {
		err = cloneSystemConfigs(cloner, *configFile, *baseDirPath, *externalOnly, *inputGraph)
	}

	if err != nil {
		logger.Log.Panicf("Failed to clone RPM repo. Error: %s", err)
	}

	timestamp.StartEvent("finalize cloned packages", nil)

	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		logger.Log.Panicf("Failed to convert downloaded RPMs into a repo. Error: %s", err)
	}

	if strings.TrimSpace(*outputSummaryFile) != "" {
		err = repoutils.SaveClonedRepoContents(cloner, *outputSummaryFile)
		logger.PanicOnError(err, "Failed to save cloned repo contents")
	}

	timestamp.StopEvent(nil) // finalize cloned packages
}

func cloneSystemConfigs(cloner repocloner.RepoCloner, configFile, baseDirPath string, externalOnly bool, inputGraph string) (err error) {
	timestamp.StartEvent("cloning system config", nil)
	defer timestamp.StopEvent(nil)

	const cloneDeps = true

	cfg, err := configuration.LoadWithAbsolutePaths(configFile, baseDirPath)
	if err != nil {
		return
	}

	packageVersionsInConfig, err := installutils.PackageNamesFromConfig(cfg)
	if err != nil {
		return
	}

	// Add kernel packages from KernelOptions
	packageVersionsInConfig = append(packageVersionsInConfig, installutils.KernelPackages(cfg)...)

	if externalOnly {
		packageVersionsInConfig, err = filterExternalPackagesOnly(packageVersionsInConfig, inputGraph)
		if err != nil {
			return
		}
	}

	// Add any packages required by the install tools
	packageVersionsInConfig = append(packageVersionsInConfig, installutils.GetRequiredPackagesForInstall()...)

	logger.Log.Infof("Cloning: %v", packageVersionsInConfig)
	// The image tools don't care if a package was created locally or not, just that it exists. Disregard if it is prebuilt or not.
	_, err = cloner.CloneByPackageVerSingleTransaction(cloneDeps, packageVersionsInConfig...)
	if err != nil {
		// Fallback to legacy flow with multiple transactions in case we get a OOM error from a large transaction.
		logger.Log.Warnf("Failed to clone packages in a single transaction, will retry with individual transactions... (%s)", err)
		_, err = cloner.CloneByPackageVer(cloneDeps, packageVersionsInConfig...)
	}
	return
}

// filterExternalPackagesOnly returns the subset of packageVersionsInConfig that only contains external packages.
func filterExternalPackagesOnly(packageVersionsInConfig []*pkgjson.PackageVer, inputGraph string) (filteredPackages []*pkgjson.PackageVer, err error) {
	dependencyGraph, err := pkggraph.ReadDOTGraphFile(inputGraph)
	if err != nil {
		return
	}

	for _, pkgVer := range packageVersionsInConfig {
		pkgNode, _ := dependencyGraph.FindBestPkgNode(pkgVer)

		// There are two ways an external package will be represented by pkgNode.
		// 1) pkgNode may be nil. This is possible if the package is never consumed during the build phase,
		//    which means it will not be in the graph.
		// 2) pkgNode will be of 'StateUnresolved'. This will be the case if a local package has it listed as
		//    a Requires or BuildRequires.
		if pkgNode == nil || (pkgNode.RunNode != nil && pkgNode.RunNode.State == pkggraph.StateUnresolved) {
			filteredPackages = append(filteredPackages, pkgVer)
		}
	}

	return
}
