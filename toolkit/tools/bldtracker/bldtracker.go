// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to initialize a CSV file or record a new timestamp
// for shell scripts during the image-building process.

package main

import (
	"os"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp_v2"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	initializeMode = "init"
	recordMode     = "record"
	stopMode       = "stop"
	finishMode     = "finish"
	watchMode      = "watch"
)

var (
	app           = kingpin.New("bldtracker", "A tool that helps track build time of different steps in the makefile.")
	scriptName    = app.Flag("script-name", "The name of the current tool.").Required().String()
	stepPath      = app.Flag("step-path", "A '/' separated path of steps").Default("").String()
	expectedSteps = app.Flag("expected-steps", "Expected number of substeps for this new step").Default("0").Int()
	outPath       = app.Flag("out-path", "The file that stores timestamp CSVs.").Required().String() // currently must be absolute
	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	validModes    = []string{initializeMode, recordMode, stopMode, finishMode, watchMode}
	mode          = app.Flag("mode", "The mode of this tool. Could be 'initialize' ('i') or 'record' ('r').").Required().Enum(validModes...)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	//logger.Log.Warnf("Printing log to '%s'", *outPath)

	// Perform different actions based on the input "mode".
	switch *mode {
	case initializeMode:
		initialize(*outPath, *scriptName, *expectedSteps)

	case recordMode:
		record(*outPath, *scriptName, *stepPath, *expectedSteps)

	case stopMode:
		stop(*outPath, *scriptName, *stepPath)

	case finishMode:
		finish(*outPath, *scriptName)

	case watchMode:
		watch(*outPath)

	default:
		logger.Log.Warnf("Invalid call. Mode must be 'n' for initialize or 'r' for record. ")
	}
}

// Creates a CSV specifically for the shell script mentioned in "scriptName".
func initialize(completePath, toolName string, expectedSteps int) {
	timestamp_v2.StartTiming(toolName, completePath, expectedSteps)
}

// Records a new timestamp to the specific CSV for the specified shell script.
func record(completePath, toolName, path string, expectedSteps int) {
	_, err := timestamp_v2.ResumeTiming(completePath)
	if err != nil {
		logger.Log.Errorf("Failed to record timestamp: %s", err)
	}

	fullPath := toolName + "/" + path
	_, err = timestamp_v2.StartMeasuringEventByPath(fullPath, expectedSteps)
	if err != nil {
		logger.Log.Errorf("Failed to record timestamp: %s", err)
	}
}

func stop(completePath, toolName, path string) {
	_, err := timestamp_v2.ResumeTiming(completePath)
	if err != nil {
		logger.Log.Errorf("Failed to record timestamp: %s", err)
	}

	fullPath := toolName + "/" + path
	_, err = timestamp_v2.StopMeasurementByPath(fullPath)
	if err != nil {
		logger.Log.Errorf("Failed to record timestamp: %s", err)
	}
}

func finish(completePath, toolName string) {
	_, err := timestamp_v2.ResumeTiming(completePath)
	if err != nil {
		logger.Log.Errorf("Failed to record timestamp: %s", err)
	}

	timestamp_v2.EndTiming()
}

func watch(completePath string) {
	for {
		ts, err := timestamp_v2.ReadOnlyTimingData(completePath)
		if err != nil {
			logger.Log.Errorf("Failed to record timestamp: %s", err)
		} else {
			logger.Log.Warnf("Progress: %f", ts.Progress()*100)
		}
		time.Sleep(time.Second)
	}
}
