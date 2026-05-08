// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

// ---------------------------------------------------------------------------
// processPackageVersionString tests
// ---------------------------------------------------------------------------

func TestProcessPackageVersionString_ValidInput(t *testing.T) {
	distTag := ".azl3"

	macros, err := processPackageVersionString("mypackage: 1.2.3-4.azl3", "mypackage.spec", distTag)
	require.NoError(t, err)
	assert.Contains(t, macros, "%azl_mypackage_version 1.2.3")
	assert.Contains(t, macros, "%azl_mypackage_release 4")
}

func TestProcessPackageVersionString_DashesInSpecName(t *testing.T) {
	distTag := ".azl3"

	macros, err := processPackageVersionString("my-cool-pkg: 2.0.0-1.azl3", "my-cool-pkg.spec", distTag)
	require.NoError(t, err)
	// Dashes should be replaced with underscores in macro names.
	assert.Contains(t, macros, "%azl_my_cool_pkg_version 2.0.0")
	assert.Contains(t, macros, "%azl_my_cool_pkg_release 1")
}

func TestProcessPackageVersionString_ReleaseWithoutDistTag(t *testing.T) {
	distTag := ".azl3"

	macros, err := processPackageVersionString("pkg: 1.0-5", "pkg.spec", distTag)
	require.NoError(t, err)
	// When the dist tag is not present in the release, it should remain unchanged.
	assert.Contains(t, macros, "%azl_pkg_version 1.0")
	assert.Contains(t, macros, "%azl_pkg_release 5")
}

func TestProcessPackageVersionString_EpochInVersion(t *testing.T) {
	distTag := ".azl3"

	macros, err := processPackageVersionString("pkg: 2:3.4.5-6.azl3", "pkg.spec", distTag)
	require.NoError(t, err)
	assert.Contains(t, macros, "%azl_pkg_epoch 2")
	assert.Contains(t, macros, "%azl_pkg_version 3.4.5")
	assert.Contains(t, macros, "%azl_pkg_release 6")
}

func TestProcessPackageVersionString_PanicsOnBadFormat(t *testing.T) {
	distTag := ".azl3"

	// Input without the expected "name: version-release" format will cause a panic
	// from the regex submatch slice indexing.
	assert.Panics(t, func() {
		processPackageVersionString("totally-invalid-input", "bad.spec", distTag)
	})
}

func TestProcessPackageVersionString_EmptyDistTag(t *testing.T) {
	distTag := ""

	macros, err := processPackageVersionString("pkg: 1.0-2.azl3", "pkg.spec", distTag)
	require.NoError(t, err)
	// With an empty dist tag, the release should not be modified.
	assert.Contains(t, macros, "%azl_pkg_release 2.azl3")
}

