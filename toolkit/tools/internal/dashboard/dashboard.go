package main

import (
	"fmt"
	"io/fs"
	"os"
	"strings"
	"time"
)

var (
	targetCSV = []string{"create_worker_chroot.csv", "imageconfigvalidator.csv", "imagepkgfetcher.csv", "imager.csv", "roast.csv"}
	CSVSize   = []int64{0, 0, 0, 0, 0}
	// targetJSON = []string{}
)

func main() {
	fmt.Println("Starting dashboard")
	wd, _ := os.Getwd()
	idx := strings.Index(wd, "CBL-Mariner/toolkit")
	wd = wd[0 : idx+19]

	// Use an infinite for loop to watch out for new updates
	for {
		// run this iteration periodically for smaller overhead
		time.Sleep(2 * time.Second)

		// Check if the target directory exists. Assume we only need to check one directory for now.
		targetDir := wd + "/tools/internal/timestamp/results/"
		currStat, err := os.Stat(targetDir)
		if os.IsNotExist(err) {
			// fmt.Printf("The target directory %s doesn't exist. \n", targetDir)
			continue
		}

		// Check update for each target file.
		for idx, filePath := range targetCSV {
			filePath = targetDir + filePath
			// fmt.Printf("Processing file %s. \n", filePath)
			currStat, err = os.Stat(filePath)
			// Check if the file exists.
			if os.IsNotExist(err) {
				// fmt.Printf("File doesn't exist. \n")
				continue
			}
			getUpdate(currStat, idx, filePath)
		}
	}

}

// Check if the file has been updated, and get updated contents if it did.
// Assumption: the file and its parent directories of the file have been created.
func getUpdate(currStat fs.FileInfo, idx int, filePath string) {
	if currStat.Size() != CSVSize[idx] {
		CSVSize[idx] = currStat.Size()
		fmt.Printf("%s has %d bytes\n", filePath, currStat.Size())
	}
	// fmt.Printf("No change in file size for %s \n.", filePath)
}
