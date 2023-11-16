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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	packagelist "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packlist"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"github.com/jinzhu/copier"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	// Spaces added on purpose to simplify substring matching.
	andCondition  = " and "
	ifCondition   = " if "
	orCondition   = " or "
	withCondition = " with "
)

var (
	supportedBooleanConditions = []string{
		andCondition,
		ifCondition,
		orCondition,
		withCondition,
	}

	// Spaces added on purpose to simplify substring matching.
	unsupportedBooleanConditions = []string{
		" else ",
		" unless ",
		" without ",
	}
)

// parseResult holds the worker results from parsing a SPEC file.
type parseResult struct {
	packages []*pkgjson.Package
	err      error
}

const (
	defaultWorkerCount = "100"
)

var (
	app                     = kingpin.New("specreader", "A tool to parse spec dependencies into JSON")
	specsDir                = exe.InputDirFlag(app, "Directory to scan for SPECS")
	specListFile            = app.Flag("spec-list", "Path to a list of SPECs to parse. If empty will parse all SPECs.").ExistingFile()
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

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	logger.PanicOnError(err, "Unable to read toolchain manifest file '%s': %s", *toolchainManifest, err)

	// A parse list may be provided, if so only parse this subset.
	// If none is provided, parse all specs.
	specMap, err := packagelist.ParsePackageListFile(*specListFile)
	logger.PanicOnError(err)

	// Convert specsDir to an absolute path
	specsAbsDir, err := filepath.Abs(*specsDir)
	logger.PanicOnError(err, "Unable to get absolute path for specs directory '%s': %s", *specsDir, err)

	err = parseSPECsWrapper(*buildDir, specsAbsDir, *rpmsDir, *srpmsDir, *existingToolchainRpmDir, *distTag, *output, *workerTar, specMap, toolchainRPMs, *workers, *runCheck)
	logger.PanicOnError(err)
}

