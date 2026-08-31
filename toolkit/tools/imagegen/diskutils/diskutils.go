// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package diskutils

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/sirupsen/logrus"
	"golang.org/x/sys/unix"
)

var (
	// When calling mkfs, the default options change depending on the host OS you are running on and typically match
	// what the distro has decided is best for their OS. For example, for ext2/3/4, the defaults are stored in
	// /etc/mke2fs.conf.
	// However, when building Azure Linux images, the defaults should be as consistent as possible and should only contain
	// features that are supported on Azure Linux.
	DefaultMkfsOptions = map[string][]string{
		"ext2": {"-b", "4096", "-O", "none,sparse_super,large_file,filetype,resize_inode,dir_index,ext_attr"},
		"ext3": {"-b", "4096", "-O", "none,sparse_super,large_file,filetype,resize_inode,dir_index,ext_attr,has_journal"},
		// grub2 doesn't recognize ext4 with metadata_csum_seed enabled
		// ^metadata_csum_seed disables filesystem to store the metadata checksum seed in the superblock, hence disables changing uuid of mounted filesystem
		"ext4": {"-b", "4096", "-O", "none,sparse_super,large_file,filetype,resize_inode,dir_index,ext_attr,has_journal,extent,huge_file,flex_bg,metadata_csum,64bit,dir_nlink,extra_isize,^metadata_csum_seed"},
	}
)

type blockDevicesOutput struct {
	Devices []blockDeviceInfo `json:"blockdevices"`
}

type blockDeviceInfo struct {
	Name   string      `json:"name"`    // Example: sda
	MajMin string      `json:"maj:min"` // Example: 1:2
	Size   json.Number `json:"size"`    // Number of bytes. Can be a quoted string or a JSON number, depending on the util-linux version
	Model  string      `json:"model"`   // Example: 'Virtual Disk'
}

// SystemBlockDevice defines a block device on the host computer
type SystemBlockDevice struct {
	DevicePath  string // Example: /dev/sda
	RawDiskSize uint64 // Size in bytes
	Model       string // Example: Virtual Disk
}

type partitionInfoOutput struct {
	Devices []PartitionInfo `json:"blockdevices"`
}

type PartitionInfo struct {
	Name              string `json:"name"`       // Example: nbd0p1
	Path              string `json:"path"`       // Example: /dev/nbd0p1
	PartitionTypeUuid string `json:"parttype"`   // Example: c12a7328-f81f-11d2-ba4b-00a0c93ec93b
	FileSystemType    string `json:"fstype"`     // Example: vfat
	Uuid              string `json:"uuid"`       // Example: 4BD9-3A78
	PartUuid          string `json:"partuuid"`   // Example: 7b1367a6-5845-43f2-99b1-a742d873f590
	Mountpoint        string `json:"mountpoint"` // Example: /mnt/os/boot
	PartLabel         string `json:"partlabel"`  // Example: boot
	Type              string `json:"type"`       // Example: part
	SizeInBytes       uint64 `json:"size"`       // Example: 4096
}

type loopbackListOutput struct {
	Devices []loopbackDevice `json:"loopdevices"`
}

type loopbackDevice struct {
	Name        string `json:"name"`
	BackingFile string `json:"back-file"`
}

type PartitionTablePartition struct {
	// Populated from "sfdisk --json":
	Path         string `json:"node"`  // Example: /dev/loop1p1
	Start        int64  `json:"start"` // Example: 2048
	Size         int64  `json:"size"`  // Example: 16384
	PartTypeUuid string `json:"type"`  // Example: C12A7328-F81F-11D2-BA4B-00A0C93EC93B
	PartUuid     string `json:"uuid"`  // Example: 2789D1BC-3909-4B06-AD2D-DA531DABF7C8
	PartLabel    string `json:"name"`  // Example: rootfs

	// Populated from "blkid --probe":
	FileSystemType string // Example: vfat
	FileSystemUuid string // Example: 4BD9-3A78
}

type PartitionTable struct {
	Label      string                    `json:"label"`      // Example: gpt
	Id         string                    `json:"id"`         // Example: 1DFD88CF-6214-4574-97A2-C605D411CFBE
	Device     string                    `json:"device"`     // Example: /dev/loop1
	Unit       string                    `json:"unit"`       // Example: sectors
	FirstLba   int64                     `json:"firstlba"`   // Example: 2048
	LastLba    int64                     `json:"lastlba"`    // Example: 8388574
	SectorSize int                       `json:"sectorsize"` // Example: 512
	Partitions []PartitionTablePartition `json:"partitions"`
}

type partitionTableOutput struct {
	PartitionTable *PartitionTable `json:"partitiontable"`
}

const (
	// AutoEndSize is used as the disk's "End" value to indicate it should be picked automatically
	AutoEndSize = 0

	EfiSystemPartitionTypeUuid    = "c12a7328-f81f-11d2-ba4b-00a0c93ec93b"
	BiosBootPartitionTypeUuid     = "21686148-6449-6e6f-744e-656564454649"
	GenericLinuxPartitionTypeUuid = "0fc63daf-8483-4772-8e79-3d69d8477de4"
)

const (
	// mappingFilePath is used for device mapping paths
	mappingFilePath = "/dev/mapper/"

	// maxPrimaryPartitionsForMBR is the maximum number of primary partitions
	// allowed in the case of MBR partition
	maxPrimaryPartitionsForMBR = 4

	// name of all possible partition types
	primaryPartitionType  = "primary"
	extendedPartitionType = "extended"
	logicalPartitionType  = "logical"
)

