// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"

	"gopkg.in/alecthomas/kingpin.v2"

	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/installutils"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/rpm"
)

type srpmBuildStateJob struct {
	sourceDir string
	specFile  string
	srpm      string
}

const (
	defaultNodeToCheck = 0
	defaultWorkerCount = "10"
	emptyResult        = ""
)

var (
	app = kingpin.New("graphoptimizer", "A tool to optimize a package graph, marking nodes that do not need to be rebuilt.")

	inputGraphFile  = exe.InputFlag(app, "Path to the DOT graph file to optimize.")
	outputGraphFile = exe.OutputFlag(app, "Path to save the optimized DOT graph file.")

	pkgsToBuild         = app.Flag("packages", "Space seperated list of top-level packages that should be built. Omit for all packages.").String()
	pkgsToRebuild       = app.Flag("rebuild-packages", "Space seperated list of base package names packages that should be rebuilt.").String()
	pkgsToIgnore        = app.Flag("ignore-packages", "Space seperated list of base package names that should never be rebuilt (ie name of spec file).").String()
	imageConfig         = app.Flag("image-config-file", "Optional image config file to extract a package list from.").String()
	baseDirPath         = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	rpmDir              = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	macroDir            = app.Flag("macro-dir", "Directory containing rpm macros.").Default("").String()
	distTag             = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	invalidateDepChains = app.Flag("rebuild-missing-dep-chains", "If a package is built already, but its dependencies are not, rebuild the package anyways.").Bool()
	workers             = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Int()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	// Override the host's RPM config dir
	_, err := rpm.SetMacroDir(*macroDir)
	logger.PanicOnError(err, "Unable to set rpm macro directory (%s). Error: %v", *macroDir, err)

	pkgsToBuildSplit := exe.ParseListArgument(*pkgsToBuild)
	desiredPackages := make([]*pkgjson.PackageVer, len(pkgsToBuildSplit))
	for i, pkg := range pkgsToBuildSplit {
		logger.Log.Debugf("Adding requested package to desired list(%s)", pkg)
		desiredPackages[i] = &pkgjson.PackageVer{
			Name: pkg,
		}
	}

	if *imageConfig != "" {
		var packagesFromConfig []*pkgjson.PackageVer

		packagesFromConfig, err := readConfigFile(*imageConfig, *baseDirPath)
		logger.PanicOnError(err, "Unable to get list of packages from config (%s). Erorr: %v", *imageConfig, err)

		desiredPackages = append(desiredPackages, packagesFromConfig...)
	}

	packagesToRebuild := exe.ParseListArgument(*pkgsToRebuild)
	packagesToIgnore := exe.ParseListArgument(*pkgsToIgnore)

	err = optimizeGraph(*inputGraphFile, *outputGraphFile, *rpmDir, *distTag, desiredPackages, packagesToRebuild, packagesToIgnore, *invalidateDepChains, *workers)
	logger.PanicOnError(err, "Unable to optimize package graph (%s). Error: %v", *inputGraphFile, err)
}

// readConfigFile reads configuration file and returns a package list required for the said configuration
// Package list is assembled from packageList and KernelOptions.
func readConfigFile(configFile, baseDirPath string) (packageList []*pkgjson.PackageVer, err error) {
	cfg, err := configuration.LoadWithAbsolutePaths(configFile, baseDirPath)
	if err != nil {
		logger.Log.Errorf("Failed to load config file (%s) with base directory (%s) for package list generation", configFile, baseDirPath)
		return
	}

	packageList, err = installutils.PackageNamesFromConfig(cfg)
	// Add kernel packages from KernelOptions
	packageList = append(packageList, installutils.KernelPackages(cfg)...)

	return
}

