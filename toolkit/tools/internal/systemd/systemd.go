// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package systemd

import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// IsServiceEnabled checks if a service is enabled or disabled.
func IsServiceEnabled(name string, imageChroot safechroot.ChrootInterface) (bool, error) {
	serviceEnabled := true
	err := imageChroot.UnsafeRun(func() error {
		err := shell.ExecuteLive(true, "systemctl", "is-enabled", name)

		// is-enabled returns:
		//   0: service is enabled
		//   1: service is disabled
		var exitError *exec.ExitError
		if errors.As(err, &exitError) && exitError.ExitCode() == 1 {
			serviceEnabled = false
			return nil
		}
		return err
	})
	if err != nil {
		return false, fmt.Errorf("failed to check if (%s) service is enabled:\n%w", name, err)
	}

	return serviceEnabled, nil
}
