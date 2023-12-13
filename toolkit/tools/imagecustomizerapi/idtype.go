// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type IdType string

const (
	IdTypePartition IdType = "PARTITION"
	IdTypeId        IdType = "ID"
	IdTypeLabel     IdType = "LABEL"
	IdTypePartlabel IdType = "PARTLABEL"
	IdTypeUuid      IdType = "UUID"
	IdTypePartuuid  IdType = "PARTUUID"
)

func (i IdType) IsValid() error {
	switch i {
	case IdTypePartition, IdTypeId, IdTypeLabel, IdTypePartlabel, IdTypeUuid, IdTypePartuuid:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid IdType value (%v)", i)
	}
}