// Unit to byte conversion values
const (
	B  = 1
	KB = 1000
	MB = 1000 * 1000
	GB = 1000 * 1000 * 1000
	TB = 1000 * 1000 * 1000 * 1000

	KiB = 1024
	MiB = 1024 * 1024
	GiB = 1024 * 1024 * 1024
	TiB = 1024 * 1024 * 1024 * 1024
)

var (
	sizeAndUnitRegexp = regexp.MustCompile(`(\d+)((Ki?|Mi?|Gi?|Ti?)?B)`)
	diskDevPathRegexp = regexp.MustCompile(`^/dev/(\w+)$`)

	unitToBytes = map[string]uint64{
		"B":   B,
		"KB":  KB,
		"MB":  MB,
		"GB":  GB,
		"TB":  TB,
		"KiB": KiB,
		"MiB": MiB,
		"GiB": GiB,
		"TiB": TiB,
	}
)

// BytesToSizeAndUnit takes a number of bytes and returns friendly representation of a size (for example 100GB).
func BytesToSizeAndUnit(bytes uint64) string {
	var (
		unitSize  uint64
		unitCount uint64
		unitName  string
	)

	sizes := []uint64{B, KiB, MiB, GiB, TiB}

	// Default to unit "Bytes" to handle the case where bytes is 0
	unitSize = B

	for _, unit := range sizes {
		if bytes >= unit {
			unitSize = unit
		}
	}

	for unit, unitBytes := range unitToBytes {
		if unitBytes == unitSize {
			unitName = unit
			break
		}
	}

	unitCount = bytes / unitSize

	return fmt.Sprintf("%d%s", unitCount, unitName)
}

// SizeAndUnitToBytes takes a friendly representation of a size (for example 100GB) and return the number of bytes it represents.
func SizeAndUnitToBytes(sizeAndUnit string) (bytes uint64, err error) {
	const (
		sizeIndex = 1
		unitIndex = 2
	)

	// Match size and unit.  Examples: 2GB, 512MiB
	matches := sizeAndUnitRegexp.FindAllStringSubmatch(sizeAndUnit, -1)

	// must be at least one match
	if len(matches) == 0 || len(matches[0]) <= 2 {
		err = fmt.Errorf("sizeAndUnit must contain a number and a unit type")
		return
	}
	match := matches[0]

	sizeString := match[sizeIndex]
	unit := match[unitIndex]

	size, err := strconv.ParseUint(sizeString, 10, 64)
	if err != nil {
		return
	}

	if unitBytes, ok := unitToBytes[unit]; ok {
		bytes = size * unitBytes
	} else {
		err = fmt.Errorf("unknown unit type (%s)", unit)
		return
	}

	return
}

// ApplyRawBinaries applies all raw binaries described in disk configuration to the specified disk
func ApplyRawBinaries(diskDevPath string, disk configuration.Disk) (err error) {
	rawBinaries := disk.RawBinaries

	for idx := range rawBinaries {
		rawBinary := rawBinaries[idx]
		err = ApplyRawBinary(diskDevPath, rawBinary)
		if err != nil {
			return err
		}
	}
	return
}

// ApplyRawBinary applies a single raw binary at offset (seek) with blocksize to the specified disk
func ApplyRawBinary(diskDevPath string, rawBinary configuration.RawBinary) (err error) {
	ddArgs := []string{
		fmt.Sprintf("if=%s", rawBinary.BinPath),   // Input file.
		fmt.Sprintf("of=%s", diskDevPath),         // Output file.
		fmt.Sprintf("bs=%d", rawBinary.BlockSize), // Size of one copied block.
		fmt.Sprintf("seek=%d", rawBinary.Seek),    // Block number to start copying in the output file at.
		"conv=notrunc",                            // Prevent truncation.
	}

	_, stderr, err := shell.Execute("dd", ddArgs...)
	if err != nil {
		err = fmt.Errorf("failed to apply raw binary with dd:\n%v\n%w", stderr, err)
	}
	return
}

// CreateEmptyDisk creates an empty raw disk in the given working directory as described in disk configuration
func CreateEmptyDisk(workDirPath, diskName string, maxSize uint64) (diskFilePath string, err error) {
	diskFilePath = filepath.Join(workDirPath, diskName)

	err = CreateSparseDisk(diskFilePath, maxSize, 0o644)
	return
}

// CreateSparseDisk creates an empty sparse disk file.
func CreateSparseDisk(diskPath string, size uint64, perm os.FileMode) (err error) {
	// Open and truncate the file.
	file, err := os.OpenFile(diskPath, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, perm)
	if err != nil {
		return fmt.Errorf("failed to create empty disk file:\n%w", err)
	}

	// Resize the file to the desired size.
	err = file.Truncate(int64(size * MiB))
	if err != nil {
		return fmt.Errorf("failed to set empty disk file's size:\n%w", err)
	}
	return
}

// SetupLoopbackDevice creates a /dev/loop device for the given disk file
func SetupLoopbackDevice(diskFilePath string) (devicePath string, err error) {
	logger.Log.Debugf("Attaching Loopback: %v", diskFilePath)
	stdout, stderr, err := shell.Execute("losetup", "--show", "-f", "-P", diskFilePath)
	if err != nil {
		err = fmt.Errorf("failed to create loopback device using losetup:\n%v\n%w", stderr, err)
		return
	}
	devicePath = strings.TrimSpace(stdout)
	logger.Log.Debugf("Created loopback device at device path: %v", devicePath)
	return
}

