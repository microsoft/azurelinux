// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"runtime"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/pkgjson"

	"github.com/stretchr/testify/assert"
)

func TestShouldReturnCorrectRequiredPackagesForArch(t *testing.T) {
	arm64RequiredPackages := []*pkgjson.PackageVer{}
	amd64RequiredPackages := []*pkgjson.PackageVer{{Name: "grub2-pc"}}

	requiredPackages := GetRequiredPackagesForInstall()

	switch arch := runtime.GOARCH; arch {
	case "arm64":
		assert.Equal(t, arm64RequiredPackages, requiredPackages)
	case "amd64":
		assert.Equal(t, amd64RequiredPackages, requiredPackages)
	default:
		assert.Fail(t, "unknown GOARCH detected: "+arch)
	}
}
