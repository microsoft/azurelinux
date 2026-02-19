// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

// MountIdentifierType indicates how a partition should be identified in the fstab file
type MountIdentifierType string

const (
	// MountIdentifierTypeUuid mounts this partition via the filesystem UUID
	MountIdentifierTypeUuid MountIdentifierType = "uuid"

	// MountIdentifierTypePartUuid mounts this partition via the GPT/MBR PARTUUID
	MountIdentifierTypePartUuid MountIdentifierType = "partuuid"

	// MountIdentifierTypePartLabel mounts this partition via the GPT PARTLABEL
	MountIdentifierTypePartLabel MountIdentifierType = "partlabel"

	// MountIdentifierTypeDefault uses the default type, which is PARTUUID.
	MountIdentifierTypeDefault MountIdentifierType = ""
)

func (m MountIdentifierType) IsValid() error {
	switch m {
	case MountIdentifierTypeUuid, MountIdentifierTypePartUuid, MountIdentifierTypePartLabel, MountIdentifierTypeDefault:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid mountIdentifierType value (%v)", m)
	}
}
