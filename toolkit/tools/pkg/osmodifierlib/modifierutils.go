// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/osmodifierapi"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
)

func doModifications(baseConfigPath string, osConfig *osmodifierapi.OS) error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	err := imagecustomizerlib.AddOrUpdateUsers(osConfig.Users, baseConfigPath, dummyChroot)
	if err != nil {
		return err
	}

	err = imagecustomizerlib.UpdateHostname(osConfig.Hostname, dummyChroot)
	if err != nil {
		return err
	}

	if osConfig.Overlays != nil {
		_, err = imagecustomizerlib.EnableOverlays(osConfig.Overlays, dummyChroot)
		if err != nil {
			return err
		}
	}

	if osConfig.SELinux.Mode != "" {
		bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
		if err != nil {
			return err
		}

		err = handleSELinux(osConfig.SELinux.Mode, bootCustomizer, dummyChroot)
		if err != nil {
			return err
		}

		err = bootCustomizer.WriteToFile(dummyChroot)
		if err != nil {
			return err
		}
	}

	return nil
}
