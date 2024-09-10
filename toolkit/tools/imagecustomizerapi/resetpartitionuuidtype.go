// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type ResetPartitionsUuidsType string

const (
	ResetPartitionsUuidsTypeDefault ResetPartitionsUuidsType = ""
	ResetPartitionsUuidsTypeAll     ResetPartitionsUuidsType = "reset-all"
)

func (t ResetPartitionsUuidsType) IsValid() error {
	switch t {
	case ResetPartitionsUuidsTypeDefault, ResetPartitionsUuidsTypeAll:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid resetPartitionUuidType value (%v)", t)
	}
}
