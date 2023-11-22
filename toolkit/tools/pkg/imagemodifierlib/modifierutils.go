// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagemodifierlib

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagecustomizerlib"
)

func doModifications(baseConfigPath string, systemConfig *imagecustomizerapi.SystemConfig) error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	err := imagecustomizerlib.AddOrUpdateUsers(systemConfig.Users, baseConfigPath, dummyChroot)
	if err != nil {
		return err
	}

	return nil
}