func TestProcessPackageVersionString_TableDriven(t *testing.T) {
	distTag := ".azl3"

	tests := []struct {
		name            string
		input           string
		specFile        string
		prefix          string
		expectedVersion string
		expectedRelease string
	}{
		{
			name:            "simple package",
			input:           "bash: 5.1.8-1.azl3",
			specFile:        "bash.spec",
			prefix:          "azl",
			expectedVersion: "%azl_bash_version 5.1.8",
			expectedRelease: "%azl_bash_release 1",
		},
		{
			name:            "package with underscores already",
			input:           "python_dateutil: 2.8.2-3.azl3",
			specFile:        "python_dateutil.spec",
			prefix:          "azl",
			expectedVersion: "%azl_python_dateutil_version 2.8.2",
			expectedRelease: "%azl_python_dateutil_release 3",
		},
		{
			name:            "multi digit release",
			input:           "kernel: 6.6.51.1-9.azl3",
			specFile:        "kernel.spec",
			prefix:          "azl",
			expectedVersion: "%azl_kernel_version 6.6.51.1",
			expectedRelease: "%azl_kernel_release 9",
		},
		{
			name:            "release with extra suffixes after dist tag",
			input:           "openssl: 3.3.0-1.azl3.1",
			specFile:        "openssl.spec",
			prefix:          "azl",
			expectedVersion: "%azl_openssl_version 3.3.0",
			expectedRelease: "%azl_openssl_release 1.1",
		},
		{
			name:            "dot in spec name replaced with underscore",
			input:           "rubygem-cool.io: 1.8.0-1.azl3",
			specFile:        "rubygem-cool.io.spec",
			prefix:          "azl",
			expectedVersion: "%azl_rubygem_cool_io_version 1.8.0",
			expectedRelease: "%azl_rubygem_cool_io_release 1",
		},
		{
			name:            "plus in spec name replaced with underscore",
			input:           "libxml++: 5.0.3-1.azl3",
			specFile:        "libxml++.spec",
			prefix:          "azl",
			expectedVersion: "%azl_libxml___version 5.0.3",
			expectedRelease: "%azl_libxml___release 1",
		},
		{
			name:            "versioned spec name with dot",
			input:           "rust-1.75: 1.75.0-27.azl3",
			specFile:        "rust-1.75.spec",
			prefix:          "azl",
			expectedVersion: "%azl_rust_1_75_version 1.75.0",
			expectedRelease: "%azl_rust_1_75_release 27",
		},
		{
			name:            "golang versioned spec with dot",
			input:           "golang-1.25: 1.25.9-1.azl3",
			specFile:        "golang-1.25.spec",
			prefix:          "azl",
			expectedVersion: "%azl_golang_1_25_version 1.25.9",
			expectedRelease: "%azl_golang_1_25_release 1",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			macros, err := processPackageVersionString(tt.input, tt.specFile, distTag)
			require.NoError(t, err)
			assert.Contains(t, macros, tt.expectedVersion)
			assert.Contains(t, macros, tt.expectedRelease)
		})
	}
}

// ---------------------------------------------------------------------------
// Helper: create a minimal spec file that rpmspec can parse
// ---------------------------------------------------------------------------

const specTemplate = `Summary:        Test spec
Name:           %s
Version:        %s
Release:        %s
License:        MIT
URL:            https://test.com
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%%description
Test spec.

%%changelog
* Mon Oct 11 2021 Test User <test@test.com> %s-%s
- Test entry.
`

func createSpecFile(t *testing.T, dir, name, version, release string) string {
	t.Helper()
	specDir := filepath.Join(dir, name)
	err := os.MkdirAll(specDir, 0755)
	require.NoError(t, err)

	specPath := filepath.Join(specDir, name+".spec")
	content := fmt.Sprintf(specTemplate, name, version, release, version, release)
	err = os.WriteFile(specPath, []byte(content), 0644)
	require.NoError(t, err)
	return specPath
}

func testBuildArch(t *testing.T) string {
	t.Helper()
	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	require.NoError(t, err)
	return arch
}

// ---------------------------------------------------------------------------
// processSpecFile tests
// ---------------------------------------------------------------------------

func TestProcessSpecFile_SinglePackage(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specPath := createSpecFile(t, tmpDir, "testpkg", "1.2.3", "4%{?dist}")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	assert.NotContains(t, macros[0], "%azl_testpkg_epoch ")
	assert.Contains(t, macros[0], "%azl_testpkg_version 1.2.3")
	assert.Contains(t, macros[1], "%azl_testpkg_release 4")
}

func TestProcessSpecFile_VersionOnly(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specPath := createSpecFile(t, tmpDir, "simplepkg", "5.0", "1%{?dist}")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	assert.Contains(t, macros[0], "%azl_simplepkg_version 5.0")
}

func TestProcessSpecFile_ReleaseDistTagStripped(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specPath := createSpecFile(t, tmpDir, "mypkg", "2.0.0", "7%{?dist}")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	// The dist tag ".azl3" should be stripped from the release.
	assert.Contains(t, macros[1], "%azl_mypkg_release 7")
	assert.NotContains(t, macros[1], ".azl3")
}

