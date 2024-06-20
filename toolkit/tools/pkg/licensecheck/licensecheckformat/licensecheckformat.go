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
func FormatResults(results []licensecheck.LicenseCheckResult, pedantic bool) string {
	var sb strings.Builder
	filteredResults := licensecheck.SortAndFilterResults(results)

	// Print warnings first, but only if they don't also have an error
	if !pedantic {
		for _, result := range filteredResults {
			if result.HasWarningResult() && !result.HasBadResult() {
				sb.WriteString(formatWarning(result))
			}
		}
	}

	// Now print the errors
	for _, result := range filteredResults {
		if result.HasBadResult() || (pedantic && result.HasWarningResult()) {
			sb.WriteString(formatError(result, pedantic))
			if !pedantic && result.HasWarningResult() {
				// If pedantic was set, the warning was already printed as an error.
				// Otherwise print the warning now.
				sb.WriteString(formatWarning(result))
			}
		}
	}

	return sb.String()
}

func formatWarning(result licensecheck.LicenseCheckResult) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("WARN: (%s) has license warnings:\n", filepath.Base(result.RpmPath)))
	sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
	return sb.String()
}

func formatError(result licensecheck.LicenseCheckResult, pedantic bool) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("ERROR: (%s) has license errors:\n", filepath.Base(result.RpmPath)))
	if len(result.BadDocs) > 0 {
		sb.WriteString(fmt.Sprintf("\tbad %%doc files:\n\t\t%s\n", strings.Join(result.BadDocs, "\n\t\t")))
	}
	if len(result.BadFiles) > 0 {
		sb.WriteString(fmt.Sprintf("\tbad general file:\n\t\t%s\n", strings.Join(result.BadFiles, "\n\t\t")))
	}
	if pedantic && len(result.DuplicatedDocs) > 0 {
		sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
	}
	return sb.String()
}
