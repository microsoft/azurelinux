package imagecustomizerlib

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func shrinkFilesystems(imageLoopDevice string, verityHashPartition *imagecustomizerapi.IdentifiedPartition) error {
	logger.Log.Infof("Shrinking filesystems")

	// Get partition info
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	// Get the start sectors of all partitions
	matchStarts, err := getStartSectors(imageLoopDevice, len(diskPartitions)-1)
	// Number of partitions is len(diskPartitions)-1 as diskPartitions[0] refers to the loop device for the image itself
	if err != nil {
		return err
	}

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		diskPartition := diskPartitions[partitionNum]
		if diskPartition.Type != "part" {
			continue
		}

		partitionLoopDevice := diskPartition.Path

		// Check if the filesystem type is supported
		fstype := diskPartition.FileSystemType
		if !supportedShrinkFsType(fstype) {
			logger.Log.Infof("Shrinking partition (%s): unsupported filesystem type (%s)", partitionLoopDevice, fstype)
			continue
		}

		if verityHashPartition != nil {
			matches, err := partitionMatchesId(*verityHashPartition, diskPartition)
			if err != nil {
				return err
			}

			if matches {
				logger.Log.Infof("Shrinking partition (%s): skipping verity hash partition", partitionLoopDevice)
				continue
			}
		}

		logger.Log.Infof("Shrinking partition (%s)", partitionLoopDevice)

		// Check the file system with e2fsck
		err := shell.ExecuteLive(true /*squashErrors*/, "sudo", "e2fsck", "-fy", partitionLoopDevice)
		if err != nil {
			return fmt.Errorf("failed to check %s with e2fsck:\n%w", partitionLoopDevice, err)
		}

		// Shrink the file system with resize2fs -M
		stdout, stderr, err := shell.Execute("sudo", "resize2fs", "-M", partitionLoopDevice)
		if err != nil {
			return fmt.Errorf("failed to resize %s with resize2fs:\n%v", partitionLoopDevice, stderr)
		}

		// Find the new partition end value
		end, err := getNewPartitionEndInSectors(stdout, stderr, matchStarts[partitionNum-1][1], imageLoopDevice)
		if err != nil {
			return fmt.Errorf("failed to calculate new partition end:\n%w", err)
		}

		if end == "" {
			// Filesystem wasn't resized. So, there is no need to resize the partition.
			logger.Log.Infof("Filesystem is already at its min size (%s)", partitionLoopDevice)
			continue
		}

		// Resize the partition with parted resizepart
		_, stderr, err = shell.ExecuteWithStdin("yes" /*stdin*/, "sudo", "parted", "---pretend-input-tty", imageLoopDevice, "resizepart", strconv.Itoa(partitionNum), end)
		if err != nil {
			return fmt.Errorf("failed to resizepart %s with parted:\n%v", partitionLoopDevice, stderr)
		}

		// Re-read the partition table
		err = shell.ExecuteLive(true, "flock", "--timeout", "5", imageLoopDevice, "partprobe", "-s", imageLoopDevice)
		if err != nil {
			return fmt.Errorf("partprobe failed:\n%w", err)
		}
	}
	return nil
}

// Get the start sectors of all partitions.
func getStartSectors(imageLoopDevice string, partitionCount int) (matchStarts [][]string, err error) {
	stdout, stderr, err := shell.Execute("sudo", "fdisk", "-l", imageLoopDevice)
	if err != nil {
		return nil, fmt.Errorf("fdisk failed to list partitions:\n%v", stderr)
	}

	// Example line from fdisk -l output: "/dev/loop41p2   18432  103064   84633 41.3M Linux filesystem"
	reStarts, err := regexp.Compile(`(?m:^` + imageLoopDevice + `p\d+ *(\d+).*?)`)
	if err != nil {
		return nil, fmt.Errorf("failed to compile regex:\n%w", err)
	}
	matchStarts = reStarts.FindAllStringSubmatch(stdout, -1)
	if len(matchStarts) < partitionCount {
		return nil, fmt.Errorf("could not find all partition starts")
	}

	return matchStarts, nil
}

