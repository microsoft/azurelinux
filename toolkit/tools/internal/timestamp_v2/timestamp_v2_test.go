// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package timestamp_v2

import (
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

// type TimeStamp struct {
// 	Name          string      `json:"Name"`
// 	StartTime     time.Time   `json:"StartTime"`
// 	EndTime       time.Time   `json:"StartTime"`
// 	ExpectedSteps int         `json:"ExpectedSteps"`
// 	Steps         []TimeStamp `json:"Steps"`
// 	// Weight     float     `json:"Weight"`
// }

func runAsserts(t *testing.T, ts *TimeStamp, err error) {
	assert.NotNil(t, ts)
	assert.NoError(t, err)
}

func timestampHasEquivalentTiming(a, b TimeStamp) bool {
	var st, et, elap bool
	if a.StartTime != nil && b.StartTime != nil {
		st = a.StartTime.Equal(*b.StartTime)
	} else {
		st = a.StartTime == b.StartTime
	}

	if a.EndTime != nil && b.EndTime != nil {
		et = a.StartTime.Equal(*b.StartTime)
	} else {
		et = a.EndTime == b.EndTime
	}

	elap = a.ElapsedSeconds == b.ElapsedSeconds
	return st && et && elap
}

func cleanupFiles() {
	files1, err := filepath.Glob("./testout/*.json")
	if err != nil {
		logger.Log.Panicf("Failed to tidy up timestamp tests: '%s'", err.Error())
	}
	files2, err := filepath.Glob("./testout/*.lock")
	if err != nil {
		logger.Log.Panicf("Failed to tidy up timestamp tests: '%s'", err.Error())
	}
	for _, file := range append(files1, files2...) {
		err = os.Remove(file)
		if err != nil {
			logger.Log.Panicf("Failed to tidy up timestamp tests: '%s'", err.Error())
		}
	}
}

func TestMain(m *testing.M) {
	// Need to create logger since the json tools use it, will just
	// print to console for errors.
	logger.InitStderrLog()
	ret := m.Run()

	// To preserve the output .json files for debugging, comment out the following line.
	cleanupFiles()
	os.Exit(ret)
}

// Test if we can read an existing json file, add lines to it, then write it out
func TestLoadDemo(t *testing.T) {
	var timestamp TimeStamp
	err := jsonutils.ReadJSONFile("./testdata/time.json", &timestamp)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	now := time.Now()
	future := now.Add(time.Minute * 5)
	timestamp.StartTime = &now
	timestamp.EndTime = &future

	err = jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &timestamp)
	assert.NoError(t, err)
	if err != nil {
		return
	}
}

func TestCreateTimeStamp(t *testing.T) {
	ts, err := createTimeStamp("name", time.Now(), 0)
	runAsserts(t, ts, err)
}