// BlockOnDiskIO waits until all outstanding operations against a disk complete.
func BlockOnDiskIO(diskDevPath string) (err error) {
	maj, min, err := GetDiskIds(diskDevPath)
	if err != nil {
		return
	}

	return BlockOnDiskIOByIds(diskDevPath, maj, min)
}

func GetDiskIds(diskDevPath string) (maj string, min string, err error) {
	rawDiskOutput, stderr, err := shell.Execute("lsblk", "--nodeps", "--json", "--output", "NAME,MAJ:MIN", diskDevPath)
	if err != nil {
		err = fmt.Errorf("failed to find IDs for disk (%s):\n%v\n%w", diskDevPath, stderr, err)
		return
	}

	var blockDevices blockDevicesOutput
	if rawDiskOutput != "" {
		err = json.Unmarshal([]byte(rawDiskOutput), &blockDevices)
		if err != nil {
			return
		}
	}

	if len(blockDevices.Devices) != 1 {
		err = fmt.Errorf("couldn't find disk IDs for %s (%s), expecting only one result", diskDevPath, rawDiskOutput)
		return
	}
	// MAJ:MIN is returned in the form "1:2"
	diskIDs := strings.Split(blockDevices.Devices[0].MajMin, ":")
	if len(diskIDs) != 2 {
		err = fmt.Errorf("couldn't find disk IDs for %s (%s), couldn't parse MAJ:MIN", diskDevPath, rawDiskOutput)
		return
	}
	maj = diskIDs[0]
	min = diskIDs[1]
	return
}

// BlockOnDiskIOById waits until all outstanding operations against a disk complete.
func BlockOnDiskIOByIds(debugName string, maj string, min string) (err error) {
	const (
		// Indices for values in /proc/diskstats
		majIdx            = 0
		minIdx            = 1
		outstandingOpsIdx = 11
	)

	logger.Log.Debugf("Flushing all IO to disk")
	_, _, err = shell.Execute("sync")
	if err != nil {
		return
	}

	logger.Log.Tracef("Searching /proc/diskstats for %s (%s:%s)", debugName, maj, min)
	for {
		var (
			foundEntry     = false
			outstandingOps = ""
		)

		// Find the entry with Major#, Minor#, ..., IOs which matches our disk
		onStdout := func(line string) {
			// Bail early if we already found the entry
			if foundEntry {
				return
			}

			deviceStatsFields := strings.Fields(line)
			if maj == deviceStatsFields[majIdx] && min == deviceStatsFields[minIdx] {
				outstandingOps = deviceStatsFields[outstandingOpsIdx]
				foundEntry = true
			}
		}

		err = shell.NewExecBuilder("cat", "/proc/diskstats").
			StdoutCallback(onStdout).
			WarnLogLines(shell.DefaultWarnLogLines).
			LogLevel(logrus.TraceLevel, logrus.ErrorLevel).
			Execute()
		if err != nil {
			return
		}
		if !foundEntry {
			return fmt.Errorf("couldn't find entry for '%s' in /proc/diskstats", debugName)
		}
		logger.Log.Debugf("Outstanding operations on '%s': %s", debugName, outstandingOps)

		if outstandingOps == "0" {
			break
		}

		// Sleep breifly
		time.Sleep(time.Second / 4)
	}
	return
}

// DetachLoopbackDevice detaches the specified disk
func DetachLoopbackDevice(diskDevPath string) (err error) {
	logger.Log.Debugf("Detaching Loopback Device Path: %v", diskDevPath)
	_, stderr, err := shell.Execute("losetup", "-d", diskDevPath)
	if err != nil {
		logger.Log.Warnf("Failed to detach loopback device using losetup: %v", stderr)
	}
	return
}

func WaitForLoopbackToDetach(devicePath string, diskPath string) error {
	if !filepath.IsAbs(diskPath) {
		return fmt.Errorf("internal error: loopback disk path must be absolute (%s)", diskPath)
	}

	delay := 120 * time.Millisecond
	attempts := 10
	for failures := 0; failures < attempts; failures++ {
		stdout, _, err := shell.Execute("losetup", "--list", "--json", "--output", "NAME,BACK-FILE")
		if err != nil {
			return fmt.Errorf("failed to read loopback list:\n%w", err)
		}

		var output loopbackListOutput
		if stdout != "" {
			err = json.Unmarshal([]byte(stdout), &output)
			if err != nil {
				return fmt.Errorf("failed to parse loopback devices list JSON:\n%w", err)
			}
		}

		found := false
		for _, device := range output.Devices {
			if device.Name == devicePath && device.BackingFile == diskPath {
				found = true
				break
			}
		}

		if !found {
			return nil
		}

		time.Sleep(delay)
		delay *= 2
	}

	return fmt.Errorf("timed out waiting for loopback device (%s) for disk (%s) to close", devicePath, diskPath)
}

