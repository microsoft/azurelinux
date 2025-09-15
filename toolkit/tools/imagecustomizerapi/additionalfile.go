// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type AdditionalFileList []AdditionalFile

type AdditionalFile struct {
	// The destination file path in the target OS that the file will be copied to.
	Destination string `yaml:"destination"`

	// The source file path of the file that will copied.
	// Mutally exclusive with 'contents'.
	Source string `yaml:"source"`

	// A string that will be used as the contents of the file.
	// Mutally exclusive with 'source'.
	Content *string `yaml:"content"`

	// The file permissions to set on the file.
	Permissions *FilePermissions `yaml:"permissions"`
}

func (l AdditionalFileList) IsValid() (err error) {
	for i, additionalFile := range l {
		err = additionalFile.IsValid()
		if err != nil {
			return fmt.Errorf("invalid value at index %d:\n%w", i, err)
		}
	}

	return nil
}

func (f *AdditionalFile) IsValid() (err error) {
	if f.Destination == "" {
		return fmt.Errorf("destination path must not be empty")
	}

	if f.Source == "" && f.Content == nil {
		return fmt.Errorf("must specify either 'source' or 'content'")
	}

	if f.Source != "" && f.Content != nil {
		return fmt.Errorf("cannot specify both 'source' and 'content'")
	}

	// Permissions
	if f.Permissions != nil {
		err = f.Permissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid permissions value:\n%w", err)
		}
	}

	return nil
}
