// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.
package installutils
import (
	"fmt"
	"os"
	"strings"
	"syscall"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)
const (
	// On Fedora, the setfiles_mac_t context has permission to label files with labels that don't exist in the host OS.
	//
	// Note: The Fedora policy doesn't by default allow transitions from unconfined_t to setfiles_mac_t.
	// So, you have to run the following for it to work:
	//
	//   sudo semanage permissive -a setfiles_mac_t
	FedoraSetFilesContext = "system_u:system_r:setfiles_mac_t:s0"
)
func getSELinuxEnabled() (bool, error) {
	stdout, _, err := shell.Execute("sestatus")
	if err != nil {
		return false, fmt.Errorf("failed to check if SELinux is enabled:\ncall to sestatus failed:\n%w", err)
	}
	lines := strings.Split(stdout, "\n")
	for _, line := range lines {
		key, value, _ := strings.Cut(line, ":")
		if key == "SELinux status" {
			enabled := strings.TrimSpace(value) == "enabled"
			return enabled, nil
		}
	}
	return false, fmt.Errorf("failed to check if SELinux is enabled:\nfailed to parse sestatus output")
}
// Sets the SELinux context to use for any child processes started by the current OS thread.
// This is equivalent to using runcon, though with the advantage that it works with safechroot.
//
// Note: This function should only be run under the runtime.LockOSThread() lock.
func setSELinuxExecContext(context string) error {
	path := selinuxExecContextPath()
	logger.Log.Debugf("Set SELinux context [%s]", path)
	out, err := os.OpenFile(path, os.O_WRONLY, 0)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = out.Write([]byte(context))
	if err != nil {
		return err
	}
	err = out.Close()
	if err != nil {
		return err
	}
	return nil
}
// Clears the explicit override of the SELinux context to use for child processes started by the current OS thread.
//
// Note: This function should only be run under the runtime.LockOSThread() lock and on the same thread that called
// setSELinuxExecContext().
func resetSELinuxExecContext() error {
	path := selinuxExecContextPath()
	logger.Log.Debugf("Clean SELinux context [%s]", path)
	out, err := os.OpenFile(path, os.O_WRONLY, 0)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = out.Write([]byte(nil))
	if err != nil {
		return err
	}
	err = out.Close()
	if err != nil {
		return err
	}
	return nil
}
func selinuxExecContextPath() string {
	taskId := syscall.Gettid()
	path := fmt.Sprintf("/proc/self/task/%d/attr/exec", taskId)
	return path
}
