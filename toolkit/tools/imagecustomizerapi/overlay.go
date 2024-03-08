// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type Overlay struct {
	LowerDir  string               `yaml:"lowerDir"`
	UpperDir  string               `yaml:"upperDir"`
	WorkDir   string               `yaml:"workDir"`
	Partition *IdentifiedPartition `yaml:"partition"`
}

func (o *Overlay) IsValid() error {
	// Validate paths for UpperDir, WorkDir, and LowerDir
	if err := validatePath(o.UpperDir); err != nil {
		return fmt.Errorf("upperDir '%s': %w", o.UpperDir, err)
	}
	if err := validatePath(o.WorkDir); err != nil {
		return fmt.Errorf("workDir '%s': %w", o.WorkDir, err)
	}
	if err := validatePath(o.LowerDir); err != nil {
		return fmt.Errorf("lowerDir '%s': %w", o.LowerDir, err)
	}

	// Check if UpperDir and WorkDir are identical
	if o.UpperDir == o.WorkDir {
		return fmt.Errorf("upperDir and workDir must be distinct, but both are '%s'", o.UpperDir)
	}

	// Check if UpperDir is a subdirectory of WorkDir or vice versa
	if isSubDirString(o.UpperDir, o.WorkDir) {
		return fmt.Errorf("upperDir '%s' should not be a subdirectory of workDir '%s'", o.UpperDir, o.WorkDir)
	}
	if isSubDirString(o.WorkDir, o.UpperDir) {
		return fmt.Errorf("workDir '%s' should not be a subdirectory of upperDir '%s'", o.WorkDir, o.UpperDir)
	}

	if o.Partition != nil {
		if err := o.Partition.IsValid(); err != nil {
			return fmt.Errorf("invalid partition in upperDir '%s', workDir '%s', lowerDir '%s': %w", o.UpperDir, o.WorkDir, o.LowerDir, err)
		}
	}

	return nil
}

func validatePath(path string) error {
	// Check if the path is empty
	if path == "" {
		return fmt.Errorf("path cannot be empty")
	}

	// Check if the path contains spaces
	if strings.Contains(path, " ") {
		return fmt.Errorf("path (%s) contains spaces and is invalid", path)
	}

	return nil
}

func isSubDirString(dir1, dir2 string) bool {
	// Ensure paths are cleaned and have consistent trailing slashes
	cleanDir1 := strings.TrimSuffix(dir1, "/") + "/"
	cleanDir2 := strings.TrimSuffix(dir2, "/") + "/"

	// Check if dir2 starts with dir1 (indicating a subdirectory)
	return cleanDir1 != cleanDir2 && strings.HasPrefix(cleanDir2, cleanDir1)
}