func optimizeGraph(inputFile, outputFile, rpmDir, distTag string, desiredPackages []*pkgjson.PackageVer, packagesToRebuild []string, packagesToIgnore []string, invalidateDepChains bool, workers int) (err error) {
	const (
		goalNodeName   = "PackagesToBuild"
		strictGoalNode = true
	)

	pkgGraph := pkggraph.NewPkgGraph()

	err = pkggraph.ReadDOTGraphFile(pkgGraph, inputFile)
	if err != nil {
		return
	}

	// Add unresolved nodes for anything that has no local spec file
	for _, pkg := range desiredPackages {
		var lookup *pkggraph.LookupNode

		lookup, err = pkgGraph.FindBestPkgNode(pkg)
		if err != nil {
			return
		}
		if lookup == nil {
			// Create a new unresolved node
			logger.Log.Debugf("Requested to build an unknown package %s, adding unresolved node", pkg.Name)
			_, err = pkgGraph.AddPkgNode(pkg, pkggraph.StateUnresolved, pkggraph.TypeRemote, "<NO_SRPM_PATH>", "<NO_SPEC_PATH>", "<NO_SOURCE_PATH>", "<NO_ARCHITECTURE>", "<NO_REPO>")
			if err != nil {
				return
			}
		}
	}

	// Create a goal node
	goalNode, err := pkgGraph.AddGoalNode(goalNodeName, desiredPackages, strictGoalNode)
	if err != nil {
		return
	}

	// Create a sub graph that starts at the new goal node
	subGraph, err := pkgGraph.CreateSubGraph(goalNode)
	if err != nil {
		return
	}

	srpmToNodes := make(map[string][]*pkggraph.PkgNode)
	for _, pkgNode := range subGraph.AllBuildNodes() {
		// Only process nodes that are marked as to-be-built
		if pkgNode.Type != pkggraph.TypeBuild && pkgNode.State != pkggraph.StateBuild {
			continue
		}
		srpmToNodes[pkgNode.SrpmPath] = append(srpmToNodes[pkgNode.SrpmPath], pkgNode)
	}

	// Pass 1 - mark present sub packages
	logger.Log.Info("Pass 1: Detecting SRPMs that have already been fully built")
	validPrebuiltSRPMs := markPrebuiltPackages(srpmToNodes, rpmDir, distTag, packagesToRebuild, packagesToIgnore, workers)
	logger.Log.Debugf("Prebuilt SRPMs: %v", validPrebuiltSRPMs)

	// Pass 2 - if any nested build requirements are missing, rebuild the entire SRPM.
	// Allow the user to disable this as it may be over zealous for the user's needs.
	if invalidateDepChains {
		logger.Log.Info("Pass 2: Detecting inconsistent dependency chain build states")
		validPrebuiltSRPMs = invalidateIncompleteDependencyChains(subGraph, srpmToNodes, validPrebuiltSRPMs, packagesToIgnore)
	}

	logger.Log.Infof("Prebuilt SRPMs: %v", validPrebuiltSRPMs)

	err = pkggraph.WriteDOTGraphFile(subGraph, outputFile)
	return
}

// rpmsProvidesBySpec returns all RPMs produced from a SPEC file, relative to the RPM
// directory (i.e. prefixes the path with "%{ARCH}/")
func rpmsProvidesBySpec(specFile, sourceDir, distTag string) (rpmsProvided []string, err error) {
	const (
		// %{nvra} is the default query format, returns %{NAME}-%{VERSION}-%{REVISION}-%{ARCH}
		queryFormat = "%{ARCH}/%{nvra}\n"
	)

	defines := rpm.DefaultDefines()
	if distTag != "" {
		defines[rpm.DistTagDefine] = distTag
	}

	result, err := rpm.QuerySPECForBuiltRPMs(specFile, sourceDir, queryFormat, defines)
	if err != nil {
		return
	}

	for _, pkg := range result {
		rpmName := fmt.Sprintf("%s.rpm", pkg)
		rpmsProvided = append(rpmsProvided, rpmName)
	}

	return
}

// findAllRPMS returns true if all RPMs requested are found on disk.
func findAllRPMS(rpmDir string, rpmsToFind []string) bool {

	for _, rpm := range rpmsToFind {
		fullPath := filepath.Join(rpmDir, rpm)
		isFile, _ := file.IsFile(fullPath)

		if !isFile {
			logger.Log.Debugf("Did not find (%s) at (%s)", rpm, fullPath)
			return false
		}
	}

	return true
}

