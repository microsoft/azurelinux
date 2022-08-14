// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/image/pkgfetcher"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagepkgfetcher", "A tool to download a provided list of packages into a given directory.")

	configFile = exe.InputFlag(app, "Path to the image config file.")
	outDir     = exe.OutputDirFlag(app, "Directory to download packages into.")

	baseDirPath    = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	existingRpmDir = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir         = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").Required().String()

	workertar            = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles            = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo       = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableUpstreamRepos = app.Flag("disable-upstream-repos", "Disables pulling packages from upstream repos").Bool()

	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	externalOnly = app.Flag("external-only", "Only clone packages not provided locally.").Bool()
	inputGraph   = app.Flag("package-graph", "Path to the graph file to read, only needed if external-only is set.").ExistingFile()

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populateImagePkgFetcherConfig() *pkgfetcher.Config {
	return &pkgfetcher.Config{
		ConfigFile:           *configFile,
		OutDir:               *outDir,
		BaseDirPath:          *baseDirPath,
		ExistingRpmDir:       *existingRpmDir,
		TmpDir:               *tmpDir,
		WorkerTar:            *workertar,
		RepoFiles:            *repoFiles,
		UsePreviewRepo:       *usePreviewRepo,
		DisableUpstreamRepos: *disableUpstreamRepos,
		TlsClientCert:        *tlsClientCert,
		TlsClientKey:         *tlsClientKey,
		ExternalOnly:         *externalOnly,
		InputGraph:           *inputGraph,
		InputSummaryFile:     *inputSummaryFile,
		OutputSummaryFile:    *outputSummaryFile,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateImagePkgFetcherConfig()
	err := pkgfetcher.FetchPkgsAndCreateRepo(cfg)
	logger.PanicOnError(err, "Failed to save cloned repo contents")
}
