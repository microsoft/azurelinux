// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"io/fs"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

// TestFileCopyBasic tests file copies with default settings.
func TestFileCopyBasic(t *testing.T) {
	tempDir := t.TempDir()
	testString := "test string"
	filePerm := fs.FileMode(0o600)

	_, fileA, fileB := createTestEnv(t, tempDir, testString, filePerm)

	dstDir := filepath.Join(tempDir, "dst")
	fileADst := filepath.Join(dstDir, "a")
	fileBDst := filepath.Join(dstDir, "b")

	err := NewFileCopyBuilder(fileA, fileADst).
		Run()
	assert.NoError(t, err, "file copy (a)")

	err = NewFileCopyBuilder(fileB, fileBDst).
		Run()
	assert.NoError(t, err, "file copy (b)")

	checkPermissionsSubset(t, dstDir, os.ModePerm, "dst")

	checkFile(t, fileADst, testString, false, "a")
	checkPermissionsSame(t, fileA, fileADst, "a")

	checkFile(t, fileBDst, testString, false, "b")
}

// TestFileCopySetPerm tests file copies with file permission override.
func TestFileCopySetPerm(t *testing.T) {
	tempDir := t.TempDir()
	testString := "test string"
	filePerm := fs.FileMode(0o744)
	newFilePerm := fs.FileMode(0o600)
	newDirPerm := fs.FileMode(0o700)

	_, fileA, fileB := createTestEnv(t, tempDir, testString, filePerm)

	dstDir := filepath.Join(tempDir, "dst")
	fileADst := filepath.Join(dstDir, "a")
	fileBDst := filepath.Join(dstDir, "b")

	err := NewFileCopyBuilder(fileA, fileADst).
		SetFileMode(newFilePerm).
		SetDirFileMode(newDirPerm).
		Run()
	assert.NoError(t, err, "file copy (a)")

	err = NewFileCopyBuilder(fileB, fileBDst).
		SetFileMode(newFilePerm).
		Run()
	assert.NoError(t, err, "file copy (b)")

	checkPermissionsSubset(t, dstDir, newDirPerm, "dst")

	checkFile(t, fileADst, testString, false, "a")
	checkPermissions(t, fileADst, newFilePerm, "a")

	checkFile(t, fileBDst, testString, false, "b")
	checkPermissions(t, fileBDst, newFilePerm, "b")
}

// TestFileCopySetNoDereference tests file copies with `--no-dereference` set.
func TestFileCopySetNoDereference(t *testing.T) {
	tempDir := t.TempDir()
	testString := "test string"
	filePerm := fs.FileMode(0o600)

	_, fileA, fileB := createTestEnv(t, tempDir, testString, filePerm)

	dstDir := filepath.Join(tempDir, "dst")
	fileADst := filepath.Join(dstDir, "a")
	fileBDst := filepath.Join(dstDir, "b")

	err := NewFileCopyBuilder(fileA, fileADst).
		SetNoDereference().
		Run()
	assert.NoError(t, err, "file copy (a)")

	err = NewFileCopyBuilder(fileB, fileBDst).
		SetNoDereference().
		Run()
	assert.NoError(t, err, "file copy (b)")

	checkPermissionsSubset(t, dstDir, os.ModePerm, "dst")

	checkFile(t, fileADst, testString, false, "a")
	checkPermissionsSame(t, fileA, fileADst, "a")

	checkFile(t, fileBDst, testString, true, "b")
}

// TestFileCopyNotFile tests trying to copy a directory.
func TestFileCopyNotFile(t *testing.T) {
	tempDir := t.TempDir()
	testString := "test string"
	filePerm := fs.FileMode(0o600)

	srcDir, _, _ := createTestEnv(t, tempDir, testString, filePerm)

	dstDir := filepath.Join(tempDir, "dst")

	err := NewFileCopyBuilder(srcDir, dstDir).
		Run()
	assert.ErrorContains(t, err, "is not a file")

	err = NewFileCopyBuilder(srcDir, dstDir).
		SetNoDereference().
		Run()
	assert.ErrorContains(t, err, "is not a file or a symlink")
}

// TestFileCopyInvalidOptions tests invalid combinations of file copy options.
func TestFileCopyInvalidOptions(t *testing.T) {
	tempDir := t.TempDir()
	testString := "test string"
	filePerm := fs.FileMode(0o600)

	_, fileA, _ := createTestEnv(t, tempDir, testString, filePerm)

	dstDir := filepath.Join(tempDir, "dst")
	fileADst := filepath.Join(dstDir, "a")

	err := NewFileCopyBuilder(fileA, fileADst).
		SetNoDereference().
		SetFileMode(filePerm).
		Run()
	assert.ErrorContains(t, err, "cannot modify file permissions of symlinks")
}

func createTestEnv(t *testing.T, tempDir string, fileContents string, filePerm fs.FileMode) (string, string, string) {
	srcDir := filepath.Join(tempDir, "src")

	err := os.MkdirAll(srcDir, os.ModePerm)
	assert.NoError(t, err, "create dir (src)")

	fileA := filepath.Join(srcDir, "a")
	fileB := filepath.Join(srcDir, "b")

	err = os.WriteFile(fileA, []byte(fileContents), filePerm)
	assert.NoError(t, err, "write test file (a)")

	err = os.Symlink("./a", fileB)
	assert.NoError(t, err, "write test file (b)")

	return srcDir, fileA, fileB
}

func checkFile(t *testing.T, path string, expectedContent string, expectedIsSymlink bool,
	debugName string,
) {
	fileInfo, err := os.Lstat(path)
	assert.NoErrorf(t, err, "lstat file (%s)", debugName)

	fileIsSymlink := fileInfo.Mode().Type() == os.ModeSymlink
	assert.Equalf(t, expectedIsSymlink, fileIsSymlink, "check is symlink (%s)", debugName)

	readContent, err := os.ReadFile(path)
	assert.NoError(t, err, "read file copy (%s)", debugName)
	assert.Equalf(t, expectedContent, string(readContent), "check file copy (%s) contents", debugName)
}

// When files and directories are created in Go, the permissions specified are subject to the umask.
// So, the best we can do is ensure that the permissions are a subset.
func checkPermissionsSubset(t *testing.T, path string, expectedPerms fs.FileMode, debugName string) {
	fileInfo, err := os.Stat(path)
	assert.NoErrorf(t, err, "lstat file (%s)", debugName)

	perm := fileInfo.Mode().Perm()
	isSubset := (expectedPerms | perm) == expectedPerms
	assert.Truef(t, isSubset, "check permissions: %d subset of %d (%s)", perm, expectedPerms, debugName)
}

func checkPermissionsSame(t *testing.T, src string, dst string, debugName string) {
	fileInfo, err := os.Stat(src)
	assert.NoErrorf(t, err, "stat file (%s)", debugName)
	checkPermissions(t, dst, fileInfo.Mode().Perm(), debugName)
}

func checkPermissions(t *testing.T, path string, expectedPerms fs.FileMode, debugName string) {
	fileInfo, err := os.Stat(path)
	assert.NoErrorf(t, err, "stat file (%s)", debugName)

	perm := fileInfo.Mode().Perm()
	assert.Equalf(t, expectedPerms, perm, "check permissions (%s)", debugName)
}
