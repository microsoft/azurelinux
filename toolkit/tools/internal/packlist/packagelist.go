// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package packagelist

import (
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
)

// ParsePackageList will parse a string of packages.
// Duplicate entries in the string will be removed.
// If empty string is given, nil will be returned.
// Else, a map of [package name] -> [true] will be returned.
func ParsePackageList(packages string) (packageMap map[string]bool, err error) {
	timestamp.StartEvent("parse list", nil)
	defer timestamp.StopEvent(nil)

	if len(strings.TrimSpace(packages)) == 0 {
		return
	}

	packageMap = make(map[string]bool)
	packageList := strings.Fields(packages)

	for _, pkg := range packageList {
		packageMap[pkg] = true
	}

	return
}
