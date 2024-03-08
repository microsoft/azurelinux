// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create read-only root partitions

package diskutils

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/randomization"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	mappingVerityPrefix = "verity-"
	debugMountPoint     = "/mnt/verity_overlay_debug_tmpfs"
)

var (
	// The roothash line will be of the form "Root hash:      123456789abcd"
	// Turn on multiline mode with ?m
	rootHashLineRegex = regexp.MustCompile(`(?m)^Root hash:\s+(\S*)$`)
)

// VerityDevice represents a device mapper linear device used for a dm-verity read-only partition.
// - MappedName is the desired device mapper name
// - MappedDevice is the full path of the created device mapper device
// - BackingDevice is the underlying file/device which backs the partition
// - FecRoots is the number of error correcting roots, 0 to omit error correction
// - ValidateOnBoot will cause a full, user-mode analysis of the verity disk during boot (good for debugging)
// - UseRootHashSignature indicates a signature file has been included with the verity disk and should be checked
// - ErrorBehavior is what dm-verity should do in the event of corruption (ignore, panic, restart)
// - TmpfsOverlays is a list of tmpfs overlays which will be created after the verity partition is mounted
// - TmpfsOverlaySize is the size argument to pass to the tmpfs mount command (1234, 1234<k,m,g>, 20%)
// - TmpfsOverlaysDebugMount indicates if the overlays should be made accessible for debugging purposes
type VerityDevice struct {
	MappedName              string
	MappedDevice            string
	BackingDevice           string
	FecRoots                int
	ValidateOnBoot          bool
	UseRootHashSignature    bool
	ErrorBehavior           string
	TmpfsOverlays           []string
	TmpfsOverlaySize        string
	TmpfsOverlaysDebugMount string
}

// AddRootVerityFilesToInitramfs adds files needed for a verity root to the initramfs
// - workingFolder is a temporary folder to extract the initramfs to
// - initramfsPath is the path to the initramfs
func (v *VerityDevice) AddRootVerityFilesToInitramfs(workingFolder, initramfsPath string) (err error) {
	verityWorkingDirectory := filepath.Join(workingFolder, v.MappedName)

	// Measure the disk and generate the hash and fec files
	err = v.createVerityDisk(verityWorkingDirectory)
	if err != nil {
		return fmt.Errorf("failed while generating a verity disk:\n%w", err)
	}

	// Now place them in the initramfs
	logger.Log.Info("Adding dm-verity read-only root files into initramfs")
	initramfs, err := OpenInitramfs(initramfsPath)
	defer initramfs.Close()
	if err != nil {
		return fmt.Errorf("failed to open the initramfs:\n%w", err)
	}

	verityFiles, err := os.ReadDir(verityWorkingDirectory)
	if err != nil {
		return
	}

	for _, file := range verityFiles {
		filePath := filepath.Join(verityWorkingDirectory, file.Name())
		logger.Log.Debugf("Adding (%s) to initramfs", filePath)
		// Place each file in the root of the initramfs
		err = initramfs.AddFileToInitramfs(filePath, file.Name())
		if err != nil {
			return fmt.Errorf("failed to add (%s) to initramfs:\n%w", filePath, err)
		}
	}

	return
}