func WaitForDiskDevice(diskDevPath string) error {
	err := waitForDevicesToSettle()
	if err != nil {
		return err
	}

	// 'udevadm settle' is sometimes not enough.
	// So, double check that the partitions have been populated.
	// Ideally, we would use 'udevadm wait' instead of 'udevadm settle'. But it is too new and so isn't universally
	// available yet.
	err = waitForDiskToPopulate(diskDevPath)
	if err != nil {
		return err
	}

	return nil
}

func waitForDiskToPopulate(diskDevPath string) error {
	partitionTable, err := ReadDiskPartitionTable(diskDevPath)
	if err != nil {
		return err
	}

	if partitionTable == nil {
		// Disk is empty.
		return nil
	}

	_, err = retry.RunWithExpBackoff(context.Background(), func() error {
		kernelPartitions, err := GetDiskPartitions(diskDevPath)
		if err != nil {
			return err
		}

		errs := []error(nil)
		for _, partition := range partitionTable.Partitions {
			info, found := sliceutils.FindValueFunc(kernelPartitions, func(info PartitionInfo) bool {
				return info.Path == partition.Path
			})
			if !found {
				err := fmt.Errorf("failed to find partition device node (%s)", partition.Path)
				errs = append(errs, err)
				continue
			}

			if !strings.EqualFold(partition.PartTypeUuid, info.PartitionTypeUuid) {
				err := fmt.Errorf("partition's (%s) type UUID is wrong: expected (%s), actual (%s)",
					partition.Path, partition.PartTypeUuid, info.PartitionTypeUuid)
				errs = append(errs, err)
			}

			if !strings.EqualFold(partition.PartUuid, info.PartUuid) {
				err := fmt.Errorf("partition's (%s) UUID is wrong: expected (%s), actual (%s)",
					partition.Path, partition.PartUuid, info.PartUuid)
				errs = append(errs, err)
			}

			if partition.PartLabel != info.PartLabel {
				err := fmt.Errorf("partition's (%s) label is wrong: expected (%s), actual (%s)",
					partition.Path, partition.PartLabel, info.PartLabel)
				errs = append(errs, err)
			}

			if partition.FileSystemType != info.FileSystemType {
				err := fmt.Errorf("partition's (%s) filesystem type is wrong: expected (%s), actual (%s)",
					partition.Path, partition.FileSystemType, info.FileSystemType)
				errs = append(errs, err)
			}

			if !strings.EqualFold(partition.FileSystemUuid, info.Uuid) {
				err := fmt.Errorf("partition's (%s) filesystem UUID is wrong: expected (%s), actual (%s)",
					partition.Path, partition.FileSystemUuid, info.Uuid)
				errs = append(errs, err)
			}
		}

		if len(errs) > 0 {
			return errors.Join(errs...)
		}

		return nil
	}, 10, 120*time.Millisecond, 2.0)
	if err != nil {
		return fmt.Errorf("timed out waiting for disk (%s) info to be populated:\n%w", diskDevPath, err)
	}

	return nil
}

// waitForDevicesToSettle waits for all udev events to be processed on the system.
// This can be used to wait for partitions to be discovered after mounting a disk.
func waitForDevicesToSettle() error {
	logger.Log.Debugf("Waiting for devices to settle")
	_, _, err := shell.Execute("udevadm", "settle")
	if err != nil {
		return fmt.Errorf("failed to wait for devices to settle:\n%w", err)
	}
	return nil
}

// CreatePartitions creates partitions on the specified disk according to the disk config
func CreatePartitions(diskDevPath string, disk configuration.Disk, rootEncryption configuration.RootEncryption,
) (partDevPathMap map[string]string, partIDToFsTypeMap map[string]string, encryptedRoot EncryptedRootDevice, err error) {
	partDevPathMap = make(map[string]string)
	partIDToFsTypeMap = make(map[string]string)

	partitionTableType := disk.PartitionTableType

	// Create new partition table.
	// This will also wipe the existing partition.
	err = createPartitionTable(diskDevPath, partitionTableType)
	if err != nil {
		return
	}

	usingExtendedPartition := (len(disk.Partitions) > maxPrimaryPartitionsForMBR) && (partitionTableType == configuration.PartitionTableTypeMbr)

	// Partitions assumed to be defined in sorted order
	for idx, partition := range disk.Partitions {
		partType, partitionNumber := obtainPartitionDetail(idx, usingExtendedPartition)
		// Insert an extended partition
		if partType == extendedPartitionType {
			err = createExtendedPartition(diskDevPath, partitionTableType, disk.Partitions, partIDToFsTypeMap,
				partDevPathMap)
			if err != nil {
				return
			}

			// Update partType and partitionNumber
			partType = logicalPartitionType
			partitionNumber = partitionNumber + 1
		}

		partDevPath, err := createSinglePartition(diskDevPath, partitionNumber, partitionTableType, partition, partType)
		if err != nil {
			err = fmt.Errorf("failed to create single partition:\n%w", err)
			return partDevPathMap, partIDToFsTypeMap, encryptedRoot, err
		}

		partFsType, err := FormatSinglePartition(diskDevPath, partDevPath, partition)
		if err != nil {
			err = fmt.Errorf("failed to format partition:\n%w", err)
			return partDevPathMap, partIDToFsTypeMap, encryptedRoot, err
		}

		if rootEncryption.Enable && partition.HasFlag(configuration.PartitionFlagDeviceMapperRoot) {
			encryptedRoot, err = encryptRootPartition(partDevPath, partition, rootEncryption)
			if err != nil {
				err = fmt.Errorf("failed to initialize encrypted root:\n%w", err)
				return partDevPathMap, partIDToFsTypeMap, encryptedRoot, err
			}
			partDevPathMap[partition.ID] = GetEncryptedRootVolMapping()
		} else {
			partDevPathMap[partition.ID] = partDevPath
		}

		partIDToFsTypeMap[partition.ID] = partFsType
	}

	// Wait for the disk's metadata to populate.
	err = RefreshPartitions(diskDevPath)
	if err != nil {
		return
	}

	return
}

