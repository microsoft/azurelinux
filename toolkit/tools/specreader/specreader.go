// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/debugutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"github.com/jinzhu/copier"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultWorkerCount = "0"
	// rpmbuild usually sits doing nothing most of the time, so we can run multiple instances of it in parallel.
	defaultWorkerCountMultiplier = 8

	specExtractDir = "extracted_specs"
)

// parseResult holds the worker results from parsing a SPEC file.
type parseResult struct {
	packages []*pkgjson.Package
	err      error
}

var (
	app                     = kingpin.New("specreader", "A tool to parse spec dependencies into JSON")
	specsDir                = exe.InputDirFlag(app, "Directory to scan for SPECS")
	output                  = exe.OutputFlag(app, "Output file to export the JSON")
	workers                 = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	buildDir                = app.Flag("build-dir", "Directory to store temporary files while parsing.").String()
	srpmsDir                = app.Flag("srpm-dir", "Directory containing SRPMs.").Required().ExistingDir()
	rpmsDir                 = app.Flag("rpm-dir", "Directory containing built RPMs.").Required().ExistingDir()
	toolchainManifest       = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").ExistingFile()
	existingToolchainRpmDir = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	distTag                 = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	workerTar               = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.  If this argument is empty, specs will be parsed in the host environment.").ExistingFile()
	targetArch              = app.Flag("target-arch", "The architecture of the machine the RPM binaries run on").String()
	runCheck                = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()
	logFile                 = exe.LogFileFlag(app)
	logLevel                = exe.LogLevelFlag(app)
	profFlags               = exe.SetupProfileFlags(app)
	timestampFile           = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
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

	timestamp.BeginTiming("specreader", *timestampFile)
	defer timestamp.CompleteTiming()

	// rpmspec is fairly light and single-threaded, so we can run multiple instances of it in parallel.
	if *workers <= 0 {
		*workers = runtime.NumCPU() * defaultWorkerCountMultiplier
		logger.Log.Debugf("No worker count supplied, running %d workers per logical CPUs (total= %d).", defaultWorkerCountMultiplier, *workers)
	}

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	logger.PanicOnError(err, "Unable to read toolchain manifest file '%s': %s", *toolchainManifest, err)

	err = parseSRPMsWrapper(*buildDir, *srpmsDir, *rpmsDir, *srpmsDir, *existingToolchainRpmDir, *distTag, *output, *workerTar, toolchainRPMs, *workers, *runCheck)
	logger.PanicOnError(err)
}

// parseSRPMsWrapper wraps parseSPECs to conditionally run it inside a chroot.
// If workerTar is non-empty, parsing will occur inside a chroot, otherwise it will run on the host system.
func parseSRPMsWrapper(buildDir, inputSrpmsDir, rpmsDir, srpmsDir, toolchainDir, distTag, outputFile, workerTar string, toolchainRPMs []string, workers int, runCheck bool) (err error) {
	var (
		chroot      *safechroot.Chroot
		packageRepo *pkgjson.PackageRepo
	)

	if workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, err = createChroot(workerTar, buildDir, inputSrpmsDir)
		if err != nil {
			return
		}
		defer chroot.Close(leaveFilesOnDisk)
	}

	buildArch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	doParse := func() error {
		var parseError error

		logger.Log.Infof("Parsing specs in %s", inputSrpmsDir)

		if *targetArch == "" {
			packageRepo, parseError = parseSrpms(inputSrpmsDir, rpmsDir, srpmsDir, toolchainDir, distTag, buildArch, toolchainRPMs, workers, runCheck)
			if parseError != nil {
				err := fmt.Errorf("failed to parse native specs (%w)", parseError)
				return err
			}
		} else {
			packageRepo, parseError = parseSrpms(inputSrpmsDir, rpmsDir, srpmsDir, toolchainDir, distTag, *targetArch, toolchainRPMs, workers, runCheck)
			if parseError != nil {
				err := fmt.Errorf("failed to parse cross specs (%w)", parseError)
				return err
			}
		}

		return parseError
	}

	if chroot != nil {
		logger.Log.Info("Parsing SPECs inside a chroot environment")
		err = chroot.Run(doParse)
	} else {
		logger.Log.Info("Parsing SPECs in the host environment")
		err = doParse()
	}

	if err != nil {
		return
	}

	b, err := json.MarshalIndent(packageRepo, "", "  ")
	if err != nil {
		logger.Log.Error("Unable to marshal package info JSON")
		return
	}

	err = file.Write(string(b), outputFile)
	if err != nil {
		logger.Log.Errorf("Failed to write file (%s)", outputFile)
		return
	}

	return
}