func TestInvalidPathSeparator(t *testing.T) {
	ts, err := createTimeStamp("invalid/path/name", time.Now(), 0)
	assert.EqualError(t, err, "can't create a timestamp object with a path containing /")
	assert.Nil(t, ts)

	ts, err = StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("invalid/path/name", 0)
	assert.EqualError(t, err, "failed to create a timestamp object 'invalid/path/name': can't create a timestamp object with a path containing /")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestInvalidExpected(t *testing.T) {
	ts, err := createTimeStamp("name", time.Now(), -10)
	assert.EqualError(t, err, "can't create a timestamp object with negative expected steps")
	assert.Nil(t, ts)

	ts, err = StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("name", -10)
	assert.EqualError(t, err, "failed to create a timestamp object 'name': can't create a timestamp object with negative expected steps")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestCreateSubStep(t *testing.T) {
	root := &TimeStamp{Name: "Root", parent: nil}
	ts, err := root.addStepWithExpected("1", time.Now(), 0)
	runAsserts(t, ts, err)
}

func TestInitManager(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	time.Sleep(100 * time.Microsecond)
	err = EndTiming()
	assert.NoError(t, err)
}

func holdLock(t *testing.T, path string, timeToHoldMillis int) {
	logger.Log.Warnf("Routine Start")
	fd, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR, 0664)
	assert.NoError(t, err)
	err = waitOnFileLock(fd, 0)
	defer unlockFileLock(fd)
	assert.NoError(t, err)
	time.Sleep(time.Duration(timeToHoldMillis) * time.Millisecond)
	logger.Log.Warnf("Routine End")
}

func TestLockingCooperative(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	fd1, err := os.Create(path)
	assert.NoError(t, err)
	fd2, err := os.Create(path)
	assert.NoError(t, err)

	err = waitOnFileLock(fd1, 0)
	assert.NoError(t, err)
	unlockFileLock(fd1)
	err = waitOnFileLock(fd2, 0)
	assert.NoError(t, err)
	fd2.Close()
}

func TestLockingAlreadyLocked(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	fd1, err := os.Create(path)
	assert.NoError(t, err)
	fd2, err := os.Create(path)
	assert.NoError(t, err)

	err = waitOnFileLock(fd1, 0)
	defer unlockFileLock(fd1)
	assert.NoError(t, err)

	err = waitOnFileLock(fd2, 100)
	assert.EqualError(t, err, "failed to secure timing data lock after 100 milliseconds- resource temporarily unavailable")
	logger.Log.Warnf("Test end")
}

func TestGainsLock(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	go holdLock(t, path, 300)
	time.Sleep(100 * time.Millisecond)

	fd1, err := os.Create(path)
	assert.NoError(t, err)
	err = waitOnFileLock(fd1, 300)
	defer unlockFileLock(fd1)
	assert.NoError(t, err)
}

func TestBlocksParallelAccess(t *testing.T) {
	path := "./testout/" + t.Name() + ".json"
	ts, err := StartTiming(t.Name(), path, 0)
	runAsserts(t, ts, err)

	go holdLock(t, path, 300)
	time.Sleep(150 * time.Millisecond)

	ts, err = ReadOnlyTimingData(path)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't lock timing file (./testout/TestBlocksParallelAccess.json): failed to secure timing data lock after 100 milliseconds- resource temporarily unavailable")
	err = EndTiming()
	assert.NoError(t, err)
}

func TestInitManagerDoubleStart(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	assert.EqualError(t, err, "already recording timing data for tool 'TestInitManagerDoubleStart' into file (./testout/"+t.Name()+".json)")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, StampMgr.root)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestManagerBasic1(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M1", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M2", 0)
	runAsserts(t, ts, err)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestManagerBasic2(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M1", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M2", 3)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("child1", 0)
	runAsserts(t, ts, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("child2", 0)
	runAsserts(t, ts, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("child3", 0)
	runAsserts(t, ts, err)
	progress := StampMgr.root.Progress()
	assert.Equal(t, 2.0/3.0, progress)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	progress = StampMgr.root.Progress()
	assert.Equal(t, 0.95, progress)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestOverPopMeasurements(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M1", 0)
	runAsserts(t, ts, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)

	ts, err = StopMeasurement()
	assert.EqualError(t, err, "can't stop measuring the root timestamp 'TestOverPopMeasurements', call EndTiming() instead")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, StampMgr.root)

	assert.Equal(t, 0.95, StampMgr.root.Progress())
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopWithoutStarting(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	err := EndTiming()
	assert.EqualError(t, err, "timestamping not initialized yet, can't stop timing")
}

func TestStartMeasurementWithoutStarting(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := StartMeasuringEvent("M1", 0)
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data for 'M1'")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestStopMeasurementWithoutStarting(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := StopMeasurement()
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestParentNotStartedYet(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := StartMeasuringEventWithParent(&TimeStamp{}, "parent", 0)
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data for 'parent'")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestNilParent(t *testing.T) {
	var nilTS *TimeStamp = nil
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventWithParent(nilTS, "nil", 0)
	assert.EqualError(t, err, "invalid timestamp parent, can't add sub-step 'nil'")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopRoot(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	ts, err := StopMeasurementSpecific(root)
	assert.EqualError(t, err, "can't stop measuring the root timestamp 'TestStopRoot', call EndTiming() instead")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	ts, err = StopMeasurementByPath(t.Name())
	assert.EqualError(t, err, "can't stop measuring the root timestamp 'TestStopRoot', call EndTiming() instead")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopNoMgr(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := StopMeasurementSpecific(&TimeStamp{Name: "Not_empty"})
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data for 'Not_empty'")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestStopIsActiveNode(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	active, err := StartMeasuringEvent("activenode", 0)
	runAsserts(t, active, err)
	newActive, err := StopMeasurementSpecific(active)
	runAsserts(t, newActive, err)
	assert.Equal(t, root, newActive)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestActiveIsRootAfterStopStart(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	time.Sleep(10 * time.Millisecond)
	err = EndTiming()
	assert.NoError(t, err)
	ts, err := ResumeTiming("./testout/" + t.Name() + ".json")
	runAsserts(t, ts, err)
	newActive, err := GetActiveTimeNode()
	runAsserts(t, newActive, err)
	assert.True(t, timestampHasEquivalentTiming(*root, *newActive))
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopMiddleNode(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 0)
	runAsserts(t, a, err)
	b, err := StartMeasuringEvent("B", 0)
	runAsserts(t, b, err)
	c, err := StartMeasuringEvent("C", 0)
	runAsserts(t, c, err)
	new_active, err := StopMeasurementSpecific(b)
	runAsserts(t, new_active, err)
	assert.Equal(t, c, new_active)
	active, err := GetActiveTimeNode()
	runAsserts(t, active, err)
	assert.Equal(t, c, active)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopCleanup(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 0)
	runAsserts(t, a, err)
	b1_specific_stop, err := StartMeasuringEvent("B1", 0)
	runAsserts(t, b1_specific_stop, err)
	b2, err := StartMeasuringEventWithParent(a, "B2", 0)
	runAsserts(t, b2, err)
	b3, err := StartMeasuringEventWithParent(a, "B3", 0)
	runAsserts(t, b3, err)
	c1, err := StartMeasuringEvent("C1", 0)
	runAsserts(t, c1, err)
	c2, err := StartMeasuringEventWithParent(b1_specific_stop, "C2", 0)
	runAsserts(t, c2, err)
	c3, err := StartMeasuringEventWithParent(b1_specific_stop, "C3", 0)
	runAsserts(t, c3, err)

	time.Sleep(time.Millisecond * 50)

	ts, err := StopMeasurementSpecific(b1_specific_stop)
	runAsserts(t, ts, err)

	time.Sleep(time.Millisecond * 50)

	err = EndTiming()
	assert.NoError(t, err)

	assert.Equal(t, root.EndTime, a.EndTime)
	assert.Equal(t, root.EndTime, b2.EndTime)
	assert.Equal(t, root.EndTime, b3.EndTime)

	// Children of b1 should inherit its end time when we clean up
	assert.NotEqual(t, root.EndTime, b1_specific_stop.EndTime)
	assert.Equal(t, b1_specific_stop.EndTime, c1.EndTime)
	assert.Equal(t, b1_specific_stop.EndTime, c2.EndTime)
	assert.Equal(t, b1_specific_stop.EndTime, c3.EndTime)

	// Everything else should inherit the root node's end time
	rootElapsed := root.ElapsedSeconds
	assert.NotEqual(t, -1.0, root.ElapsedSeconds)
	assert.Equal(t, rootElapsed, a.ElapsedSeconds)
	assert.Equal(t, rootElapsed, b2.ElapsedSeconds)
	assert.Equal(t, rootElapsed, b3.ElapsedSeconds)
}

func TestGetActiveNode(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := GetActiveTimeNode()
	assert.EqualError(t, err, "timestamping not initialized yet, can't get active node")
	assert.NotNil(t, ts)
	assert.Equal(t, &TimeStamp{}, ts)

	ts, err = StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	a, err := StartMeasuringEvent("a", 0)
	runAsserts(t, a, err)
	b, err := StartMeasuringEvent("b", 0)
	runAsserts(t, b, err)
	active, err := GetActiveTimeNode()
	runAsserts(t, active, err)
	assert.Equal(t, b, active)

	b2, err := StartMeasuringEventWithParent(a, "b_2", 0)
	runAsserts(t, b2, err)
	assert.Equal(t, b, active)

	// We should never redo the active node when calling this function
	c, err := StartMeasuringEventWithParent(a, "b", 0)
	runAsserts(t, c, err)
	assert.Equal(t, b, active)

	err = EndTiming()
	assert.NoError(t, err)
}

func TestSearchByPath(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := GetNodeByPath("not/a/real/path")
	assert.EqualError(t, err, "timestamping not initialized yet, can't get search for node 'not/a/real/path'")
	assert.NotNil(t, ts)
	assert.Equal(t, &TimeStamp{}, ts)

	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 0)
	runAsserts(t, a, err)
	b2, err := StartMeasuringEventWithParent(a, "B_2", 0)
	runAsserts(t, b2, err)
	c2, err := StartMeasuringEventWithParent(b2, "C_2", 0)
	runAsserts(t, b2, err)
	b, err := StartMeasuringEvent("B", 0)
	runAsserts(t, b, err)
	c, err := StartMeasuringEvent("C", 0)
	runAsserts(t, c, err)
	d, err := StartMeasuringEvent("D", 0)
	runAsserts(t, d, err)

	// Good
	search, err := GetNodeByPath("TestSearchByPath")
	runAsserts(t, d, err)
	assert.Equal(t, search, root)
	search, err = GetNodeByPath("TestSearchByPath/A")
	runAsserts(t, d, err)
	assert.Equal(t, search, a)
	search, err = GetNodeByPath("TestSearchByPath/A/B_2")
	runAsserts(t, d, err)
	assert.Equal(t, search, b2)
	search, err = GetNodeByPath("TestSearchByPath/A/B_2/C_2")
	runAsserts(t, d, err)
	assert.Equal(t, search, c2)
	search, err = GetNodeByPath("TestSearchByPath/A/B/C/D")
	runAsserts(t, d, err)
	assert.Equal(t, search, d)
	search, err = GetNodeByPath("TestSearchByPath/A////B")
	runAsserts(t, d, err)
	assert.Equal(t, search, b)
	search, err = GetNodeByPath("TestSearchByPath/A/B///")
	runAsserts(t, d, err)
	assert.Equal(t, search, b)

	// Bad
	search, err = GetNodeByPath("")
	assert.EqualError(t, err, "could not find node for path ''")
	assert.Nil(t, search)
	search, err = GetNodeByPath("TestSearchByPath/A/B/C_2")
	assert.EqualError(t, err, "could not find node for path 'TestSearchByPath/A/B/C_2'")
	assert.Nil(t, search)

	err = EndTiming()
	assert.NoError(t, err)
}

func TestAddByPath(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 1)
	runAsserts(t, a, err)
	ts, err := StartMeasuringEventByPath(t.Name()+"/A/B/C///", 3)
	runAsserts(t, ts, err)

	new_a, err := GetNodeByPath(t.Name() + "/A")
	runAsserts(t, new_a, err)
	assert.Equal(t, a, new_a)
	new_c, err := GetNodeByPath(t.Name() + "/A/B/C")
	runAsserts(t, new_c, err)
	assert.Equal(t, 3, new_c.ExpectedSteps)

	ts, err = StopMeasurementByPath(t.Name() + "/A/B/C")
	runAsserts(t, ts, err)
	assert.NotNil(t, new_c.EndTime)
	assert.GreaterOrEqual(t, new_c.ElapsedSeconds, 0.0)

	ts, err = StopMeasurementByPath("invalid/path")
	assert.EqualError(t, err, "could not find measurement 'invalid/path' by path")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	err = EndTiming()
	assert.NoError(t, err)
}

func TestWriteAndRecover(t *testing.T) {
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 0)
	runAsserts(t, a, err)
	b, err := StartMeasuringEvent("B", 0)
	runAsserts(t, b, err)
	c, err := StartMeasuringEvent("C", 0)
	runAsserts(t, c, err)
	err = EndTiming()
	assert.NoError(t, err)

	root_real := *root
	a_real := *a
	b_real := *b
	c_real := *c

	root2, err := ResumeTiming("./testout/" + t.Name() + ".json")
	runAsserts(t, root2, err)
	new_root, err := GetNodeByPath(t.Name())
	assert.NoError(t, err)
	new_a, err := GetNodeByPath(t.Name() + "/A")
	assert.NoError(t, err)
	new_b, err := GetNodeByPath(t.Name() + "/A/B")
	assert.NoError(t, err)
	new_c, err := GetNodeByPath(t.Name() + "/A/B/C")
	assert.NoError(t, err)
	assert.True(t, timestampHasEquivalentTiming(*new_root, root_real))
	assert.True(t, timestampHasEquivalentTiming(*new_a, a_real))
	assert.True(t, timestampHasEquivalentTiming(*new_b, b_real))
	assert.True(t, timestampHasEquivalentTiming(*new_c, c_real))
	err = EndTiming()
	assert.NoError(t, err)
}

var workerParentTS *TimeStamp

func worker(t *testing.T, wait *sync.WaitGroup, task string) {
	defer wait.Done()
	ts, err := StartMeasuringEventWithParent(workerParentTS, task, 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventWithParent(ts, "2", 0)
	runAsserts(t, ts, err)
	StopMeasurementSpecific(ts)
}

func TestWorkers(t *testing.T) {
	var wait sync.WaitGroup
	root, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, root, err)
	workerParentTS = root
	for _, task := range []string{"A", "B", "C", "D"} {
		wait.Add(1)
		go worker(t, &wait, task)

	}
	wait.Wait()
	ts, err := GetNodeByPath(t.Name() + "/A/2")
	runAsserts(t, ts, err)
	ts, err = GetNodeByPath(t.Name() + "/B/2")
	runAsserts(t, ts, err)
	ts, err = GetNodeByPath(t.Name() + "/C/2")
	runAsserts(t, ts, err)
	ts, err = GetNodeByPath(t.Name() + "/D/2")
	runAsserts(t, ts, err)
}

func TestRewriteMultipleTimes(t *testing.T) {
	now := time.Now()
	ts := TimeStamp{
		Name:          "1A",
		StartTime:     &now,
		EndTime:       nil,
		ExpectedSteps: 3,
	}
	fmt.Printf("ts: %+v \n", ts)

	err := jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	var ts1 TimeStamp
	err = jsonutils.ReadJSONFile("./testout/"+t.Name()+".json", &ts1)
	assert.NoError(t, err)
	if err != nil {
		return
	}
	fmt.Printf("ts1: %+v \n", ts1)

	// Some precision for time is always lost after we write to json for the first time, but the rest of the struct is the same.
	// assert.Equal(t, ts, ts1) // false

	err = jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts1)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	var ts2 TimeStamp
	err = jsonutils.ReadJSONFile("./testout/"+t.Name()+".json", &ts2)
	assert.NoError(t, err)
	if err != nil {
		return
	}
	fmt.Printf("ts2: %+v \n", ts2)

	// If we write json with a struct that was read from a json, rewriting it wouldn't change it anymore.
	assert.Equal(t, ts1, ts2)
}

func TestUpdateJson(t *testing.T) {
	now := time.Now()
	ts := TimeStamp{
		Name:          "1A",
		StartTime:     &now,
		EndTime:       nil,
		ExpectedSteps: 3,
	}
	fmt.Printf("ts: %+v \n", ts)

	err := jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps = append(ts.Steps, &TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	err = jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps[0].Steps = append(ts.Steps[0].Steps, &TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	err = jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}
}

// Test when we just initiliazed the TimeStamp object and request for progress,
// we will receive a 0.0 output.
func TestProgressZero(t *testing.T) {
	var ts TimeStamp
	assert.Nil(t, ts.StartTime)
	assert.Nil(t, ts.EndTime)
	assert.Equal(t, 0.0, ts.Progress())
}

// Test that when we give the TimeStamp object an endtime,
// the progress will be set to 1.0.
func TestProgressFull(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: &future}

	ts.StartTime = &now
	ts.EndTime = &future

	assert.Equal(t, 1.0, ts.Progress())
}

// Test that a TimeStamp object with 4 expected steps and
// 2 completed steps will return a progress of 0.5.
func TestProgressHalf(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil}

	ts.ExpectedSteps = 4
	ts.Steps = []*TimeStamp{
		{StartTime: &now, EndTime: &future},
		{StartTime: &now, EndTime: &future}}
	assert.Equal(t, 0.5, ts.Progress())
}

// Test when expectedSteps and actual steps don't align.
func TestProgressBadGuess(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil}

	ts.ExpectedSteps = 1
	ts.Steps = []*TimeStamp{
		{StartTime: &now, EndTime: &future},
		{StartTime: &now, EndTime: nil}}
	// Works fine, because here we set maxProgress = len(ts.Steps).
	assert.Equal(t, 0.5, ts.Progress())

	// Outputs true. Although all steps are done we did not assign endtime to the outmost layer.
	ts.Steps[1].EndTime = &future
	assert.Equal(t, 0.95, ts.Progress())

	// Now setting the endtime to the outmost layer marks that the progress is done.
	ts.EndTime = &future
	assert.Equal(t, 1.0, ts.Progress())
}

// Test if total progress is calculated correctly when there are nested layers.
func TestProgressNested(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2} // 1st layer has 2 steps
	ts.Steps = append(ts.Steps,
		&TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2}) // 1st step on 2nd layer has 2 steps
	ts.Steps[0].Steps = append(ts.Steps[0].Steps,
		&TimeStamp{StartTime: &now, EndTime: &future, ExpectedSteps: 0}) // 2nd step on 2nd layer has 0 steps and is already done
	assert.Equal(t, 0.25, ts.Progress())
}
