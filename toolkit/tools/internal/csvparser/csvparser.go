// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parses the timestamps stored in CSV files and print them
// to the terminal at the end of the build.

package timestamp

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

var (
	timeArray [][]string // A 2-D array used to store all timestamps from CSVs.
	// A list of CSV files to be parsed.
	files []string
)

// Reads a CSV file and appends line by line to array.
func CSVToArray(filename string) {
	file, err := os.Open(filename)

	if err != nil {
		fmt.Println("failed to open CSV file")
	}
	defer file.Close()

	fileScanner := bufio.NewScanner(file)

	for fileScanner.Scan() {
		timeArray = append(timeArray, strings.Split(fileScanner.Text(), ","))
	}

}

// Take list of file paths, parse, and output log to terminal.
func OutputCSVLog(parentDir string) {
	var startTime time.Time
	const (
		startEntryNum       = 0
		fileNameColumnNum   = 0
		stepNameColumnNum   = 1
		actionNameColumnNum = 2
		durationColumnNum   = 3
		startTimeColumnNum  = 4
		endTimeColumnNum    = 5
	)

	init_file, err := os.Stat(parentDir + "/init")

	// Populate the slice "files".
	getFileName(parentDir)

	// Format each file to array format.
	for _, file := range files {
		CSVToArray(parentDir + file)
	}

	// Get the start and end time from the first timestamp entry.
	// Start time will be the ModTime for "init" if it exists, otherwise will be the first CSV entry.
	if os.IsNotExist(err) {
		fmt.Printf("start: %s\n", timeArray[startEntryNum][startTimeColumnNum])
		startTime, err = time.Parse(time.UnixDate, timeArray[startEntryNum][startTimeColumnNum])
	} else {
		fmt.Printf("start: %s\n", init_file.ModTime().Format(time.UnixDate))
		startTime = init_file.ModTime()
	}
	fmt.Printf("end: %s\n", timeArray[len(timeArray)-1][endTimeColumnNum])

	if err != nil {
		fmt.Printf("Unable to parse start time for the build. \n")
	}

	endTime, err := time.Parse(time.UnixDate, timeArray[len(timeArray)-1][endTimeColumnNum])
	if err != nil {
		fmt.Printf("Unable to parse end time for the build. \n")
	}

	// Get the total build time.
	difference := endTime.Sub(startTime)

	// Print timestamps.
	for i := 0; i < len(timeArray); i++ {
		fmt.Println(timeArray[i][fileNameColumnNum] + " " + timeArray[i][stepNameColumnNum] + " took " + timeArray[i][durationColumnNum] + ". ")
	}
	fmt.Println("The full build duration was " + difference.String() + ".")
}

// Iterate through the target directory and populate the files slice with strings of file names.
func getFileName(parentDir string) {
	const startFileIdx = 1
	err := filepath.Walk(parentDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Printf("Error: %s \n", err)
			return err
		}
		fileName := filepath.Base(path)
		// Skip the "init" file.
		if fileName != "init" {
			files = append(files, fileName)
		}
		return nil
	})
	if err != nil {
		fmt.Printf("Fail to complete file walk: %s \n", err)
	}

	// Remove directory name.
	files = files[startFileIdx:]
}
