// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package configuration

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

const (
	kickstartPartitionOnDisk  = "--ondisk"
	kickstartPartitionOnDrive = "--ondrive"
	kickstartPartitionSize    = "--size"
	kickstartPartitionFsType  = "--fstype"
	kickstartPartitionGrow    = "--grow"
	biosbootPartition         = "biosboot"

	onDiskInputErrorMsg = "--ondisk/--ondrive must not be empty"
	fsTypeInputErrorMsg = "--fstype must not be empty"
	mountPointErrorMsg  = "Mount Point must not be empty"
)

var (
	diskInfo                map[string]int
	curDiskIndex            int
	latestDiskIndex         int
	disks                   []Disk
	partitionSettings       []PartitionSetting
	partCmdProcess          map[string]func(string) error
	newDiskPartition        *Partition
	newDiskPartitionSetting *PartitionSetting
	shouldFillDiskSpace     bool
)

func initializePrerequisitesForParser() {
	// Create a mapping between the disk path and the index of the disk in the
	// Disk array so that when we parse through the partition commands, we can
	// determine which disk the parition instruction is targeted
	diskInfo = make(map[string]int)

	// On the very first partition (boot partition), the partition type might determine
	// what the partition table type is. Since the creation of Disk only happens when we parse
	// the "--ondisk" flag and this flag is usually specified at the end of the part command, thus
	// we need to add a placeholder disk initially so the partition table type can be updated when parsing
	// the first partition
	disks = []Disk{Disk{}}
	partitionSettings = []PartitionSetting{}
	curDiskIndex = 0
	latestDiskIndex = 0

	// Create a mapping of partition flags and corresponding processing functions
	populatepartCmdProcessMap()
}

func populatepartCmdProcessMap() {
	partCmdProcess = make(map[string]func(string) error)

	// Currently only process "ondisk", "ondrive", "size" and "fstype"
	// Expand this map if supporting more commands in the future
	partCmdProcess[kickstartPartitionOnDisk] = processDisk
	partCmdProcess[kickstartPartitionOnDrive] = processDisk
	partCmdProcess[kickstartPartitionSize] = processPartitionSize
	partCmdProcess[kickstartPartitionFsType] = processPartitionFsType
}

func processPartitionTableType() (err error) {
	// In kickstart installation scenario, the partition table type is set to
	// MBR by default. The Anaconda installer has this config "--gpt" that indicates
	// whether the users prefer creation of GPT disk label or not. The value of "--gpt"
	// is a bool where "True" indicates using GPT and "False" if not, which means using MBR.
	// This config is set as a boot option within /proc/cmdline, which will be parsed by anaconda
	// during installation process. Thus, Mariner will also pick the same design to reach compatibility
	// with kickstart scenario

	// Please note that this code is only executed during kickstart installation, when "IsKickStartBoot" is set to true.
	// Mariner installer currently does not allow direct specification of disk and partition layout within
	// the image config file for kickstart installation. So any disk/partition setting you make in the image config file
	// will be overwritten if you enable kickstart installation mode.
	isGPTPartitionTable, err := GetKernelCmdLineValue("--gpt")
	if err != nil {
		return err
	}

	if strings.TrimSpace(isGPTPartitionTable) == "True" {
		disks[latestDiskIndex].PartitionTableType = PartitionTableTypeGpt
	} else {
		disks[latestDiskIndex].PartitionTableType = PartitionTableTypeMbr
	}

	return
}

func processDisk(inputDiskValue string) (err error) {
	diskValue := strings.TrimSpace(inputDiskValue)
	if diskValue == "" {
		return fmt.Errorf(onDiskInputErrorMsg)
	}

	// Check whether this disk has already been parsed or not
	curIdx, ok := diskInfo[diskValue]
	if ok {
		curDiskIndex = curIdx
	} else {
		// Don't create new disk if processing on the initial placeholder disk
		if len(disks) != 1 || len(diskInfo) != 0 {
			disks = append(disks, Disk{})
		}

		// Determine the partition table type of the disk
		err = processPartitionTableType()
		if err != nil {
			logger.Log.Errorf("Error setting partition table type")
			return
		}

		// Set TargetDisk and TargetDiskType for unattended installation
		disks[latestDiskIndex].TargetDisk.Type = "path"
		disks[latestDiskIndex].TargetDisk.Value = diskValue

		diskInfo[diskValue] = latestDiskIndex
		curDiskIndex = latestDiskIndex
		latestDiskIndex++
	}

	return
}

