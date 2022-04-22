// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package configuration

import (
	"bufio"
	"os"
	"strings"
	"strconv"

	"microsoft.com/pkggen/internal/logger"
)

func ParseKickStartPartitionScheme(config *Config, partitionFile string) (err error) {

	var (
		parseCmd			string
		partitionFlags		[]string
		partitionTableType	PartitionTableType
		diskInfo			map[string]int
	)

	// Check whether the config already contains partition schema
	if len(config.Disks) > 0 && len(config.Disks[0].Partitions) > 0 {
		logger.Log.Infof("Partition scheme already exists")
		return
	}

	// Check whether the incoming config is for initrd
	if config.SystemConfigs[0].Name == "ISO initrd" {
		return
	}

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

	defaultDiskIndex := 0

	scanner := bufio.NewScanner(file)
	diskInfo = make(map[string]int)
	partitionTableType = PartitionTableTypeGpt

	for scanner.Scan() {
		parseCmd = scanner.Text()
		//fmt.Printf("Parse Commands: %s\n", parseCmd)

		// Find disk information
		if strings.Contains(parseCmd, "--ondisk") {
			partitionFlags = strings.Split(parseCmd, " ")
			curDiskInfo := partitionFlags[len(partitionFlags)-1]
			curDiskInfo = curDiskInfo[9 : len(curDiskInfo)]
				
			// Check whether this disk has already been parsed or not
			curIdx, ok := diskInfo[curDiskInfo]
			if !ok {
				// Create new disk struct and append it into the Disk array
				newDisk := Disk{}
				newDisk.PartitionTableType = partitionTableType

				// Set TargetDisk and TargetDiskType for unattended installation
				newDisk.TargetDisk.Type = "path"
				newDisk.TargetDisk.Value = curDiskInfo

				diskInfo[curDiskInfo] = defaultDiskIndex
				curIdx = defaultDiskIndex
				defaultDiskIndex++
				
				config.Disks = append(config.Disks, newDisk)
			}
				
			// Create new Partition and PartionSetting
			partition := new(Partition)
			partitionSetting := new(PartitionSetting)
			partitionSetting.MountIdentifier = MountIdentifierDefault
				
			// Find Mount Point
			partitionSetting.MountPoint = partitionFlags[1]
			if partitionFlags[1] == "biosboot" {
				partitionSetting.MountPoint = ""
				partitionSetting.ID = "boot"
				partition.ID = "boot"
				partition.Flags = append(partition.Flags, PartitionFlagBiosGrub)
				config.Disks[curIdx].PartitionTableType = PartitionTableTypeGpt
			} else if partitionFlags[1] == "/" {
				partitionSetting.ID = "rootfs"
				partition.ID = "rootfs"
			} else {
				partitionSetting.ID = partitionFlags[1]
				partition.ID = partitionFlags[1]
			}

			// Loop through partition flags to fetch fstype, size etc.
			for _, partOpt := range partitionFlags {

				// Find fstype
				if strings.Contains(partOpt, "--fstype") {
					fstype := partOpt[9 : len(partOpt)]
					if fstype == "biosboot" {
						partition.FsType = "fat32"
					} else if fstype == "swap" {
						partition.FsType = "linux-swap"
						partitionSetting.MountPoint = ""
					} else {
						partition.FsType = fstype
					}
				}

				// Find partition size
				if strings.Contains(partOpt, "--size") {
					partSizeStr := partOpt[7 : len(partOpt)]
						
					if len(config.Disks[curIdx].Partitions) == 0 {
						partition.Start = 1
					} else {
						partition.Start = config.Disks[curIdx].Partitions[len(config.Disks[curIdx].Partitions)-1].End
					}

					if strings.Contains(parseCmd, "--grow") {
						partition.End = 0
					} else {
						partitionSize, err := strconv.ParseUint(partSizeStr, 10, 64)
						if err != nil {
							return err
						}
						partition.End = partition.Start + partitionSize
					}
				}
			}
				
			config.Disks[curIdx].Partitions = append(config.Disks[curIdx].Partitions, *partition)
			config.SystemConfigs[curIdx].PartitionSettings = append(config.SystemConfigs[curIdx].PartitionSettings, *partitionSetting)
		} 
	}

	return
}
