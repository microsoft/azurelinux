// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to create and manipulate disks and partitions

package main

import (
	"bufio"
	"os"
	"fmt"
	"strings"


	//"microsoft.com/pkggen/imagegen/configuration"
	//"microsoft.com/pkggen/internal/logger"
)

func main() {
	file, err := os.Open("/home/henry/git/CBL-Mariner/toolkit/tools/imagegen/configuration/parse.sh")
	if err != nil {
		fmt.Println("Failed to open file")
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	diskIndex := 0
	disks := config.Disks
	disks[diskIndex] = PartitionTableTypeNone
	disks[diskIndex].MaxSize = 0
	var parseCmd string

	for scanner.Scan() {
		parseCmd = scanner.Text()
		fmt.Printf("Parse Commands: %s\n", parseCmd)

		// Check partition table type
		if strings.Contains(parseCmd, "gpt") {
			fmt.Printf("Partition table type: %s\n", "gpt")
			disks[diskIndex].PartitionTableType = PartitionTableTypeGpt	
		} else if strings.Contains(parseCmd, "mbr") {
			fmt.Printf("Partition table type: %s\n", "mbr")
			disks[diskIndex].PartitionTableType = PartitionTableTypeMbr	
		} else {
			// Look for actual partition schema which starts with the "part" command
			partitionFlags := strings.Split(parseCmd, " ")
			if partitionFlags[0] == "part" {
				for _, partOpt := range partitionFlags {
					var partition Partition
					var partitionSetting PartitionSetting

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
						partSize := partOpt[7 : len(partOpt)]
						fmt.Printf("partition size: %s\n", partSize)
					}
				}
			}
		}
	}

	return
}
