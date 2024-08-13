// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

/*
Package licensecheckformat provides functions to handle the output of the licensecheck package.
*/
package licensecheckformat

import (
	"fmt"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"
)

// FormatResults formats the results of the search to a string. Results will be ordered as follows:
// - Packages with warnings only, sorted alphabetically
// - Packages with errors (and possibly warnings), sorted alphabetically
// If pedantic is true, warnings will be treated as errors.
func FormatResults(results []licensecheck.LicenseCheckResult, mode licensecheck.LicenseCheckMode) string {
	var sb strings.Builder
	_, warnings, errors := licensecheck.SortAndFilterResults(results, mode)

	if len(warnings) == 0 && len(errors) == 0 {
		return "No license issues found\n"
	}

	// Print warnings first, but only if they don't also have an error
	for _, result := range warnings {
		if result.HasWarningResult(mode) && !result.HasErrorResult(mode) {
			sb.WriteString(formatResult(result, mode))
		}
	}

	// Now print the errors
	for _, result := range errors {
		sb.WriteString(formatResult(result, mode))
	}

	return sb.String()
}

func formatResult(result licensecheck.LicenseCheckResult, mode licensecheck.LicenseCheckMode) string {
	badDocIsError := true
	badFileIsError := true
	dupIsError := false
	if mode == licensecheck.LicenseCheckModePedantic {
		dupIsError = true
	} else if mode == licensecheck.LicenseCheckModeWarnOnly {
		badDocIsError = false
		badFileIsError = false
	}

	var sb strings.Builder
	// Print errors first if they exist
	if result.HasErrorResult(mode) {
		sb.WriteString(fmt.Sprintf("ERROR: (%s) has license errors:\n", filepath.Base(result.RpmPath)))
		if badDocIsError && len(result.BadDocs) > 0 {
			sb.WriteString(fmt.Sprintf("\tbad %%doc files:\n\t\t%s\n", strings.Join(result.BadDocs, "\n\t\t")))
		}
		if badFileIsError && len(result.BadFiles) > 0 {
			sb.WriteString(fmt.Sprintf("\tbad general file:\n\t\t%s\n", strings.Join(result.BadFiles, "\n\t\t")))
		}
		if dupIsError && len(result.DuplicatedDocs) > 0 {
			sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
		}
	}
	// Now add warnings if they exist
	if result.HasWarningResult(mode) {
		sb.WriteString(fmt.Sprintf("WARN: (%s) has license warnings:\n", filepath.Base(result.RpmPath)))
		if !badDocIsError && len(result.BadDocs) > 0 {
			sb.WriteString(fmt.Sprintf("\tbad %%doc files:\n\t\t%s\n", strings.Join(result.BadDocs, "\n\t\t")))
		}
		if !badFileIsError && len(result.BadFiles) > 0 {
			sb.WriteString(fmt.Sprintf("\tbad general file:\n\t\t%s\n", strings.Join(result.BadFiles, "\n\t\t")))
		}
		if !dupIsError && len(result.DuplicatedDocs) > 0 {
			sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
		}
	}
	return sb.String()
}
