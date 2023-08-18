// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package packagelist

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

// ParsePackageListFile will parse a list of packages to pack or parse, if one is specified.
// Duplicate list entries in the file will be removed.
// If no path is specified, nil will be returned.
// A set of [package name] -> [true] will be returned.
func ParsePackageListFile(packageListFile string) (packageList map[string]bool, err error) {
	timestamp.StartEvent("parse list", nil)
	defer timestamp.StopEvent(nil)

	if packageListFile == "" {
		return
	}

	packageList = make(map[string]bool)

	file, err := os.Open(packageListFile)
	if err != nil {
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			packageList[line] = true
		}
	}

	if len(packageList) == 0 {
		err = fmt.Errorf("cannot have empty pack list (%s)", packageListFile)
	}

	return
}
