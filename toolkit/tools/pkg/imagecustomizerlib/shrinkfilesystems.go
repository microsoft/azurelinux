package imagecustomizerlib

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"regexp"
	"strconv"
	"strings"
)

func shrinkFilesystems(imageLoopDevice string, outputImageFile string) error {
	logger.Log.Infof("Shrinking filesystems")

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		if diskPartitions[partitionNum].Type == "part" {
			fstype := diskPartitions[partitionNum].FileSystemType
			// Currently only support ext2, ext3, ext4 filesystem types
			if fstype != "ext2" && fstype != "ext3" && fstype != "ext4" {
				continue
			}

			partitionLoopDevice := diskPartitions[partitionNum].Path
			// Check the file system with e2fsck
			err := shell.ExecuteLive(true /*squashErrors*/, "sudo", "e2fsck", "-fy", partitionLoopDevice)
			if err != nil {
				return fmt.Errorf("failed to check %s with e2fsck:\n%w", partitionLoopDevice, err)
			}
			// Resize the file system with resize2fs
			stdout, stderr, err := shell.Execute("sudo", "resize2fs", "-M", partitionLoopDevice)
			// Example output:
			// Resizing the filesystem on /dev/loop31p2 to 10579 (4k) blocks.
			// The filesystem on /dev/loop31p2 is now 10579 (4k) blocks long.
			println(stdout)
			println(stderr)
			re := regexp.MustCompile(`.*to (\d+) \((\d+)([a-zA-Z])\)`)
			match := re.FindStringSubmatch(stdout)
			if len(match) < 4 { // in fact, this should be exactly equal to 4. and definitely at least 4.
				return fmt.Errorf("No number found in the input string") //TODO change string for error
			}

			// Convert the matched string to an integer
			blockCount, err := strconv.Atoi(match[1])
			if err != nil {
				return err
			}
			multiplier, err := strconv.Atoi(match[2])
			if err != nil {
				return err
			}
			unit := match[3]
			blockSize := 1
			const k = 1024 // kilobyte in bytes
			switch unit {
			case "k": 
				blockSize = multiplier*k
			default: 
				return fmt.Errorf("unrecognized unit %s", unit)
			}
			filesystemSizeInBytes := blockCount * blockSize
			fmt.Printf("fs size %d\n", filesystemSizeInBytes)

			stdout, stderr, err = shell.Execute("sudo", "parted", partitionLoopDevice, "print") 
			println(stdout)
			println(stderr)
			stdout, stderr, err = shell.Execute("sudo", "parted", imageLoopDevice, "print") 
			println(stdout)
			println(stderr)
			
			
			// stdout, stderr, err = shell.Execute("sudo", "parted", outputImageFile, "print") 
			// println(stdout)
			// println(stderr)
			stdout, stderr, _ = shell.Execute("sudo", "fdisk", "-l", imageLoopDevice)
			println(stdout)
			println(stderr)
			re = regexp.MustCompile(`Units.*= (\d+) bytes`)
			match = re.FindStringSubmatch(stdout)
			if len(match) < 2 { // in fact, this should be exactly equal to 2. and definitely at least 2.
				return fmt.Errorf("No number found in the input string") //TODO change string for error
			}
			sectorSizeInBytes, err := strconv.Atoi(match[1])
			if err != nil {
				return err
			}
			println(match[1])
			// re = regexp.MustCompile(regexp.QuoteMeta(partitionLoopDevice) + `\s*+(\d+)`)

			loopDeviceReg := strings.ReplaceAll(partitionLoopDevice, "/", `\/`) // because QuoteMeta does not esc forward slashes .-.
			re = regexp.MustCompile(loopDeviceReg + ` *(\d+)`)
			match = re.FindStringSubmatch(stdout)
			if len(match) < 2 { // in fact, this should be exactly equal to 2. and definitely at least 2.
				return fmt.Errorf("No number found in the input string") //TODO change string for error
			}
			start, err := strconv.Atoi(match[1])
			if err != nil {
				return err
			}
			// return fmt.Errorf("pause 1")
		
			
			// stdout, _, _ = shell.Execute("echo", "yes")
			// stdout, stderr, err = shell.Execute(stdout, "sudo", "parted", imageLoopDevice, "resizepart", strconv.Itoa(partitionNum), strconv.Itoa(filesystemSizeInBytes))
			// println(stdout) DOES NOT WORK
			

			// start := (18431+1) // keep same start  //TODO programmatic
			end := start + (filesystemSizeInBytes/sectorSizeInBytes) //512 is sector size
			fmt.Printf("start: %s\n", start)
			fmt.Printf("end: %s\n", end)
			println(fstype)
			println(strconv.Itoa(partitionNum))
			stdout, stderr, err = shell.Execute("sudo", "parted", imageLoopDevice, "rm", strconv.Itoa(partitionNum)) //change "2" to string(partNum)
			println(stdout)
			println(stderr)
			stdout, stderr, err = shell.Execute("sudo", "parted", imageLoopDevice, "print") 
			println(stdout)
			println(stderr)
			println("making partition")
			// stdout, stderr, err = shell.Execute("sudo", "parted", "unit", "s")

			stdout, stderr, err = shell.Execute("sudo", "parted", "-s", imageLoopDevice, "mkpart", "primary", fstype, strconv.Itoa(start) + "s", strconv.Itoa(end) + "s") // TODO try to remove primary
			println(stdout)
			println(stderr)
			stdout, stderr, err = shell.Execute("flock", "--timeout", "5", imageLoopDevice, "partprobe", "-s", imageLoopDevice)
			if err != nil {
				logger.Log.Warnf("Failed to execute partprobe: %v", stderr)
				return err
			}
			stdout, stderr, err = shell.Execute("sudo", "parted", imageLoopDevice, "print") 
			println(stdout)
			println(stderr)
			stdout, stderr, _ = shell.Execute("sudo", "fdisk", "-l", imageLoopDevice)
			println(stdout)
			println(stderr)
			return fmt.Errorf(":")
			// stdout, stderr, err = shell.Execute("sudo", "parted", imageLoopDevice, "print") 
			// println(stdout)
			// println(stderr)
			// stdout, stderr, _ = shell.Execute("sudo", "e2fsck", "-fy", partitionLoopDevice)
			// println(stdout)
			// println(stderr)
			
			// return fmt.Errorf("pause")
			
			// stdout, stderr, err = shell.Execute("sudo", "resize2fs", "-P", partitionLoopDevice)
			// println(stdout)
			// println(stderr)
			if err != nil {
				return fmt.Errorf("failed to resize %s with resize2fs:\n%w", partitionLoopDevice, err)
			}

			// stdout, stderr, err = shell.Execute("sudo", "fdisk", "-s", partitionLoopDevice)
			// println(stdout)
			// println(stderr)
			// if err != nil {
			// 	return fmt.Errorf("failed to fdisk %s:\n%w", partitionLoopDevice, err)
			// }
			
			// stdout, stderr, err = shell.Execute("sudo", "fdisk", "-s", partitionLoopDevice)
			// println(stdout)
			// println(stderr)
			// if err != nil {
			// 	return fmt.Errorf("failed to fdisk %s:\n%w", partitionLoopDevice, err)
			// }

			// stdout, stderr, err = shell.Execute("sudo", "fdisk", "-l", partitionLoopDevice)
			// println(stdout)
			// println(stderr)
			// if err != nil {
			// 	return fmt.Errorf("failed to fdisk %s:\n%w", partitionLoopDevice, err)
			// }
		}
	}
	return nil
}
