// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type VerityPartition struct {
	IdType string `yaml:"IdType"`
	Id     string `yaml:"Id"`
}

type Verity struct {
	DataPartition       VerityPartition     `yaml:"DataPartition"`
	HashPartition       VerityPartition     `yaml:"HashPartition"`
	BootPartition       VerityPartition     `yaml:"BootPartition"`
	VerityErrorBehavior VerityErrorBehavior `yaml:"VerityErrorBehavior"`
}

var (
	DefaultVerity = Verity{
		DataPartition:       VerityPartition{IdType: "PARTITION", Id: ""},
		HashPartition:       VerityPartition{IdType: "PARTITION", Id: ""},
		BootPartition:       VerityPartition{IdType: "PARTITION", Id: ""},
		VerityErrorBehavior: "",
	}
)

func (v *Verity) IsSet() bool {
	return v.DataPartition != VerityPartition{} ||
		v.HashPartition != VerityPartition{} ||
		v.BootPartition != VerityPartition{}
}

func (v *Verity) IsValid() error {
	var err error

	validIdTypes := map[string]bool{
		"PARTITION": true,
		"ID":        true,
		"LABEL":     true,
		"PARTLABEL": true,
		"UUID":      true,
		"PARTUUID":  true,
	}

	if _, ok := validIdTypes[v.DataPartition.IdType]; !ok || v.DataPartition.Id == "" {
		return fmt.Errorf("invalid DataPartition: IdType must be one of %v and Id must not be empty", validIdTypes)
	}

	if _, ok := validIdTypes[v.HashPartition.IdType]; !ok || v.HashPartition.Id == "" {
		return fmt.Errorf("invalid HashPartition: IdType must be one of %v and Id must not be empty", validIdTypes)
	}

	if _, ok := validIdTypes[v.BootPartition.IdType]; !ok || v.BootPartition.Id == "" {
		return fmt.Errorf("invalid BootPartition: IdType must be one of %v and Id must not be empty", validIdTypes)
	}

	err = v.VerityErrorBehavior.IsValid()
	if err != nil {
		return err
	}

	return nil
}
