// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import "slices"

// Valid license check modes which controls the behavior of the license checker package when filtering issues.
// These are intended to be used as command line flags in addition to being used in code.
type LicenseCheckMode string

const (
	LicenseCheckModeNone      = LicenseCheckMode("none")     // Disable license checking
	LicenseCheckModeWarnOnly  = LicenseCheckMode("warn")     // Convert all findings into warnings
	LicenseCheckModeFatalOnly = LicenseCheckMode("fatal")    // Report critical errors, but allow warnings
	LicenseCheckModePedantic  = LicenseCheckMode("pedantic") // Convert all findings into errors

	LicenseCheckModeDefault = LicenseCheckModeFatalOnly
)

// ValidLicenseCheckModes is a list of all valid license check modes
var validLicenseCheckModes = []LicenseCheckMode{LicenseCheckModeNone, LicenseCheckModeWarnOnly, LicenseCheckModePedantic, LicenseCheckModeFatalOnly}

// IsValidLicenseCheckMode returns true if the given mode is a valid license check mode
func IsValidLicenseCheckMode(mode LicenseCheckMode) bool {
	return slices.Contains(validLicenseCheckModes, mode)
}

// ValidLicenseCheckModeStrings returns a list of all valid license check modes as strings for use with the command line
func ValidLicenseCheckModeStrings() (modes []string) {
	for _, mode := range validLicenseCheckModes {
		modes = append(modes, string(mode))
	}
	return modes
}
