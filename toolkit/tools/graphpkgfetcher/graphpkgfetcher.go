// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/graph/pkgfetcher"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("graphpkgfetcher", "A tool to download a unresolved packages in a graph into a given directory.")

	inputGraph  = exe.InputStringFlag(app, "Path to the graph file to read")
	outputGraph = exe.OutputFlag(app, "Updated graph file with unresolved nodes marked as resolved")
	outDir      = exe.OutputDirFlag(app, "Directory to download packages into.")

	existingRpmDir = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir         = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").String()

	workertar            = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles            = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo       = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableUpstreamRepos = app.Flag("disable-upstream-repos", "Disables pulling packages from upstream repos").Bool()
	toolchainManifest    = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").ExistingFile()

	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	stopOnFailure = app.Flag("stop-on-failure", "Stop if failed to cache all unresolved nodes.").Bool()

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populateGraphpkgfetcherConfig() *pkgfetcher.Config {
	return &pkgfetcher.Config{
		InputGraph:        *inputGraph,
		OutputGraph:       *outputGraph,
		OutDir:            *outDir,
		ExistingRpmDir:    *existingRpmDir,
		TmpDir:            *tmpDir,
		WorkerTar:         *workertar,
		RepoFiles:         *repoFiles,
		UsePreviewRepo:    *usePreviewRepo,
		ToolchainManifest: *toolchainManifest,
		TlsClientCert:     *tlsClientCert,
		TlsClientKey:      *tlsClientKey,
		StopOnFailure:     *stopOnFailure,
		InputSummaryFile:  *inputSummaryFile,
		OutputSummaryFile: *outputSummaryFile,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateGraphpkgfetcherConfig()
	err := cfg.ResolvePackages()
	if err != nil {
		logger.Log.Panicf("Failed to write cache graph to file. Error: %s", err)
	}
}
