// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkgjson"
	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	logger.Log.SetLevel(logrus.FatalLevel)
	os.Exit(m.Run())
}

// Make a "local" package of the given name. Each package with the same pkgName will share the same
// requires, srpmpath, etc. The subPkgName is used to differentiate multiple run-nodes for each
// package. The buildRequires should be common across all packages with the same pkgName.
func makePackage(pkgName, subPkgName string, buildRequires []*pkgjson.PackageVer) *pkgjson.Package {
	// Create a package with the given name and version
	pkg := &pkgjson.Package{
		Provides: &pkgjson.PackageVer{
			Name:    subPkgName,
			Version: "1.0",
		},
		SrpmPath:      pkgName + ".src.rpm",
		RpmPath:       pkgName + ".rpm",
		SourceDir:     pkgName + "-src",
		SpecPath:      pkgName + ".spec",
		Architecture:  "x86_64",
		IsToolchain:   false,
		RunTests:      true,
		BuildRequires: buildRequires,
	}

	return pkg
}

// A very simple test case to validate that the test framework is working
func TestValidateFramework(t *testing.T) {
	testRepo := &pkgjson.PackageRepo{
		Repo: []*pkgjson.Package{
			makePackage("pkg1", "pkg1-a", nil),
			makePackage("pkg1", "pkg1-b", nil),
		},
	}
	depGraph := pkggraph.NewPkgGraph()
	err := populateGraph(depGraph, testRepo)
	require.NoError(t, err)

	// Validate that the graph is not empty
	require.Equal(t, 2, len(depGraph.AllRunNodes()))
	require.Equal(t, 2, len(depGraph.AllBuildNodes()))
}

// Load a specially crafted repo containing several sub-packages of a single SRPM, and two malicious
// packages that try to pollute the available remote dependencies. The test will check if the various build
// nodes of the sub-package SRPM are all using the same set of dependencies. The other packages will add
// new remote nodes to the graph since they may not be satisfied by the already existing nodes. Once
// this happens, the sub-package build nodes may start using the "better" dependencies, which is not what we want.
func TestScenarioMultiRemoteProvides(t *testing.T) {
	anyVerBr := []*pkgjson.PackageVer{
		{
			Name:       "build-req",
			Version:    "",
			Condition:  "",
			SVersion:   "",
			SCondition: "",
		},
	}
	lowVerBr := []*pkgjson.PackageVer{
		{
			Name:       "build-req",
			Version:    "1.0",
			Condition:  "<",
			SVersion:   "",
			SCondition: "",
		},
	}
	highVerBr := []*pkgjson.PackageVer{
		{
			Name:       "build-req",
			Version:    "2.0",
			Condition:  ">",
			SVersion:   "",
			SCondition: "",
		},
	}

	// Define the test repo
	testRepo := pkgjson.PackageRepo{
		Repo: []*pkgjson.Package{
			makePackage("pkg1", "pkg1-a", anyVerBr),
			makePackage("other-pkg-1", "other-pkg-1", lowVerBr),
			makePackage("pkg1", "pkg1-b", anyVerBr),
			makePackage("other-pkg-2", "other-pkg-2", highVerBr),
			makePackage("pkg1", "pkg1-c", anyVerBr),
		},
	}

	// The graph library is non-deterministic (likely due to the use of maps), so to accurately catch the
	// counter example we need to run the test multiple times. Experimentally, the test fails after about
	// 10 runs (p=0.1), so with 1000 runs the probability of false negatives is 0.9^1000 ~= 1.7E-46 (ie very
	// small).
	const numRuns = 1000
	for i := 0; i < numRuns; i++ {
		// Create the dependency graph
		depGraph := pkggraph.NewPkgGraph()
		err := populateGraph(depGraph, &testRepo)
		require.NoError(t, err)

		// Check our invariants
		actualDepsUsed := make(map[pkgjson.PackageVer]bool)
		buildNodes := depGraph.AllBuildNodes()
		for _, buildNode := range buildNodes {

			// Only care about the pkg1 build nodes
			if buildNode.SrpmPath != "pkg1.src.rpm" {
				continue
			}

			dependencies := depGraph.From(buildNode.ID())

			for dependencies.Next() {
				dep := dependencies.Node().(*pkggraph.PkgNode)
				// Add to the set
				actualDepsUsed[*dep.VersionedPkg] = true
			}
		}
		// Now check the map, if there is more than one entry something is wrong
		if len(actualDepsUsed) > 1 {
			t.Error("Build deps:")
			for dep := range actualDepsUsed {
				t.Logf("\t%s", dep)
			}
			assert.FailNowf(t, "Multiple dependencies used in a single build node", "Failed after %d runs", i+1)
		}
	}
}
