// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Test cases for timestamp.go.

package timestamp

import (
	"fmt"
	"os"
	"path/filepath"
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

func Test_WritetoFile_range_instant(t *testing.T) {
	initLogger()
	info1.Start()
	info1.RecordToFile("test step", "test action", os.Stdout)
}

// func Test_WritetoFile_noRange_instant(t *testing.T) {
// 	info2.Start()
// 	time.Sleep(30 * time.Millisecond)
// 	info2.RecordToFile("test step", "test action", os.Stdout)
// }

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

// func Test_WritetoCSV_noRange(t *testing.T) {
// 	InitCSV("build-time.csv", false)
// 	time.Sleep(10 * time.Millisecond) // extra sleep
// 	time.Sleep(20 * time.Millisecond)
// 	Stamp.RecordToCSV("step 1", "action 1")
// 	Stamp.Start()
// 	time.Sleep(20 * time.Millisecond)
// 	Stamp.RecordToCSV("step 2", "action 1")
// 	time.Sleep(10 * time.Millisecond) // extra sleep
// 	time.Sleep(20 * time.Millisecond)
// 	Stamp.RecordToCSV("step 2", "action 2")
// 	Stamp.Start()
// 	time.Sleep(20 * time.Millisecond)
// 	Stamp.RecordToCSV("step 3", "action 1")
// }

func Test_WritetoFile_range(t *testing.T) {
	initLogger()
	info1.Start()
	time.Sleep(10 * time.Millisecond)
	info1.RecordToFile("step 1", "action 1", os.Stdout)
	info1.Start()
	time.Sleep(10 * time.Millisecond)
	info1.RecordToFile("step 2", "action 1", os.Stdout)
	time.Sleep(20 * time.Millisecond)
	info1.Start()
	time.Sleep(10 * time.Millisecond)
	info1.RecordToFile("step 2", "action 2", os.Stdout)
	info1.Start()
	time.Sleep(10 * time.Millisecond)
	info1.RecordToFile("step 3", "action 1", os.Stdout)
}

func Test_filename(t *testing.T) {
	completePath := "/home/xuanchen/repos/pod_repo/CBL-Mariner/build/timestamp/imageconfigvalidator.csv"
	fileName := filepath.Base(completePath)
	fmt.Printf("%s \n", fileName)
	fmt.Printf("%s \n", fileName[:len(fileName)-4])
}