// createChroot creates a chroot to parse SPECs inside of.
func createChroot(workerTar, buildDir, srpmsDir string) (chroot *safechroot.Chroot, err error) {
	const (
		chrootName       = "specparser_chroot"
		existingDir      = false
		leaveFilesOnDisk = false
	)

	// Mount the specs and srpms directories to an identical path inside the chroot.
	// Since specreader saves the full paths to specs in its output that grapher will then consume,
	// the pathing needs to be preserved from the host system.
	var extraDirectories []string

	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(srpmsDir, srpmsDir, "", safechroot.BindMountPointFlags, ""),
	}

	chrootDir := filepath.Join(buildDir, chrootName)
	chroot = safechroot.NewChroot(chrootDir, existingDir)

	err = chroot.Initialize(workerTar, extraDirectories, extraMountPoints)
	if err != nil {
		return
	}

	// If this is not a regular build then copy in all of the SPECs since there are no bind mounts.
	if !buildpipeline.IsRegularBuild() {
		dirsToCopy := []string{srpmsDir}
		for _, dir := range dirsToCopy {
			dirInChroot := filepath.Join(chroot.RootDir(), dir)
			err = directory.CopyContents(dir, dirInChroot)
			if err != nil {
				closeErr := chroot.Close(leaveFilesOnDisk)
				if closeErr != nil {
					logger.Log.Errorf("Failed to close chroot, err: %s", err)
				}
				return
			}
		}
	}

	return
}

// parseSPECs will parse all specs in specsDir and return a summary of the SPECs.
func parseSrpms(inputSrpmsDir, rpmsDir, srpmsDir, toolchainDir, distTag, arch string, toolchainRPMs []string, workers int, runCheck bool) (packageRepo *pkgjson.PackageRepo, err error) {
	var (
		packageList []*pkgjson.Package
		wg          sync.WaitGroup
		srpmFiles   []string
	)

	packageRepo = &pkgjson.PackageRepo{}

	// Find the filepath for each srpm in the input SRPMS directory.
	specSearch, err := filepath.Abs(filepath.Join(inputSrpmsDir, "*.src.rpm"))

	logger.Log.Infof("Searching for *.src.rpm files in %s", specSearch)

	if err == nil {
		srpmFiles, err = filepath.Glob(specSearch)
	}
	if err != nil {
		logger.Log.Errorf("Failed to find *.src.rpm files. Check that %s is the correct directory. Error: %v", *specsDir, err)
		return
	}

	logger.Log.Infof("Found %d *.src.rpm files", len(srpmFiles))
	tsRoot, _ := timestamp.StartEvent("parse specs", nil)
	defer timestamp.StopEvent(nil)

	results := make(chan *parseResult, len(srpmFiles))
	requests := make(chan string, len(srpmFiles))
	cancel := make(chan struct{})

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go readSRPMWorker(requests, results, cancel, &wg, distTag, rpmsDir, srpmsDir, toolchainDir, toolchainRPMs, runCheck, arch, tsRoot)
	}

	for _, srpmFile := range srpmFiles {
		requests <- srpmFile
	}

	close(requests)

	// Receive the parsed spec structures from the workers and place them into a list.
	for i := 0; i < len(srpmFiles); i++ {
		parseResult := <-results
		if parseResult.err != nil {
			err = parseResult.err
			close(cancel)
			break
		}
		packageList = append(packageList, parseResult.packages...)
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	if err != nil {
		return
	}

	packageRepo.Repo = packageList
	sortPackages(packageRepo)

	return
}

