// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package main

import (
	"bufio"
	"os"
	"fmt"
	"strings"
	"strconv"


	//"microsoft.com/pkggen/imagegen/configuration"
	//"microsoft.com/pkggen/internal/logger"
)

func main() {

	var {
		parseCmd			string
		partitionFlags		[]string
		paritionTableType	PartitionTableType
		curDisk				configuration.Disk
		diskInfo			map[string]configuration.Disk
	}

	file, err := os.Open("/home/henry/git/CBL-Mariner/toolkit/tools/imagegen/configuration/parse.sh")
	if err != nil {
		fmt.Println("Failed to open file")
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	disks := []configuration.Disk{}
	diskInfo = make(map[string]configuration.Disk)

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
				}
				else {
					// Create new disk struct and append it into the Disk array
					newDisk := configuration.Disk{}
					diskInfo[curDiskInfo] = newDisk
					newDisk.PartitionTableType = paritionTableType
					disks = append(disks, newDisk)

					partitions := []configuration.Partition{}
					partitionSettings := []configuration.PartitionSetting{}
					newDisk.Partitions = partitions

					// Deal with system config here for settings
				}
				
				// Create new Partition and PartionSetting
				partition := configuration.Partition{}
				partitionSetting := configuration.PartitionSetting{}

				// Loop through partition flags to fetch fstype, size etc.
				for _, partOpt := range partitionFlags {
					// Find Mount Point
					partitionSetting.MountPoint = partOpt[1]

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

				partitions = append(partitions, partition)
				partitionSettings = append(partitionSettings, partitionSetting)
			} 
		}
	}

	return
}
