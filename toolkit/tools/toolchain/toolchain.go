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

type buildConfig struct {
	doBuild                 bool
	doDeltaBuild            bool
	doDownload              bool
	doCache                 bool
	doUpdateManifestArchive bool
	doUpdateManifestPMC     bool
	doUpdateManifestLocal   bool
	doArchive               bool
}

const (
	defaultNetOpsCount = "40"
	rebuildAuto        = "auto"
	rebuildFast        = "fast"
	rebuildForce       = "force"
	rebuildNever       = "never"
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
	downloadManifest = app.Flag("download-manifest", "Path to a list of RPMs that were downloaded.").Required().String()
	specsDir         = app.Flag("specs-dir", "Path to the specs directory.").Required().ExistingDir()

	toolchainManifest  = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").Required().ExistingFile()
	useLatestAvailable = app.Flag("use-latest-available", "Use the latest available version of the toolchain RPMs in the repo.").Default("false").Bool()
	toolchainRpmDir    = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	cacheDir           = app.Flag("cache-dir", "Directory to cache resources in.").Required().ExistingDir()
	disableCache       = app.Flag("disable-cache", "Block the use of cached resources.").Default("false").Bool()

	allowRebuild    = app.Flag("rebuild", "Require all packages to be available from a repo.").Default("auto").Enum(rebuildAuto, rebuildFast, rebuildForce, rebuildNever)
	existingArchive = app.Flag("existing-archive", "Path to an existing archive to use instead of building a new one.").ExistingFile()
	summaryFile     = app.Flag("summary-file", "Path to the summary file which records any changes made.").String()

	// Bootstrap script inputs
	bootstrapOutputFile = app.Flag("bootstrap-output-file", "Path to the output file.").Required().String()
	bootstrapScript     = app.Flag("bootstrap-script", "Path to the bootstrap script.").Required().String()
	bootstrapWorkingDir = app.Flag("bootstrap-working-dir", "Path to the working directory.").Required().ExistingDir()
	bootstrapBuildDir   = app.Flag("bootstrap-build-dir", "Path to the build directory.").Required().ExistingDir()
	bootstrapSourceURL  = app.Flag("bootstrap-source-url", "URL to the source code.").Required().String()
	//bootstrapUseIncremental = app.Flag("bootstrap-incremental-toolchain", "Use incremental build mode.").Default("false").Bool()
	bootstrapInputFiles = app.Flag("bootstrap-input-files", "List of input files to hash for validating the cache.").Required().ExistingFiles()

	// Official build inputs
	officialBuildOutputFile     = app.Flag("official-build-output-file", "Path to the output file.").Required().String()
	officialBuildScript         = app.Flag("official-build-script", "Path to the official build script.").Required().String()
	officialBuildWorkingDir     = app.Flag("official-build-working-dir", "Path to the working directory.").Required().ExistingDir()
	officialBuildDistTag        = app.Flag("official-build-dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	officialBuildBuildNumber    = app.Flag("official-build-build-number", "The build number the SPEC will be built with.").Required().String()
	officialBuildReleaseVersion = app.Flag("official-build-release-version", "The release version the SPEC will be built with.").Required().String()
	officialBuildBuildDir       = app.Flag("official-build-build-dir", "Path to the build directory.").Required().ExistingDir()
	officialBuildRpmsDir        = app.Flag("official-build-rpms-dir", "Path to the directory containing the built RPMs.").Required().ExistingDir()
	officialBuildSpecsDir       = app.Flag("official-build-specs-dir", "Path to the directory containing the SPEC files.").Required().ExistingDir()
	officialBuildRunCheck       = app.Flag("official-build-run-check", "Run the check step after building the RPMs.").Default("false").Bool()
	//officialBuildUseIncremental       = app.Flag("official-build-incremental-toolchain", "Use incremental build mode.").Default("false").Bool()
	officialBuildIntermediateSrpmsDir = app.Flag("official-build-intermediate-srpms-dir", "Path to the directory containing the intermediate SRPMs.").Required().ExistingDir()
	officialBuildSrpmsDir             = app.Flag("official-build-srpms-dir", "Path to the directory containing the SRPMs.").Required().ExistingDir()
	officialBuildToolchainFromRepos   = app.Flag("official-build-toolchain-from-repos", "WHAT IS THIS?").Required().ExistingDir()
	officialBuildBldTracker           = app.Flag("official-build-bld-tracker", "Path to the bld-tracker tool").Required().ExistingFile()
	officialBuildTimestampFile        = app.Flag("official-build-timestamp-file", "Path to the timestamp file.").Required().String()
	officialInputFiles                = app.Flag("official-input-files", "List of input files to hash for validating the cache.").Required().Strings()
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

	buildConfig, err := validateConfiguOptions(*allowRebuild, *existingArchive, *useLatestAvailable, *disableCache)
	if err != nil {
		logger.Log.Fatalf("Failed to validate configuration options:\n%s", err)
	}
	printConfigSummary(buildConfig)

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	if err != nil {
		logger.Log.Fatalf("Failed to read toolchain manifest file '%s': %s", *toolchainManifest, err)
	}

	// TODO: This does nothing right now...
	if buildConfig.doUpdateManifestPMC || buildConfig.doUpdateManifestLocal || buildConfig.doUpdateManifestArchive {
		toolchainRPMs, err = toolchain.UpdateManifestsToLatestAvailable(toolchainRPMs, *existingArchive, *specsDir)
		if err != nil {
			logger.Log.Fatalf("Failed to update toolchain manifest file '%s': %s", *toolchainManifest, err)
		}
	}

	// Track any chages we make to the environment
	var changesMade []string

	// All steps that follow are additive, so we need to remove any unwanted packages first
	removedRpms, err := toolchain.CleanToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to clean toolchain RPMs: %s", err)
	}
	for _, rpm := range removedRpms {
		changesMade = append(changesMade, fmt.Sprintf("Removed %s from toolchain dir", rpm))
	}

	modifications, err := produceToolchain(buildConfig, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to produce toolchain rpms:\n%s", err)
	}
	for _, modification := range modifications {
		changesMade = append(changesMade, fmt.Sprintf("Updated: %s", modification))
	}

	// Do a final check of the toolchain RPMs
	ready, missingRPMs, err := validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
	if err != nil {
		logger.Log.Fatalf("Failed to validate toolchain RPMs are ready:\n%s", err)
	}
	if !ready {
		logger.Log.Fatalf("Missing toolchain RPMs:\n%s", missingRPMs)
	} else {
		logger.Log.Infof("Toolchain RPMs are ready.")
	}

	if len(*summaryFile) > 0 {
		logger.Log.Warnf("Writing summary file to %s", *summaryFile)
		logger.Log.Warnf("Changes made:\n%s", changesMade)
		err = file.WriteLines(changesMade, *summaryFile)
		if err != nil {
			return
		}
	}
}