func (v *VerityDevice) createVerityDisk(verityDirectory string) (err error) {
	const (
		saltLength = 64
		hashAlg    = "sha256"
	)
	var (
		verityFecArgs    []string
		verityArgs       []string
		verityVerifyArgs []string
		fileBase         = filepath.Join(verityDirectory, v.MappedName)
		rootHashPath     = fmt.Sprintf("%s.roothash", fileBase)
		hashtreePath     = fmt.Sprintf("%s.hashtree", fileBase)
		fecFilePath      = fmt.Sprintf("%s.fec", fileBase)
	)

	err = os.MkdirAll(verityDirectory, os.ModePerm)
	if err != nil {
		return
	}

	rootHashFile, err := os.Create(rootHashPath)
	if err != nil {
		return
	}
	defer rootHashFile.Close()

	salt, err := randomization.RandomString(64, randomization.LegalCharactersHex)
	if err != nil {
		return
	}

	if v.FecRoots > 0 {
		verityFecArgs = []string{
			fmt.Sprintf("--fec-device=%s", fecFilePath),
			fmt.Sprintf("--fec-roots=%d", v.FecRoots),
		}
	}

	verityArgs = []string{
		"--salt",
		salt,
		"--hash",
		hashAlg,
		"--verbose",
		"--debug",
		"format",
		v.MappedDevice,
		hashtreePath,
	}

	logger.Log.Info("Generating a dm-verity read-only partition")
	verityOutput, stderr, err := shell.Execute("veritysetup", append(verityFecArgs, verityArgs...)...)
	if err != nil {
		err = fmt.Errorf("failed to create verity disk:\n%v:\n%w", stderr, err)
		return
	}

	// Searches for a line like: "Root hash:      1234567890abcdefg..."
	matches := rootHashLineRegex.FindStringSubmatch(verityOutput)

	if len(matches) != 2 {
		err = fmt.Errorf("failed to extract root hash from veritysetup output: (%s), matched: (%#v)", verityOutput, matches)
		return
	}
	rootHash := matches[1]

	logger.Log.Infof("Verity partition completed, root hash: (%s)", rootHash)
	_, err = rootHashFile.WriteString(rootHash)
	if err != nil {
		return
	}

	//Verify the disk was created correctly:
	verityVerifyArgs = []string{
		"--verbose",
		"--debug",
		"verify",
		v.MappedDevice,
		hashtreePath,
		rootHash,
	}

	logger.Log.Info("Verifying the verity partition")
	verityOutput, stderr, err = shell.Execute("veritysetup", verityVerifyArgs...)
	if err != nil {
		err = fmt.Errorf("failed to validate new verity disk (%s):\n%v\n%w", verityOutput, stderr, err)
	}

	return
}

// PrepReadOnlyDevice sets up a device mapper linear map.
// This map will have the correct name of the final verity disk, and can be
// switched to read-only when the final image is ready for measurement.
// - partDevPath is the path of the root partition device (likely a loopback device)
// - partition is the disk configuration
// - readOnlyConfig is the root read-only settings
func PrepReadOnlyDevice(partDevPath string, partition configuration.Partition, readOnlyConfig configuration.ReadOnlyVerityRoot) (readOnlyDevice VerityDevice, err error) {
	const (
		linearTable = `0 (%d) linear (%s) 0`
	)

	if !readOnlyConfig.Enable {
		err = fmt.Errorf("verity is not enabled, can't update partition (%s)", partition.ID)
		return
	}

	// Save the required information from the config into the device struct
	finalDeviceName := fmt.Sprintf("%s%s", mappingVerityPrefix, readOnlyConfig.Name)
	readOnlyDevice.BackingDevice = partDevPath
	readOnlyDevice.MappedName = finalDeviceName
	readOnlyDevice.MappedDevice = filepath.Join("/dev/mapper/", finalDeviceName)
	readOnlyDevice.ErrorBehavior = readOnlyConfig.VerityErrorBehavior.String()
	readOnlyDevice.ValidateOnBoot = readOnlyConfig.ValidateOnBoot
	if readOnlyConfig.ErrorCorrectionEnable {
		readOnlyDevice.FecRoots = readOnlyConfig.ErrorCorrectionEncodingRoots
	} else {
		readOnlyDevice.FecRoots = 0
	}
	readOnlyDevice.TmpfsOverlays = readOnlyConfig.TmpfsOverlays
	if len(readOnlyDevice.TmpfsOverlays) > 0 {
		readOnlyDevice.TmpfsOverlaySize = readOnlyConfig.TmpfsOverlaySize
	}
	if readOnlyConfig.TmpfsOverlayDebugEnabled {
		readOnlyDevice.TmpfsOverlaysDebugMount = debugMountPoint
	}
	readOnlyDevice.UseRootHashSignature = readOnlyConfig.RootHashSignatureEnable

	// linear mappings need to know the size of the disk in blocks ahead of time
	deviceSizeStr, stderr, err := shell.Execute("blockdev", "--getsz", readOnlyDevice.BackingDevice)
	if err != nil {
		err = fmt.Errorf("failed to get loopback device size (%s):\n%v\n%w", partDevPath, stderr, err)
		return
	}
	deviceSizeInt, err := strconv.ParseUint(strings.TrimSpace(deviceSizeStr), 10, 64)
	if err != nil {
		err = fmt.Errorf("failed to convert disk size (%s) to integer:\n%w", deviceSizeStr, err)
		return
	}

	populatedTable := fmt.Sprintf(linearTable, deviceSizeInt, readOnlyDevice.BackingDevice)
	dmsetupArgs := []string{
		"create",
		readOnlyDevice.MappedName,
		"--table",
		populatedTable,
	}
	_, stderr, err = shell.Execute("dmsetup", dmsetupArgs...)
	if err != nil {
		err = fmt.Errorf("failed to create a device mapper device (%s):\n%w", stderr, err)
		return
	}

	logger.Log.Debugf("Remapped partition (%s) for read-only prep to %s", partition.ID, readOnlyDevice.MappedDevice)

	return
}

