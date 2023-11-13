// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"bufio"
	"bytes"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"os/user"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/marinertoolusers"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const compareBufferSize = 4096

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

// Move moves a file from src to dst. Will preserve permissions.
func Move(src, dst string) (err error) {
	const squashErrors = false

	src, err = filepath.Abs(src)
	if err != nil {
		logger.Log.Errorf("Failed to get absolute path for move source (%s).", src)
		return
	}

	dst, err = filepath.Abs(dst)
	if err != nil {
		logger.Log.Errorf("Failed to get absolute path for move destination (%s).", dst)
		return
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
	return copyWithPermissions(src, dst, os.ModePerm, false, os.ModePerm, nil)
}

// Copy copies a file from src to dst, creating directories for the destination if needed.
// dst is assumed to be a file and not a directory. Will preserve permissions. Ownership will
// be assigned to the given user.
func CopyWithUser(src, dst string, user *user.User) (err error) {
	return copyWithPermissions(src, dst, os.ModePerm, false, os.ModePerm, user)
}

// CopyAndChangeMode copies a file from src to dst, creating directories with the given access rights for the destination if needed.
// dst is assumed to be a file and not a directory. Will change the permissions to the given value.
func CopyAndChangeMode(src, dst string, dirmode os.FileMode, filemode os.FileMode) (err error) {
	return copyWithPermissions(src, dst, dirmode, true, filemode, nil)
}

// CopyAndChangeModeWithUser copies a file from src to dst, creating directories with the given access rights for the destination if needed.
// dst is assumed to be a file and not a directory. Will change the permissions to the given value. Ownership will be
// assigned to the given user.
func CopyAndChangeModeWithUser(src, dst string, dirmode os.FileMode, filemode os.FileMode, user *user.User) (err error) {
	return copyWithPermissions(src, dst, dirmode, true, filemode, user)
}

func CalculateHashes(inputFiles []string) (hash []byte, err error) {
	fileHasher := sha256.New()
	for _, inputFile := range inputFiles {
		// Read the file, and pass into the hasher
		var data []byte
		data, err = os.ReadFile(inputFile)
		if err != nil {
			err = fmt.Errorf("unable to read input file:\n%w", err)
			return
		}
		_, err = fileHasher.Write(data)
		if err != nil {
			err = fmt.Errorf("unable to hash file:\n%w", err)
			return
		}
	}
	hash = fileHasher.Sum(nil)
	return
}

func readOneCompareBlock(in io.Reader, buffer *[]byte) (readSize int, err error) {
	readSize = 0
	for currentRead := 0; readSize < compareBufferSize; {
		currentRead, err = in.Read((*buffer)[readSize:])
		readSize += currentRead
		if err != nil {
			break
		}
	}
	return
}

func compareFileByteStreams(in1, in2 io.Reader) (isSame bool, err error) {
	buffer1 := make([]byte, compareBufferSize)
	buffer2 := make([]byte, compareBufferSize)
	isSame = true
	for {
		var readSize1 int
		readSize1, err = readOneCompareBlock(in1, &buffer1)
		if err != nil && err != io.EOF {
			err = fmt.Errorf("unable to read from input 1 while comparing files:\n%w", err)
			isSame = false
			return
		} else {
			err = nil
		}

		var readSize2 int
		readSize2, err = readOneCompareBlock(in2, &buffer2)
		if err != nil && err != io.EOF {
			err = fmt.Errorf("unable to read from input 2 while comparing files:\n%w", err)
			isSame = false
			return
		} else {
			err = nil
		}

		if readSize1 != readSize2 {
			isSame = false
			return
		}
		if readSize1 == 0 {
			break
		}
		if !bytes.Equal(buffer1, buffer2) {
			isSame = false
			return
		}
	}
	return
}

func ContentsAreSame(src, dst string) (isSame bool, err error) {
	isSame = false
	srcExists, err := PathExists(src)
	if err != nil {
		err = fmt.Errorf("unable to check if destination file exists:\n%w", err)
		return
	}
	dstExists, err := PathExists(dst)
	if err != nil {
		err = fmt.Errorf("unable to check if destination file exists:\n%w", err)
		return
	}
	if srcExists && dstExists {
		// var hash1, hash2 []byte
		// // check if the files are the same
		// hash1, err = CalculateHashes([]string{src})
		// if err != nil {
		// 	err = fmt.Errorf("unable to calculate hash:\n%w", err)
		// 	return
		// }
		// hash2, err = CalculateHashes([]string{dst})
		// if err != nil {
		// 	err = fmt.Errorf("unable to calculate hash:\n%w", err)
		// 	return
		// }
		// if bytes.Equal(hash1, hash2) {
		// 	// The files are the same, so skip the restore
		// 	isSame = true
		// }
		var srcFile, dstFile *os.File
		srcFile, err = os.Open(src)
		if err != nil {
			err = fmt.Errorf("unable to open source file:\n%w", err)
			return
		}
		defer srcFile.Close()
		dstFile, err = os.Open(dst)
		if err != nil {
			err = fmt.Errorf("unable to open destination file:\n%w", err)
			return
		}
		defer dstFile.Close()
		isSame, err = compareFileByteStreams(srcFile, dstFile)
		if err != nil {
			err = fmt.Errorf("unable to compare files:\n%w", err)
			return
		}
	}
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

	dstFile, err := os.Create(dst)
	if err != nil {
		return
	}
	defer dstFile.Close()

	_, err = dstFile.WriteString(data)
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

// copyWithPermissions copies a file from src to dst, creating directories with the requested mode for the destination if needed.
// Depending on the changeMode parameter, it may also change the file mode.
func copyWithPermissions(src, dst string, dirmode os.FileMode, changeMode bool, filemode os.FileMode, user *user.User) (err error) {
	const squashErrors = false

	logger.Log.Debugf("Copying (%s) -> (%s)", src, dst)

	isSrcFile, err := IsFile(src)
	if err != nil {
		return
	}
	if !isSrcFile {
		return fmt.Errorf("source (%s) is not a file", src)
	}

	err = createDestinationDir(dst, dirmode, user)
	if err != nil {
		return
	}

	err = shell.ExecuteLive(squashErrors, "cp", "--preserve=mode", src, dst)
	if err != nil {
		return
	}

	if changeMode {
		logger.Log.Debugf("Calling chmod on (%s) with the mode (%v)", dst, filemode)
		err = os.Chmod(dst, filemode)
	}

	if user != nil {
		err = marinerusers.GiveSinglePathToUser(dst, user)
		if err != nil {
			return
		}
	}

	return
}

func createDestinationDir(dst string, dirmode os.FileMode, user *user.User) (err error) {
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
		if user != nil {
			err = marinertoolusers.GiveSinglePathToUser(destDir, user)
			if err != nil {
				return
			}
		}
	}

	return
}

// CopyResourceFile copies a file from an embedded binary resource file.
func CopyResourceFile(srcFS fs.FS, srcFile, dst string, dirmode os.FileMode, filemode os.FileMode, user *user.User) error {
	logger.Log.Debugf("Copying resource (%s) -> (%s)", srcFile, dst)

	err := createDestinationDir(dst, dirmode, user)
	if err != nil {
		return err
	}

	source, err := srcFS.Open(srcFile)
	if err != nil {
		return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to open source:\n%w", srcFile, dst, err)
	}
	defer source.Close()

	destination, err := os.OpenFile(dst, os.O_WRONLY|os.O_CREATE, filemode)
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

	if user != nil {
		err = marinertoolusers.GiveSinglePathToUser(dst, user)
		if err != nil {
			return fmt.Errorf("failed to copy resource (%s) -> (%s):\nfailed to set ownership:\n%w", srcFile, dst, err)
		}
	}

	return nil
}
