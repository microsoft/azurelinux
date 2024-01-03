// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package timestamp

import (
	"bufio"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

var (
	defaultStartTime = time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	defaultEndTime   = time.Date(2023, 1, 1, 1, 0, 0, 0, time.UTC)
)

func TestMain(m *testing.M) {
	// init logger to be used by the timestamp tool
	logger.InitStderrLog()

	retVal := m.Run()

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

	testFile := filepath.Join(t.TempDir(), "test_create_timestamp_file.jsonl")
	_, err := BeginTiming("test", testFile)
	defer CompleteTiming()

	assert.NoError(err)
	assert.FileExists(testFile)
}

func TestResumeAndAppend(t *testing.T) {
	assert := assert.New(t)

	testFile := filepath.Join(t.TempDir(), "test_resume_and_append.jsonl")
	_, err := BeginTiming("test", testFile)
	FlushAndCleanUpResources()

	assert.NoError(err)
	assert.FileExists(testFile)

	err = ResumeTiming("test", testFile)

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
	FlushAndCleanUpResources()

	ResumeTiming("test", testFile)
	ts, err = StopEventByPath("test/A")
	assert.NoError(err)
	FlushAndCleanUpResources()

	assert.NotNil(ts.EndTime)
}

func TestStartStopEvent(t *testing.T) {
	assert := assert.New(t)

	testFile := filepath.Join(t.TempDir(), "test_start_stop_event.jsonl")
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

func TestPauseResumeEvent(t *testing.T) {
	assert := assert.New(t)

	testFile := filepath.Join(t.TempDir(), "test_pause_resume_event.jsonl")
	root, _ := BeginTiming("test", testFile)

	ts, _ := StartEvent("A", root)
	idA := ts.ID
	ts, _ = PauseEvent(ts)
	ts, _ = ResumeEvent(ts)
	StopEvent(ts)

	FlushAndCleanUpResources()

	records := make([]*TimeStamp, 0)
	fd, err := os.OpenFile(testFile, os.O_RDONLY, 0644)
	if err != nil {
		return
	}
	scanner := bufio.NewScanner(fd)
	for scanner.Scan() {
		var record TimeStampRecord
		err = json.Unmarshal(scanner.Bytes(), &record)
		if err != nil {
			return
		}
		if idA != record.ID {
			continue
		}
		if record.EventType == EventPause || record.EventType == EventStop {
			records = append(records, record.TimeStamp)
		}
	}

	assert.Equal(len(records), 2)
	assert.Greater(records[0].ElapsedTime(), time.Duration(0))
	assert.Greater(records[1].ElapsedTime(), time.Duration(0))
	assert.Less(*records[0].EndTime, *records[1].StartTime)
}

func TestRerun(t *testing.T) {
	assert := assert.New(t)

	testFile := filepath.Join(t.TempDir(), "test_rerun.jsonl")

	// first, create a file and write complete timestamp data to it
	root, _ := BeginTiming("test", testFile)
	StartEvent("A", root)
	StopEvent(nil)
	StartEvent("B", root)
	StopEvent(nil)
	CompleteTiming()

	assert.FileExists(testFile)

	// now, simulate a new run on the same file, there should be no error
	// and existing data should be erased, i.e the new file should have 1 line
	_, err := BeginTiming("test", testFile)
	assert.NoError(err)
	FlushAndCleanUpResources()

	records := make([]*TimeStamp, 0)
	fd, err := os.OpenFile(testFile, os.O_RDONLY, 0644)
	if err != nil {
		return
	}
	scanner := bufio.NewScanner(fd)
	for scanner.Scan() {
		var record TimeStampRecord
		err = json.Unmarshal(scanner.Bytes(), &record)
		if err != nil {
			return
		}
		records = append(records, record.TimeStamp)
	}

	root = timestampMgr.root
	assert.Equal(len(records), 1)
	assert.Equal(records[0].ID, root.ID)
}
