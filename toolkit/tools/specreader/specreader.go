// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/rpm"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkgjson"
)

const (
	defaultWorkerCount = "10"
)

var (
	app      = kingpin.New("specreader", "A tool to parse spec dependencies into JSON")
	dir      = exe.InputDirFlag(app, "Directory to scan for SPECS")
	output   = exe.OutputFlag(app, "Output file to export the JSON")
	workers  = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	srpmDir  = app.Flag("srpm-dir", "Directory containing SRPMs.").Required().ExistingDir()
	macroDir = app.Flag("macro-dir", "Directory containing rpm macros.").Default("").String()
	distTag  = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	var (
		packageRepo pkgjson.PackageRepo
		packageList []*pkgjson.Package
		wg          sync.WaitGroup
		specFiles   []string
		err         error
	)

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	// Override the host's RPM config dir
	_, err = rpm.SetMacroDir(*macroDir)
	logger.PanicOnError(err, "Unable to set rpm macro directory (%s). Error: %v", *macroDir, err)

	// Find the filepath for each spec in the SPECS directory.
	specsearch, err := filepath.Abs(filepath.Join(*dir, "**/*.spec"))
	if err == nil {
		specFiles, err = filepath.Glob(specsearch)
	}
	if err != nil {
		logger.Log.Panicf("Failed to find *.spec files. Check that %s is the correct directory. Error: %v", *dir, err)
	}

	ch := make(chan []*pkgjson.Package)
	sem := make(chan int, *workers)

	for _, file := range specFiles {
		wg.Add(1)
		go readspec(file, *distTag, *srpmDir, &wg, ch, sem)
	}

	// Set a goroutine to wait for all workers to finish so it can clean up the channel.
	go func() {
		wg.Wait()
		close(ch)
	}()

	// Receive the parsed spec structures from the workers and place them into a list.
	for specparsed := range ch {
		packageList = append(packageList, specparsed...)
	}

	packageRepo.Repo = packageList
	sortPackages(&packageRepo)
	b, err := json.MarshalIndent(&packageRepo, "", "  ")
	if err != nil {
		logger.Log.Panic("Unable to marshal package info JSON. Error: ", err)
	}

	err = file.Write(string(b), *output)
	if err != nil {
		logger.Log.Panicf("Failed to write file (%s). Error: %v", *output, err)
	}
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

// readspec is a goroutine that takes a full filepath to a spec file and scrapes it into the Specdef structure
// Concurrency is limited by the size of the semaphore channel passed in. Too many goroutines at once can deplete
// available filehandles.
func readspec(specfile, distTag, srpmDir string, wg *sync.WaitGroup, ch chan []*pkgjson.Package, sem chan int) {
	const (
		emptyQueryFormat      = ""
		queryProvidedPackages = `srpm %{NAME}-%{VERSION}-%{RELEASE}.src.rpm\n[provides %{PROVIDENEVRS}\n][requires %{REQUIRENEVRS}\n][arch %{ARCH}\n]`
	)

	var (
		sourcedir         string
		results           []string
		providerList      []*pkgjson.Package
		buildRequiresList []*pkgjson.PackageVer
		err               error
	)

	sourcedir = filepath.Dir(specfile)
	defines := rpm.DefaultDefines()
	defines[rpm.DistTagDefine] = distTag

	sem <- 1

	// Clear the semaphore and signal the wait group whenever the function returns.
	defer func() {
		<-sem
		wg.Done()
	}()

	// Sanity check that rpmspec can read the spec file so we dont flood the log with warning if it cant.
	_, err = rpm.QuerySPEC(specfile, sourcedir, emptyQueryFormat, defines)
	if err != nil {
		logger.Log.Warnf(`rpmspec could not parse %s`, specfile)
		return
	}

	// Find every package that the spec provides
	results, err = rpm.QuerySPEC(specfile, sourcedir, queryProvidedPackages, defines)
	if err == nil && len(results) != 0 {
		providerList = parseProvides(srpmDir, results)
	}

	// Query the BuildRequires fields from this spec and turn them into an array of PackageVersions
	results, err = rpm.QuerySPEC(specfile, sourcedir, emptyQueryFormat, defines, rpm.BuildRequiresArgument)
	if err == nil && len(results) != 0 {
		buildRequiresList = parsePackageVersionList(results)
	}

	// Every package provided by a spec will have the same BuildRequires and SrpmPath
	for i := range providerList {
		providerList[i].SpecPath = specfile
		providerList[i].SourceDir = sourcedir
		providerList[i].Requires = condensePackageVersionArray(providerList[i].Requires, specfile)
		providerList[i].BuildRequires = condensePackageVersionArray(buildRequiresList, specfile)
	}

	// Submit the result to the main thread, the defered function will clear the semaphore.
	ch <- providerList
}

// parseProvides parses a newline separated list of Provides, Requires, and Arch from a single spec file.
// Several Provides may be in a row, so for each Provide the parser needs to look ahead for the first line that starts
// with a Require then ingest that line and every subsequent as a Requires until it sees a line that begins with Arch.
// Provide: package
// Require: requiresa = 1.0
// Require: requiresb
// Arch: noarch
// The return is an array of Package structures, one for each Provides in the spec (implicit and explicit).
func parseProvides(srpmDir string, list []string) (providerlist []*pkgjson.Package) {
	var (
		reqlist      []*pkgjson.PackageVer
		packagearch  string
		srpmPath     string
		listEntry    []string
		sublistEntry []string
	)

	const (
		tag   = iota
		value = iota
	)

	listEntry = minArrayLength(strings.SplitN(list[0], " ", 2), 2)
	if listEntry[tag] == "srpm" {
		srpmPath = filepath.Join(srpmDir, listEntry[value])
	} else {
		logger.Log.Panic("First element returned by rpmspec was not an srpm tag: ", list)
	}

	logger.Log.Trace(list)
	for i := range list {
		listEntry = minArrayLength(strings.SplitN(list[i], " ", 2), 1)

		if listEntry[tag] == "provides" {
			logger.Log.Trace("provides ", listEntry[value])
			for _, v := range list[i:] {
				sublistEntry = minArrayLength(strings.SplitN(v, " ", 2), 2)
				if sublistEntry[tag] == "requires" {
					logger.Log.Trace("   requires ", sublistEntry[value])
					requirePkgVers := parsePackageVersions(sublistEntry[value])
					filteredRequirePkgVers := filterOutDynamicDependencies(requirePkgVers)
					reqlist = append(reqlist, filteredRequirePkgVers...)
				} else if sublistEntry[tag] == "arch" {
					logger.Log.Trace("   arch ", sublistEntry[value])
					packagearch = sublistEntry[value]
					break
				}
			}
			newProviderVer := parsePackageVersions(listEntry[value])[0]
			providerlist = append(providerlist, &pkgjson.Package{Provides: newProviderVer, SrpmPath: srpmPath, Architecture: packagearch, Requires: reqlist})
			reqlist = nil
		}
	}

	logger.Log.Tracef("Provider: %+v", providerlist)

	return
}

// parsePackageVersions takes a package name and splits it into a set of PackageVer structures.
// Normally a list of length 1 is returned, however parsePackageVersions is also responsible for
// identifying if the package name is an "or" condition and returning all options.
func parsePackageVersions(packagename string) (newpkgs []*pkgjson.PackageVer) {
	const (
		NameField      = iota
		ConditionField = iota
		VersionField   = iota
	)

	packageSplit := minArrayLength(strings.Split(packagename, " "), 1)

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

	return append(newpkgs, newpkg)
}

// parsePackageVersionList takes the output from rpmspec --buildrequires
// and parses it into an array of PackageVersion structures
func parsePackageVersionList(pkgList []string) (pkgVerList []*pkgjson.PackageVer) {
	for _, pkgListEntry := range pkgList {
		pkgVerList = append(pkgVerList, parsePackageVersions(pkgListEntry)...)
	}
	return
}

// condensePackageVersionArray deduplicates entries in an array of Package Versions
// and represents double conditionals in a single PackageVersion structure.
// If a non-blank package version is specified more than twice in a SPEC then panic.
func condensePackageVersionArray(packagelist []*pkgjson.PackageVer, specfile string) (processedPkgList []*pkgjson.PackageVer) {
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
					logger.Log.Panicf("Spec '%s' attempted to set more than two conditions for package '%s'.", specfile, processedPkg.Name)
				}
			}
		}
		if nameMatch == false {
			processedPkgList = append(processedPkgList, pkg)
		}
	}
	return
}

// parseOrCondition splits a package name like (foo or bar) and returns both foo and bar as separate requirements.
func parseOrCondition(packagename string) (versions []*pkgjson.PackageVer) {
	logger.Log.Warnf("'OR' clause found (%s), make sure both packages are available. Please refer to 'docs/how_it_works/3_package_building.md#or-clauses' for explanation of limitations.", packagename)
	packagename = strings.ReplaceAll(packagename, "(", "")
	packagename = strings.ReplaceAll(packagename, ")", "")
	packageSplit := minArrayLength(strings.Split(packagename, " or "), 1)
	versions = make([]*pkgjson.PackageVer, 0, len(packageSplit))
	for _, condition := range packageSplit {
		versions = append(versions, parsePackageVersions(condition)...)
	}
	return versions
}

// minArrayLength checks that a string array is >= a minimum length and panics
// explicitly if the condition is not met rather than letting an index into the array
// crash later.
func minArrayLength(array []string, minLength int) []string {
	if len(array) < minLength {
		logger.Log.Panicf("Array not required length (minLength = %d) %+v", minLength, array)
	}
	return array
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
