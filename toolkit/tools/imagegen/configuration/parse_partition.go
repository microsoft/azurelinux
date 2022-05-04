// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package configuration

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"fmt"

	"microsoft.com/pkggen/internal/logger"
)

var (
	diskInfo			map[string]int
	curDiskIndex 		int
	latestDiskIndex	int
	disks 				[]Disk
	partitionSettings	[]PartitionSetting
)

func updateNewDisk(diskValue string) {
	// Don't create new disk if processing on the initial placeholder disk
	if len(disks) != 1 || len(diskInfo) != 0 {
		disks = append(disks, Disk{})
	}
	
	disks[latestDiskIndex].PartitionTableType = PartitionTableTypeGpt

	// Set TargetDisk and TargetDiskType for unattended installation
	disks[latestDiskIndex].TargetDisk.Type = "path"
	disks[latestDiskIndex].TargetDisk.Value = diskValue

	diskInfo[diskValue] = latestDiskIndex
	curDiskIndex = latestDiskIndex
	latestDiskIndex++
}

func calculatePartitionSize(partSize string, diskPart *Partition) (err error) {
	if len(disks[curDiskIndex].Partitions) == 0 {
		diskPart.Start = 1
	} else {
		diskPart.Start = disks[curDiskIndex].Partitions[len(disks[curDiskIndex].Partitions)-1].End
	}

	partitionSize, err := strconv.ParseUint(partSize, 10, 64)
	if err != nil {
		return err
	}

	if !diskPart.Grow {
		diskPart.End = diskPart.Start + partitionSize
	}

	return
}

func processPartitionInfo(option, value string, diskPart *Partition, diskPartitionSetting *PartitionSetting) (err error) {
	// Check --ondisk flag
	if option == "ondisk" {
		// Check whether this disk has already been parsed or not
		curIdx, ok := diskInfo[value]
		if ok {
			curDiskIndex = curIdx
		} else {
			updateNewDisk(value) 
		}
	}

	// Check --fstype flag
	if option == "fstype" {
		if value == "biosboot" {
			diskPart.FsType = "fat32"
		} else if value == "swap" {
			diskPart.FsType = "linux-swap"
			// swap partition does not have a mount point
			diskPartitionSetting.MountPoint = ""
		} else {
			diskPart.FsType = value
		}
	}

	// Check --size flag
	if option == "size" {
		err := calculatePartitionSize(value, diskPart)
		if err != nil {
			return err
		}
	}

	return
}

func processMountPoint(mountPoint string, diskPart *Partition, diskPartitionSetting *PartitionSetting) (err error) {
	diskPartitionSetting.MountPoint = mountPoint
	if mountPoint == "biosboot" {
		diskPart.ID = "boot"
		diskPart.Flags = append(diskPart.Flags, PartitionFlagBiosGrub)	
		diskPartitionSetting.MountPoint = ""
		diskPartitionSetting.ID = "boot"
		disks[curDiskIndex].PartitionTableType = PartitionTableTypeGpt
	} else if mountPoint == "/" {
		diskPartitionSetting.ID = "rootfs"
		diskPart.ID = "rootfs"
	} else if strings.Contains(mountPoint, "/") || mountPoint == "swap" {
		diskPartitionSetting.ID = mountPoint
		diskPart.ID = mountPoint
	} else {
		// Other types of mount points are currently not supported
		err := fmt.Errorf("Invalid mount point specified: (%s)", mountPoint)
		return err
	}

	return
}

// ParsePartitionFlags parses the kickstart syntax of a kickstart-generated partition file
func ParsePartitionFlags(partCmd string) (err error) {
	// Only need to parse commands that contains --ondisk options
	if strings.Contains(partCmd, "--ondisk") {
		// Create new partition and partitionsetting
		partition := new(Partition)
		partitionSetting := new(PartitionSetting)
 		partitionSetting.MountIdentifier = MountIdentifierDefault
		
		partitionFlags := strings.Split(partCmd, " ")
		for _, partitionFlag := range partitionFlags {
			err := parseFlag(partitionFlag, partition, partitionSetting)
			if err != nil {
				return err
			}
		}

		disks[curDiskIndex].Partitions = append(disks[curDiskIndex].Partitions, *partition)
		partitionSettings = append(partitionSettings, *partitionSetting)
	}

	return
}

func parseFlag(partitionFlag string, diskPart *Partition, diskPartitionSetting *PartitionSetting) (err error) {
	const optionStart = "--"
	if strings.HasPrefix(partitionFlag, optionStart) {
		// Find the index of "="
		index := strings.Index(partitionFlag, "=")
		if index != -1 {
			optionName := partitionFlag[len(optionStart):index]
			optionVal := partitionFlag[(index+1):len(partitionFlag)]
			
			err := processPartitionInfo(optionName, optionVal, diskPart, diskPartitionSetting)
			if err != nil {
				return err
			}
		} else {
			// Check grow flag
			if partitionFlag == "--grow" {
				diskPart.Grow = true
				diskPart.End = 0
			}
		}
	} else {
		// Update mount point
		if partitionFlag != "part" {
			err := processMountPoint(partitionFlag, diskPart, diskPartitionSetting)
			if err != nil {
				return err
			}
		} 
	}

	return
}

// ParseKickStartPartitionScheme parses a kickstart-generated partition file and 
// construct the Disk and PartitionSetting information
func ParseKickStartPartitionScheme(partitionFile string) (Retdisks []Disk, RetpartitionSettings []PartitionSetting, err error) {
	file, err := os.Open(partitionFile)
	if err != nil {
		logger.Log.Errorf("Failed to open file (%s)", partitionFile)
		return
	}
	defer file.Close()

	// Check if the file is empty
	_, err = file.Stat()
	if err != nil {
		logger.Log.Errorf("Empty partition file (%s)", partitionFile)
		return
	}

	disks = append(disks, Disk{})	
	scanner := bufio.NewScanner(file)

	// Create a mapping between the disk path and the index of the disk in the
	// Disk array so that when we parse through the partition commands, we can
	// determine which disk the parition instruction is targeted
	diskInfo = make(map[string]int)

	for scanner.Scan() {
		parseCmd := scanner.Text()
		err = ParsePartitionFlags(parseCmd)
		if err != nil {
			return
		}
	}

	Retdisks = disks
	RetpartitionSettings = partitionSettings
	return
}