func createPartitionTable(diskDevPath string, partitionTableType configuration.PartitionTableType) error {
	if partitionTableType != configuration.PartitionTableTypeGpt {
		// When switching from "parted" to "sfdisk", MBR support was omitted.
		return fmt.Errorf("only support for GPT disks is implemented")
	}

	// Create new partition table.
	// This replaces any existing partition table.
	sfdiskScript := "label: gpt"

	// sfdisk only wipes pre-existing filesystem/RAID signatures when it is run interactively, so ask for it
	// explicitly. Otherwise, stale signatures from a previous install survive in the newly partitioned space and
	// confuse blkid/lsblk/udev. (This replaces the `sfdisk --delete` call that used to run before `parted mklabel`.)
	err := shell.NewExecBuilder("flock", "--timeout", "5", diskDevPath, "sfdisk", "--lock=no", "--wipe=always",
		"--wipe-partitions=always", diskDevPath).
		Stdin(sfdiskScript).
		LogLevel(logrus.DebugLevel, logrus.WarnLevel).
		ErrorStderrLines(1).
		Execute()
	if err != nil {
		return fmt.Errorf("failed to create partition table (%s) using sfdisk:\n%w", diskDevPath, err)
	}

	return nil
}

// createSinglePartition creates a single partition based on the partition config
func createSinglePartition(diskDevPath string, partitionNumber int, partitionTableType configuration.PartitionTableType,
	partition configuration.Partition, partType string,
) (partDevPath string, err error) {
	const (
		timeoutInSeconds = "5"
	)

	logicalSectorSize, physicalSectorSize, err := GetSectorSize(diskDevPath)
	if err != nil {
		return
	}

	if partition.End != 0 && partition.Start >= partition.End {
		return "", fmt.Errorf("invalid partition: start (%d) >= end (%d)", partition.Start, partition.End)
	}

	start := partition.Start * MiB / logicalSectorSize

	end := partition.End*MiB/logicalSectorSize - 1
	if partition.End == 0 {
		end = 0
	}

	if partType == logicalPartitionType {
		start = start + 1
		if end != 0 {
			end = end + 1
		}
	}

	// Check whether the start sector is 4K-aligned
	start = alignSectorAddress(start, logicalSectorSize, physicalSectorSize)

	sizeArg := ""
	if end > 0 {
		size := end - start + 1
		sizeArg = fmt.Sprintf(", size=%d", size)
	}

	logger.Log.Debugf("Input partition start: %d, aligned start sector: %d", partition.Start, start)
	logger.Log.Debugf("Input partition end: %d, end sector: %d", partition.End, end)

	name := ""
	typeId := ""
	switch partitionTableType {
	case configuration.PartitionTableTypeMbr:
		// When switching from using "parted" to using "sfdisk", MBR support was omitted.
		return "", fmt.Errorf("MBR support is not implemented")

	case configuration.PartitionTableTypeGpt:
		name = escapeSfdiskString(partition.Name)
		typeId = GenericLinuxPartitionTypeUuid

		for _, flag := range partition.Flags {
			switch flag {
			case configuration.PartitionFlagESP, configuration.PartitionFlagBoot:
				typeId = EfiSystemPartitionTypeUuid

			case configuration.PartitionFlagGrub, configuration.PartitionFlagBiosGrub, configuration.PartitionFlagBiosGrubLegacy:
				typeId = BiosBootPartitionTypeUuid

			case configuration.PartitionFlagDeviceMapperRoot:
				//Ignore, only used for internal tooling

			default:
				return partDevPath, fmt.Errorf("unknown partition (%d) flag (%v)", partitionNumber, flag)
			}
		}

		switch {
		case partition.TypeUUID != "":
			typeId = partition.TypeUUID

		case partition.Type != "":
			typeId = configuration.PartitionTypeNameToUUID[partition.Type]
		}
	}

	sfdiskScript := fmt.Sprintf("unit: sectors\nstart=%d, type=%s, name=%s%s", start, typeId, name, sizeArg)
	logger.Log.Debugf("sfdisk script:\n%s", sfdiskScript)

	err = shell.NewExecBuilder("flock", "--timeout", timeoutInSeconds, diskDevPath, "sfdisk", "--lock=no",
		"--wipe-partitions=always", "--append", diskDevPath).
		Stdin(sfdiskScript).
		LogLevel(logrus.DebugLevel, logrus.WarnLevel).
		ErrorStderrLines(1).
		Execute()
	if err != nil {
		return "", fmt.Errorf("failed to create partition using sfdisk:\n%w", err)
	}

	partDevPath, err = waitForPartitionCreation(diskDevPath, partitionNumber)
	if err != nil {
		return "", err
	}

	return partDevPath, nil
}

