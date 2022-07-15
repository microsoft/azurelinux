package main

import (
	"bufio"
	"fmt"
	"io/fs"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gosuri/uiprogress"
)

type stampedFile struct {
	fileName  string
	currLine  int32
	totalLine int32
	bar       *uiprogress.Bar
}

var (
	wg            sync.WaitGroup
	currProgress  = int32(0) // chose int32 instead of int to use the atomic package
	totalProgress = int32(24)
	isInit        = false // set to true the first time we detec the "init" file in build/timestamp folder.
	targetDir     string
	targetCSV     = []*stampedFile{
		&stampedFile{
			fileName:  "create_worker_chroot.csv",
			currLine:  0,
			totalLine: 5,
		},
		&stampedFile{
			fileName:  "imageconfigvalidator.csv",
			currLine:  0,
			totalLine: 2,
		},
		&stampedFile{
			fileName:  "imagepkgfetcher.csv",
			currLine:  0,
			totalLine: 9,
		},
		&stampedFile{
			fileName:  "imager.csv",
			currLine:  0,
			totalLine: 4,
		},
		&stampedFile{
			fileName:  "roast.csv",
			currLine:  0,
			totalLine: 3,
		},
	}
	// targetJSON = []string{} // for future version
)

func main() {
	fmt.Println("Starting dashboard")
	uiprogress.Start()
	bar := uiprogress.AddBar(int(totalProgress)).AppendCompleted().PrependElapsed()
	SetSubBar()

	wd, _ := os.Getwd()
	idx := strings.Index(wd, "CBL-Mariner")
	wd = wd[0 : idx+11]
	targetDir = wd + "/build/timestamp/"

	for {
		time.Sleep(1 * time.Second)
		// fmt.Printf("%d \n", int(currProgress))
		bar.Set(int(currProgress))

		// Check if the target directory exists. Assume we only need to check one directory for now.
		_, err := os.Stat(targetDir)
		if os.IsNotExist(err) {
			continue
		}

		// Check if build has started; if so, add a timestamp to init.csv
		if isInit == false {
			// fmt.Printf("incrementing in checkinit() \n")
			checkInit()
		}

		// Check update for each target file.
		for i, _ := range targetCSV {
			currFile := targetCSV[i]
			// Check if the file exists.
			currStat, err := os.Stat(targetDir + currFile.fileName)
			if os.IsNotExist(err) {
				continue
			}

			// If the file exists, check if there has been any updates since we last visited.
			currFile.getUpdate(currStat)
		}
	}

}

// Check if the file has been updated, and get updated contents if it did.
// Assumption: the file and its parent directories of the file have been created.
func (file *stampedFile) getUpdate(currStat fs.FileInfo) {
	currNumLines := file.getNumLines()
	if currNumLines != file.currLine {
		atomic.AddInt32(&currProgress, currNumLines-file.currLine)
		file.currLine = currNumLines
		// fmt.Printf("Progress: %d / %d \n", currProgress, totalProgress)
		file.bar.Set(int(currNumLines))
		// pop one task off the queue when it's done
		if currNumLines == file.totalLine {
			wg.Done()
		}
	}
}

// Naive implementation (potentially inefficient for larger files).
func (file *stampedFile) getNumLines() int32 {
	currfile, _ := os.Open(targetDir + file.fileName)
	fileScanner := bufio.NewScanner(currfile)
	count := int32(0)

	for fileScanner.Scan() {
		count += 1
		if count > file.currLine {
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
	atomic.AddInt32(&currProgress, 1)
}

func SetSubBar() {
	for i, _ := range targetCSV {
		currFile := targetCSV[i]
		currFile.bar = uiprogress.AddBar(int(currFile.totalLine)).AppendCompleted().PrependElapsed()
		wg.Add(1)
	}
}
