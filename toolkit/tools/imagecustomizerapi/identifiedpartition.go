// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"regexp"
)

type IdentifiedPartition struct {
	IdType IdType `yaml:"IdType"`
	Id     string `yaml:"Id"`
}

var uuidRegex = regexp.MustCompile(`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[4][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$`)

func (i *IdentifiedPartition) IsValid() error {
	// Check if IdType is valid
	if err := i.IdType.IsValid(); err != nil {
		return fmt.Errorf("invalid IdType: %v", err)
	}

	// Check if Id is not empty
	if i.Id == "" {
		return fmt.Errorf("invalid Id: empty string")
	}

	// Check Id format based on IdType
	switch i.IdType {
	case IdTypePartLabel:
		// Validate using isGPTNameValid function for IdTypePartLabel
		if err := isGPTNameValid(i.Id); err != nil {
			return fmt.Errorf("invalid Id for IdTypePartLabel: %v", err)
		}
	case IdTypeUuid, IdTypePartUuid:
		// UUID validation (standard format)
		if !uuidRegex.MatchString(i.Id) {
			return fmt.Errorf("invalid Id format for %s: %s", i.IdType, i.Id)
		}
	}

	return nil
}
