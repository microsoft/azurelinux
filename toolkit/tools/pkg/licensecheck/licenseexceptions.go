// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"fmt"
	"regexp"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
)

type PkgExceptions struct {
	PackageName             string   `json:"PackageName"`
	IgnoredFilesRegexList   []string `json:"IgnoredFilesRegexList"`
	compiledIgnoreRegexList []*regexp.Regexp
}

type LicenseExceptions struct {
	PkgExceptions                 []PkgExceptions `json:"PkgExceptions"`
	GlobalExceptionsRegexList     []string        `json:"GlobalExceptionsRegexList"`
	compiledGlobalIgnoreRegexList []*regexp.Regexp
}

// ShouldIgnoreFile checks if the given file should be ignored based on the license exceptions
// - packageName: the name of the package as returned by rpm query '%{NAME}'
// - filePath: the path of the file to be checked as returned by rpm query '%{FILENAMES}'
func (l *LicenseExceptions) ShouldIgnoreFile(packageName, filePath string) bool {
	// Check if the file should be ignored globally
	for _, ignoredRegex := range l.compiledGlobalIgnoreRegexList {
		if ignoredRegex.MatchString(filePath) {
			return true
		}
	}

	// Check if the file should be ignored for the given package
	for _, exception := range l.PkgExceptions {
		if exception.PackageName == packageName {
			for _, ignoredRegex := range exception.compiledIgnoreRegexList {
				if ignoredRegex.MatchString(filePath) {
					return true
				}
			}
		}
	}
	return false
}

// LoadLicenseExceptions loads the license exceptions from the given .json file into a LicenseExceptions struct
func LoadLicenseExceptions(file string) (LicenseExceptions, error) {
	config := LicenseExceptions{}
	err := jsonutils.ReadJSONFile(file, &config)
	if err != nil {
		return LicenseExceptions{}, fmt.Errorf("failed to read license exceptions file:\n%w", err)
	}

	// Compile regexes for ignored files
	for i := range config.PkgExceptions {
		for j := range config.PkgExceptions[i].IgnoredFilesRegexList {
			regex, err := regexp.Compile(config.PkgExceptions[i].IgnoredFilesRegexList[j])
			if err != nil {
				return LicenseExceptions{}, fmt.Errorf("failed to compile regex for ignored file %s:\n%w", config.PkgExceptions[i].IgnoredFilesRegexList[j], err)
			}
			config.PkgExceptions[i].compiledIgnoreRegexList = append(config.PkgExceptions[i].compiledIgnoreRegexList, regex)
		}
	}

	// Compile regexes for global ignored files
	for i := range config.GlobalExceptionsRegexList {
		regex, err := regexp.Compile(config.GlobalExceptionsRegexList[i])
		if err != nil {
			return LicenseExceptions{}, fmt.Errorf("failed to compile regex for global ignored file %s:\n%w", config.GlobalExceptionsRegexList[i], err)
		}
		config.compiledGlobalIgnoreRegexList = append(config.compiledGlobalIgnoreRegexList, regex)
	}

	return config, nil
}
