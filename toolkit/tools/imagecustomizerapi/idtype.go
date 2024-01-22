// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type IdType string

const (
	IdTypePartLabel IdType = "PartLabel"
	IdTypeUuid      IdType = "Uuid"
	IdTypePartUuid  IdType = "PartUuid"
)

func (i IdType) IsValid() error {
	switch i {
	case IdTypePartLabel, IdTypeUuid, IdTypePartUuid:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid IdType value (%v)", i)
	}
}