// CleanupVerityDevice removes the device mapper linear mapping, but leaves the backing device unchanged
func (v *VerityDevice) CleanupVerityDevice() (err error) {
	stdout, stderr, err := shell.Execute("dmsetup", "remove", v.MappedName)
	if err != nil {
		err = fmt.Errorf("failed to clean up device mapper device:%s\n%v\n%w", stdout, stderr, err)
		return
	}
	return
}

// SwitchDeviceToReadOnly switches the root device linear map to read only
// Will also re-mount the moint point to respect this.
// - mountPointOrDevice is either the location of the mount, or the device which was mounted (mount command will take either)
// - mountArgs are any special mount options used which should continue to be used
func (v *VerityDevice) SwitchDeviceToReadOnly(mountPointOrDevice, mountArgs string) (err error) {
	const (
		remountOptions = "remount,ro"
	)

	// Suspending the mapped device will force a sync
	_, stderr, err := shell.Execute("dmsetup", "suspend", v.MappedName)
	if err != nil {
		return fmt.Errorf("failed to suspend device (%s):\n%v\n%w", v.MappedDevice, stderr, err)
	}

	// Need to get the table data to "recreate" the device with read-only set
	table, stderr, err := shell.Execute("dmsetup", "table", v.MappedName)
	if err != nil {
		return fmt.Errorf("failed to get table for device (%s):\n%v\n%w", v.MappedDevice, stderr, err)
	}

	// Switch the linear map to read-only
	dmsetupArgs := []string{
		"reload",
		"--readonly",
		v.MappedName,
		"--table",
		table,
	}
	_, stderr, err = shell.Execute("dmsetup", dmsetupArgs...)
	if err != nil {
		return fmt.Errorf("failed to reload device (%s) in read-only mode:\n%v\n%w", v.MappedDevice, stderr, err)
	}

	// Re-enable the device
	_, stderr, err = shell.Execute("dmsetup", "resume", v.MappedName)
	if err != nil {
		return fmt.Errorf("failed to resume device (%s):\n%v\n%w", v.MappedDevice, stderr, err)
	}

	// Mounts don't respect the read-only nature of the underlying device, force a remount
	_, stderr, err = shell.Execute("mount", "-o", mountArgs+remountOptions, mountPointOrDevice)
	if err != nil {
		return fmt.Errorf("failed to remount (%s):\n%v\n%w", mountPointOrDevice, stderr, err)
	}
	return
}

// IsReadOnlyDevice checks if a given device is a dm-verity read-only device
// - devicePath is the device to check
func IsReadOnlyDevice(devicePath string) (result bool) {
	verityPrefix := filepath.Join(mappingFilePath, mappingVerityPrefix)
	return strings.HasPrefix(devicePath, verityPrefix)
}
