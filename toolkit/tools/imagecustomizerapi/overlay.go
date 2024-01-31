// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type Overlay struct {
	LowerDir  string           `yaml:"LowerDir"`
	UpperDir  string           `yaml:"UpperDir"`
	WorkDir   string           `yaml:"WorkDir"`
	Partition *VerityPartition `yaml:"Partition"`
}

func (o *Overlay) IsValid() error {
	// Validate paths for UpperDir, WorkDir, and LowerDir
	if err := validatePath(o.UpperDir); err != nil {
		return fmt.Errorf("UpperDir: %v", err)
	}
	if err := validatePath(o.WorkDir); err != nil {
		return fmt.Errorf("WorkDir: %v", err)
	}
	if err := validatePath(o.LowerDir); err != nil {
		return fmt.Errorf("LowerDir: %v", err)
	}

	// Check if UpperDir and WorkDir are identical
	if o.UpperDir == o.WorkDir {
		return fmt.Errorf("UpperDir and WorkDir must be distinct")
	}

	// Check if UpperDir is a subdirectory of WorkDir or vice versa
	if isSubDirString(o.UpperDir, o.WorkDir) || isSubDirString(o.WorkDir, o.UpperDir) {
		return fmt.Errorf("UpperDir and WorkDir should not be a subdirectory of one another")
	}

	if o.Partition != nil {
		if err := o.Partition.IsValid(); err != nil {
			return fmt.Errorf("invalid Partition: %v", err)
		}
	}

	return nil
}

func validatePath(path string) error {
	// Check if the path is empty
	if path == "" {
		return fmt.Errorf("path of lowerdir, upperdir or workdir cannot be empty")
	}

	// Check if the path contains spaces
	if strings.Contains(path, " ") {
		return fmt.Errorf("path '%s' contains spaces and is invalid", path)
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