// sortPackages orders the package lists into reasonable and deterministic orders.
// Sort the main package list by "Name", "Version", "SRPM"
// Sort each nested Requires/BuildRequires by "Name", "Version"
func sortPackages(packageRepo *pkgjson.PackageRepo) {
	sort.Slice(packageRepo.Repo, func(i, j int) bool {
		iName := packageRepo.Repo[i].Provides.Name + packageRepo.Repo[i].Provides.Version + packageRepo.Repo[i].SrpmPath
		jName := packageRepo.Repo[j].Provides.Name + packageRepo.Repo[j].Provides.Version + packageRepo.Repo[j].SrpmPath
		return strings.Compare(iName, jName) < 0
	})

	for _, pkg := range packageRepo.Repo {
		sort.Slice(pkg.Requires, func(i, j int) bool {
			iName := pkg.Requires[i].Name + pkg.Requires[i].Version
			jName := pkg.Requires[j].Name + pkg.Requires[j].Version
			return strings.Compare(iName, jName) < 0
		})
		sort.Slice(pkg.BuildRequires, func(i, j int) bool {
			iName := pkg.BuildRequires[i].Name + pkg.BuildRequires[i].Version
			jName := pkg.BuildRequires[j].Name + pkg.BuildRequires[j].Version
			return strings.Compare(iName, jName) < 0
		})
	}
}

// readSRPMWorker is a goroutine that takes a full filepath to a spec file and scrapes it into the Specdef structure
// Concurrency is limited by the size of the semaphore channel passed in. Too many goroutines at once can deplete
// available filehandles.
func readSRPMWorker(requests <-chan string, results chan<- *parseResult, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, rpmsDir, srpmsDir, toolchainDir string, toolchainRPMs []string, runCheck bool, arch string, tsRoot *timestamp.TimeStamp) {
	const (
		emptyQueryFormat      = ``
		querySrpm             = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		queryProvidedPackages = `rpm %{ARCH}/%{nvra}.rpm\n[provides %{PROVIDENEVRS}\n][requires %{REQUIRENEVRS}\n][arch %{ARCH}\n]`
	)

	defer wg.Done()

	defines := rpm.DefaultDefinesWithDist(runCheck, distTag)

	var ts *timestamp.TimeStamp = nil
	for srpmfile := range requests {
		select {
		case <-cancel:
			logger.Log.Debug("Cancellation signal received")
			return
		default:
		}

		// Many code paths hit 'continue', finish timing those here.
		if ts != nil {
			timestamp.StopEvent(ts)
			ts = nil
		}
		ts, _ = timestamp.StartEvent(filepath.Base(srpmfile), tsRoot)

		result := &parseResult{}

		providerList := []*pkgjson.Package{}
		buildRequiresList := []*pkgjson.PackageVer{}

		specfile, err := extractSpecIntoFolder(srpmfile, specExtractDir)
		sourcedir := filepath.Dir(specfile)
		if err != nil {
			result.err = fmt.Errorf("failed to extract specfile from %s: %w", srpmfile, err)
			results <- result
			continue
		}

		logger.Log.Warnf("Done extracting specfile %s, now parsing", specfile)

		// Find the SRPM associated with the SPEC.
		srpmResults, err := rpm.QuerySPEC(specfile, sourcedir, querySrpm, arch, defines)
		if err != nil {
			result.err = fmt.Errorf("failed to query %s: %w", specfile, err)
			debugutils.WaitForUser("hello!")
			results <- result
			continue
		}

		logger.Log.Warnf("Found %d SRPMs for %s", len(srpmResults), specfile)

		srpmPath := filepath.Join(srpmsDir, srpmResults[0])

		logger.Log.Warnf("checking arch compatibility for %s", specfile)

		isCompatible, err := rpm.SpecArchIsCompatible(specfile, sourcedir, arch, defines)
		if err != nil {
			result.err = fmt.Errorf("failed to check arch compatibility for %s: %w", specfile, err)
			results <- result
			continue
		}

		if !isCompatible {
			logger.Log.Debugf(`Skipping (%s) since it cannot be built on current architecture.`, specfile)
			results <- result
			continue
		}

		logger.Log.Warnf("Q 1")

		// Find every package that the spec provides
		queryResults, err := rpm.QuerySPEC(specfile, sourcedir, queryProvidedPackages, arch, defines)
		if err == nil && len(queryResults) != 0 {
			providerList, err = parseProvides(rpmsDir, toolchainDir, toolchainRPMs, srpmPath, queryResults)
			if err != nil {
				result.err = fmt.Errorf("failed to parse provides for %s: %w", specfile, err)
				results <- result
				continue
			}
		}

		logger.Log.Warnf("Q 2")

		// Query the BuildRequires fields from this spec and turn them into an array of PackageVersions
		queryResults, err = rpm.QuerySPEC(specfile, sourcedir, emptyQueryFormat, arch, defines, rpm.BuildRequiresArgument)
		if err == nil && len(queryResults) != 0 {
			buildRequiresList, err = parsePackageVersionList(queryResults)
			if err != nil {
				result.err = fmt.Errorf("failed to parse build requires for %s: %w", specfile, err)
				results <- result
				continue
			}
		}

		logger.Log.Warnf("checking list")

		// Every package provided by a spec will have the same BuildRequires and SrpmPath
		for i := range providerList {
			providerList[i].SpecPath = specfile
			providerList[i].SourceDir = sourcedir
			providerList[i].Requires, err = condensePackageVersionArray(providerList[i].Requires, specfile)
			if err != nil {
				err = fmt.Errorf("failed to condense Requires for %s: %w", specfile, err)
				break
			}

			providerList[i].BuildRequires, err = condensePackageVersionArray(buildRequiresList, specfile)
			if err != nil {
				err = fmt.Errorf("failed to condense BuildRequires for %s: %w", specfile, err)
				break
			}
		}

		if err != nil {
			result.err = err
		} else {
			result.packages = providerList
		}

		// Submit the result to the main thread, the deferred function will clear the semaphore.
		results <- result
	}
	if ts != nil {
		timestamp.StopEvent(ts)
	}
}

