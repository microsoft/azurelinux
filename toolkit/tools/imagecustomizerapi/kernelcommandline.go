// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type KernelCommandLine struct {
	// SELinux specifies whether or not to enable SELinux on the image (and what mode SELinux should be in).
	SELinux SELinux `yaml:"selinux"`
	// Extra kernel command line args.
	ExtraCommandLine KernelExtraArguments `yaml:"extraCommandLine"`
}

func (s *KernelCommandLine) IsValid() error {
	err := s.SELinux.IsValid()
	if err != nil {
		return err
	}

	err = s.ExtraCommandLine.IsValid()
	if err != nil {
		return err
	}

	return nil
}
