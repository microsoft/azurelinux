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

// HasBadResult returns true if the result contains at least one bad document or file.
func (r *LicenseCheckResult) HasBadResult() bool {
	return len(r.BadDocs) > 0 || len(r.BadFiles) > 0
}

// HasWarningResult returns true if the result contains at least one duplicated documents.
func (r *LicenseCheckResult) HasWarningResult() bool {
	return len(r.DuplicatedDocs) > 0
}

// SaveLicenseCheckResults saves a list of all warnings and errors to a json file.
func SaveLicenseCheckResults(savePath string, resultsList []LicenseCheckResult) error {
	// Create parent dir if missing
	err := os.MkdirAll(filepath.Dir(savePath), os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory for results file. Error:\n%w", err)
	}

	sortedList := SortAndFilterResults(resultsList)
	err = jsonutils.WriteJSONFile(savePath, sortedList)
	if err != nil {
		return fmt.Errorf("failed to save license check results. Error:\n%w", err)
	}
	return nil
}

// SortAndFilterResults returns a copy of the list that is sorted and contains only warnings and errors.
func SortAndFilterResults(results []LicenseCheckResult) (sortedList []LicenseCheckResult) {
	sortedList = make([]LicenseCheckResult, len(results))
	for i, result := range results {
		if result.HasBadResult() || result.HasWarningResult() {
			sortedList[i] = result
		}
	}
	sort.Slice(sortedList, func(i, j int) bool {
		return sortedList[i].RpmPath < sortedList[j].RpmPath
	})
	return sortedList
}
