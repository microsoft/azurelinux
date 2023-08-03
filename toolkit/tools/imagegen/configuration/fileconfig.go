// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

//

package configuration

import (
	"encoding/json"
	"fmt"
)

// DestinationFileConfigList is a list of destination files where the source file will be copied to in the final image.
// This type exists to allow a custom marshaller to be attached to it.
type FileConfigList []FileConfig

// FileConfig specifies options for how a file is copied in the target OS.
type FileConfig struct {
	// The file path in the target OS that the file will be copied to.
	Path string `json:"Path"`

	// The file permissions to set on the file.
	Permissions *FilePermissions `json:"Permissions"`
}

var (
	DefaultFileConfig = FileConfig{
		Path:        "",
		Permissions: nil,
	}
)

func (l *FileConfigList) IsValid() (err error) {
	if len(*l) <= 0 {
		return fmt.Errorf("list is empty")
	}

	for i, fileConfig := range *l {
		err = fileConfig.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [FileConfig] at index %d: %w", i, err)
		}
	}

	return nil
}

func (l *FileConfigList) UnmarshalJSON(b []byte) error {
	var err error

	err = l.unmarshalJSONHelper(b)
	if err != nil {
		return err
	}

	// Validate the unmarshaled object.
	err = l.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [FileConfigList]: %w", err)
	}

	return nil
}

func (l *FileConfigList) unmarshalJSONHelper(b []byte) error {
	var err error

	// Try to parse as a single value.
	var fileConfig FileConfig
	err = json.Unmarshal(b, &fileConfig)
	if err == nil {
		*l = FileConfigList{fileConfig}
		return nil
	}

	// Try to parse as a list.
	type IntermediateTypeFileConfigList FileConfigList
	err = json.Unmarshal(b, (*IntermediateTypeFileConfigList)(l))
	if err != nil {
		return fmt.Errorf("failed to parse [FileConfigList]: %w", err)
	}

	return nil
}

func (f *FileConfig) IsValid() (err error) {
	// Path
	if f.Path == "" {
		return fmt.Errorf("invalid [Path] value: empty string")
	}

	// Permissions
	if f.Permissions != nil {
		err = f.Permissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [Permissions] value: %w", err)
		}
	}

	return nil
}

func (f *FileConfig) UnmarshalJSON(b []byte) error {
	var err error

	err = f.unmarshalJSONHelper(b)
	if err != nil {
		return err
	}

	// Validate the unmarshaled object.
	err = f.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [FileConfig]: %w", err)
	}

	return nil
}

func (f *FileConfig) unmarshalJSONHelper(b []byte) error {
	var err error

	// Try to parse as a string.
	var path string
	err = json.Unmarshal(b, &path)
	if err == nil {
		*f = FileConfig{
			Path:        path,
			Permissions: nil,
		}
		return nil
	}

	// Try to parse as a struct.
	*f = DefaultFileConfig

	type IntermediateTypeFileConfig FileConfig
	err = json.Unmarshal(b, (*IntermediateTypeFileConfig)(f))
	if err != nil {
		return fmt.Errorf("failed to parse [FileConfig]: %w", err)
	}

	return nil
}