// Adds escaping of string values for sfdisk scripts.
//
// Note: Support string escaping was only added in util-linux v2.32.1 (commits: 75ef5a1, 810b313)
//
// util-linux versions:
// - Ubuntu 20.04: v2.34.0
// - Azure Linux 2.0: v2.37.4
//
// So, it should be fine to assume that it is supported.
func escapeSfdiskString(value string) string {
	builder := strings.Builder{}
	builder.WriteString("\"")

	for _, c := range value {
		switch c {
		case '"':
			builder.WriteString("\\x22")

		case '\\':
			builder.WriteString("\\x5c")

		default:
			builder.WriteRune(c)
		}
	}

	builder.WriteString("\"")
	return builder.String()
}

// InitializeSinglePartition initializes a single partition based on the given partition configuration
func waitForPartitionCreation(diskDevPath string, partitionNumber int) (partDevPath string, err error) {
	const (
		retryDuration    = time.Second
		timeoutInSeconds = "5"
		totalAttempts    = 5
	)

	partitionNumberStr := strconv.Itoa(partitionNumber)

	// There are two primary partition naming conventions:
	// - /dev/sdN<y>
	// - /dev/loopNp<x>
	// Detect the exact one we are using.
	testPartDevPaths := []string{
		fmt.Sprintf("%sp%s", diskDevPath, partitionNumberStr),
	}

	// If disk path ends in a digit, then the 'p<x>' style must be used.
	// So, don't check the other style to avoid ambiguities. For example, /dev/loop1 vs. /dev/loop11.
	// This is particularly relevant on Ubuntu, due to snap's use of loopback devices.
	if !isDigit(diskDevPath[len(diskDevPath)-1]) {
		devPath := fmt.Sprintf("%s%s", diskDevPath, partitionNumberStr)
		testPartDevPaths = append(testPartDevPaths, devPath)
	}

	err = retry.Run(func() error {
		for _, testPartDevPath := range testPartDevPaths {
			exists, err := file.PathExists(testPartDevPath)
			if err != nil {
				err = fmt.Errorf("failed to find device path (%s):\n%w", testPartDevPath, err)
				return err
			}
			if exists {
				partDevPath = testPartDevPath
				return nil
			}
			logger.Log.Debugf("Could not find partition path (%s). Checking other naming convention", testPartDevPath)
		}
		logger.Log.Warnf("Could not find any valid partition paths. Will retry up to %d times", totalAttempts)
		err = fmt.Errorf("could not find partition (%d) in /dev", partitionNumber)
		return err
	}, totalAttempts, retryDuration)
	if err != nil {
		return
	}

	return
}

func isDigit(c byte) bool {
	return c >= '0' && c <= '9'
}

// FormatSinglePartition formats the given partition to the type specified in the partition configuration
func FormatSinglePartition(diskDevPath string, partDevPath string, partition configuration.Partition,
) (fsType string, err error) {
	const (
		totalAttempts = 5
		retryDuration = time.Second
	)

	fsType = partition.FsType

	// Note: It is possible for the format partition command to fail with error "The file does not exist and no size was specified".
	// This is due to a possible race condition in Linux where the partition may not actually be ready after being newly created.
	// To handle such cases, we can retry the command.
	switch fsType {
	case "fat32", "fat16", "vfat", "ext2", "ext3", "ext4", "xfs":
		mkfsOptions := DefaultMkfsOptions[fsType]

		if fsType == "fat32" || fsType == "fat16" {
			fsType = "vfat"
		}

		mkfsArgs := []string{"--timeout", "5", diskDevPath, "mkfs", "-t", fsType}
		mkfsArgs = append(mkfsArgs, mkfsOptions...)
		mkfsArgs = append(mkfsArgs, partDevPath)

		err = retry.Run(func() error {
			_, stderr, err := shell.Execute("flock", mkfsArgs...)
			if err != nil {
				logger.Log.Warnf("Failed to format partition using mkfs: %v", stderr)
				return err
			}

			return err
		}, totalAttempts, retryDuration)
		if err != nil {
			err = fmt.Errorf("could not format partition with type %v after %v retries", fsType, totalAttempts)
		}
	case "linux-swap":
		err = retry.Run(func() error {
			_, stderr, err := shell.Execute("mkswap", partDevPath)
			if err != nil {
				logger.Log.Warnf("Failed to format swap partition using mkswap: %v", stderr)
				return err
			}
			return err
		}, totalAttempts, retryDuration)
		if err != nil {
			err = fmt.Errorf("could not format partition with type %v after %v retries", fsType, totalAttempts)
		}

		_, stderr, err := shell.Execute("swapon", partDevPath)
		if err != nil {
			err = fmt.Errorf("failed to execute swapon:\n%v\n%w", stderr, err)
			return "", err
		}
	case "":
		logger.Log.Debugf("No filesystem type specified. Ignoring for partition: %v", partDevPath)
	default:
		return fsType, fmt.Errorf("unrecognized filesystem format: %v", fsType)
	}

	return
}

