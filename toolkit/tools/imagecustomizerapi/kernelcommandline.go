// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type KernelCommandLine struct {
	// Extra kernel command line args.
	ExtraCommandLine KernelExtraArguments `yaml:"extraCommandLine"`
}

func (s *KernelCommandLine) IsValid() error {
	err := s.ExtraCommandLine.IsValid()
	if err != nil {
		return err
	}

	return nil
}
