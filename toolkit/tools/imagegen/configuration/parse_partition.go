// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package parse_partition

import (
	"bufio"
	"os"
	"fmt"
	"strings"
	"strconv"


	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/internal/logger"
)

func parseKickStartParitionScheme(config configuration.Config) {

	var {
		parseCmd			string
		partitionFlags		[]string
		paritionTableType	PartitionTableType
		curDisk				configuration.Disk
		curConfig			configuration.SystemConfig
		diskInfo			map[string]configuration.Disk
		configInfo			map[string]configuration.SystemConfig
	}

	file, err := os.Open("/home/henry/git/CBL-Mariner/toolkit/tools/imagegen/configuration/parse.sh")
	if err != nil {
		fmt.Println("Failed to open file")
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	disks := []configuration.Disk{}
	config.Disks = disks
	diskInfo = make(map[string]configuration.Disk)
	defaultConfigIndex := 0

	for scanner.Scan() {
		parseCmd = scanner.Text()
		fmt.Printf("Parse Commands: %s\n", parseCmd)

		// Check partition table type
		if strings.Contains(parseCmd, "gpt") {
			fmt.Printf("Partition table type: %s\n", "gpt")
			partitionTableType = PartitionTableTypeGpt	
		} else if strings.Contains(parseCmd, "mbr") {
			fmt.Printf("Partition table type: %s\n", "mbr")
			partitionTableType = PartitionTableTypeMbr	
		} else {
			// Check disk information
			if strings.Contains(parseCmd, "--ondisk") {
				partitionFlags = strings.Split(parseCmd, " ")
				curDiskInfo := partitionFlags[len(partitionFlags)-1]
				curDiskInfo = curDiskInfo[9 : len(curDiskInfo)]
				
				// Check whether this disk already exists or not
				val, ok := diskInfo[curDiskInfo]
				if ok {
					curDisk = val
					curConfig = configInfo[curDiskInfo]
				}
				else {
					// Create new disk struct and append it into the Disk array
					curDisk = configuration.Disk{}
					diskInfo[curDiskInfo] = curDisk
					curDisk.PartitionTableType = paritionTableType
					disks = append(disks, curDisk)
					curDisk.Partitions = []configuration.Partition{}
					
					// Create new partitionSetting struct and append it into the sysconfig array
					curConfig = config.SystemConfigs[defaultConfigIndex]
					configInfo[curDiskInfo] = curConfig
					curConfig.PartitionSettings = []configuration.PartitionSetting{}
					defaultConfigIndex++
				}
				
				// Create new Partition and PartionSetting
				partition := configuration.Partition{}
				partitionSetting := configuration.PartitionSetting{}

				// Loop through partition flags to fetch fstype, size etc.
				for _, partOpt := range partitionFlags {
					// Find Mount Point
					partitionSetting.MountPoint = partOpt[1]
					if partOpt[1] == "biosboot" {
						partitionSetting.MountPoint = ""
					}

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
						
						if len(partitions) == 0 {
							partition.Start = 1
						} else {
							partition.Start = partitions[len(partitions)-1].End
						}

						if strings.Contains(parseCmd, "--grow") {
							partition.End = 0
						} else {
							partition.End = partition.Start + strconv.Atoi(partSizeStr)
						}
					}
				}

				curDisk.Partitions = append(curDisk.Partitions, partition)
				curConfig.PartitionSettings = append(curConfig.PartitionSettings, partitionSetting)
			} 
		}
	}

	return
}