// Get the filesystem size in sectors.
// Returns -1 if the resize was a no-op.
func getFilesystemSizeInSectors(resize2fsStdout string, resize2fsStderr string, imageLoopDevice string,
) (filesystemSizeInSectors int, err error) {
	const resize2fsNopMessage = "Nothing to do!"
	if strings.Contains(resize2fsStderr, resize2fsNopMessage) {
		// Resize operation was a no-op.
		return -1, nil
	}

	// Example resize2fs output first line: "Resizing the filesystem on /dev/loop44p2 to 21015 (4k) blocks."
	re, err := regexp.Compile(`.*to (\d+) \((\d+)([a-zA-Z])\)`)
	if err != nil {
		return 0, fmt.Errorf("failed to compile regex:\n%w", err)
	}

	// Get the block count and block size
	match := re.FindStringSubmatch(resize2fsStdout)
	if match == nil {
		return 0, fmt.Errorf("failed to parse output of resize2fs:\nstdout:\n%s\nstderr:\n%s", resize2fsStdout,
			resize2fsStderr)
	}

	blockCount, err := strconv.Atoi(match[1]) // Example: 21015
	if err != nil {
		return 0, fmt.Errorf("failed to parse block count (%s):\n%w", match[1], err)
	}
	multiplier, err := strconv.Atoi(match[2]) // Example: 4
	if err != nil {
		return 0, fmt.Errorf("failed to parse multiplier for block size (%s):\n%w", match[2], err)
	}
	unit := match[3] // Example: 'k'

	// Calculate block size
	var blockSize int
	const KiB = 1024 // kibibyte in bytes
	switch unit {
	case "k":
		blockSize = multiplier * KiB
	default:
		return 0, fmt.Errorf("unrecognized unit (%s)", unit)
	}

	filesystemSizeInBytes := blockCount * blockSize

	// Get the sector size
	logicalSectorSize, _, err := diskutils.GetSectorSize(imageLoopDevice)
	if err != nil {
		return 0, fmt.Errorf("failed to get sector size:\n%w", err)
	}
	sectorSizeInBytes := int(logicalSectorSize) // cast from uint64 to int

	filesystemSizeInSectors = filesystemSizeInBytes / sectorSizeInBytes
	if filesystemSizeInBytes%sectorSizeInBytes != 0 {
		filesystemSizeInSectors++
	}

	return filesystemSizeInSectors, nil
}

// Get the new partition end in sectors.
// Returns an empty string if the resize was a no-op.
func getNewPartitionEndInSectors(resize2fsStdout string, resize2fsStderr string, startSector string,
	imageLoopDevice string,
) (endInSectors string, err error) {
	filesystemSizeInSectors, err := getFilesystemSizeInSectors(resize2fsStdout, resize2fsStderr, imageLoopDevice)
	if err != nil {
		return "", fmt.Errorf("failed to get filesystem size:\n%w", err)
	}

	if filesystemSizeInSectors < 0 {
		// Resize operation was a no-op.
		return "", nil
	}

	// Convert start sector string to int
	start, err := strconv.Atoi(startSector)
	if err != nil {
		return "", fmt.Errorf("failed to convert start sector to int:\n%w", err)
	}
	// Calculate the new end
	end := start + filesystemSizeInSectors
	// Convert to a string with sectors unit appended
	endInSectors = strconv.Itoa(end) + "s"
	return endInSectors, nil
}

// Checks if the provided fstype is supported by shrink filesystems.
func supportedShrinkFsType(fstype string) (isSupported bool) {
	switch fstype {
	// Currently only support ext2, ext3, ext4 filesystem types
	case "ext2", "ext3", "ext4":
		return true
	default:
		return false
	}
}
