// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type IdType string

const (
	IdTypePartition IdType = "Partition"
	IdTypeId        IdType = "ID"
	//IdTypeLabel     IdType = "Label"
	IdTypePartlabel IdType = "PartLabel"
	IdTypeUuid      IdType = "Uuid"
	IdTypePartuuid  IdType = "PartUuid"
)

func (i IdType) IsValid() error {
	switch i {
	case IdTypePartition, IdTypeId, IdTypePartlabel, IdTypeUuid, IdTypePartuuid:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid IdType value (%v)", i)
	}
}
