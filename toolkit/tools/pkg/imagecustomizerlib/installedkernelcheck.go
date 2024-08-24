// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

// Check if the user accidentally uninstalled the kernel package without installing a substitute package.
func checkForInstalledKernel(imageChroot *safechroot.Chroot) error {
	kernelModulesDir := filepath.Join(imageChroot.RootDir(), "/lib/modules")

	kernels, err := os.ReadDir(kernelModulesDir)
	if err != nil {
		return fmt.Errorf("failed to read installed kernels list:\n%w", err)
	}

	for _, kernel := range kernels {
		// There is a bug in Azure Linux 2.0, where uninstalling the kernel package doesn't remove the directory
		// /lib/modules/<ver>. Instead the directory is just emptied. So, ensure the directory isn't empty.
		files, err := os.ReadDir(filepath.Join(kernelModulesDir, kernel.Name()))
		if err != nil {
			return fmt.Errorf("failed to read installed kernel (%s) module directory:\n%w", kernel.Name(), err)
		}

		if len(files) > 0 {
			// Found at least 1 kernel.
			return nil
		}
	}

	return fmt.Errorf("no installed kernel found")
}
