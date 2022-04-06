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

func ParseKickStartParitionScheme(config Config) (err error) {

	var (
		parseCmd			string
		partitionFlags		[]string
		partitionTableType	PartitionTableType
		curDisk				Disk
		curConfig			SystemConfig
		diskInfo			map[string]Disk
		configInfo			map[string]SystemConfig
	)

	file, err := os.Open("/home/henry/git/CBL-Mariner/toolkit/tools/imagegen/configuration/parse.sh")
	if err != nil {
		fmt.Println("Failed to open file")
		return
	}
	defer file.Close()

	// Check if the file is empty
	_, err = file.Stat()
	if err != nil {
		fmt.Println("File is empty")
		return
	}

	scanner := bufio.NewScanner(file)
	disks := []Disk{}
	config.Disks = disks
	diskInfo = make(map[string]Disk)
	configInfo = make(map[string]SystemConfig)
	defaultConfigIndex := 0
	partitionTableType = PartitionTableTypeNone

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
				} else {
					// Create new disk struct and append it into the Disk array
					curDisk = Disk{}
					diskInfo[curDiskInfo] = curDisk
					curDisk.PartitionTableType = partitionTableType
					disks = append(disks, curDisk)
					curDisk.Partitions = []Partition{}
					
					// Create new partitionSetting struct and append it into the sysconfig array
					curConfig = config.SystemConfigs[defaultConfigIndex]
					configInfo[curDiskInfo] = curConfig
					curConfig.PartitionSettings = []PartitionSetting{}
					defaultConfigIndex++
				}
				
				// Create new Partition and PartionSetting
				partition := Partition{}
				partitionSetting := PartitionSetting{}
				
				// Find Mount Point
				partitionSetting.MountPoint = partitionFlags[1]
				if partitionFlags[1] == "biosboot" {
					partitionSetting.MountPoint = ""
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
						
						if len(curDisk.Partitions) == 0 {
							partition.Start = 1
						} else {
							partition.Start = curDisk.Partitions[len(curDisk.Partitions)-1].End
						}

						if strings.Contains(parseCmd, "--grow") {
							partition.End = 0
						} else {
							partitionSize, err := strconv.ParseUint(partSizeStr, 10, 64)
							if err != nil {
								fmt.Println("Invalid partition size")
								return err
							}
							partition.End = partition.Start + partitionSize
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
