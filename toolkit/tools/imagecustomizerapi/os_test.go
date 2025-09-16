// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestOSValidEmpty(t *testing.T) {
	testValidYamlValue[*OS](t, "{ }", &OS{})
}

func TestOSValidHostname(t *testing.T) {
	testValidYamlValue[*OS](t, "{ \"hostname\": \"validhostname\" }", &OS{Hostname: "validhostname"})
}

func TestOSInvalidHostname(t *testing.T) {
	os := OS{
		Hostname: "invalid_hostname",
	}
	err := os.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid hostname")
}

func TestOSIsValidInvalidAdditionalFilesSource(t *testing.T) {
	os := OS{
		AdditionalFiles: []AdditionalFile{
			{
				Destination: "/a.txt",
				Source:      "a.txt",
			},
		},
	}
	err := os.IsValid()
	assert.NoError(t, err)
}

func TestOSIsValidInvalidAdditionalFilesContent(t *testing.T) {
	os := OS{
		AdditionalFiles: []AdditionalFile{
			{
				Destination: "/a.txt",
				Content:     ptrutils.PtrTo("abc"),
			},
		},
	}
	err := os.IsValid()
	assert.NoError(t, err)
}

func TestOSIsValidInvalidResetBootLoaderType(t *testing.T) {
	os := OS{
		ResetBootLoaderType: "bad",
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid resetBootLoaderType value (bad)")
}

func TestOSIsValidInvalidSELinux(t *testing.T) {
	os := OS{
		SELinux: SELinux{
			Mode: "bad",
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid selinux")
	assert.ErrorContains(t, err, "invalid mode")
	assert.ErrorContains(t, err, "invalid selinux value (bad)")
}

func TestOSIsValidInvalidAdditionalFiles(t *testing.T) {
	os := OS{
		AdditionalFiles: AdditionalFileList{
			{},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid additionalFiles")
	assert.ErrorContains(t, err, "invalid value at index 0")
}

func TestOSIsValidInvalidAdditionalDirs(t *testing.T) {
	os := OS{
		AdditionalDirs: DirConfigList{
			{
				Source:      "",
				Destination: "/a",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid additionalDirs")
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid 'source' value: empty string")
}

func TestOSIsValidInvalidUser(t *testing.T) {
	os := OS{
		Users: []User{
			{
				Name: "",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid users item at index 0")
	assert.ErrorContains(t, err, "user () is invalid")
}

func TestOSIsValidInvalidServices(t *testing.T) {
	os := OS{
		Services: Services{
			Enable: []string{
				"",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid service enable at index (0)")
	assert.ErrorContains(t, err, "name of service may not be empty")
}

func TestOSIsValidInvalidModule(t *testing.T) {
	os := OS{
		Modules: []Module{
			{
				Name: "",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid modules item at index 0")
	assert.ErrorContains(t, err, "module name cannot be empty")
}

func TestOSIsValidModuleDuplicateName(t *testing.T) {
	os := OS{
		Modules: []Module{
			{
				Name: "nbd",
			},
			{
				Name: "nbd",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "duplicate module found: nbd at index 1")
}

func TestOSIsValidInvalidOverlay(t *testing.T) {
	os := OS{
		Overlays: &[]Overlay{
			{},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid overlay at index 0")
}

func TestOSIsValidOverlayDuplicateUpperDir(t *testing.T) {
	os := OS{
		Overlays: &[]Overlay{
			{
				LowerDirs:  []string{"/"},
				UpperDir:   "/upper_root",
				WorkDir:    "/work_root",
				MountPoint: "/mnt/root",
			},
			{
				LowerDirs:  []string{"/var"},
				UpperDir:   "/upper_root",
				WorkDir:    "/work_var",
				MountPoint: "/mnt/var",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "duplicate upperDir (/upper_root) found in overlay at index 1")
}

func TestOSIsValidOverlayDuplicateWorkDir(t *testing.T) {
	os := OS{
		Overlays: &[]Overlay{
			{
				LowerDirs:  []string{"/"},
				UpperDir:   "/upper_root",
				WorkDir:    "/work_root",
				MountPoint: "/mnt/root",
			},
			{
				LowerDirs:  []string{"/"},
				UpperDir:   "/upper_var",
				WorkDir:    "/work_root",
				MountPoint: "/mnt/var",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "duplicate workDir (/work_root) found in overlay at index 1")
}
