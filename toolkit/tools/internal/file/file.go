// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"bufio"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// IsDir check if a given file path is a directory.
func IsDir(filePath string) (isDir bool, err error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return
	}

	return info.IsDir(), nil
}

// IsFile returns true if the provided path is a file.
func IsFile(path string) (isFile bool, err error) {
	info, err := os.Stat(path)
	if err != nil {
		return
	}

	return !info.IsDir(), nil
}

// IsFileOrSymlink returns true if the provided path is a file or a symlink.
func IsFileOrSymlink(path string) (isFile bool, err error) {
	info, err := os.Lstat(path)
	if err != nil {
		return
	}

	isSymlink := info.Mode().Type() == os.ModeSymlink
	return isSymlink || !info.IsDir(), nil
}

// Move moves a file from src to dst. Will preserve permissions.
func Move(src, dst string) (err error) {
	const squashErrors = false

	src, err = filepath.Abs(src)
	if err != nil {
		return fmt.Errorf("failed to get absolute path for move source (%s):\n%w", src, err)
	}

	dst, err = filepath.Abs(dst)
	if err != nil {
		return fmt.Errorf("failed to get absolute path for move destination (%s):\n%w", dst, err)
	}

	if src == dst {
		logger.Log.Warnf("Skipping move. Source and destination are the same file (%s).", src)
		return
	}

	logger.Log.Debugf("Moving (%s) -> (%s)", src, dst)

	// Create the directory for the destination file
	err = os.MkdirAll(filepath.Dir(dst), os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Could not create directory for destination file (%s)", dst)
		return
	}

	// use mv command so cross partition is handled
	err = shell.ExecuteLive(squashErrors, "mv", src, dst)
	return
}

// Copy copies a file from src to dst, creating directories for the destination if needed.
// dst is assumed to be a file and not a directory. Will preserve permissions.
func Copy(src, dst string) (err error) {
	return NewFileCopyBuilder(src, dst).Run()
}

// CopyDir copies src directory to dst, creating the dst directory if needed.
// dst is assumed to be a directory and not a file.
func CopyDir(src, dst string, newDirPermissions, childFilePermissions fs.FileMode, mergedDirPermissions *fs.FileMode) (err error) {
	isDstExist, err := PathExists(dst)
	if err != nil {
		return err
	}
	if isDstExist {
		isDstDir, err := IsDir(dst)
		if err != nil {
			return err
		}
		if !isDstDir {
			return fmt.Errorf("destination exists but is not a directory (%s)", dst)
		}
		logger.Log.Debugf("Destination (%s) already exists and is a directory", dst)
		if mergedDirPermissions != nil {
			if err := os.Chmod(dst, *mergedDirPermissions); err != nil {
				return fmt.Errorf("error setting file permissions: %w", err)
			}
		}
	}

	if !isDstExist {
		logger.Log.Infof("Creating destination directory on chroot (%s)", dst)
		// Create dst dir
		err = os.MkdirAll(dst, newDirPermissions)
		if err != nil {
			return err
		}

	}

	// Open the source directory
	entries, err := os.ReadDir(src)
	if err != nil {
		return err
	}

	// Iterate over the entries in the source directory
	for _, entry := range entries {
		srcPath := filepath.Join(src, entry.Name())
		dstPath := filepath.Join(dst, entry.Name())

		if entry.IsDir() {
			// If it's a directory, recursively copy it
			if err := CopyDir(srcPath, dstPath, newDirPermissions, childFilePermissions, mergedDirPermissions); err != nil {
				return err
			}
		} else {
			// If it's a file, copy it and set file permissions
			if err := NewFileCopyBuilder(srcPath, dstPath).SetFileMode(childFilePermissions).Run(); err != nil {
				return err
			}
		}
	}

	return nil
}

// Read reads a string from the file src.
func Read(src string) (data string, err error) {
	logger.Log.Debugf("Reading from (%s)", src)

	bytes, err := os.ReadFile(src)
	data = string(bytes)
	return
}

// readLines reads file under path and returns lines as strings and any error encountered
func ReadLines(path string) (lines []string, err error) {
	handle, err := os.Open(path)
	if err != nil {
		return
	}
	defer handle.Close()

	scanner := bufio.NewScanner(handle)

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines, scanner.Err()
}

// Create creates a new file with the provided Unix permissions
func Create(dst string, perm os.FileMode) (err error) {
	logger.Log.Debugf("Creating (%s) with mode (%v)", dst, perm)

	dstFile, err := os.OpenFile(dst, os.O_CREATE|os.O_EXCL, perm)
	if err != nil {
		return
	}
	defer dstFile.Close()
	return
}

// Write writes a string to the file dst.
func Write(data string, dst string) (err error) {
	logger.Log.Debugf("Writing to (%s)", dst)

	err = os.WriteFile(dst, []byte(data), 0o666)
	return
}

// WriteLines writes each string to the same file, separated by lineSeparator (e.g. "\n").
func WriteLines(dataLines []string, destinationPath string) (err error) {
	logger.Log.Debugf("Writing to (%s)", destinationPath)

	dstFile, err := os.Create(destinationPath)
	if err != nil {
		return
	}
	defer dstFile.Close()

	for _, line := range dataLines {
		_, err = fmt.Fprintln(dstFile, line)
		if err != nil {
			return
		}
	}
	return
}

