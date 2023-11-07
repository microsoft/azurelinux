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
	existingArchive = app.Flag("existing-archive", "Path to an existing archive to use instead of building a new one.").ExistingFile()

	// Bootstrap script inputs
	bootstrapOutputFile     = app.Flag("bootstrap-output-file", "Path to the output file.").Required().String()
	bootstrapScript         = app.Flag("bootstrap-script", "Path to the bootstrap script.").Required().String()
	bootstrapWorkingDir     = app.Flag("bootstrap-working-dir", "Path to the working directory.").Required().ExistingDir()
	bootstrapBuildDir       = app.Flag("bootstrap-build-dir", "Path to the build directory.").Required().ExistingDir()
	bootstrapSpecsDir       = app.Flag("bootstrap-specs-dir", "Path to the specs directory.").Required().ExistingDir()
	bootstrapSourceURL      = app.Flag("bootstrap-source-url", "URL to the source code.").Required().String()
	bootstrapUseIncremental = app.Flag("bootstrap-incremental-toolchain", "Use incremental build mode.").Default("false").Bool()
	bootstrapInputFiles     = app.Flag("bootstrap-input-files", "List of input files to hash for validating the cache.").Required().ExistingFiles()

	// Official build inputs
	officialBuildOutputFile           = app.Flag("official-build-output-file", "Path to the output file.").Required().String()
	officialBuildScript               = app.Flag("official-build-script", "Path to the official build script.").Required().String()
	officialBuildWorkingDir           = app.Flag("official-build-working-dir", "Path to the working directory.").Required().ExistingDir()
	officialBuildDistTag              = app.Flag("official-build-dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	officialBuildBuildNumber          = app.Flag("official-build-build-number", "The build number the SPEC will be built with.").Required().String()
	officialBuildReleaseVersion       = app.Flag("official-build-release-version", "The release version the SPEC will be built with.").Required().String()
	officialBuildBuildDir             = app.Flag("official-build-build-dir", "Path to the build directory.").Required().ExistingDir()
	officialBuildRpmsDir              = app.Flag("official-build-rpms-dir", "Path to the directory containing the built RPMs.").Required().ExistingDir()
	officialBuildSpecsDir             = app.Flag("official-build-specs-dir", "Path to the directory containing the SPEC files.").Required().ExistingDir()
	officialBuildRunCheck             = app.Flag("official-build-run-check", "Run the check step after building the RPMs.").Default("false").Bool()
	officialBuildUseIncremental       = app.Flag("official-build-incremental-toolchain", "Use incremental build mode.").Default("false").Bool()
	officialBuildIntermediateSrpmsDir = app.Flag("official-build-intermediate-srpms-dir", "Path to the directory containing the intermediate SRPMs.").Required().ExistingDir()
	officialBuildSrpmsDir             = app.Flag("official-build-srpms-dir", "Path to the directory containing the SRPMs.").Required().ExistingDir()
	officialBuildToolchainFromRepos   = app.Flag("official-build-toolchain-from-repos", "WHAT IS THIS?").Required().ExistingDir()
	officialBuildBldTracker           = app.Flag("official-build-bld-tracker", "Path to the bld-tracker tool").Required().ExistingFile()
	officialBuildTimestampFile        = app.Flag("official-build-timestamp-file", "Path to the timestamp file.").Required().String()
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

	if *disallowRebuild && *forceRebuild {
		logger.Log.Fatalf("Cannot --force-rebuild rebuild when --disallow-rebuild is set.")
	}

	if *existingArchive != "" && *forceRebuild {
		logger.Log.Fatalf("Cannot --force-rebuild rebuild when --existing-archive is set.")
	}

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	if err != nil {
		logger.Log.Fatalf("Failed to read toolchain manifest file '%s': %s", *toolchainManifest, err)
	}

	// Check if we are already good to go (i.e. all toolchain RPMs are present)

	err = toolchain.CleanToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to clean toolchain RPMs: %s", err)
	}

	// Use the provided archive if it exists

	if *existingArchive != "" {
		archive := toolchain.Archive{
			ArchivePath: *existingArchive,
		}
		var missingFromArchive, missingFromManifest []string
		missingFromArchive, missingFromManifest, err = archive.ValidateArchiveContents(toolchainRPMs)
		if err != nil {
			logger.Log.Fatalf("Failed to validate toolchain archive contents: %s", err)
		}
		if len(missingFromArchive) > 0 || len(missingFromManifest) > 0 {
			for _, line := range toolchain.CreateManifestMissmatchReport(missingFromArchive, missingFromManifest, *existingArchive, *toolchainManifest) {
				logger.Log.Warn(line)
			}
			logger.Log.Fatalf("Toolchain archive (%s) and manifest (%s) are missmatched", *existingArchive, *toolchainManifest)
		}

		logger.Log.Infof("Using existing archive '%s'.", *existingArchive)
		err = archive.ExtractToolchainRpms(*toolchainRpmDir)
		if err != nil {
			logger.Log.Fatalf("Failed to extract toolchain RPMs from archive: %s", err)
		}
		ready, _, err := validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
		if err != nil {
			logger.Log.Fatalf("Failed to validate toolchain RPMs are ready: %s", err)
		}
		if ready {
			logger.Log.Infof("Toolchain RPMs are ready.")
			return
		} else {
			logger.Log.Fatal("Toolchain archive is missing RPMs.")
		}
	}

	ready, _, err := validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to validate toolchain RPMs are ready: %s", err)
	}
	if ready {
		logger.Log.Infof("Toolchain RPMs are ready.")
		return
	}

	// Download toolchain RPMs if they are missing

	if !*forceRebuild {
		caCerts, tlsCerts, err := prepCerts(*tlsClientCert, *tlsClientKey, *caCertFile)
		if err != nil {
			logger.Log.Fatalf("Failed to load certificates: %s", err)
		}

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

	// Bootstrap

	bootstrap := toolchain.BootstrapScript{
		OutputFile:     *bootstrapOutputFile,
		ScriptPath:     *bootstrapScript,
		WorkingDir:     *bootstrapWorkingDir,
		BuildDir:       *bootstrapBuildDir,
		SpecsDir:       *bootstrapSpecsDir,
		SourceURL:      *bootstrapSourceURL,
		UseIncremental: *bootstrapUseIncremental,
	}
	bootstrap.InputFiles = append(bootstrap.InputFiles, *bootstrapInputFiles...)

	_, cacheOk, err := bootstrap.CheckCache(*cacheDir)
	if err != nil {
		logger.Log.Fatalf("Failed to check bootstrap cache: %s", err)
	}

	if cacheOk && !*forceRebuild {
		logger.Log.Infof("Bootstrap cache is valid, restoring.")
		err = bootstrap.RestoreFromCache(*cacheDir)
		if err != nil {
			logger.Log.Fatalf("Failed to restore bootstrap from cache: %s", err)
		}
	} else {
		err = bootstrap.Bootstrap()
		if err != nil {
			logger.Log.Fatalf("Failed to bootstrap toolchain: %s", err)
		} else {
			_, err = bootstrap.AddToCache(*cacheDir)
			if err != nil {
				logger.Log.Fatalf("Failed to add bootstrap to cache: %s", err)
			}
		}
	}

	// Official build

	official := toolchain.OfficialScript{
		OutputFile:           *officialBuildOutputFile,
		ScriptPath:           *officialBuildScript,
		WorkingDir:           *officialBuildWorkingDir,
		DistTag:              *officialBuildDistTag,
		BuildNumber:          *officialBuildBuildNumber,
		ReleaseVersion:       *officialBuildReleaseVersion,
		BuildDir:             *officialBuildBuildDir,
		RpmsDir:              *officialBuildRpmsDir,
		SpecsDir:             *officialBuildSpecsDir,
		RunCheck:             *officialBuildRunCheck,
		UseIncremental:       *officialBuildUseIncremental,
		IntermediateSrpmsDir: *officialBuildIntermediateSrpmsDir,
		OutputSrpmsDir:       *officialBuildSrpmsDir,
		ToolchainFromRepos:   *officialBuildToolchainFromRepos,
		ToolchainManifest:    *toolchainManifest,
		BldTracker:           *officialBuildBldTracker,
		TimestampFile:        *officialBuildTimestampFile,
	}
	official.InputFiles = append(official.InputFiles, *toolchainManifest)
	official.InputFiles = append(official.InputFiles, bootstrap.OutputFile)
	builtArchive := toolchain.Archive{
		ArchivePath: official.OutputFile,
	}

	_, cacheOk, err = official.CheckCache(*cacheDir)
	if err != nil {
		logger.Log.Fatalf("Failed to check official toolchain rpms cache: %s", err)
	}

	if cacheOk && !*forceRebuild {
		logger.Log.Infof("Official toolchain rpms cache is valid, restoring.")
		err = official.RestoreFromCache(*cacheDir)
		if err != nil {
			logger.Log.Fatalf("Failed to restore official toolchain rpms from cache: %s", err)
		}
	} else {
		if !*forceRebuild {
			// Toolchain script expects rpms or empty files in a specific directory do do incremental builds
			err = official.PrepIncrementalRpms(*toolchainRpmDir, toolchainRPMs)
			if err != nil {
				logger.Log.Fatalf("Failed to prep delta rpms: %s", err)
			}
		}
		err = official.BuildOfficialToolchainRpms()
		if err != nil {
			logger.Log.Fatalf("Failed to build official toolchain rpms: %s", err)
		} else {
			_, err = official.AddToCache(*cacheDir)
			if err != nil {
				logger.Log.Fatalf("Failed to add official toolchain rpms to cache: %s", err)
			}
		}

		err = official.TransferBuiltRpms()
		if err != nil {
			logger.Log.Fatalf("Failed to transfer built rpms: %s", err)
		}
	}

	err = builtArchive.ExtractToolchainRpms(*toolchainRpmDir)
	if err != nil {
		logger.Log.Fatalf("Failed to extract official toolchain rpms: %s", err)
	}

	ready, missingRPMs, err = validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to validate toolchain RPMs are ready: %s", err)
	}
	if !ready {
		logger.Log.Fatalf("Missing toolchain RPMs: %s", missingRPMs)
	} else {
		logger.Log.Infof("Toolchain RPMs are ready.")
		return
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