// SystemBlockDevices returns all block devices on the host system.
func SystemBlockDevices() (systemDevices []SystemBlockDevice, err error) {
	const (
		scsiDiskMajorNumber      = "8"
		mmcBlockMajorNumber      = "179"
		virtualDiskMajorNumber   = "252,253,254"
		blockExtendedMajorNumber = "259"
	)

	blockDeviceMajorNumbers := []string{scsiDiskMajorNumber, mmcBlockMajorNumber, virtualDiskMajorNumber, blockExtendedMajorNumber}
	includeFilter := strings.Join(blockDeviceMajorNumbers, ",")
	rawDiskOutput, stderr, err := shell.Execute("lsblk", "-d", "--bytes", "-I", includeFilter, "-n", "--json", "--output", "NAME,SIZE,MODEL")
	if err != nil {
		err = fmt.Errorf("%v\n%w", stderr, err)
		return
	}

	var blockDevices blockDevicesOutput
	if rawDiskOutput != "" {
		err = json.Unmarshal([]byte(rawDiskOutput), &blockDevices)
		if err != nil {
			return
		}
	}

	if len(blockDevices.Devices) <= 0 {
		err = fmt.Errorf("failed to find supported disks:\n%w", err)
		return
	}

	systemDevices = make([]SystemBlockDevice, len(blockDevices.Devices))

	for i, disk := range blockDevices.Devices {
		systemDevices[i].DevicePath = fmt.Sprintf("/dev/%s", disk.Name)

		systemDevices[i].RawDiskSize, err = strconv.ParseUint(disk.Size.String(), 10, 64)
		if err != nil {
			return
		}

		systemDevices[i].Model = strings.TrimSpace(disk.Model)
	}

	return
}

// GetDiskPartitions gets the kernel's view of a disk's partitions.
func GetDiskPartitions(diskDevPath string) ([]PartitionInfo, error) {
	// Read the disk's partitions.
	jsonString, _, err := shell.Execute("lsblk", diskDevPath, "--output",
		"NAME,PATH,PARTTYPE,FSTYPE,UUID,MOUNTPOINT,PARTUUID,PARTLABEL,TYPE,SIZE", "--bytes", "--json", "--list")
	if err != nil {
		return nil, fmt.Errorf("failed to list disk (%s) partitions:\n%w", diskDevPath, err)
	}

	var output partitionInfoOutput
	if jsonString != "" {
		err = json.Unmarshal([]byte(jsonString), &output)
		if err != nil {
			return nil, fmt.Errorf("failed to parse disk (%s) partitions JSON:\n%w", diskDevPath, err)
		}
	}

	return output.Devices, err
}

// ReadPartitionTable reads the partition table directly from the disk.
func ReadDiskPartitionTable(diskDevPath string) (*PartitionTable, error) {
	// Read the partition table directly from disk.
	stdout, stderr, err := shell.Execute("flock", "--timeout", "5", "--shared", diskDevPath,
		"sfdisk", "--lock=no", "--dump", "--json", diskDevPath)
	if err != nil {
		if strings.Contains(stderr, "does not contain a recognized partition table") {
			// Empty partition table.
			return nil, nil
		}

		return nil, fmt.Errorf("failed to read partition table (%s):\n%s\n%w", diskDevPath, stderr, err)
	}

	var output partitionTableOutput
	if stdout == "" {
		return output.PartitionTable, nil
	}

	err = json.Unmarshal([]byte(stdout), &output)
	if err != nil {
		return nil, fmt.Errorf("failed to parse disk (%s) partition table JSON:\n%w", diskDevPath, err)
	}

	if output.PartitionTable == nil {
		// Disk is empty.
		return nil, nil
	}

	partitionTable := output.PartitionTable

	if partitionTable.Unit != "sectors" {
		return nil, fmt.Errorf("sfdisk returned unexpected unit size '%s': expecting 'sectors'", partitionTable.Unit)
	}

	for i := range partitionTable.Partitions {
		partition := &partitionTable.Partitions[i]

		// Read the filesystem type directly from disk.
		stdout, _, err := shell.Execute("flock", "--timeout", "5", "--shared", diskDevPath,
			"blkid", "--probe", "-s", "TYPE", "-o", "value", partition.Path)
		if err != nil {
			return nil, fmt.Errorf("failed to get filesystem type of partition (%s)\n%w", partition.Path, err)
		}

		partition.FileSystemType = strings.TrimSpace(stdout)

		// Read the filesystem UUID directly from disk.
		stdout, _, err = shell.Execute("flock", "--timeout", "5", "--shared", diskDevPath,
			"blkid", "--probe", "-s", "UUID", "-o", "value", partition.Path)
		if err != nil {
			return nil, fmt.Errorf("failed to get filesystem UUID of partition (%s)\n%w", partition.Path, err)
		}

		partition.FileSystemUuid = strings.TrimSpace(stdout)
	}

	return output.PartitionTable, nil
}

func createExtendedPartition(diskDevPath string, partitionTableType configuration.PartitionTableType,
	partitions []configuration.Partition, partIDToFsTypeMap, partDevPathMap map[string]string,
) (err error) {
	// Create a new partition object for extended partition
	extendedPartition := configuration.Partition{}
	extendedPartition.ID = extendedPartitionType
	extendedPartition.Start = partitions[maxPrimaryPartitionsForMBR-1].Start
	extendedPartition.End = partitions[len(partitions)-1].End

	partDevPath, err := createSinglePartition(diskDevPath, maxPrimaryPartitionsForMBR, partitionTableType,
		extendedPartition, extendedPartitionType)
	if err != nil {
		err = fmt.Errorf("failed to create extended partition:\n%w", err)
		return
	}
	partIDToFsTypeMap[extendedPartition.ID] = ""
	partDevPathMap[extendedPartition.ID] = partDevPath
	return
}

