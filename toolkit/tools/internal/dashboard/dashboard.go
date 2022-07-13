package main

import (
	"bufio"
	"fmt"
	"io/fs"
	"os"
	"strings"
	"time"

	"github.com/gosuri/uiprogress"
)

var (
	currProgress  = 0
	totalProgress = 24
	targetDir     string
	targetCSV     = map[string][]int{
		"create_worker_chroot.csv": []int{0, 5},
		"imageconfigvalidator.csv": []int{0, 2},
		"imagepkgfetcher.csv":      []int{0, 9},
		"imager.csv":               []int{0, 4},
		"roast.csv":                []int{0, 3},
	}
	isInit = false // set to true the first time we detec the "init" file in build/timestamp folder.
	// targetJSON = []string{} // for future version
)

func main() {
	fmt.Println("Starting dashboard")
	uiprogress.Start() // start rendering
	bar := uiprogress.AddBar(totalProgress)
	bar.AppendCompleted()
	bar.PrependElapsed()

	wd, _ := os.Getwd()
	idx := strings.Index(wd, "CBL-Mariner/toolkit")
	wd = wd[0 : idx+19]
	targetDir = wd + "/tools/internal/timestamp/results/"

	// Use an infinite for loop to watch out for new updates
	for {
		// run this iteration periodically for smaller overhead
		time.Sleep(1 * time.Second)
		bar.Set(currProgress)

		// Check if the target directory exists. Assume we only need to check one directory for now.
		currStat, err := os.Stat(targetDir)
		if os.IsNotExist(err) {
			continue
		}

		// Check if build has started; if so, add a timestamp to init.csv
		if isInit == false {
			checkInit()
			// bar.Set(currProgress)
		}

		// Check update for each target file.
		for filePath, _ := range targetCSV {
			currStat, err = os.Stat(targetDir + filePath)
			// Check if the file exists.
			currStat, err := os.Stat(targetDir + filePath)
			if os.IsNotExist(err) {
				continue
			}
			// getUpdate(currStat, idx, filePath)
			currNumLines := getNumLines(targetDir + filePath)
			if currNumLines != targetCSV[filePath][0] {
				targetCSV[filePath][0] = currNumLines
				fmt.Printf("%s has %d lines \n", currStat.Name(), currNumLines)
				bar.Incr()
			}
			// getUpdate(currStat, idx, filePath)
		}
	}

}

// Check if the file has been updated, and get updated contents if it did.
// Assumption: the file and its parent directories of the file have been created.
func getUpdate(currStat fs.FileInfo, filePath string) {
	currNumLines := getNumLines(filePath)
	if currNumLines != targetCSV[filePath][0] {
		currProgress += currNumLines - targetCSV[filePath][0]
		targetCSV[filePath][0] = currNumLines
		fmt.Printf("%s has %d lines \n", currStat.Name(), currNumLines)
	}
}

// Naive implementation (potentially inefficient for larger files).
func getNumLines(filepath string) int {
	file, _ := os.Open(targetDir + filepath)
	fileScanner := bufio.NewScanner(file)
	count := 0

	for fileScanner.Scan() {
		count++
		if count > int(targetCSV[filepath][0]) {
			// fmt.Printf("[%d / %d] in %s: %s \n", count, targetCSV[filepath][1], filepath, fileScanner.Text())
		}
	}

	return count
}

// Checks if the build has started, and update the progress bar if it did start.
func checkInit() {
	_, err := os.Stat(targetDir + "/init")
	if os.IsNotExist(err) {
		return
	}
	isInit = true
	currProgress += 1
}
