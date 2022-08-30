// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to initialize a CSV file or record a new timestamp
// for shell scripts during the image-building process.

package main

import (
	"os"
	"path/filepath"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	initializeMode = "i"
	recordMode     = "r"
)

var (
	app        = kingpin.New("bldtracker", "A tool that helps track build time of different steps in the makefile.")
	scriptName = app.Flag("script-name", "The name of the current tool.").Required().String()
	stepName   = app.Flag("step-name", "The name of the current step.").Required().String()
	actionName = app.Flag("action-name", "The name of the current action.").Default("").String()
	dirPath    = app.Flag("dir-path", "The folder that stores timestamp CSVs.").Required().ExistingDir() // currently must be absolute
	logFile    = app.Flag("log-file", "Directory for log files").Required().ExistingFile()
	validModes = []string{initializeMode, recordMode}
	mode       = app.Flag("mode", "The mode of this tool. Could be 'initialize' ('i') or 'record' ('r').").Required().Enum(validModes...)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, "trace")

	// Construct the CSV path.
	completePath := filepath.Join(*dirPath, *scriptName+".csv")

	// Perform different actions based on the input "mode".
	switch *mode {
	case initializeMode:
		initialize(completePath)
		break
	case recordMode:
		record(completePath)
		break
	default:
		logger.Log.Warnf("Invalid call. Mode must be 'n' for initialize or 'r' for record. ")
	}
}

// Creates a CSV specifically for the shell script mentioned in "scriptName".
func initialize(completePath string) {
	file, err := os.Create(completePath)
	if err != nil {
		logger.Log.Panicf("Unable to create file: %s", completePath)
	}
	file.Close()

	// Make a timestamp record right when a shell script starts.
	record(completePath)
}

// Records a new timestamp to the specific CSV for the specified shell script.
func record(completePath string) {
	file, err := os.OpenFile(completePath, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		logger.Log.Panicf("Unable to open file (may not have been created): %s", completePath)
	}
	defer file.Close()

	// Write the timestamp to CSV file using a helper function from timestamp.go.
	timestamp.WriteStamp(file, timestamp.NewBldTracker(*scriptName, *stepName, *actionName, time.Now()))
}
