package imagecustomizerapi

import (
	"fmt"
)

// SELinux sets the SELinux mode
type SELinux string

const (
	// SELinuxDefault keeps the base image's existing SELinux mode.
	SELinuxDefault SELinux = ""
	// SELinuxDisabled disables SELinux
	SELinuxDisabled SELinux = "disabled"
	// SELinuxEnforcing sets SELinux to enforcing
	SELinuxEnforcing SELinux = "enforcing"
	// SELinuxPermissive sets SELinux to permissive
	SELinuxPermissive SELinux = "permissive"
	// SELinuxForceEnforcing both sets SELinux to enforcing, and forces it via the kernel command line
	SELinuxForceEnforcing SELinux = "force-enforcing"
)

func (s SELinux) IsValid() error {
	switch s {
	case SELinuxDefault, SELinuxDisabled, SELinuxEnforcing, SELinuxPermissive, SELinuxForceEnforcing:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid SELinux value (%v)", s)
	}
}