// markPrebuildSubPackages will update `pkgGraph`
func markPrebuiltPackages(srpmToNodes map[string][]*pkggraph.PkgNode, rpmDir, distTag string, packagesToRebuild []string, packagesToIgnore []string, workers int) (prebuiltSRPMs []string) {
	allJobs := make(chan *srpmBuildStateJob, len(srpmToNodes))
	builtSRPMResults := make(chan string, len(srpmToNodes))

	// Start the workers now so they begin processing jobs as jobs are buffered
	for i := 0; i < workers; i++ {
		go srpmBuildStateWorker(allJobs, builtSRPMResults, rpmDir, distTag, packagesToRebuild, packagesToIgnore)
	}

	for srpm, nodes := range srpmToNodes {
		// Since all nodes associated with a given SRPM should have the same
		// SPEC file and SOURCE dir, only check the first node for the information.
		if len(nodes) == 0 {
			logger.Log.Panicf("Invalid graph state: encountered SRPM with no associated nodes: (%s)", srpm)
		}

		job := &srpmBuildStateJob{
			sourceDir: nodes[defaultNodeToCheck].SourceDir,
			specFile:  nodes[defaultNodeToCheck].SpecPath,
			srpm:      srpm,
		}
		allJobs <- job
	}

	// Signal to the workers that there are no more new jobs
	close(allJobs)

	prebuiltSRPMs = make([]string, 0)
	for i := 0; i < len(srpmToNodes); i++ {
		builtSRPM := <-builtSRPMResults

		// Skip empty results
		if builtSRPM == emptyResult {
			continue
		}

		for _, n := range srpmToNodes[builtSRPM] {
			n.State = pkggraph.StateUpToDate
		}

		prebuiltSRPMs = append(prebuiltSRPMs, builtSRPM)
	}

	logger.Log.Infof("After removing missing packages, %d of %d SRPMs need to be rebuilt", len(srpmToNodes)-len(prebuiltSRPMs), len(srpmToNodes))

	return
}

func srpmBuildStateWorker(allJobs chan *srpmBuildStateJob, builtSRPMResults chan string, rpmDir, distTag string, packagesToRebuild []string, packagesToIgnore []string) {
	const specSuffix = ".spec"

	// On job failure or skip, continue to the next value in the channel.
allJobs:
	for job := range allJobs {
		logger.Log.Debugf("Scanning %s", job.specFile)
		specName := strings.TrimSuffix(filepath.Base(job.specFile), specSuffix)
		for _, pkg := range packagesToIgnore {
			if pkg == specName {
				logger.Log.Warnf("Marking missing package (%s) as ignored (always assume its built) per user request", pkg)
				builtSRPMResults <- job.srpm
				continue allJobs
			}
		}
		for _, pkg := range packagesToRebuild {
			if pkg == specName {
				logger.Log.Infof("Marking (%s) as rebuild per user request", pkg)
				builtSRPMResults <- emptyResult
				continue allJobs
			}
		}

		// Get a list of paths relative to RPMS/. Each path is prefixed with ${ARCH}/ already
		rpmsToCheck, err := rpmsProvidesBySpec(job.specFile, job.sourceDir, distTag)
		if err != nil {
			logger.Log.Warnf("Error processing SPEC (%s). Error: %v", job.specFile, err)
			builtSRPMResults <- emptyResult
			continue allJobs
		}

		//
		// For a package to be marked as built enforce that all subpackages provided by its SRPM are also present,
		// otherwise the build may be non-deterministic:
		//	- Given packages foo-devel.rpm, foo.rpm, bar.rpm, bar2.rpm
		// 		- bar.rpm and bar2.rpm needs foo-devel.rpm
		//  	- foo-devel.rpm is already built
		//  	- foo.rpm is not built
		//  - Seeing this, the orchestrator may build `bar`, then `foo`, then `bar2`
		//  	- `bar` would be built with the prebuilt `foo-devel.rpm`
		//  	- `foo*` packages would be rebuilt since `foo.rpm` was missing
		//      - `bar2` would be built with the *new* `foo-devel.rpm` package
		//	- Both `bar.rpm` and `bar2.rpm` should be built with the same `foo-devel.rpm` package,
		//    to avoid this, always rebuild `foo` if any of its packages are missing
		//
		foundAll := findAllRPMS(rpmDir, rpmsToCheck)
		if !foundAll {
			logger.Log.Debugf("Did not find all RPMs produced by (%s)", job.srpm)
			builtSRPMResults <- emptyResult
			continue allJobs
		}

		logger.Log.Debugf("Marking (%s) as already built", job.srpm)
		builtSRPMResults <- job.srpm
	}
}