func getPartUUID(device string) (uuid string, err error) {
	stdout, _, err := shell.Execute("blkid", device, "-s", "UUID", "-o", "value")
	if err != nil {
		return
	}
	logger.Log.Trace(stdout)
	uuid = strings.TrimSpace(stdout)
	return
}

func getSectorSizeFromFile(sectorFile string) (sectorSize uint64, err error) {
	if exists, ferr := file.PathExists(sectorFile); ferr != nil {
		err = fmt.Errorf("failed to access sector size file (%s):\n%w", sectorFile, ferr)
		return
	} else if !exists {
		err = fmt.Errorf("could not find the hw sector size file %s to obtain the sector size of the system", sectorFile)
		return
	}

	fileContent, err := file.ReadLines(sectorFile)
	if err != nil {
		err = fmt.Errorf("failed to read from (%s):\n%w", sectorFile, err)
		return
	}

	// sector file should only have one line, return error if not
	if len(fileContent) != 1 {
		err = fmt.Errorf("%s has more than one line", sectorFile)
		return
	}

	sectorSize, err = strconv.ParseUint(fileContent[0], 10, 64)
	return
}

func GetSectorSize(diskDevPath string) (logicalSectorSize, physicalSectorSize uint64, err error) {
	const (
		diskNameStartIndex = 5
	)

	// Grab the specific disk name from /dev/xxx
	matchResult := diskDevPathRegexp.MatchString(diskDevPath)
	if !matchResult {
		err = fmt.Errorf("input disk device path (%s) is of invalud format", diskDevPath)
		return
	}
	diskName := diskDevPath[diskNameStartIndex:len(diskDevPath)]

	hw_sector_size_file := fmt.Sprintf("/sys/block/%s/queue/hw_sector_size", diskName)
	physical_sector_size_file := fmt.Sprintf("/sys/block/%s/queue/physical_block_size", diskName)

	logicalSectorSize, err = getSectorSizeFromFile(hw_sector_size_file)
	if err != nil {
		return
	}

	physicalSectorSize, err = getSectorSizeFromFile(physical_sector_size_file)
	return
}

func alignSectorAddress(sectorAddr, logicalSectorSize, physicalSectorSize uint64) (alignedSector uint64) {
	// Need to make sure that starting sector of a partition is aligned based on the physical sector size of the system.
	// For example, suppose the physical sector size is 4096. If the input start sector is 40960001, then this is misaligned,
	// and need to be elevated to the next aligned address, which is (40960001/4096 + 1)*4096 = 4100096.

	// We do need to take care of a special case, which is the first partition (normally boot partition) might be less than
	// the physical sector size. In this case, we need to check whether the start sector is a multiple of 1 MiB.
	alignedSector = 0
	if sectorAddr < physicalSectorSize {
		if sectorAddr%(MiB/logicalSectorSize) == 0 {
			alignedSector = sectorAddr
		}
	} else if (sectorAddr % physicalSectorSize) == 0 {
		alignedSector = sectorAddr
	} else {
		alignedSector = (sectorAddr/physicalSectorSize + 1) * physicalSectorSize
	}

	return
}

func obtainPartitionDetail(partitionIndex int, hasExtendedPartition bool) (partType string, partitionNumber int) {
	const (
		indexOffsetForNormalPartitionNumber  = 1
		indexOffsetForLogicalPartitionNumber = 2
	)

	// partitionIndex is the index of the partition in the partition array, which starts at 0.
	// partitionNumber, however, starts at 1 (E.g. /dev/sda1), and thus partitionNumber = partitionIndex + 1.
	// In the case of logical partitions, since an extra extended partition has to be created first in order to
	// to create logical partitions, so the partition number will further increase by 1, which equals partitionIndex + 2.

	if hasExtendedPartition && partitionIndex >= (maxPrimaryPartitionsForMBR-1) {
		if partitionIndex == (maxPrimaryPartitionsForMBR - 1) {
			partType = extendedPartitionType
			partitionNumber = partitionIndex + indexOffsetForNormalPartitionNumber
		} else {
			partType = logicalPartitionType
			partitionNumber = partitionIndex + indexOffsetForLogicalPartitionNumber
		}
	} else {
		partType = primaryPartitionType
		partitionNumber = partitionIndex + indexOffsetForNormalPartitionNumber
	}

	return
}

func RefreshPartitions(diskDevPath string) error {
	err := requestKernelRereadPartitionTable(diskDevPath)
	if err != nil {
		return fmt.Errorf("failed to request partition table reread (%s):\n%w", diskDevPath, err)
	}

	err = WaitForDiskDevice(diskDevPath)
	if err != nil {
		return err
	}

	return nil
}

// Requests that the kernel reread the partition table for the given disk device.
func requestKernelRereadPartitionTable(diskDevPath string) error {
	diskFile, err := os.OpenFile(diskDevPath, os.O_RDONLY, 0)
	if err != nil {
		return err
	}
	defer diskFile.Close()

	waitTime := 125 * time.Millisecond
	retries := 10
	for i := 0; ; i = 1 {
		_, _, errno := unix.Syscall(unix.SYS_IOCTL, diskFile.Fd(), unix.BLKRRPART, 0)
		switch {
		case errno == unix.EBUSY && i < retries:
			// Something else is using the disk at the moment.
			// So, retry in a little bit.
			time.Sleep(waitTime)
			waitTime *= 2
			continue

		case errno != 0:
			return errno

		default:
			return nil
		}
	}
}