func TestProcessSpecFile_DashInPackageName(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specPath := createSpecFile(t, tmpDir, "my-cool-pkg", "3.1.0", "2%{?dist}")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	// The spec file name has dashes, which should become underscores in macro names.
	assert.NotContains(t, macros[0], "%azl_my_cool_pkg_epoch ")
	assert.Contains(t, macros[0], "%azl_my_cool_pkg_version 3.1.0")
	assert.Contains(t, macros[1], "%azl_my_cool_pkg_release 2")
}

func TestProcessSpecFile_WithSubpackages(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specDir := filepath.Join(tmpDir, "multipkg")
	err := os.MkdirAll(specDir, 0755)
	require.NoError(t, err)

	specContent := `Summary:        Test spec with subpackages
Name:           multipkg
Version:        4.0.0
Release:        3%{?dist}
License:        MIT
URL:            https://test.com
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%description
Main package.

%package devel
Summary:        Development files

%description devel
Dev files.

%package libs
Summary:        Libraries

%description libs
Libs.

%changelog
* Mon Oct 11 2021 Test User <test@test.com> 4.0.0-3
- Test entry.
`
	specPath := filepath.Join(specDir, "multipkg.spec")
	err = os.WriteFile(specPath, []byte(specContent), 0644)
	require.NoError(t, err)

	arch := testBuildArch(t)
	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	// With --srpm, rpmspec returns the source RPM entry (1 result).
	require.Len(t, macros, 2)

	assert.NotContains(t, macros[0], "%azl_multipkg_epoch ")
	assert.Contains(t, macros[0], "%azl_multipkg_version 4.0.0")
	assert.Contains(t, macros[1], "%azl_multipkg_release 3")
}

func TestProcessSpecFile_NonexistentFile(t *testing.T) {
	distTag := ".azl3"

	arch := testBuildArch(t)
	macros, err := processSpecFile("/nonexistent/path/fake.spec", arch, distTag, nil)
	assert.Error(t, err)
	assert.Nil(t, macros)
}

func TestProcessSpecFile_InvalidSpec(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specDir := filepath.Join(tmpDir, "badspec")
	err := os.MkdirAll(specDir, 0755)
	require.NoError(t, err)

	specPath := filepath.Join(specDir, "badspec.spec")
	err = os.WriteFile(specPath, []byte("this is not a valid spec file"), 0644)
	require.NoError(t, err)

	arch := testBuildArch(t)
	macros, err := processSpecFile(specPath, arch, distTag, nil)
	assert.Error(t, err)
	assert.Nil(t, macros)
}

func TestProcessSpecFile_ReleaseWithoutDistMacro(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	// Create spec with a release that has no %{?dist} macro.
	specPath := createSpecFile(t, tmpDir, "nodist", "1.0", "5")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	// Release should remain as-is since there's no dist tag to strip.
	assert.NotContains(t, macros[0], "%azl_nodist_epoch ")
	assert.Contains(t, macros[0], "%azl_nodist_version 1.0")
	assert.Contains(t, macros[1], "%azl_nodist_release 5")
}

func TestProcessSpecFile_MultiDigitVersion(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	specPath := createSpecFile(t, tmpDir, "bigver", "10.20.30", "100%{?dist}")
	arch := testBuildArch(t)

	macros, err := processSpecFile(specPath, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)
	assert.NotContains(t, macros[0], "%azl_bigver_epoch ")
	assert.Contains(t, macros[0], "%azl_bigver_version 10.20.30")
	assert.Contains(t, macros[1], "%azl_bigver_release 100")
}

