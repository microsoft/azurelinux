// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type IdType string

const (
	IdTypePartlabel IdType = "PartLabel"
	IdTypeUuid      IdType = "Uuid"
	IdTypePartuuid  IdType = "PartUuid"
)

func (i IdType) IsValid() error {
	switch i {
	case IdTypePartlabel, IdTypeUuid, IdTypePartuuid:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid IdType value (%v)", i)
	}
}
