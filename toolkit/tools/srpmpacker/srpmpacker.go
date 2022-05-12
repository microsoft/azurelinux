// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/srpmpacker"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	signatureEnforceString   = "enforce"
	signatureSkipCheckString = "skip"
	signatureUpdateString    = "update"
)
const (
	defaultBuildDir    = "./build/SRPMS"
	defaultWorkerCount = "10"
)

var (
	app = kingpin.New("srpmpacker", "A tool to package a SRPM.")

	specsDir = exe.InputDirFlag(app, "Path to the SPEC directory to create SRPMs from.")
	outDir   = exe.OutputDirFlag(app, "Directory to place the output SRPM.")
	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	buildDir     = app.Flag("build-dir", "Directory to store temporary files while building.").Default(defaultBuildDir).String()
	distTag      = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	packListFile = app.Flag("pack-list", "Path to a list of SPECs to pack. If empty will pack all SPECs.").ExistingFile()
	runCheck     = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()

	workers          = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Int()
	repackAll        = app.Flag("repack", "Rebuild all SRPMs, even if already built.").Bool()
	nestedSourcesDir = app.Flag("nested-sources", "Set if for a given SPEC, its sources are contained in a SOURCES directory next to the SPEC file.").Bool()

	// Use String() and not ExistingFile() as the Makefile may pass an empty string if the user did not specify any of these options
	sourceURL     = app.Flag("source-url", "URL to a source server to download SPEC sources from.").String()
	caCertFile    = app.Flag("ca-cert", "Root certificate authority to use when downloading files.").String()
	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz. If this argument is empty, SRPMs will be packed in the host environment.").ExistingFile()

	validSignatureLevels = []string{signatureEnforceString, signatureSkipCheckString, signatureUpdateString}
	signatureHandling    = app.Flag("signature-handling", "Specifies how to handle signature mismatches for source files.").Default(signatureEnforceString).PlaceHolder(exe.PlaceHolderize(validSignatureLevels)).Enum(validSignatureLevels...)
)

func populateSrpmPackerConfig() *srpmpacker.Config {
	return &srpmpacker.Config{
		SpecsDir:             *specsDir,
		OutDir:               *outDir,
		BuildDir:             *buildDir,
		DistTag:              *distTag,
		PackListFile:         *packListFile,
		RunCheck:             *runCheck,
		Workers:              *workers,
		RepackAll:            *repackAll,
		NestedSourcesDir:     *nestedSourcesDir,
		SourceURL:            *sourceURL,
		CaCertFile:           *caCertFile,
		TlsClientCert:        *tlsClientCert,
		TlsClientKey:         *tlsClientKey,
		WorkerTar:            *workerTar,
		ValidSignatureLevels: validSignatureLevels,
		SignatureHandling:    *signatureHandling,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	if *workers <= 0 {
		logger.Log.Fatalf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	cfg := populateSrpmPackerConfig()

	err := cfg.CreateAllSRPMsWrapper()
	logger.PanicOnError(err)

}
