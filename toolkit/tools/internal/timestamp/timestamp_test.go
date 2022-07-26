// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package timestamp

import (
	"fmt"
	"os"
	"testing"
	"time"
)

var (
	info1 = New("tool 1", true)
	info2 = New("tool 2", false)
)

//TestMain found in configuration_test.go.

func Test_WritetoFile_range_instant(t *testing.T) {
	info1.Start()
	info1.RecordToFile("test step", "test action", os.Stdout)
}

func Test_WritetoFile_noRange_instant(t *testing.T) {
	info2.Start()
	time.Sleep(30 * time.Millisecond)
	info2.RecordToFile("test step", "test action", os.Stdout)
}

func Test_WritetoCSV_range(t *testing.T) {
	InitCSV("build-time.csv", true)
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

func Test_getHomeDir(t *testing.T) {
	home, _ := os.UserHomeDir()
	fmt.Printf("%s\n", home)
	curr, _ := os.Getwd()
	fmt.Printf("%s\n", curr)
}

func Test_WritetoCSV_noRange(t *testing.T) {
	InitCSV("build-time.csv", false)
	time.Sleep(10 * time.Millisecond) // extra sleep
	// info2.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 1", "action 1")
	Stamp.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 1")
	time.Sleep(10 * time.Millisecond) // extra sleep
	// info2.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 2", "action 2")
	Stamp.Start()
	time.Sleep(20 * time.Millisecond)
	Stamp.RecordToCSV("step 3", "action 1")
}

func Test_WritetoFile_noRange(t *testing.T) {
	info2.Start()
	time.Sleep(10 * time.Millisecond)
	info2.RecordToFile("step 1", "action 1", os.Stdout)
	info2.Start()
	time.Sleep(10 * time.Millisecond)
	info2.RecordToFile("step 2", "action 1", os.Stdout)
	time.Sleep(20 * time.Millisecond)
	info2.Start()
	time.Sleep(10 * time.Millisecond)
	info2.RecordToFile("step 2", "action 2", os.Stdout)
	info2.Start()
	time.Sleep(10 * time.Millisecond)
	info2.RecordToFile("step 3", "action 1", os.Stdout)
}

func WritetoCSV(info *TimeInfo, seconds time.Duration) {
	Stamp.Start()
	time.Sleep(seconds * time.Millisecond)
	Stamp.RecordToCSV("test tool", "test step")
}