// parseSPECsWrapper wraps parseSPECs to conditionally run it inside a chroot.
// If workerTar is non-empty, parsing will occur inside a chroot, otherwise it will run on the host system.
func parseSPECsWrapper(buildDir, specsDir, rpmsDir, srpmsDir, toolchainDir, distTag, outputFile, workerTar string, specMap map[string]bool, toolchainRPMs []string, workers int, runCheck bool) (err error) {
	var (
		chroot      *safechroot.Chroot
		packageRepo *pkgjson.PackageRepo
	)

	if workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, err = createChroot(workerTar, buildDir, specsDir, srpmsDir)
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

		if *targetArch == "" {
			packageRepo, parseError = parseSPECs(specsDir, rpmsDir, srpmsDir, toolchainDir, distTag, buildArch, specMap, toolchainRPMs, workers, runCheck)
			if parseError != nil {
				err := fmt.Errorf("failed to parse native specs (%w)", parseError)
				return err
			}
		} else {
			packageRepo, parseError = parseSPECs(specsDir, rpmsDir, srpmsDir, toolchainDir, distTag, *targetArch, specMap, toolchainRPMs, workers, runCheck)
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
func createChroot(workerTar, buildDir, specsDir, srpmsDir string) (chroot *safechroot.Chroot, err error) {
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
		safechroot.NewMountPoint(specsDir, specsDir, "", safechroot.BindMountPointFlags, ""),
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
		dirsToCopy := []string{specsDir, srpmsDir}
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

func findSpecFiles(specsDir string, specMap map[string]bool) (specFiles []string, err error) {
	// Find the filepath for each spec in the SPECS directory.
	if len(specMap) == 0 {
		specSearch, err := filepath.Abs(filepath.Join(specsDir, "**/*.spec"))
		if err != nil {
			err = fmt.Errorf("invalid spec dir: '%s'. Error:\n%w", specsDir, err)
			return nil, err
		}
		specFiles, err = filepath.Glob(specSearch)
		if err != nil {
			err = fmt.Errorf("failed to find *.spec files. Check that '%s' is the correct directory. Error:\n%w", specsDir, err)
			return nil, err
		}
	} else {
		for specName := range specMap {
			specSearch := filepath.Join(specsDir, fmt.Sprintf("**/%s.spec", specName))
			matchingSpecFiles, err := filepath.Glob(specSearch)

			// If a SPEC is in the parse list, it should be parsed.
			if err != nil {
				err = fmt.Errorf("spec search failed on '%s'. Error:\n%w", specSearch, err)
				return nil, err
			}
			if len(matchingSpecFiles) != 1 {
				err = fmt.Errorf("unexpected number of matches '%d' for spec file '%s'", len(matchingSpecFiles), specName)
				return nil, err
			}
			specFiles = append(specFiles, matchingSpecFiles[0])
		}
	}
	return
}

// parseSPECs will parse all specs in specsDir and return a summary of the SPECs.
func parseSPECs(specsDir, rpmsDir, srpmsDir, toolchainDir, distTag, arch string, specMap map[string]bool, toolchainRPMs []string, workers int, runCheck bool) (packageRepo *pkgjson.PackageRepo, err error) {
	var (
		packageList []*pkgjson.Package
		wg          sync.WaitGroup
		specFiles   []string
	)

	packageRepo = &pkgjson.PackageRepo{}

	specFiles, err = findSpecFiles(specsDir, specMap)
	if err != nil {
		logger.Log.Errorf("Failed to find *.spec files. Check that %s is the correct directory. Error: %v", specsDir, err)
		return
	}

	tsRoot, _ := timestamp.StartEvent("parse specs", nil)
	defer timestamp.StopEvent(nil)

	results := make(chan *parseResult, len(specFiles))
	requests := make(chan string, len(specFiles))
	cancel := make(chan struct{})

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go readSpecWorker(requests, results, cancel, &wg, distTag, rpmsDir, srpmsDir, toolchainDir, toolchainRPMs, runCheck, arch, tsRoot)
	}

	for _, specFile := range specFiles {
		requests <- specFile
	}

	close(requests)

	// Receive the parsed spec structures from the workers and place them into a list.
	for i := 0; i < len(specFiles); i++ {
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

// readSpecWorker is a goroutine that takes a full filepath to a spec file and scrapes it into the Specdef structure
// Concurrency is limited by the size of the semaphore channel passed in. Too many goroutines at once can deplete
// available file handles.
func readSpecWorker(requests <-chan string, results chan<- *parseResult, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, rpmsDir, srpmsDir, toolchainDir string, toolchainRPMs []string, runCheck bool, arch string, tsRoot *timestamp.TimeStamp) {
	const (
		querySrpm             = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		queryProvidedPackages = `rpm %{ARCH}/%{nvra}.rpm\n[provides %{PROVIDENEVRS}\n][requires %{REQUIRENEVRS}\n][arch %{ARCH}\n]`
	)

	defer wg.Done()

	noCheckDefines := rpm.DefaultDefinesWithDist(false, distTag)
	checkDefines := rpm.DefaultDefinesWithDist(true, distTag)

	var ts *timestamp.TimeStamp = nil
	for specFile := range requests {
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
		ts, _ = timestamp.StartEvent(filepath.Base(specFile), tsRoot)

		providerList := []*pkgjson.Package{}
		sourceDir := filepath.Dir(specFile)
		testBuildRequiresList := []*pkgjson.PackageVer{}

		// Find the SRPM associated with the SPEC.
		srpmResults, err := rpm.QuerySPEC(specFile, sourceDir, querySrpm, arch, noCheckDefines, rpm.QueryHeaderArgument)
		if err != nil {
			sendEmptyResult(results, err)
			continue
		}

		srpmPath := filepath.Join(srpmsDir, srpmResults[0])

		isCompatible, err := rpm.SpecArchIsCompatible(specFile, sourceDir, arch, noCheckDefines)
		if err != nil {
			sendEmptyResult(results, err)
			continue
		}

		if !isCompatible {
			logger.Log.Debugf(`Skipping (%s) since it cannot be built on current architecture.`, specFile)
			sendEmptyResult(results, err)
			continue
		}

		// Find every package that the spec provides
		queryResults, err := rpm.QuerySPEC(specFile, sourceDir, queryProvidedPackages, arch, noCheckDefines, rpm.QueryBuiltRPMHeadersArgument)
		if err != nil {
			sendEmptyResult(results, err)
			continue
		}

		if len(queryResults) != 0 {
			providerList, err = parseProvides(rpmsDir, toolchainDir, toolchainRPMs, srpmPath, queryResults)
			if err != nil {
				sendEmptyResult(results, err)
				continue
			}
		}

		// Query the BuildRequires fields from this spec and turn them into an array of PackageVersions
		buildRequiresList, err := readBuildRequires(specFile, sourceDir, arch, noCheckDefines)
		if err != nil {
			sendEmptyResult(results, err)
			continue
		}

		specHasCheckSection, err := rpm.SpecHasCheckSection(specFile, sourceDir, arch, checkDefines)
		if err != nil {
			sendEmptyResult(results, err)
			continue
		}

		readTestDependencies := runCheck && specHasCheckSection
		if readTestDependencies {
			// Query the test BuildRequires fields from this spec and turn them into an array of PackageVersions
			testBuildRequiresList, err = readBuildRequires(specFile, sourceDir, arch, checkDefines)
			if err != nil {
				sendEmptyResult(results, err)
				continue
			}
		}

		// Every package provided by a spec will have the same BuildRequires and SrpmPath
		for _, provider := range providerList {
			provider.BuildRequires = buildRequiresList
			provider.SourceDir = sourceDir
			provider.SpecPath = specFile
			provider.TestRequires = testBuildRequiresList
			provider.RunTests = readTestDependencies
		}

		// Submit the result to the main thread, the deferred function will clear the semaphore.
		results <- &parseResult{packages: providerList}
	}
	if ts != nil {
		timestamp.StopEvent(ts)
	}
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

			reqlist, err = dedupPackageVersionArray(reqlist)
			if err != nil {
				err = fmt.Errorf("failed to dedup run-time PackageVer array for SRPM (%s):\n%w", srpmPath, err)
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

// parsePackageVersions takes a package string and splits it into a list of PackageVer structures.
// Normally a list of length 1 is returned, however parsePackageVersions is also responsible for
// identifying if the package name is an "or" condition and returning all options.
func parsePackageVersions(packageString string) (newPackages []*pkgjson.PackageVer, err error) {
	packageString = strings.TrimSpace(packageString)

	// If the first character of the packageString is a "(" then it's an "or" condition.
	if packageString[0] == '(' {
		return parseRichDependency(packageString)
	}

	pkgVer, err := pkgjson.PackageStringToPackageVer(packageString)
	if err != nil {
		return
	}

	newPackages = append(newPackages, pkgVer)
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

// dedupPackageVersionArray deduplicates entries in an array of Package Versions
// and represents double conditionals in a single PackageVersion structure.
// If a non-blank package version is specified more than twice, return an error.
func dedupPackageVersionArray(packagelist []*pkgjson.PackageVer) (processedPkgList []*pkgjson.PackageVer, err error) {
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
					err = fmt.Errorf("attempting to set more than two conditions for package (%s)", processedPkg.Name)
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

// parseRichDependency splits a package name like '(foo or bar)' and returns both foo and bar as separate requirements.
func parseRichDependency(richDependency string) (versions []*pkgjson.PackageVer, err error) {
	const documentationHint = "Please refer to 'docs/how_it_works/3_package_building.md#rich-dependencies' for explanation of limitations"

	// All single condition strings are surrounded by spaces to match full words.
	for _, singleCondition := range unsupportedBooleanConditions {
		if strings.Contains(richDependency, singleCondition) {
			err = fmt.Errorf("found unsupported boolean condition '%s' inside '%s'. %s", singleCondition, richDependency, documentationHint)
			return
		}
	}

	conditionsCount := 0
	// All single condition strings are surrounded by spaces to match full words.
	for _, singleCondition := range supportedBooleanConditions {
		conditionsCount += strings.Count(richDependency, singleCondition)
	}
	if conditionsCount > 1 {
		err = fmt.Errorf("found more than one boolean condition inside '%s'. %s", richDependency, documentationHint)
		return
	}

	richDependency = strings.ReplaceAll(richDependency, "(", "")
	richDependency = strings.ReplaceAll(richDependency, ")", "")

	packageStrings := []string{}
	// All single condition strings are surrounded by spaces to match full words.
	for _, singleCondition := range supportedBooleanConditions {
		if strings.Contains(richDependency, singleCondition) {
			packageStrings = strings.Split(richDependency, singleCondition)
			break
		}
	}
	err = minSliceLength(packageStrings, 2)
	if err != nil {
		return
	}

	switch {
	case strings.Contains(richDependency, andCondition) || strings.Contains(richDependency, orCondition) || strings.Contains(richDependency, withCondition):
		logger.Log.Warnf("Found a boolean condition '%s', make sure both packages are available. %s.", richDependency, documentationHint)
	case strings.Contains(richDependency, ifCondition):
		logger.Log.Warnf("Found a boolean condition '%s', make sure the packages on the left is available. %s.", richDependency, documentationHint)
		packageStrings = []string{packageStrings[0]}
	default:
		err = fmt.Errorf("found a unsupported boolean condition inside '%s'. %s", richDependency, documentationHint)
		return
	}

	versions = make([]*pkgjson.PackageVer, 0, len(packageStrings))
	for _, packageString := range packageStrings {
		pkgVer, err := pkgjson.PackageStringToPackageVer(packageString)
		if err != nil {
			return nil, err
		}

		versions = append(versions, pkgVer)
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

func readBuildRequires(specFile, sourceDir, arch string, defines map[string]string) (result []*pkgjson.PackageVer, err error) {
	const emptyQueryFormat = ``

	queryResults, err := rpm.QuerySPEC(specFile, sourceDir, emptyQueryFormat, arch, defines, rpm.BuildRequiresArgument)
	if err != nil {
		return
	}

	result, err = parsePackageVersionList(queryResults)
	if err != nil {
		return
	}

	result, err = dedupPackageVersionArray(result)
	if err != nil {
		err = fmt.Errorf("failed to dedup build-time PackageVer array for spec (%s):\n%w", specFile, err)
	}

	return
}

func sendEmptyResult(results chan<- *parseResult, err error) {
	results <- &parseResult{err: err}
}
