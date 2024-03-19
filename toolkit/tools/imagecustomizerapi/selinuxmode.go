package imagecustomizerapi

import (
	"fmt"
)

// SELinux sets the SELinux mode
type SELinuxMode string

const (
	// SELinuxDefault keeps the base image's existing SELinux mode.
	SELinuxModeDefault SELinuxMode = ""
	// SELinuxDisabled disables SELinux
	SELinuxModeDisabled SELinuxMode = "disabled"
	// SELinuxEnforcing sets SELinux to enforcing
	SELinuxModeEnforcing SELinuxMode = "enforcing"
	// SELinuxPermissive sets SELinux to permissive
	SELinuxModePermissive SELinuxMode = "permissive"
	// SELinuxForceEnforcing both sets SELinux to enforcing, and forces it via the kernel command line
	SELinuxModeForceEnforcing SELinuxMode = "force-enforcing"
)

func (s SELinuxMode) IsValid() error {
	switch s {
	case SELinuxModeDefault, SELinuxModeDisabled, SELinuxModeEnforcing, SELinuxModePermissive,
		SELinuxModeForceEnforcing:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid selinux value (%v)", s)
	}
}
