// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"gopkg.in/yaml.v3"
)

type FileConfigList []FileConfig

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	AdditionalFiles map[string]FileConfigList `yaml:"AdditionalFiles"`
}

// Configuration of files that are to be added to the image.
type FileConfig struct {
	DestinationFile string `yaml:"DestinationFile"`
	FilePermissions string `yaml:"FilePermissions"`
}

// Allow FileConfigList to be parsed from just a single value.
func (l *FileConfigList) UnmarshalYAML(value *yaml.Node) error {
	// Try to parse the value as a single value.
	var fileConfig FileConfig
	if err := value.Decode(&fileConfig); err == nil {
		*l = append(*l, fileConfig)
		return nil
	}

	// Try to parse the value as a list.
	if err := value.Decode((*[]FileConfig)(l)); err != nil {
		return err
	}

	return nil
}

// Allow FileConfig to be parsed from just a string containing the destination file.
func (f *FileConfig) UnmarshalYAML(value *yaml.Node) error {
	// Try to parse the value as a string.
	var destinationFile string
	if err := value.Decode(&destinationFile); err == nil {
		f.DestinationFile = destinationFile
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
