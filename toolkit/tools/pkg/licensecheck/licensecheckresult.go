// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
)

// LicenseCheckResult is the result of a license check on an single RPM
type LicenseCheckResult struct {
	RpmPath        string   `json:"RpmPath"`
	PackageName    string   `json:"PackageName,omitempty"`
	BadDocs        []string `json:"BadDocs,omitempty"`
	BadFiles       []string `json:"BadFiles,omitempty"`
	DuplicatedDocs []string `json:"DuplicatedDocs,omitempty"`
}

// HasErrorResult returns true if the result contains at least one finding that should be treated as an error based on
// the provided mode.
func (r *LicenseCheckResult) HasErrorResult(mode LicenseCheckMode) (hasErrorResult bool) {
	switch mode {
	case LicenseCheckModeNone:
		return false
	case LicenseCheckModeWarnOnly:
		return false
	case LicenseCheckModePedantic:
		if len(r.DuplicatedDocs) > 0 {
			return true
		}
		fallthrough
	case LicenseCheckModeFatalOnly:
		return len(r.BadDocs) > 0 || len(r.BadFiles) > 0
	}

	return false
}

// HasWarningResult returns true if the result contains at least one finding that should be treated as a warning based on
// the provided mode.
func (r *LicenseCheckResult) HasWarningResult(mode LicenseCheckMode) bool {
	switch mode {
	case LicenseCheckModeNone:
		return false
	case LicenseCheckModePedantic:
		// Pedantic mode treats warnings as errors, so we never have warnings
		return false
	case LicenseCheckModeWarnOnly:
		// We are treating all findings as warnings
		if r.HasErrorResult(LicenseCheckModeFatalOnly) {
			return true
		}
		fallthrough
	case LicenseCheckModeFatalOnly:
		return len(r.DuplicatedDocs) > 0
	}

	return false
}

// SaveLicenseCheckResults saves a list of all warnings and errors to a json file.
func SaveLicenseCheckResults(savePath string, resultsList []LicenseCheckResult) error {
	// Create parent dir if missing
	err := os.MkdirAll(filepath.Dir(savePath), os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory for results file. Error:\n%w", err)
	}

	sortedListOfFindings, _, _ := SortAndFilterResults(resultsList, LicenseCheckModeDefault)
	err = jsonutils.WriteJSONFile(savePath, sortedListOfFindings)
	if err != nil {
		return fmt.Errorf("failed to save license check results. Error:\n%w", err)
	}
	return nil
}

// SortAndFilterResults sorts the provided input slice, then filters them into three categories: anyResult, warnings, and errors.
// The results slice passed to the function will also be sorted in-place. The mode flag will control how the results are filtered.
func SortAndFilterResults(results []LicenseCheckResult, mode LicenseCheckMode) (anyResult, warnings, errors []LicenseCheckResult) {
	// Sort the input
	sort.Slice(results, func(i, j int) bool {
		return results[i].RpmPath < results[j].RpmPath
	})

	anyResult = []LicenseCheckResult{}
	warnings = []LicenseCheckResult{}
	errors = []LicenseCheckResult{}
	for _, result := range results {
		if result.HasErrorResult(mode) || result.HasWarningResult(mode) {
			anyResult = append(anyResult, result)
		}

		if result.HasErrorResult(mode) {
			errors = append(errors, result)
		}

		if result.HasWarningResult(mode) {
			warnings = append(warnings, result)
		}
	}

	return anyResult, warnings, errors
}