// extractSpecIntoFolder extracts the spec file from the SRPM into a temporary folder. Returns an error if more than one
// spec file is found in the SRPM, or the folder already exists.
func extractSpecIntoFolder(srpmfile, specExtractDir string) (string, error) {
	targetDir := filepath.Join(specExtractDir, filepath.Base(srpmfile))

	// If the target directory already exists, its an error
	if exists, err := file.DirExists(targetDir); exists || err != nil {
		if err != nil {
			return "", fmt.Errorf("error checking for target directory %s: %w", targetDir, err)
		} else {
			return "", fmt.Errorf("target directory %s already exists", targetDir)
		}
	}

	// Create the target directory
	if err := os.MkdirAll(targetDir, 0755); err != nil {
		return "", fmt.Errorf("error creating target directory %s: %w", targetDir, err)
	}

	//Command
	program := "bash"
	args := []string{
		"-c",
		fmt.Sprintf("rpm2cpio %s | cpio -idvu *.spec *.macros", srpmfile),
	}
	_, stderr, err := shell.ExecuteInDirectory(targetDir, program, args...)
	if err != nil {
		return "", fmt.Errorf("error extracting spec file from SRPM (%s): %w", stderr, err)
	}

	// Find the spec file in the target directory and make sure we only  have one
	specfiles, err := filepath.Glob(filepath.Join(targetDir, "*.spec"))
	if err != nil {
		return "", fmt.Errorf("error finding spec file in target directory %s: %w", targetDir, err)
	}

	if len(specfiles) != 1 {
		return "", fmt.Errorf("expected one spec file in target directory %s, found %d", targetDir, len(specfiles))
	}

	return specfiles[0], nil
}