// printConfigSummary will explain what the tools will try to do
func validateConfiguOptions(allowRebuild, existingArchive string, useLatestAvailable, disableCache bool) (config buildConfig, err error) {
	config = buildConfig{
		doBuild:                 false,
		doDeltaBuild:            false,
		doDownload:              false,
		doCache:                 !disableCache,
		doUpdateManifestArchive: false,
		doUpdateManifestPMC:     false,
		doUpdateManifestLocal:   false,
		doArchive:               false,
	}

	// ensure allowRebuild is one of the known consts
	if allowRebuild != rebuildAuto && allowRebuild != rebuildFast && allowRebuild != rebuildForce && allowRebuild != rebuildNever {
		err = fmt.Errorf("invalid rebuild option %s", allowRebuild)
		return
	}

	if existingArchive != "" {
		// Archive mode. Never build, optionally update manifests, cache doesn't matter

		// Never allow rebuilds when using an existing archive
		if !((allowRebuild == rebuildAuto) || (allowRebuild == rebuildNever)) {
			err = fmt.Errorf("must use --rebuild=auto or --rebuild=never when using --existing-archive")
		}
		config.doArchive = true
		if useLatestAvailable {
			config.doUpdateManifestArchive = true
		}
		return

	} else {
		// No archive
		if allowRebuild == rebuildNever {

			// Only use PMC
			config.doDownload = true
			if useLatestAvailable {
				config.doUpdateManifestPMC = true
			}
			return
		}

		// Otherwise, we will be doing a build assuming the toolchain RPMs are not available
		config.doBuild = true
		// If we are rebuilding and want updated manifests, always update the local manifest
		if useLatestAvailable {
			config.doUpdateManifestLocal = true
		}

		// Local build only
		if allowRebuild == rebuildForce {
			config.doDownload = false
			config.doDeltaBuild = false
			if useLatestAvailable {
				config.doUpdateManifestLocal = true
			}
			return
		}

		// Hybrid build
		if allowRebuild == rebuildFast || allowRebuild == rebuildAuto {
			config.doDownload = true
			config.doDeltaBuild = true
			if useLatestAvailable {
				config.doUpdateManifestPMC = true
			}
			return
		}
	}

	err = fmt.Errorf("unhandled build inputs %v %v %v %v", allowRebuild, existingArchive, useLatestAvailable, disableCache)
	return
}

