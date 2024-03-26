// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package interfaceutils

import (
	"fmt"

//	packagelist "github.com/microsoft/azurelinux/toolkit/tools/internal/packlist"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"
	"github.com/microsoft/azurelinux/toolkit/tools/toolinterface/configutils"
)

var (
	azlSpecsDirs = [...] string {"SPECS", "SPECS-EXTENDED", "SPECS-SIGNED"}
	// get relevant configs
	toolkit_dir string
)

func BuildPackage(spec string) (err error) {

	configutils.PopulateConfigFromFile()
	toolkit_dir,_ = configutils.GetConfig("toolkit_root")

	fmt.Println("Building packages specs are (%s)", spec)

	// check specs exist
	specsDir, err := validateSpecExistance(spec)
	if err != nil {
		err = fmt.Errorf("failed to validate specs:\n%w", err)
		return err
	}

	// TODO: set sepcs dir in config

	// any other checks

	// build toolchain if required

	// put toolchain rpms into toolchain_archive and use it

	// build tools if required

	// set extra configs

	// show dependency graph - use graphanalytics tool

	// build package
	err = buildSpecs(spec, specsDir)
	if err != nil {
		err = fmt.Errorf("failed to build specs:\n%w", err)
		return err
	}

	// show output

	return
}

// validateSpecExistance checks if each spec in specList exists
// and assigns it the correct specsDir in which it exists
func validateSpecExistance(specList string) (specsDir string, err error) {
	fmt.Println("Checking if spec exists for (%s)", specList)
//	specMap, err := packagelist.ParsePackageList(*specList)
//	if err != nil {
//		err = fmt.Errorf("failed to parse package list file:\n%w", err)
//		return nil, err
//	}

	// TODO: currently, we have a limitation that all specs to be built must be present in the same specsDir
	var specMap = make(map[string]bool)
	for _, specsDir := range azlSpecsDirs {
		specFiles, err := specreaderutils.FindSpecFiles(specsDir, specMap)
		if err != nil {
			err = fmt.Errorf("failed to FindSpecFiles:\n%w", err)
			return "", err
		} else {
			fmt.Println("done with specreader, returned specFiles (%s)", specFiles)
			return specsDir, nil
		}
	}
	fmt.Println("done with specreader")
	return
}

func buildSpecs (specs, specsDir string) (err error) {
	// TODO: use a command builder
	err = execCommands("/usr/bin/make", "/home/neha/repos/test/CBL-Mariner/toolkit/", "build-packages", "SRPM_PACK_LIST=\"cracklib\"", "SPECS_DIR=/home/neha/repos/test/CBL-Mariner/SPECS2/")
	if err != nil {
		fmt.Println(err)
	}
	return
}
