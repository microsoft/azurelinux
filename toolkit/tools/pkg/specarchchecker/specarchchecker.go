// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for filtering specs by architecture.

package specarchchecker

import (
	"fmt"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	simplechroottool "github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/simplechroottool"
)

type ArchChecker struct {
	*simplechroottool.SimpleChrootTool
}

const chrootName = "specarchchecker_chroot"

// New creates an unitialized RPMs snapshot generator.
func New(buildDirPath, workerTarPath string) *ArchChecker {
	return &ArchChecker{
		SimpleChrootTool: &simplechroottool.SimpleChrootTool{
			BuildDirPath:  buildDirPath,
			WorkerTarPath: workerTarPath,
		},
	}
}

// GenerateSnapshot generates a snapshot of all packages built from the specs inside the input directory.
func (a *ArchChecker) FilterSpecsByArch(specsDirPath, distTag string, specFiles []string) (validSpecs []string, err error) {
	err = a.InitializeChroot(chrootName, specsDirPath)
	if err != nil {
		return
	}
	defer a.CleanUp()

	logger.Log.Infof("Filtering spec list in (%s).", specsDirPath)
	logger.Log.Debugf("Distribution tag: %s.", distTag)
	logger.Log.Debugf("Input list: %v.", specFiles)

	err = a.Chroot.Run(func() error {
		var runErr error
		validSpecs, runErr = a.filterListInChroot(distTag, specFiles)
		return runErr
	})
	if err != nil {
		return
	}

	return
}

func (a *ArchChecker) buildAllSpecsListFromNames(specNames []string) (specPaths []string, err error) {
	for _, specName := range specNames {
		var fullSpecPath []string
		specFilesGlob := filepath.Join(a.ChrootSpecDir, "**", fmt.Sprintf("%s.spec", specName))

		fullSpecPath, err = filepath.Glob(specFilesGlob)
		if err != nil {
			err = fmt.Errorf("failed while trying to enumerate all spec files with (%s). Error: %w", specFilesGlob, err)
			return
		}
		if len(fullSpecPath) != 1 {
			err = fmt.Errorf("expected to find exactly one spec file with (%s). Found %d", specFilesGlob, len(fullSpecPath))
			return
		}

		specPaths = append(specPaths, fullSpecPath[0])
	}

	return
}

func (a *ArchChecker) filterListInChroot(distTag string, specFileNames []string) (filteredSpecNames []string, err error) {
	defines := a.BuildDefines(distTag)
	specPaths, err := a.buildAllSpecsListFromNames(specFileNames)
	if err != nil {
		err = fmt.Errorf("failed to translate names to specs inside (%s). Error: %w", a.ChrootSpecDir, err)
		return
	}
	logger.Log.Debugf("Got specs: %v.", specPaths)
	filteredSpecs, err := a.BuildCompatibleSpecsList(specPaths, defines)
	if err != nil {
		err = fmt.Errorf("failed to retrieve a list of compatible  specs inside (%s). Error: %w", a.ChrootSpecDir, err)
		return
	}
	logger.Log.Debugf("Got filtered specs: %v.", filteredSpecs)

	for _, filteredSpec := range filteredSpecs {
		// We only want the base name of the spec file, without the .spec extension.
		specName := filepath.Base(filteredSpec)
		specName = strings.TrimSuffix(specName, ".spec")
		filteredSpecNames = append(filteredSpecNames, specName)
	}

	return
}