// parseProvides parses a newline separated list of Provides, Requires, and Arch from a single spec file.
// Several Provides may be in a row, so for each Provide the parser needs to look ahead for the first line that starts
// with a Require then ingest that line and every subsequent as a Requires until it sees a line that begins with Arch.
// Provide: package
// Require: requiresa = 1.0
// Require: requiresb
// Arch: noarch
// The return is an array of Package structures, one for each Provides in the spec (implicit and explicit).
func parseProvides(rpmsDir, toolchainDir string, toolchainRPMs []string, srpmPath string, list []string) (providerlist []*pkgjson.Package, err error) {
	var (
		reqlist      []*pkgjson.PackageVer
		packagearch  string
		rpmPath      string
		listEntry    []string
		sublistEntry []string
	)

	const (
		tag   = iota
		value = iota
	)

	listEntry = strings.SplitN(list[0], " ", 2)
	err = minSliceLength(listEntry, 2)
	if err != nil {
		return
	}

	if listEntry[tag] != "rpm" {
		err = fmt.Errorf("first element returned by rpmspec was not an rpm tag: %v", list)
		return
	}

	rpmPath = filepath.Join(rpmsDir, listEntry[value])

	logger.Log.Trace(list)
	for i := range list {
		listEntry = strings.SplitN(list[i], " ", 2)
		err = minSliceLength(listEntry, 1)
		if err != nil {
			return
		}

		if listEntry[tag] == "rpm" {
			logger.Log.Trace("rpm ", listEntry[value])
			// We will decide if this is a toolchain package later, and update the path if so.
			rpmPath = filepath.Join(rpmsDir, listEntry[value])
		} else if listEntry[tag] == "provides" {
			logger.Log.Trace("provides ", listEntry[value])
			for _, v := range list[i:] {
				sublistEntry = strings.SplitN(v, " ", 2)
				err = minSliceLength(sublistEntry, 2)
				if err != nil {
					return
				}

				if sublistEntry[tag] == "requires" {
					logger.Log.Trace("   requires ", sublistEntry[value])
					var requirePkgVers []*pkgjson.PackageVer
					requirePkgVers, err = parsePackageVersions(sublistEntry[value])
					if err != nil {
						return
					}
					filteredRequirePkgVers := filterOutDynamicDependencies(requirePkgVers)
					reqlist = append(reqlist, filteredRequirePkgVers...)
				} else if sublistEntry[tag] == "arch" {
					logger.Log.Trace("   arch ", sublistEntry[value])
					packagearch = sublistEntry[value]
					break
				}
			}

			var newProviderVer []*pkgjson.PackageVer
			newProviderVer, err = parsePackageVersions(listEntry[value])
			if err != nil {
				return
			}

			isToolchain := schedulerutils.IsReservedFile(rpmPath, toolchainRPMs)
			if isToolchain {
				rpmPath = convertToToolchainRpmPath(rpmPath, packagearch, toolchainDir)
			}

			providerPkgVer := &pkgjson.Package{
				Provides:     newProviderVer[0],
				SrpmPath:     srpmPath,
				RpmPath:      rpmPath,
				Architecture: packagearch,
				Requires:     reqlist,
			}

			providerlist = append(providerlist, providerPkgVer)
			reqlist = nil
		}
	}

	logger.Log.Tracef("Provider: %+v", providerlist)

	return
}

// parsePackageVersions takes a package name and splits it into a set of PackageVer structures.
// Normally a list of length 1 is returned, however parsePackageVersions is also responsible for
// identifying if the package name is an "or" condition and returning all options.
func parsePackageVersions(packagename string) (newpkgs []*pkgjson.PackageVer, err error) {
	const (
		NameField      = iota
		ConditionField = iota
		VersionField   = iota
	)

	packageSplit := strings.Split(packagename, " ")
	err = minSliceLength(packageSplit, 1)
	if err != nil {
		return
	}

	// If first character of the packagename is a "(" then its an "or" condition
	if packagename[0] == '(' {
		return parseOrCondition(packagename)
	}

	newpkg := &pkgjson.PackageVer{Name: packageSplit[NameField]}
	if len(packageSplit) == 1 {
		// Nothing to do, no condition or version was found.
	} else if packageSplit[ConditionField] != "or" {
		newpkg.Condition = packageSplit[ConditionField]
		newpkg.Version = packageSplit[VersionField]
	} else {
		// Replace the name with the first name that appears in (foo or bar)
		substr := packageSplit[NameField][1:]
		newpkg.Name = substr
	}

	newpkgs = append(newpkgs, newpkg)
	return
}

// parsePackageVersionList takes the output from rpmspec --buildrequires
// and parses it into an array of PackageVersion structures
func parsePackageVersionList(pkgList []string) (pkgVerList []*pkgjson.PackageVer, err error) {
	for _, pkgListEntry := range pkgList {
		var parsedPkgVers []*pkgjson.PackageVer
		parsedPkgVers, err = parsePackageVersions(pkgListEntry)
		if err != nil {
			return
		}
		pkgVerList = append(pkgVerList, parsedPkgVers...)
	}
	return
}