// validateChain returns true if all nodes required to build `node` are UpToDate and do not need to be built.
func validateChain(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode) bool {
	var (
		pkgNode *pkggraph.PkgNode
		search  = traverse.BreadthFirst{}
		valid   = true
	)

	search.Walk(pkgGraph, node, func(n graph.Node, d int) bool {
		pkgNode = n.(*pkggraph.PkgNode)

		// Skip non-build nodes
		if pkgNode.Type != pkggraph.TypeBuild {
			return false
		}

		// If a package in the chain is marked for build,
		// stop the search and report the dependency chain is incomplete.
		if pkgNode.State == pkggraph.StateBuild {
			logger.Log.Warnf("Incomplete dependency chain for (%s) at (%s)", node.FriendlyName(), pkgNode.FriendlyName())
			valid = false
			return true
		}

		return false
	})

	return valid
}

// invalidateIncompleteDependencyChains will update `pkgGraph`
func invalidateIncompleteDependencyChains(pkgGraph *pkggraph.PkgGraph, srpmToNodes map[string][]*pkggraph.PkgNode, prebuiltSRPMs []string, packagesToIgnore []string) (validPrebuiltSRPMs []string) {
	for _, srpm := range prebuiltSRPMs {
		logger.Log.Debugf("Checking (%s) for incomplete dependency chain", srpm)

		if len(srpmToNodes[srpm]) == 0 {
			logger.Log.Panicf("Invalid graph state: encountered SRPM with no associated nodes: (%s)", srpm)
		}

		// Check if this SRPM has already be invalidated by a previous chain.
		//
		// All nodes should be in the same State after `markPrebuiltPackages` runs,
		// so just check the first to see if the SRPM was marked as present.
		node := srpmToNodes[srpm][defaultNodeToCheck]
		if node.State != pkggraph.StateUpToDate {
			logger.Log.Debugf("SRPM (%s) has already been marked as rebuild by a previously invalidated chain", srpm)
			continue
		}

		isValid := true
		for _, node := range srpmToNodes[srpm] {
			isValid = validateChain(pkgGraph, node)
			if !isValid {
				break
			}
		}

		// If we are ignoring the package, never mark it for rebuild even if its dependencies update
		if !isValid {
			specName := strings.TrimSuffix(filepath.Base(node.SpecPath), ".spec")
			for _, pkg := range packagesToIgnore {
				isValid = (pkg == specName)
				if isValid {
					logger.Log.Warnf("Marking out of date package (%s) as ignored (always assume its built) per user request", pkg)
					break
				}
			}
		}

		if isValid {
			validPrebuiltSRPMs = append(validPrebuiltSRPMs, srpm)
		} else {
			logger.Log.Debugf("Incomplete dependency chain for (%s)", srpm)
			for _, node := range srpmToNodes[srpm] {
				node.State = pkggraph.StateBuild
			}
		}
	}
	logger.Log.Infof("After removing out of date SRPMs, %d of %d SRPMs need to be rebuilt", len(srpmToNodes)-len(validPrebuiltSRPMs), len(srpmToNodes))
	return
}
