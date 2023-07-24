// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"gopkg.in/yaml.v3"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	AdditionalFiles map[string]FileConfig `yaml:"AdditionalFiles"`
}

// Configuration of files that are to be added to the image.
type FileConfig struct {
	SourceFile      string `yaml:"SourceFile"`
	FilePermissions string `yaml:"FilePermissions"`
}

// Allow FileConfig to be parsed from just a string containing the source file.
func (f *FileConfig) UnmarshalYAML(value *yaml.Node) error {
	// Try to parse the value as a string.
	var sourceFile string
	if err := value.Decode(&sourceFile); err == nil {
		f.SourceFile = sourceFile
		return nil
	}

	// Try to parse the value as the struct.
	// The type rawFileConfig exists to prevent infinite recursion.
	type rawFileConfig FileConfig
	if err := value.Decode((*rawFileConfig)(f)); err != nil {
		return err
	}

	return nil
}
