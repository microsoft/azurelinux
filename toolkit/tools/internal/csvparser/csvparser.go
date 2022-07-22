// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parses the timestamps stored in csv files and print them
// to the terminal at the end of the build.

package csvparser

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

var (
	timeArray [][]string // A 2-D array used to store all timestamps from csvs.
	// A list of csv files to be parsed.
	files = []string{"/imageconfigvalidator.csv", "/imagepkgfetcher.csv", "/imager.csv", "/roast.csv"}
)

// Reads a CSV file and appends line by line to array.
func CSVToArray(filename string) {
	file, err := os.Open(filename)

	if err != nil {
		fmt.Println("failed to open csv file")
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
	init_file, err := os.Stat(parentDir + "/init")

	// Format each file to array format.
	for _, file := range files {
		CSVToArray(parentDir + file)
	}

	// Get the start and end time from the first timestamp entry.
	// Start time will be the ModTime for "init" if it exists, otherwise will be the first csv entry.
	if os.IsNotExist(err) {
		fmt.Printf("start: %s\n", timeArray[0][4])
		startTime, err = time.Parse(time.UnixDate, timeArray[0][4])
	} else {
		fmt.Printf("start: %s\n", init_file.ModTime().Format(time.UnixDate))
		startTime = init_file.ModTime()
	}
	fmt.Printf("end: %s\n", timeArray[len(timeArray)-1][5])

	if err != nil {
		fmt.Printf("Unable to parse start time for the build. \n")
	}

	endTime, err := time.Parse(time.UnixDate, timeArray[len(timeArray)-1][5])
	if err != nil {
		fmt.Printf("Unable to parse end time for the build. \n")
	}

	// Get the total build time.
	difference := endTime.Sub(startTime)

	// Print timestamps.
	for i := 0; i < len(timeArray); i++ {
		fmt.Println(timeArray[i][0] + " " + timeArray[i][1] + " took " + timeArray[i][3] + ". ")
	}
	fmt.Println("The full build duration was " + difference.String() + ".")
}
