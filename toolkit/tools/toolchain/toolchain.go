// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/toolchain"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultNetOpsCount = "40"
)

var (
	app = kingpin.New("grapher", "Dependency graph generation tool")

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()

	caCertFile       = app.Flag("ca-certificate", "Root certificate authority to use when downloading files.").String()
	tlsClientCert    = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey     = app.Flag("tls-key", "TLS client key to use when downloading files.").String()
	packageURLs      = app.Flag("package-urls", "List of URLs to download RPMs from.").Required().Strings()
	concurrentNetOps = app.Flag("concurrent-net-ops", "Number of concurrent network operations to perform.").Default(defaultNetOpsCount).Uint()

	toolchainManifest = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").Required().ExistingFile()
	toolchainRpmDir   = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	cacheDir          = app.Flag("cache-dir", "Directory to cache resources in.").Required().ExistingDir()

	disallowRebuild = app.Flag("disallow-rebuild", "Require all packages to be available from a repo.").Default("false").Bool()
	forceRebuild    = app.Flag("force-rebuild", "Force rebuilding of all packages.").Default("false").Bool()

	// Bootstrap script inputs
	bootstrapOutputFile     = app.Flag("bootstrap-output-file", "Path to the output file.").Required().String()
	bootstrapScript         = app.Flag("bootstrap-script", "Path to the bootstrap script.").Required().String()
	bootstrapWorkingDir     = app.Flag("bootstrap-working-dir", "Path to the working directory.").Required().String()
	bootstrapBuildDir       = app.Flag("bootstrap-build-dir", "Path to the build directory.").Required().String()
	bootstrapSpecsDir       = app.Flag("bootstrap-specs-dir", "Path to the specs directory.").Required().String()
	bootstrapSourceURL      = app.Flag("bootstrap-source-url", "URL to the source code.").Required().String()
	bootstrapUseIncremental = app.Flag("bootstrap-incremental-toolchain", "Use incremental build mode.").Default("false").Bool()
	bootstrapArchiveTool    = app.Flag("bootstrap-archive-tool", "Path to the archive tool.").Required().String()
	bootstrapInputFiles     = app.Flag("bootstrap-input-files", "List of input files to hash for validating the cache.").Required().Strings()
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

	timestamp.BeginTiming("toolchain", *timestampFile)
	defer timestamp.CompleteTiming()

	if !*disallowRebuild && *forceRebuild {
		logger.Log.Fatalf("Cannot --force-rebuild rebuild when --allow-rebuild is false.")
	}

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	if err != nil {
		logger.Log.Fatalf("Failed to read toolchain manifest file '%s': %s", *toolchainManifest, err)
	}

	caCerts, tlsCerts, err := prepCerts(*tlsClientCert, *tlsClientKey, *caCertFile)
	if err != nil {
		logger.Log.Fatalf("Failed to load certificates: %s", err)
	}

	err = toolchain.CleanToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to clean toolchain RPMs: %s", err)
	}

	if !*forceRebuild {
		err = toolchain.DownloadToolchainRpms(*toolchainRpmDir, toolchainRPMs, *packageURLs, caCerts, tlsCerts, *concurrentNetOps)
		if err != nil {
			logger.Log.Fatalf("Failed to download toolchain RPMs: %s", err)
		}
	}

	ready, missingRPMs, err := validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to validate toolchain RPMs are ready: %s", err)
	}
	if !ready {
		logger.Log.Infof("Missing toolchain RPMs: %s", missingRPMs)
		if *disallowRebuild {
			logger.Log.Fatalf("Toolchain RPMs are not ready, and --disallow-rebuild is set.")
		}
	} else {
		logger.Log.Infof("Toolchain RPMs are ready.")
		return
	}

	bootstrap := toolchain.BootstrapScript{
		OutputFile:     *bootstrapOutputFile,
		ScriptPath:     *bootstrapScript,
		WorkingDir:     *bootstrapWorkingDir,
		BuildDir:       *bootstrapBuildDir,
		SpecsDir:       *bootstrapSpecsDir,
		SourceURL:      *bootstrapSourceURL,
		UseIncremental: *bootstrapUseIncremental,
		ArchiveTool:    *bootstrapArchiveTool,
	}
	bootstrap.InputFiles = append(bootstrap.InputFiles, *bootstrapInputFiles...)

	_, cacheOk, err := toolchain.CheckBootstrapCache(bootstrap, *cacheDir)
	if err != nil {
		logger.Log.Fatalf("Failed to check bootstrap cache: %s", err)
	}

	if cacheOk {
		logger.Log.Infof("Bootstrap cache is valid.")
		toolchain.RestoreFromCache(bootstrap, *cacheDir)
		return
	} else {
		err = toolchain.Bootstrap(bootstrap)
		if err != nil {
			logger.Log.Fatalf("Failed to bootstrap toolchain: %s", err)
		} else {
			_, err = toolchain.AddToCache(bootstrap, *cacheDir)
			if err != nil {
				logger.Log.Fatalf("Failed to add bootstrap to cache: %s", err)
			}
		}
	}
}

// validateToolchainRpms checks that all of the toolchain RPMs exist in the toolchain directory.
func validateToolchainRpms(toolchainDir string, toolchainRPMs []string) (ready bool, missingRpms []string, err error) {
	for _, rpm := range toolchainRPMs {
		rpmPath := filepath.Join(toolchainDir, rpm)
		exists, rpmErr := file.PathExists(rpmPath)
		if rpmErr != nil {
			err = fmt.Errorf("failed to check if toolchain RPM '%s' exists. Error:\n%w", rpmPath, rpmErr)
			return
		}
		if !exists {
			missingRpms = append(missingRpms, rpm)
		}
	}

	if len(missingRpms) == 0 {
		ready = true
	}
	return
}

// prepCerts loads the system certificates and any additional certificates specified by the user.
func prepCerts(tlsClientCert, tlsClientKey, caCertFile string) (caCerts *x509.CertPool, tlsCerts []tls.Certificate, err error) {
	caCerts, err = x509.SystemCertPool()
	if err != nil {
		err = fmt.Errorf("failed to load system certificate pool. Error:\n%w", err)
	}
	if caCertFile != "" {
		newCACert, certErr := os.ReadFile(caCertFile)
		if certErr != nil {
			err = fmt.Errorf("invalid CA certificate (%s), Error:\n%w", caCertFile, certErr)
			return
		}

		caCerts.AppendCertsFromPEM(newCACert)
	}

	if tlsClientCert != "" && tlsClientKey != "" {
		cert, tlsErr := tls.LoadX509KeyPair(tlsClientCert, tlsClientKey)
		if tlsErr != nil {
			err = fmt.Errorf("invalid TLS client key pair (%s) (%s), Error:\n%w", tlsClientCert, tlsClientKey, tlsErr)
			return
		}

		tlsCerts = append(tlsCerts, cert)
	}

	return
}
