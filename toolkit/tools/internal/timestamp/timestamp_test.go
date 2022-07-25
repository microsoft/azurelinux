// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Test cases for timestamp.go.

package timestamp

import (
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	info1 = New("tool 1")
	// info2 = New("tool 2", false)
)

//TestMain found in configuration_test.go.

func initLogger() {
	logger.InitStderrLog()
}

func Test_WritetoCSV_range(t *testing.T) {
	initLogger()
	InitCSV("build-time.csv")
	Stamp.Start()
	time.Sleep(10 * time.Millisecond)
	Stamp.RecordToCSV("step 1", "action 1")
	Stamp.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 1")
	Stamp.Start()
	time.Sleep(10 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 2")
	Stamp.Start()
	time.Sleep(30 * time.Millisecond)
	Stamp.RecordToCSV("step 3", "action 1")
}

func Test_WritetoCSV_noSetUp(t *testing.T) {
	initLogger()
	Stamp.Start()
	time.Sleep(10 * time.Millisecond)
	Stamp.RecordToCSV("step 1", "action 1")
	Stamp.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 1")
	Stamp.Start()
	time.Sleep(10 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 2")
	Stamp.Start()
	time.Sleep(30 * time.Millisecond)
	Stamp.RecordToCSV("step 3", "action 1")
}
