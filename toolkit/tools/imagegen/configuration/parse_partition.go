// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package configuration

import (
	"bufio"
	"os"
	"fmt"
	"strings"
	"strconv"
)

func ParseKickStartParitionScheme(config *Config) (err error) {

	var (
		parseCmd			string
		partitionFlags		[]string
		partitionTableType	PartitionTableType
		diskInfo			map[string]int
		configInfo			map[string]int
	)

	// Check whether the config already contains partition schema
	if len(config.Disks) > 0 && len(config.Disks[0].Partitions) > 0 {
		fmt.Printf("Partition scheme already exists\n")
		return
	} 

	file, err := os.Open("/home/henry/git/CBL-Mariner/toolkit/tools/imagegen/configuration/parse.sh")
	if err != nil {
		fmt.Printf("Failed to open file")
		return
	}
	defer file.Close()

	// Check if the file is empty
	_, err = file.Stat()
	if err != nil {
		fmt.Printf("File is empty\n")
		return
	}	

	defaultConfigIndex := 0

	scanner := bufio.NewScanner(file)
	diskInfo = make(map[string]int)
	configInfo = make(map[string]int)
	partitionTableType = PartitionTableTypeNone

	for scanner.Scan() {
		parseCmd = scanner.Text()
		fmt.Printf("Parse Commands: %s\n", parseCmd)

		// Check disk information
		if strings.Contains(parseCmd, "--ondisk") {
			partitionFlags = strings.Split(parseCmd, " ")
			curDiskInfo := partitionFlags[len(partitionFlags)-1]
			curDiskInfo = curDiskInfo[9 : len(curDiskInfo)]
				
			// Check whether this disk already exists or not
			curIdx, ok := diskInfo[curDiskInfo]
			if !ok {
				fmt.Printf("Create new disk object: %s\n", curDiskInfo)

				// Create new disk struct and append it into the Disk array
				newDisk := Disk{}
				newDisk.MaxSize = 2048
				artifacts := []Artifact{
					Artifact{
						Name: "core",
						Type: "vhd",
					},
				}
				newDisk.Artifacts = artifacts

				diskInfo[curDiskInfo] = defaultConfigIndex
				configInfo[curDiskInfo] = defaultConfigIndex
				curIdx = defaultConfigIndex
				defaultConfigIndex++
				newDisk.PartitionTableType = partitionTableType
				config.Disks = append(config.Disks, newDisk)
				fmt.Printf("Check size of disk array: %d\n", len(config.Disks))
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
					partition.FsType = fstype
					fmt.Printf("fstype: %s\n", fstype)
				}

				// Find partition size
				if strings.Contains(partOpt, "--size") {
					partSizeStr := partOpt[7 : len(partOpt)]
					fmt.Printf("partition size: %s\n", partSizeStr)
						
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
				
			fmt.Printf("Finish parsing line: start appending\n")
			config.Disks[curIdx].Partitions = append(config.Disks[curIdx].Partitions, *partition)
			config.SystemConfigs[curIdx].PartitionSettings = append(config.SystemConfigs[curIdx].PartitionSettings, *partitionSetting)
			fmt.Printf("Check Disk0 partition length: %d\n", len(config.Disks[0].Partitions))
		} 
	}

	// Print our disk and partitionSettings for validation
	for _, disk := range config.Disks {
		fmt.Printf("Partition table type: %s\n", disk.PartitionTableType)
		fmt.Printf("Artifact type: %s\n", disk.Artifacts[0].Type)
		for _, partition := range disk.Partitions {
			fmt.Printf("Partition ID: %s\n", partition.ID)
			fmt.Printf("Partition Start: %d\n", partition.Start)
			fmt.Printf("Partition End: %d\n", partition.End)
			fmt.Printf("Partition fstype: %s\n", partition.FsType)
		}
	}

	for _, sysconfig := range config.SystemConfigs {
		fmt.Printf("System config name: %s\n", sysconfig.Name)
		for _, partitionsetting := range sysconfig.PartitionSettings {
			fmt.Printf("Partition ID: %s\n", partitionsetting.ID)
			fmt.Printf("Partition Mount Point: %s\n", partitionsetting.MountPoint)
		}
	}

	return
}
