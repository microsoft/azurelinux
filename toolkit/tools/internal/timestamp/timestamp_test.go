// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package timestamp

import (
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

const (
	testDataDir   = "./testdata/"
	testOutputDir = "./testout/"
)

var (
	defaultStartTime = time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	defaultEndTime   = time.Date(2023, 1, 1, 1, 0, 0, 0, time.UTC)
)

func setUp() {
	// init logger to be used by the timestamp tool
	logger.InitStderrLog()

	if _, err := os.Stat(testOutputDir); os.IsNotExist(err) {
		err = os.Mkdir(testOutputDir, 0755)
		if err != nil {
			panic(err)
		}
	}
}

func tearDown() {
	timestampRecordFiles, err := filepath.Glob(testOutputDir + "*.jsonl")
	if err != nil {
		panic(err)
	}
	for _, file := range timestampRecordFiles {
		err = os.Remove(file)
		if err != nil {
			panic(err)
		}
	}
}

func TestMain(m *testing.M) {
	setUp()
	retVal := m.Run()
	tearDown()
	os.Exit(retVal)
}

func TestElapsedTime(t *testing.T) {
	assert := assert.New(t)

	ts, _ := newTimeStamp("test", nil)
	ts.StartTime = &defaultStartTime

	assert.Equal(ts.ElapsedTime(), time.Duration(-1))

	ts.EndTime = &defaultEndTime
	elapsedTime, _ := time.ParseDuration("1h")
	assert.Equal(ts.ElapsedTime(), elapsedTime)
}

func TestDisplayName(t *testing.T) {
	assert := assert.New(t)

	// construct the following timestamp tree
	// root
	//   -> A
	//     -> B
	//     -> C
	//   -> D
	rootTS, _ := newTimeStamp("root", nil)
	tsA, _ := newTimeStamp("A", nil)
	tsB, _ := newTimeStamp("B", nil)
	tsC, _ := newTimeStamp("C", nil)
	tsD, _ := newTimeStamp("D", nil)

	rootTS.addSubStep(tsA)
	rootTS.addSubStep(tsD)
	tsA.addSubStep(tsB)
	tsA.addSubStep(tsC)

	assert.Equal(rootTS.DisplayName(), "root")
	assert.Equal(tsA.DisplayName(), "root/A")
	assert.Equal(tsB.DisplayName(), "root/A/B")
	assert.Equal(tsC.DisplayName(), "root/A/C")
	assert.Equal(tsD.DisplayName(), "root/D")
}

func TestNewTimeStampInvalidPathSeparator(t *testing.T) {
	_, err := newTimeStamp("invalid/name", nil)

	assert.Error(t, err)
}

func TestNewTimeStampByPath(t *testing.T) {
	assert := assert.New(t)

	rootTS, _ := newTimeStamp("root", nil)
	tsA, _ := newTimeStamp("A", nil)

	rootTS.addSubStep(tsA)

	// success path
	tsB, err := newTimeStampByPath(rootTS, "root/A/B")
	assert.Equal(tsB.DisplayName(), "root/A/B")
	assert.NoError(err)

	// non-existent node
	_, err = newTimeStampByPath(rootTS, "root/A/B/C/D")
	assert.Error(err)

	// non-existent node - invalid root name
	_, err = newTimeStampByPath(rootTS, "invalid/root/A/C")
	assert.Error(err)
}

func TestTimeStampComplete(t *testing.T) {
	assert := assert.New(t)

	ts, _ := newTimeStamp("test", nil)
	ts.StartTime = &defaultStartTime

	assert.Equal(ts.ElapsedTime(), time.Duration(-1))

	ts.complete(defaultEndTime)
	elapsedTime, _ := time.ParseDuration("1h")
	assert.Equal(ts.ElapsedTime(), elapsedTime)

	assert.Equal(ts.ElapsedSeconds, elapsedTime.Seconds())
}

func TestCreateTimeStampFile(t *testing.T) {
	assert := assert.New(t)

	testFile := testOutputDir + "test_create_timestamp_file.jsonl"
	_, err := BeginTiming("test", testFile)
	defer CompleteTiming()

	assert.NoError(err)
	assert.FileExists(testFile)
}

func TestResumeAndAppend(t *testing.T) {
	assert := assert.New(t)

	testFile := testOutputDir + "test_resume_and_append.jsonl"
	_, err := BeginTiming("test", testFile)
	FlushAndCleanUpResources()

	assert.NoError(err)
	assert.FileExists(testFile)

	err = ResumeTiming("test", testFile)
	defer CompleteTiming()

	assert.NoError(err)
	root := timestampMgr.root
	assert.Equal(root.Name, "test")
	assert.NotNil(root.StartTime)
	assert.Nil(root.EndTime)

	ts, err := StartEventByPath("test/A")
	assert.NoError(err)
	// make sure the ID generator doesn't cause collision
	assert.Equal(root.ID+1, ts.ID)
	assert.Equal(root.ID, ts.ParentID)
}

func TestStartStopEvent(t *testing.T) {
	assert := assert.New(t)

	testFile := testOutputDir + "test_start_stop_event.jsonl"
	root, err := BeginTiming("test", testFile)

	assert.NoError(err)
	assert.FileExists(testFile)

	tsA, err := StartEvent("A", root)
	assert.NoError(err)

	tsB, err := StartEvent("B", nil)
	assert.NoError(err)

	StopEvent(tsB) // stop B
	StopEvent(nil) // stop A

	tsC, err := StartEvent("C", nil)
	assert.NoError(err)

	StopEvent(nil) // stop C
	StopEvent(nil) // stop root

	FlushAndCleanUpResources()

	// verify timestamp tree structure
	root = timestampMgr.root
	assert.NotNil(root.EndTime)
	assert.NotNil(tsA.EndTime)
	assert.NotNil(tsB.EndTime)
	assert.NotNil(tsC.EndTime)
	assert.Nil(timestampMgr.lastVisited)
	assert.Equal(root.DisplayName(), "test")
	assert.Equal(tsA.DisplayName(), "test/A")
	assert.Equal(tsB.DisplayName(), "test/A/B")
	assert.Equal(tsC.DisplayName(), "test/C")
}