// Append appends a string to the end of file dst.
func Append(data string, dst string) (err error) {
	logger.Log.Debugf("Appending to file (%s): (%s)", dst, data)

	dstFile, err := os.OpenFile(dst, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0644)
	if err != nil {
		return
	}
	defer dstFile.Close()

	_, err = dstFile.WriteString(data)
	return
}

// RemoveFileIfExists will delete a file if it exists on disk.
func RemoveFileIfExists(path string) (err error) {
	removeErr := os.Remove(path)
	if removeErr != nil && !errors.Is(removeErr, fs.ErrNotExist) {
		err = fmt.Errorf("failed to remove file (%s):\n%w", path, err)
	}
	return
}

// RemoveDirectoryContents will delete the contents of a directory, but not the
// directory itself. If the directory does not exist, it will return an error.
func RemoveDirectoryContents(path string) (err error) {
	dir, err := os.ReadDir(path)
	if err != nil {
		return
	}

	for _, entry := range dir {
		childPath := filepath.Join(path, entry.Name())
		logger.Log.Debugf("Removing (%s)", childPath)
		err = os.RemoveAll(childPath)
		if err != nil {
			return
		}
	}

	return
}

// GenerateSHA1 calculates a sha1 of a file
func GenerateSHA1(path string) (hash string, err error) {
	file, err := os.Open(path)
	if err != nil {
		return
	}
	defer file.Close()

	sha1Generator := sha1.New()
	_, err = io.Copy(sha1Generator, file)
	if err != nil {
		return
	}

	rawHash := sha1Generator.Sum(nil)
	hash = hex.EncodeToString(rawHash)

	return
}

// GenerateSHA256 calculates a sha256 of a file
func GenerateSHA256(path string) (hash string, err error) {
	file, err := os.Open(path)
	if err != nil {
		return
	}
	defer file.Close()

	sha256Generator := sha256.New()
	_, err = io.Copy(sha256Generator, file)
	if err != nil {
		return
	}

	rawHash := sha256Generator.Sum(nil)
	hash = hex.EncodeToString(rawHash)

	return
}

// DirExists returns true if the directory exists,
// false otherwise.
func DirExists(path string) (exists bool, err error) {
	stat, err := os.Stat(path)
	if err == nil && stat.IsDir() {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return stat.IsDir(), err
}

// PathExists returns true if the path exists,
// false otherwise.
func PathExists(path string) (exists bool, err error) {
	_, err = os.Stat(path)
	if os.IsNotExist(err) {
		return false, nil
	}
	return (err == nil), err
}

// GetAbsPathWithBase converts 'inputPath' to an absolute path starting
// from 'baseDirPath', but only if it wasn't an absolute path in the first place.
func GetAbsPathWithBase(baseDirPath, inputPath string) string {
	if filepath.IsAbs(inputPath) {
		return inputPath
	}

	return filepath.Join(baseDirPath, inputPath)
}

func IsDirEmpty(path string) (bool, error) {
	file, err := os.Open(path)
	if err != nil {
		return false, err
	}
	defer file.Close()

	_, err = file.Readdirnames(1)
	if err == io.EOF {
		// Directory has no children.
		return true, nil
	}
	if err != nil {
		return false, err
	}

	// Directory has at least 1 child.
	return false, nil
}

func createDestinationDir(dst string, dirmode os.FileMode) (err error) {
	isDstExist, err := PathExists(dst)
	if err != nil {
		return err
	}
	if isDstExist {
		isDstDir, err := IsDir(dst)
		if err != nil {
			return err
		}
		if isDstDir {
			return fmt.Errorf("destination (%s) already exists and is a directory", dst)
		}
	}

	if !isDstExist {
		// Create destination directory if needed
		destDir := filepath.Dir(dst)
		err = os.MkdirAll(destDir, dirmode)
		if err != nil {
			return
		}
	}

	return
}

// CopyResourceFile copies a file from an embedded binary resource file to disk.
// This will override any existing file.
func CopyResourceFile(srcFS fs.FS, srcFile, dst string, dirmode os.FileMode, filemode os.FileMode) error {
	logger.Log.Debugf("Copying resource (%s) -> (%s)", srcFile, dst)

	err := createDestinationDir(dst, dirmode)
	if err != nil {
		return err
	}

	source, err := srcFS.Open(srcFile)
	if err != nil {
		return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to open source:\n%w", srcFile, dst, err)
	}
	defer source.Close()

	destination, err := os.OpenFile(dst, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, filemode)
	if err != nil {
		return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to open destination:\n%w", srcFile, dst, err)
	}
	defer destination.Close()

	_, err = io.Copy(destination, source)
	if err != nil {
		return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to copy bytes:\n%w", srcFile, dst, err)
	}

	err = os.Chmod(dst, filemode)
	if err != nil {
		return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to set filemode:\n%w", srcFile, dst, err)
	}

	return nil
}

func EnumerateDirFiles(dirPath string) (filePaths []string, err error) {
	err = filepath.Walk(dirPath, func(filePath string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		filePaths = append(filePaths, filePath)

		return nil
	})
	if err != nil {
		return nil, fmt.Errorf("failed to enumerate files under %s:\n%w", dirPath, err)
	}
	return filePaths, nil
}

func CommandExists(name string) (bool, error) {
	_, err := exec.LookPath("mkinitrd")
	if err != nil {
		if errors.Is(err, exec.ErrNotFound) {
			return false, nil
		}
		return false, err
	}
	return true, nil
}
