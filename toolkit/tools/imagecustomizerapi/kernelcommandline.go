// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type KernelCommandLine struct {
	// Extra kernel command line args.
	ExtraCommandLine []string `yaml:"extraCommandLine"`
}

func (k *KernelCommandLine) IsValid() error {
	for i, arg := range k.ExtraCommandLine {
		if arg == "" {
			return fmt.Errorf("kernel argument cannot be empty at index %d", i)
		}
	}
	return nil
}
