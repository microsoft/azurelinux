// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

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

func TestOSInvalidAdditionalFiles(t *testing.T) {
	os := OS{
		AdditionalFiles: AdditionalFilesMap{
			"a.txt": FileConfigList{},
		},
	}
	err := os.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid additionalFiles:\ninvalid file configs for (a.txt):\nlist is empty")
}

func TestOSIsValidInvalidAdditionalFilesEmptySourcePath(t *testing.T) {
	os := OS{
		AdditionalFiles: AdditionalFilesMap{
			"": FileConfigList{
				{
					Path: "/a.txt",
				},
			},
		},
	}
	err := os.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid additionalFiles:\ninvalid source path: cannot be empty")
}

func TestOSIsValidVerityInValidPartUuid(t *testing.T) {
	invalidVerity := OS{
		Verity: &Verity{
			DataPartition: IdentifiedPartition{
				IdType: "part-uuid",
				Id:     "incorrect-uuid-format",
			},
			HashPartition: IdentifiedPartition{
				IdType: "part-label",
				Id:     "hash_partition",
			},
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id format")
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

func TestOSIsValidInvalidAdditionalDirs(t *testing.T) {
	os := OS{
		AdditionalDirs: DirConfigList{
			{
				SourcePath:      "",
				DestinationPath: "/a",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid additionalDirs")
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid sourcePath value: empty string")
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
				LowerDir: "/",
				UpperDir: "/upper_root",
				WorkDir:  "/work_root",
			},
			{
				LowerDir: "/var",
				UpperDir: "/upper_root",
				WorkDir:  "/work_var",
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
				LowerDir: "/",
				UpperDir: "/upper_root",
				WorkDir:  "/work_root",
			},
			{
				LowerDir: "/",
				UpperDir: "/upper_var",
				WorkDir:  "/work_root",
			},
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "duplicate workDir (/work_root) found in overlay at index 1")
}

func TestOSIsValidInvalidKernelCommandLine(t *testing.T) {
	os := OS{
		KernelCommandLine: KernelCommandLine{
			ExtraCommandLine: "\"",
		},
	}

	err := os.IsValid()
	assert.ErrorContains(t, err, "invalid kernelCommandLine")
}