func TestProcessSpecFile_AccumulatesMacros(t *testing.T) {
	distTag := ".azl3"

	tmpDir := t.TempDir()
	arch := testBuildArch(t)

	// Process a first spec and collect its macros.
	specPath1 := createSpecFile(t, tmpDir, "pkga", "1.0", "1%{?dist}")
	macros, err := processSpecFile(specPath1, arch, distTag, nil)
	require.NoError(t, err)
	require.Len(t, macros, 2)

	// Process a second spec, passing the existing macros slice.
	specPath2 := createSpecFile(t, tmpDir, "pkgb", "2.0", "2%{?dist}")
	macros, err = processSpecFile(specPath2, arch, distTag, macros)
	require.NoError(t, err)
	// Should now contain macros from both specs.
	require.Len(t, macros, 4)
	combined := strings.Join(macros, "\n")
	assert.Contains(t, combined, "%azl_pkga_version 1.0")
	assert.Contains(t, combined, "%azl_pkgb_version 2.0")
}

// ---------------------------------------------------------------------------
// writeExtraFilesToOutput tests
// ---------------------------------------------------------------------------

func TestWriteExtraFilesToOutput_NoExtraFiles(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")
	macros := []string{"%azl_pkg_version 1.0", "%azl_pkg_release 1"}

	err := writeExtraFilesToOutput(nil, macros, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	content := string(data)
	assert.Contains(t, content, "%azl_pkg_version 1.0")
	assert.Contains(t, content, "%azl_pkg_release 1")
}

func TestWriteExtraFilesToOutput_WithExtraFile(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")

	// Create an extra macros file.
	extraFile := filepath.Join(tmpDir, "extra.macros")
	err := os.WriteFile(extraFile, []byte("%extra_macro value123"), 0644)
	require.NoError(t, err)

	macros := []string{"%azl_pkg_version 1.0"}

	err = writeExtraFilesToOutput([]string{extraFile}, macros, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	content := string(data)
	assert.Contains(t, content, "%azl_pkg_version 1.0")
	assert.Contains(t, content, "%extra_macro value123")
}

func TestWriteExtraFilesToOutput_MultipleExtraFiles(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")

	extra1 := filepath.Join(tmpDir, "extra1.macros")
	extra2 := filepath.Join(tmpDir, "extra2.macros")
	err := os.WriteFile(extra1, []byte("%macro_a valA"), 0644)
	require.NoError(t, err)
	err = os.WriteFile(extra2, []byte("%macro_b valB"), 0644)
	require.NoError(t, err)

	macros := []string{"%azl_pkg_version 1.0"}

	err = writeExtraFilesToOutput([]string{extra1, extra2}, macros, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	content := string(data)
	assert.Contains(t, content, "%azl_pkg_version 1.0")
	assert.Contains(t, content, "%macro_a valA")
	assert.Contains(t, content, "%macro_b valB")
}

func TestWriteExtraFilesToOutput_SkipsEmptyPaths(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")

	macros := []string{"%azl_pkg_version 1.0"}

	err := writeExtraFilesToOutput([]string{"", "   ", ""}, macros, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	content := string(data)
	// Should only contain the original macros, nothing extra.
	assert.Contains(t, content, "%azl_pkg_version 1.0")
	lines := strings.Split(strings.TrimSpace(content), "\n")
	assert.Equal(t, len(lines), 1)
}

func TestWriteExtraFilesToOutput_NonexistentExtraFile(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")

	macros := []string{"%azl_pkg_version 1.0"}

	// Should not fail entirely — the bad file is logged and skipped.
	err := writeExtraFilesToOutput([]string{"/nonexistent/file.macros"}, macros, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	content := string(data)
	assert.Contains(t, content, "%azl_pkg_version 1.0")
}

func TestWriteExtraFilesToOutput_EmptyMacrosOutput(t *testing.T) {
	tmpDir := t.TempDir()
	outputPath := filepath.Join(tmpDir, "output.macros")

	err := writeExtraFilesToOutput(nil, nil, outputPath)
	require.NoError(t, err)

	data, err := os.ReadFile(outputPath)
	require.NoError(t, err)
	assert.Equal(t, "", string(data))
}

func TestWriteExtraFilesToOutput_InvalidOutputPath(t *testing.T) {
	// Writing to a path that cannot be created should return an error.
	err := writeExtraFilesToOutput(nil, []string{"macro"}, "/nonexistent/dir/subdir/output.macros")
	assert.Error(t, err)
}
