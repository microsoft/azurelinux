// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to initialize a CSV file or record a new timestamp
// for shell scripts during the image-building process.

package bldtracker

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/globals"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

const (
	initializeMode = "init"
	recordMode     = "record"
	stopMode       = "stop"
	finishMode     = "finish"
)

type BldTrackerCmd struct {
	Mode       string `enum:"init,record,stop,finish" required:"" help:"The mode of this tool. Can be any of (${enum})"`
	ScriptName string `required:"" help:"The name of the current tool"`
	StepPath   string `help:"A '/' separated path of steps" default:""`
	OutPath    string `required:"" help:"The file to write timestamp data to"`
}

func (cmd *BldTrackerCmd) Run(globals *globals.Globals) error {
	// Perform different actions based on the input "mode"
	switch cmd.Mode {
	case initializeMode:
		initialize(cmd.OutPath, cmd.ScriptName)
	case recordMode:
		record(cmd.OutPath, cmd.ScriptName, cmd.StepPath)
	case stopMode:
		stop(cmd.OutPath, cmd.ScriptName, cmd.StepPath)
	case finishMode:
		finish(cmd.OutPath, cmd.ScriptName)
	default:
		logger.Log.Panicf("Invalid mode")
	}
	return nil
}

// Creates a JSON specifically for the shell script mentioned in "scriptName".
func initialize(completePath, toolName string) {
	timestamp.BeginTiming(toolName, completePath)
	timestamp.FlushAndCleanUpResources()
}

// Records a new timestamp to the specific JSON for the specified shell script.
func record(completePath, toolName, path string) {
	fullPath := toolName + "/" + path
	timestamp.ResumeTiming(toolName, completePath)
	defer timestamp.FlushAndCleanUpResources()
	timestamp.StartEventByPath(fullPath)
}

func stop(completePath, toolName, path string) {
	fullPath := toolName + "/" + path
	timestamp.ResumeTiming(toolName, completePath)
	defer timestamp.FlushAndCleanUpResources()
	timestamp.StopEventByPath(fullPath)
}

func finish(completePath, toolName string) {
	timestamp.ResumeTiming(toolName, completePath)
	timestamp.CompleteTiming()
}
