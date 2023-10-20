// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"reflect"
)

type OSSubrelease struct {
	Name          string `yaml:"Name" file:"NAME"`
	Version       string `yaml:"Version" file:"VERSION"`
	ID            string `yaml:"ID" file:"ID"`
	IDLike        string `yaml:"IDLike" file:"ID_LIKE"`
	PrettyName    string `yaml:"PrettyName" file:"PRETTY_NAME"`
	VersionID     string `yaml:"VersionID" file:"VERSION_ID"`
	BuilderName   string `yaml:"BuilderName" file:"BUILDER_NAME"`
	BuildDate     string `yaml:"BuildDate" file:"BUILD_DATE"`
	HomeURL       string `yaml:"HomeURL" file:"HOME_URL"`
	MarinerBranch string `yaml:"MarinerBranch" file:"MARINER_BRANCH"`
}

func (o OSSubrelease) IsValid() error {

	val := reflect.ValueOf(o)

	for i := 0; i < val.NumField(); i++ {
		field := val.Field(i)
		if field.Interface() == "" {
			return fmt.Errorf("%s field in %s is empty", val.Type().Field(i).Name, val.Type())
		}
	}

	return nil
}