func processPartitionSize(inputPartSize string) (err error) {
	partSize := strings.TrimSpace(inputPartSize)

	if len(disks[curDiskIndex].Partitions) == 0 {
		newDiskPartition.Start = 1
	} else {
		newDiskPartition.Start = disks[curDiskIndex].Partitions[len(disks[curDiskIndex].Partitions)-1].End
	}

	partitionSize, err := strconv.ParseUint(partSize, 10, 64)
	if err != nil {
		return err
	}

	if shouldFillDiskSpace {
		shouldFillDiskSpace = false
	} else {
		newDiskPartition.End = newDiskPartition.Start + partitionSize
	}

	return
}

func processPartitionFsType(inputFsType string) (err error) {
	fstype := strings.TrimSpace(inputFsType)
	if fstype == "" {
		return fmt.Errorf(fsTypeInputErrorMsg)
	} else if fstype == biosbootPartition {
		newDiskPartition.FsType = "fat32"
	} else if fstype == "swap" {
		newDiskPartition.FsType = "linux-swap"

		// swap partition does not have a mount point
		newDiskPartitionSetting.MountPoint = ""
	} else {
		newDiskPartition.FsType = fstype
	}

	return
}

func processMountPoint(inputMountPoint string, partitionNumber int) (err error) {
	mountPoint := strings.TrimSpace(inputMountPoint)
	if mountPoint == "" {
		return fmt.Errorf(mountPointErrorMsg)
	}

	newDiskPartitionSetting.MountPoint = mountPoint
	newDiskPartition.ID = fmt.Sprintf("Partition%d", partitionNumber)
	newDiskPartitionSetting.ID = fmt.Sprintf("Partition%d", partitionNumber)

	if mountPoint == biosbootPartition {
		newDiskPartition.Flags = append(newDiskPartition.Flags, PartitionFlagBiosGrub)
		newDiskPartitionSetting.MountPoint = ""
	} else if mountPoint == "swap" {
		newDiskPartitionSetting.MountPoint = ""
	} else {
		if !strings.HasPrefix(mountPoint, "/") {
			// Other types of mount points are currently not supported
			err = fmt.Errorf("Invalid mount point specified: (%s)", mountPoint)
		}
	}

	return
}

func parsePartitionFlags(partCmd string, partitionNumber int) (err error) {
	// Only need to parse commands that contains --ondisk options
	if strings.Contains(partCmd, kickstartPartitionOnDisk) || strings.Contains(partCmd, kickstartPartitionOnDrive) {
		// Create new partition and partitionsetting
		newDiskPartition = new(Partition)
		newDiskPartitionSetting = new(PartitionSetting)
		newDiskPartitionSetting.MountIdentifier = MountIdentifierDefault

		partitionFlags := strings.Split(partCmd, " ")
		for _, partitionFlag := range partitionFlags {
			err := parseFlag(partitionFlag, partitionNumber)
			if err != nil {
				return err
			}
		}

		disks[curDiskIndex].Partitions = append(disks[curDiskIndex].Partitions, *newDiskPartition)
		partitionSettings = append(partitionSettings, *newDiskPartitionSetting)
	}

	return
}

func parseFlag(partitionFlag string, partitionNumber int) (err error) {
	if strings.HasPrefix(partitionFlag, "--") {
		// Find the index of "="
		index := strings.Index(partitionFlag, "=")
		if index != -1 {
			optionName := partitionFlag[0:index]
			optionVal := partitionFlag[(index + 1):len(partitionFlag)]

			err := partCmdProcess[optionName](optionVal)
			if err != nil {
				return err
			}
		} else {
			// Check grow flag
			if partitionFlag == kickstartPartitionGrow {
				shouldFillDiskSpace = true
				newDiskPartition.End = 0
			}
		}
	} else {
		// Update mount point
		if partitionFlag != "part" {
			err := processMountPoint(partitionFlag, partitionNumber)
			if err != nil {
				return err
			}
		}
	}

	return
}

// ParseKickStartPartitionScheme parses a kickstart-generated partition file and
// construct the Disk and PartitionSetting information
func ParseKickStartPartitionScheme(partitionFile string) (retdisks []Disk, retpartitionSettings []PartitionSetting, err error) {
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

	initializePrerequisitesForParser()

	scanner := bufio.NewScanner(file)
	partitionNumber := 1

	for scanner.Scan() {
		parseCmd := scanner.Text()
		err = parsePartitionFlags(parseCmd, partitionNumber)
		if err != nil {
			return
		}

		partitionNumber = partitionNumber + 1
	}

	retdisks = disks
	retpartitionSettings = partitionSettings
	return
}
