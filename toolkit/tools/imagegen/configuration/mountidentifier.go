// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// MountIdentifier indicates how a partition should be identified in the fstab file
type MountIdentifier string

// label
const (
	// MountIdentifierUuid mounts this partition via the filesystem UUID
	MountIdentifierUuid MountIdentifier = "uuid"
	// MountIdentifierPartUuid mounts this partition via the GPT/MBR PARTUUID
	MountIdentifierPartUuid MountIdentifier = "partuuid"
	// MountIdentifierPartLabel mounts this partition via the GPT PARTLABEL
	MountIdentifierPartLabel MountIdentifier = "partlabel"

	// There is not a clear way to set arbitrary partitions via a device path (ie /dev/sda1)
	// so we do not support those.

	// We currently do not set filesystem LABELS, so those are also not useful here.

	MountIdentifierDefault MountIdentifier = MountIdentifierPartUuid
	MountIdentifierNone    MountIdentifier = ""
)

func (m MountIdentifier) String() string {
	return fmt.Sprint(string(m))
}

// GetValidMountIdentifiers returns a list of all the supported mount identifiers
func (m *MountIdentifier) GetValidMountIdentifiers() (types []MountIdentifier) {
	return []MountIdentifier{
		MountIdentifierUuid,
		MountIdentifierPartUuid,
		MountIdentifierPartLabel,
		MountIdentifierNone,
	}
}

func GetDefaultMountIdentifier() (defaultVal MountIdentifier) {
	return MountIdentifierDefault
}

// IsValid returns an error if the PartitionFlag is not valid
func (m *MountIdentifier) IsValid() (err error) {
	for _, valid := range m.GetValidMountIdentifiers() {
		if *m == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for Mount Identifier (%s)", m)
}

// UnmarshalJSON Unmarshals an MountIdentifier entry
func (m *MountIdentifier) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeMountIdentifier MountIdentifier

	// Populate non-standard default
	*m = GetDefaultMountIdentifier()

	err = json.Unmarshal(b, (*IntermediateTypeMountIdentifier)(m))
	if err != nil {
		return fmt.Errorf("failed to parse [MountIdentifier]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = m.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [MountIdentifier]: %w", err)
	}
	return
}
