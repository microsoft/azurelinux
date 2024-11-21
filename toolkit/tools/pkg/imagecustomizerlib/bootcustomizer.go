// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

type BootCustomizer struct {
	// The contents of the /boot/grub2/grub.cfg file.
	grubCfgContent string

	// The contents of the /etc/default/grub file.
	defaultGrubFileContent string

	// Whether or not the image is using grub-mkconfig.
	isGrubMkconfig bool
}

func NewBootCustomizer(imageChroot *safechroot.Chroot) (*BootCustomizer, error) {
	grubCfgContent, err := readGrub2ConfigFile(imageChroot)
	if err != nil {
		return nil, err
	}

	defaultGrubFileContent, err := readDefaultGrubFile(imageChroot)
	if err != nil {
		return nil, err
	}

	isGrubMkconfig := isGrubMkconfigConfig(grubCfgContent)

	b := &BootCustomizer{
		grubCfgContent:         grubCfgContent,
		defaultGrubFileContent: defaultGrubFileContent,
		isGrubMkconfig:         isGrubMkconfig,
	}
	return b, nil
}

// Returns whether or not the OS uses grub-mkconfig.
func (b *BootCustomizer) IsGrubMkconfigImage() bool {
	return b.isGrubMkconfig
}

// Inserts new kernel command-line args into the grub config file.
func (b *BootCustomizer) AddKernelCommandLine(extraCommandLine string) error {
	extraCommandLine = strings.TrimSpace(extraCommandLine)
	if extraCommandLine == "" {
		return nil
	}

	if b.isGrubMkconfig {
		defaultGrubFileContent, err := addExtraCommandLineToDefaultGrubFile(b.defaultGrubFileContent, extraCommandLine)
		if err != nil {
			return err
		}

		b.defaultGrubFileContent = defaultGrubFileContent
	} else {
		// Add the args directly to the /boot/grub2/grub.cfg file.
		grubCfgContent, err := appendKernelCommandLineArgs(b.grubCfgContent, extraCommandLine)
		if err != nil {
			return err
		}

		b.grubCfgContent = grubCfgContent
	}

	return nil
}

// Gets the image's configured SELinux mode.
func (b *BootCustomizer) getSELinuxModeFromGrub() (imagecustomizerapi.SELinuxMode, error) {
	var err error
	var args []grubConfigLinuxArg

	// Get the SELinux kernel command-line args.
	if b.isGrubMkconfig {
		_, args, _, err = getDefaultGrubFileLinuxArgs(b.defaultGrubFileContent, defaultGrubFileVarNameCmdlineForSELinux)
		if err != nil {
			return "", err
		}
	} else {
		args, _, err = getLinuxCommandLineArgs(b.grubCfgContent)
		if err != nil {
			return imagecustomizerapi.SELinuxModeDefault, err
		}
	}

	// Get the SELinux mode from the kernel command-line args.
	selinuxMode, err := getSELinuxModeFromLinuxArgs(args)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	return selinuxMode, nil
}

func (b *BootCustomizer) GetSELinuxMode(imageChroot *safechroot.Chroot) (imagecustomizerapi.SELinuxMode, error) {
	// Get the SELinux mode from the kernel command-line args.
	selinuxMode, err := b.getSELinuxModeFromGrub()
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDefault {
		// Get the SELinux mode from the /etc/selinux/config file.
		selinuxMode, err = getSELinuxModeFromConfigFile(imageChroot)
		if err != nil {
			return imagecustomizerapi.SELinuxModeDefault, err
		}
	}

	return selinuxMode, nil
}

// Update the image's SELinux kernel command-line args.
func (b *BootCustomizer) UpdateSELinuxCommandLine(selinuxMode imagecustomizerapi.SELinuxMode) error {
	newSELinuxArgs, err := selinuxModeToArgs(selinuxMode)
	if err != nil {
		return err
	}

	err = b.UpdateKernelCommandLineArgs(defaultGrubFileVarNameCmdlineForSELinux, selinuxArgNames, newSELinuxArgs)
	if err != nil {
		return err
	}

	return nil
}

func (b *BootCustomizer) UpdateKernelCommandLineArgs(defaultGrubFileVarName defaultGrubFileVarName,
	argsToRemove []string, newArgs []string,
) error {
	if b.isGrubMkconfig {
		defaultGrubFileContent, err := updateDefaultGrubFileKernelCommandLineArgs(b.defaultGrubFileContent,
			defaultGrubFileVarName, argsToRemove, newArgs)
		if err != nil {
			return err
		}

		b.defaultGrubFileContent = defaultGrubFileContent
	} else {
		grubCfgContent, err := updateKernelCommandLineArgs(b.grubCfgContent, argsToRemove, newArgs)
		if err != nil {
			return err
		}

		b.grubCfgContent = grubCfgContent
	}

	return nil
}

// Makes changes to the /etc/default/grub file that are needed/useful for enabling verity.
func (b *BootCustomizer) PrepareForVerity() error {
	if b.isGrubMkconfig {
		// Force root command-line arg to be referenced by /dev path instead of by UUID.
		defaultGrubFileContent, err := updateDefaultGrubFileVariable(b.defaultGrubFileContent, "GRUB_DISABLE_UUID",
			"true")
		if err != nil {
			return err
		}

		// Disable recovery menu entry, to avoid having more than 1 linux command in the grub.cfg file.
		// This will make it easier to modify the grub.cfg file to add the verity args.
		defaultGrubFileContent, err = updateDefaultGrubFileVariable(defaultGrubFileContent, "GRUB_DISABLE_RECOVERY",
			"true")
		if err != nil {
			return err
		}

		b.defaultGrubFileContent = defaultGrubFileContent
	}

	return nil
}

func (b *BootCustomizer) WriteToFile(imageChroot *safechroot.Chroot) error {
	if b.isGrubMkconfig {
		// Update /etc/defaukt/grub file.
		err := writeDefaultGrubFile(b.defaultGrubFileContent, imageChroot)
		if err != nil {
			return err
		}

		// Update /boot/grub2/grub.cfg file.
		err = installutils.CallGrubMkconfig(imageChroot)
		if err != nil {
			return fmt.Errorf("failed to generate grub.cfg via grub2-mkconfig:\n%w", err)
		}
	} else {
		// Update grub.cfg file.
		err := writeGrub2ConfigFile(b.grubCfgContent, imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}
