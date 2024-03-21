// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type SELinux struct {
	// SELinux specifies whether or not to enable SELinux on the image (and what mode SELinux should be in).
	Mode SELinuxMode `yaml:"mode"`
}

func (s *SELinux) IsValid() error {
	err := s.Mode.IsValid()
	if err != nil {
		return fmt.Errorf("invalid mode:\n%w", err)
	}

	return nil
}
