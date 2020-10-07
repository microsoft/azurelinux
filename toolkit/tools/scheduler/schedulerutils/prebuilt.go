// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/rpm"
)

// isSRPMPrebuilt checks if an SRPM is prebuilt, returning true if so along with a slice of corresponding prebuilt RPMs.
func isSRPMPrebuilt(specFile, rpmDir, sourceDir, distTag string) (isPrebuilt bool, builtFiles []string) {
	builtFiles, err := rpmsProvidesBySpec(specFile, sourceDir, rpmDir, distTag)
	if err != nil {
		logger.Log.Warnf("Error processing SPEC (%s). Error: %v", specFile, err)
		return
	}

	isPrebuilt = findAllRPMS(builtFiles)
	return
}

// rpmsProvidesBySpec returns all RPMs produced from a SPEC file.
func rpmsProvidesBySpec(specFile, sourceDir, rpmDir, distTag string) (rpmsProvided []string, err error) {
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
		rpmFile := filepath.Join(rpmDir, fmt.Sprintf("%s.rpm", pkg))
		rpmsProvided = append(rpmsProvided, rpmFile)
	}

	return
}

// findAllRPMS returns true if all RPMs requested are found on disk.
func findAllRPMS(rpmsToFind []string) bool {
	for _, rpm := range rpmsToFind {
		isFile, _ := file.IsFile(rpm)

		if !isFile {
			logger.Log.Debugf("Did not find (%s)", rpm)
			return false
		}
	}

	return true
}
