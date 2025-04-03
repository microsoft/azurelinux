// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type IdType string

const (
	IdTypeId        IdType = "id"
	IdTypePartLabel IdType = "part-label"
	IdTypeUuid      IdType = "uuid"
	IdTypePartUuid  IdType = "part-uuid"
)

func (i IdType) IsValid() error {
	switch i {
	case IdTypeId, IdTypePartLabel, IdTypeUuid, IdTypePartUuid:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid idType value (%v)", i)
	}
}