// condensePackageVersionArray deduplicates entries in an array of Package Versions
// and represents double conditionals in a single PackageVersion structure.
// If a non-blank package version is specified more than twice in a SPEC then return an error.
func condensePackageVersionArray(packagelist []*pkgjson.PackageVer, specfile string) (processedPkgList []*pkgjson.PackageVer, err error) {
	for _, pkg := range packagelist {
		nameMatch := false
		for i, processedPkg := range processedPkgList {
			if pkg.Name == processedPkg.Name {
				nameMatch = true
				if processedPkg.Version == "" {
					processedPkgList[i].Version = pkg.Version
					processedPkgList[i].Condition = pkg.Condition
					break
				} else if processedPkg.SVersion == "" {
					processedPkgList[i].SVersion = pkg.Version
					processedPkgList[i].SCondition = pkg.Condition
					break
				} else if processedPkg.Version == processedPkg.SVersion {
					processedPkgList[i].Version = pkg.Version
					processedPkgList[i].SVersion = pkg.Version
					processedPkgList[i].Condition = pkg.Condition
					processedPkgList[i].SCondition = pkg.Condition
					break
				} else {
					err = fmt.Errorf("spec (%s) attempted to set more than two conditions for package (%s)", specfile, processedPkg.Name)
					return
				}
			}
		}
		if !nameMatch {
			var processPkg pkgjson.PackageVer
			copier.Copy(&processPkg, pkg)
			processedPkgList = append(processedPkgList, &processPkg)
		}
	}
	return
}

// parseOrCondition splits a package name like (foo or bar) and returns both foo and bar as separate requirements.
func parseOrCondition(packagename string) (versions []*pkgjson.PackageVer, err error) {
	logger.Log.Warnf("'OR' clause found (%s), make sure both packages are available. Please refer to 'docs/how_it_works/3_package_building.md#or-clauses' for explanation of limitations.", packagename)
	packagename = strings.ReplaceAll(packagename, "(", "")
	packagename = strings.ReplaceAll(packagename, ")", "")

	packageSplit := strings.Split(packagename, " or ")
	err = minSliceLength(packageSplit, 1)
	if err != nil {
		return
	}

	versions = make([]*pkgjson.PackageVer, 0, len(packageSplit))
	for _, condition := range packageSplit {
		var parsedPkgVers []*pkgjson.PackageVer
		parsedPkgVers, err = parsePackageVersions(condition)
		if err != nil {
			return
		}
		versions = append(versions, parsedPkgVers...)
	}

	return
}

// minSliceLength checks that a string slice is >= a minimum length and returns an error
// if the condition is not met.
func minSliceLength(slice []string, minLength int) (err error) {
	if len(slice) < minLength {
		return fmt.Errorf("slice is not required length (minLength = %d) %+v", minLength, slice)
	}
	return
}

// filterOutDynamicDependencies removes dynamic RPM dependencies from pkgVers.
// These entries are automatically injected by RPM when processing an SRPM
// and represent an internal RPM feature requirement.
//
// For example if a SPEC uses a Lua scriplet, RPM will inject a requirement for
// `rpmlib(BuiltinLuaScripts)` so that future RPM invocations on the SRPM know
// what features it needs to properly handle the package.
//
// These dynamic dependencies are not backed by a real package or a provides, but
// are instead an internal notation of RPM itself. Filter these out from the list of
// requirements of actual packages.
func filterOutDynamicDependencies(pkgVers []*pkgjson.PackageVer) (filteredPkgVers []*pkgjson.PackageVer) {
	const dynamicDependencyPrefix = "rpmlib("
	for _, req := range pkgVers {
		if strings.HasPrefix(req.Name, dynamicDependencyPrefix) {
			logger.Log.Debugf("Ignoring dynamic dependency: %s", req.Name)
			continue
		}
		filteredPkgVers = append(filteredPkgVers, req)
	}

	return
}

// convertToToolchainRpmPath updates the RPM path to point the the toolchain directory rather than the normal out/RPMs
// directory
func convertToToolchainRpmPath(currentRpmPath, arch, toolchainDir string) (toolchainPath string) {
	rpmFileName := filepath.Base(currentRpmPath)
	toolchainPath = filepath.Join(toolchainDir, arch)
	toolchainPath = filepath.Join(toolchainPath, rpmFileName)
	logger.Log.Debugf("Toolchain changing '%s' to '%s'.", currentRpmPath, toolchainPath)
	return toolchainPath
}