func printConfigSummary(config buildConfig) {
	logger.Log.Infof("Configuration Summary:")
	logger.Log.Infof("  Use Archive:        %t", config.doArchive)
	logger.Log.Infof("  Download Toolchain: %t", config.doDownload)
	logger.Log.Infof("  Build Toolchain:    %t", config.doBuild)
	logger.Log.Infof("    Delta Build:      %t", config.doDeltaBuild)
	logger.Log.Infof("  Update Manifest:")
	logger.Log.Infof("    Archive:          %t", config.doUpdateManifestArchive)
	logger.Log.Infof("    PMC:              %t", config.doUpdateManifestPMC)
	logger.Log.Infof("    Local:            %t", config.doUpdateManifestLocal)
	logger.Log.Infof("  Use Cache:          %t", config.doCache)
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

func produceToolchain(config buildConfig, toolchainRPMs []string) (newRpms []string, err error) {
	// Only build if we don't pass an explicit archive file.
	var archive toolchain.Archive
	if config.doArchive {
		archive = toolchain.Archive{
			ArchivePath: *existingArchive,
		}
	} else {
		// Download toolchain RPMs if they are missing
		if config.doDownload {
			caCerts, tlsCerts, err := prepCerts(*tlsClientCert, *tlsClientKey, *caCertFile)
			if err != nil {
				err = fmt.Errorf("failed to load certificates:\n%s", err)
				return newRpms, err
			}

			downloads, err := toolchain.DownloadToolchainRpms(*toolchainRpmDir, toolchainRPMs, *packageURLs, caCerts, tlsCerts, *concurrentNetOps, *downloadManifest)
			newRpms = append(newRpms, downloads...)
			if err != nil {
				err = fmt.Errorf("failed to download toolchain RPMs:\n%s", err)
				return newRpms, err
			}
		}

		ready, missingRPMs, err := validateToolchainRpms(*toolchainRpmDir, toolchainRPMs)
		if err != nil {
			err = fmt.Errorf("failed to validate toolchain RPMs are ready:\n%s", err)
			return newRpms, err
		}

		// Might be able to if all the RPMs are there already.
		if ready {
			logger.Log.Infof("Toolchain build not required, all RPMs are present.")
			return newRpms, err
		} else {
			logger.Log.Infof("Missing toolchain RPMs: %s", missingRPMs)
		}

		if config.doBuild {
			// Bootstrap
			bootstrap, err := buildBootstrapToolchainArchive(config)
			if err != nil {
				err = fmt.Errorf("failed to build bootstrap toolchain archive:\n%s", err)
				logger.Log.Errorf("Toolchain failure, check log file at: %s", *logFile)
				return newRpms, err
			}

			// Official build
			_, _, archive, err = buildOfficialToolchainArchive(config, bootstrap, toolchainRPMs)
			if err != nil {
				err = fmt.Errorf("failed to build official toolchain archive:\n%s", err)
				logger.Log.Errorf("Toolchain failure, check log file at: %s", *logFile)
				return newRpms, err
			}

		} else {
			err = fmt.Errorf("toolchain RPMs are not ready, and but toolchain rebuild is disabled")
			return newRpms, err
		}
	}

	// Extract and validate the archive
	missingFiles, err := extractArchive(archive, toolchainRPMs)
	if err != nil {
		err = fmt.Errorf("failed to extract toolchain archive:\n%s", err)
		return
	}
	newRpms = append(newRpms, missingFiles...)

	return
}

func buildBootstrapToolchainArchive(config buildConfig) (bootstrap toolchain.BootstrapScript, err error) {
	bootstrap = toolchain.BootstrapScript{
		OutputFile:     *bootstrapOutputFile,
		ScriptPath:     *bootstrapScript,
		WorkingDir:     *bootstrapWorkingDir,
		BuildDir:       *bootstrapBuildDir,
		SpecsDir:       *specsDir,
		SourceURL:      *bootstrapSourceURL,
		UseIncremental: config.doDeltaBuild,
	}
	bootstrap.InputFiles = append(bootstrap.InputFiles, *bootstrapInputFiles...)

	cacheOk := false
	if config.doCache {
		_, cacheOk, err = bootstrap.CheckCache(*cacheDir)
		if err != nil {
			err = fmt.Errorf("failed to check bootstrap cache, error:\n%w", err)
			return
		}
	}

	if cacheOk {
		logger.Log.Infof("Bootstrap cache is valid, restoring.")
		err = bootstrap.RestoreFromCache(*cacheDir)
		if err != nil {
			err = fmt.Errorf("failed to restore bootstrap from cache, error:\n%w", err)
			return
		}
	} else {
		err = bootstrap.Bootstrap()
		if err != nil {
			err = fmt.Errorf("failed to bootstrap toolchain, error:\n%w", err)
			return
		} else {
			_, err = bootstrap.AddToCache(*cacheDir)
			if err != nil {
				err = fmt.Errorf("failed to add bootstrap to cache, error:\n%w", err)
				return
			}
		}
	}
	return
}

func buildOfficialToolchainArchive(config buildConfig, bootstrap toolchain.BootstrapScript, toolchainRPMs []string) (builtRpms []string, official toolchain.OfficialScript, builtArchive toolchain.Archive, err error) {
	official = toolchain.OfficialScript{
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
		UseIncremental:       config.doDeltaBuild,
		IntermediateSrpmsDir: *officialBuildIntermediateSrpmsDir,
		OutputSrpmsDir:       *officialBuildSrpmsDir,
		ToolchainFromRepos:   *officialBuildToolchainFromRepos,
		ToolchainManifest:    *toolchainManifest,
		BldTracker:           *officialBuildBldTracker,
		TimestampFile:        *officialBuildTimestampFile,
	}
	official.InputFiles = append(official.InputFiles, *officialInputFiles...)
	official.InputFiles = append(official.InputFiles, *toolchainManifest)
	official.InputFiles = append(official.InputFiles, bootstrap.OutputFile)
	builtArchive = toolchain.Archive{
		ArchivePath: official.OutputFile,
	}

	cacheOk := false
	if config.doCache {
		_, cacheOk, err = official.CheckCache(*cacheDir)
		if err != nil {
			err = fmt.Errorf("failed to check official toolchain rpms cache, error:\n%w", err)
			return
		}
	}

	if cacheOk {
		logger.Log.Infof("Official toolchain rpms cache is valid, restoring.")
		err = official.RestoreFromCache(*cacheDir)
		if err != nil {
			err = fmt.Errorf("failed to restore official toolchain rpms from cache, error:\n%w", err)
			return
		}
	} else {
		if config.doDeltaBuild {
			//TODO Clean delta folder if not doing delta
			// Toolchain script expects rpms or empty files in a specific directory do do incremental builds
			err = official.PrepIncrementalRpms(*toolchainRpmDir, toolchainRPMs)
			if err != nil {
				err = fmt.Errorf("failed to prep delta rpms, error:\n%w", err)
				return
			}
		} else {
			// Remove any delta rpms from previous builds
			err = official.CleanIncrementalRpms()
			if err != nil {
				err = fmt.Errorf("failed to clean old delta rpms, error:\n%w", err)
				return
			}
		}
		builtRpms, err = official.BuildOfficialToolchainRpms()
		if err != nil {
			err = fmt.Errorf("failed to build official toolchain rpms, error:\n%w", err)
			return
		} else {
			_, err = official.AddToCache(*cacheDir)
			if err != nil {
				err = fmt.Errorf("failed to add official toolchain rpms to cache, error:\n%w", err)
				return
			}
		}

		var movedRpms []string
		movedRpms, err = official.TransferBuiltRpms()
		if err != nil {
			err = fmt.Errorf("failed to transfer built rpms, error:\n%w", err)
			return
		}
		builtRpms = append(builtRpms, movedRpms...)
	}
	return
}

func extractArchive(archive toolchain.Archive, toolchainRPMs []string) (extractedRpms []string, err error) {
	// Finalize the RPMs from the archive
	var missingFromArchive, missingFromManifest []string

	// Extract rpms
	extracated, err := archive.ExtractToolchainRpms(*toolchainRpmDir)
	if err != nil {
		err = fmt.Errorf("failed to extract official toolchain rpms, error:\n%w", err)
		return
	}
	for _, rpm := range extracated {
		extractedRpms = append(extractedRpms, fmt.Sprintf("Extracted: %s", rpm))
	}

	missingFromArchive, missingFromManifest, err = archive.ValidateArchiveContents(toolchainRPMs)
	if err != nil {
		err = fmt.Errorf("failed to validate toolchain archive contents, error:\n%w", err)
		return
	}
	if len(missingFromArchive) > 0 || len(missingFromManifest) > 0 {
		for _, line := range toolchain.CreateManifestMissmatchReport(missingFromArchive, missingFromManifest, *existingArchive, *toolchainManifest) {
			logger.Log.Warn(line)
		}
		err = fmt.Errorf("toolchain archive (%s) and manifest (%s) are missmatched", *existingArchive, *toolchainManifest)
		return
	}
	return
}
