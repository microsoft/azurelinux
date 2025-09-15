// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierapi

import (
	"fmt"
)

type IdentifiedPartition struct {
	Id string `yaml:"id"`
}

func (i *IdentifiedPartition) IsValid() error {
	// Check if Id is not empty
	if i.Id == "" {
		return fmt.Errorf("invalid id: empty string")
	}

	return nil
}
