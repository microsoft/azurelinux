// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package timestamp_v2

import (
	"bytes"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func runAsserts(t *testing.T, ts *TimeStamp, err error) {
	// This is a helper function, report the caller's line number  instead of this function's
	t.Helper()
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
	files3, err := filepath.Glob("./testout/*.csv")
	if err != nil {
		logger.Log.Panicf("Failed to tidy up timestamp tests: '%s'", err.Error())
	}
	for _, file := range append(files1, append(files2, files3...)...) {
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
	//logger.SetStderrLogLevel("trace")
	ret := m.Run()

	// To preserve the output .json files for debugging, comment out the following line.
	cleanupFiles()
	os.Exit(ret)
}

// Test if we can read an existing json file, add lines to it, then write it out
func TestLoadDemoAndWrite(t *testing.T) {
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

func TestInheritMeasurement(t *testing.T) {
	root, err := createTimeStamp("name", time.Now(), 0)
	runAsserts(t, root, err)
	time.Sleep(50 * time.Millisecond)

	A, err := root.addStep("A", time.Now(), 0)
	runAsserts(t, A, err)
	time.Sleep(50 * time.Millisecond)

	err = root.InheritMeasurements()
	assert.EqualError(t, err, "could not inherit time, no substeps are completed")

	B, err := A.addStep("B", time.Now(), 0)
	runAsserts(t, B, err)
	B.completeTimeStamp(time.Now())

	err = root.InheritMeasurements()
	assert.NoError(t, err)
	assert.Equal(t, root.EndTime, B.EndTime)

	time.Sleep(50 * time.Millisecond)
	root.EndTime = nil
	A2, err := root.addStep("A2", time.Now(), 0)
	time.Sleep(50 * time.Millisecond)
	A2.completeTimeStamp(time.Now())
	runAsserts(t, A2, err)

	err = root.InheritMeasurements()
	assert.NoError(t, err)
	assert.Equal(t, root.EndTime, A2.EndTime)
}

func TestInvalidPathSeparator(t *testing.T) {
	ts, err := createTimeStamp("invalid/path/name", time.Now(), 0)
	assert.EqualError(t, err, "can't create a timestamp object with a path containing /")
	assert.Nil(t, ts)

	ts, err = BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("invalid/path/name", 0)
	assert.EqualError(t, err, "failed to create a timestamp object 'invalid/path/name': can't create a timestamp object with a path containing /")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestInvalidFilePathStart(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "/a/path/that/shouldnt/exist", 0, false)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "unable to create file /a/path/that/shouldnt/exist: open /a/path/that/shouldnt/exist: no such file or directory")
	assert.Nil(t, StampMgr)

	ts, err = ResumeTiming(t.Name(), "/a/path/that/shouldnt/exist", false, false)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't read existing timing file (/a/path/that/shouldnt/exist): open /a/path/that/shouldnt/exist: no such file or directory")
	assert.Nil(t, StampMgr)

	ts, err = ReadTimingData("/a/path/that/shouldnt/exist")
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't read existing timing file (/a/path/that/shouldnt/exist): open /a/path/that/shouldnt/exist: no such file or directory")
}

func TestCorruptFile(t *testing.T) {
	ts, err := ResumeTiming(t.Name(), "./testdata/corrupt.json", false, false)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't recover existing timing data (./testdata/corrupt.json): unexpected end of JSON input")
	assert.Nil(t, StampMgr)

	ts, err = ReadTimingData("./testdata/corrupt.json")
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't recover existing timing data (./testdata/corrupt.json): unexpected end of JSON input")
}

func TestInvalidExpected(t *testing.T) {
	ts, err := createTimeStamp("name", time.Now(), -10)
	assert.EqualError(t, err, "can't create a timestamp object with negative expected weight")
	assert.Nil(t, ts)

	ts, err = BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("name", -10)
	assert.EqualError(t, err, "failed to create a timestamp object 'name': can't create a timestamp object with negative expected weight")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	ts, err = StartMeasuringEventByPath(t.Name()+"/path", -10)
	assert.EqualError(t, err, "failed to create a timestamp object 'TestInvalidExpected/path': can't create a timestamp object with negative expected weight")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	err = EndTiming()
	assert.NoError(t, err)
}

func TestInvalidRoot(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventByPath("not_the_root"+"/path", 0)
	assert.EqualError(t, err, "timestamp root miss-match ('not_the_root', expected 'TestInvalidRoot')")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestCreateSubStep(t *testing.T) {
	root := &TimeStamp{Name: "Root", parent: nil}
	ts, err := root.addStep("1", time.Now(), 0)
	runAsserts(t, ts, err)
}

func TestCreateSubstepAlreadyDone(t *testing.T) {
	root := &TimeStamp{Name: "Root", parent: nil}
	root.completeTimeStamp(time.Now())
	ts, err := root.addStep("1", time.Now(), 0)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "parent timestamp has already completed measurement, can't add another substep")
}

func TestInitManager(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	time.Sleep(100 * time.Microsecond)
	err = EndTiming()
	assert.NoError(t, err)
}

func holdAtomicOrphan(t *testing.T, name, path string, millisToHold int) {
	ts, err := BeginTiming(name, path, 0, true)
	runAsserts(t, ts, err)
	orphanedStampMgr := StampMgr
	// Remove the current stamp manager so we can try to make a new one
	StampMgr = nil
	_ = orphanedStampMgr

	time.Sleep(time.Duration(millisToHold) * time.Millisecond)
}

func holdAtomicRelease(t *testing.T, name, path string, millisToHold int) {
	ts, err := BeginTiming(name, path, 0, true)
	runAsserts(t, ts, err)
	time.Sleep(time.Duration(millisToHold) * time.Millisecond)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestAtomic(t *testing.T) {
	go holdAtomicOrphan(t, t.Name(), "./testout/"+t.Name()+"_1.json", blockTimeMilliseconds*3)
	time.Sleep(blockTimeMilliseconds * 1 * time.Millisecond)
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+"_1.json", 0, true)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't lock timestamp file: failed to secure timing data lock after 250 milliseconds- resource temporarily unavailable")

	go holdAtomicRelease(t, t.Name(), "./testout/"+t.Name()+"_2.json", blockTimeMilliseconds*1)
	time.Sleep(blockTimeMilliseconds * 3 * time.Millisecond)
	ts, err = BeginTiming(t.Name(), "./testout/"+t.Name()+"_2.json", 0, true)
	runAsserts(t, ts, err)
	err = EndTiming()
	assert.NoError(t, err)
}

func holdLock(t *testing.T, path string, timeToHoldMillis int, exclusive bool) {
	logger.Log.Warnf("Routine Start")
	fd, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR, 0664)
	assert.NoError(t, err)
	err = waitOnFileLock(fd, 0, exclusive)
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

	err = waitOnFileLock(fd1, 0, true)
	assert.NoError(t, err)
	unlockFileLock(fd1)
	err = waitOnFileLock(fd2, 0, true)
	assert.NoError(t, err)
	fd2.Close()
}

func TestNilLock(t *testing.T) {
	err := waitOnFileLock(nil, 0, true)
	assert.EqualError(t, err, "failed to open timing data lock on nil file descriptor")
}

func TestLockingAlreadyLocked(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	fd1, err := os.Create(path)
	assert.NoError(t, err)
	fd2, err := os.Create(path)
	assert.NoError(t, err)

	err = waitOnFileLock(fd1, 0, true)
	defer unlockFileLock(fd1)
	assert.NoError(t, err)

	err = waitOnFileLock(fd2, 100, true)
	assert.EqualError(t, err, "failed to secure timing data lock after 100 milliseconds- resource temporarily unavailable")
	logger.Log.Warnf("Test end")
}

func TestGainsLock(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	fd1, err := os.Create(path)
	go holdLock(t, path, 300, true)
	time.Sleep(100 * time.Millisecond)

	assert.NoError(t, err)
	err = waitOnFileLock(fd1, 300, true)
	defer unlockFileLock(fd1)
	assert.NoError(t, err)
}

func TestAllowSharedLock(t *testing.T) {
	path := "./testout/" + t.Name() + ".lock"
	fd1, err := os.Create(path)
	assert.NoError(t, err)

	go holdLock(t, path, 300, false)
	time.Sleep(100 * time.Millisecond)

	err = waitOnFileLock(fd1, 0, false)
	assert.NoError(t, err)
}

func TestBlocksParallelExclusiveAccess(t *testing.T) {
	path := "./testout/" + t.Name() + ".json"

	go holdLock(t, path, blockTimeMilliseconds*3, true)
	time.Sleep(blockTimeMilliseconds * time.Millisecond)

	ts, err := BeginTiming(t.Name(), path, 0, false)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't lock timestamp file: failed to secure timing data lock after 250 milliseconds- resource temporarily unavailable")

	time.Sleep(blockTimeMilliseconds * 2 * time.Millisecond)
	go holdLock(t, path, blockTimeMilliseconds*3, false)
	time.Sleep(blockTimeMilliseconds * time.Millisecond)

	ts, err = BeginTiming(t.Name(), path, 0, false)
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't lock timestamp file: failed to secure timing data lock after 250 milliseconds- resource temporarily unavailable")

	_ = EndTiming()
}

func TestInitManagerDoubleStart(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	assert.EqualError(t, err, "already recording timing data for a tool into file (./testout/"+t.Name()+".json)")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, StampMgr.root)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestManagerBasic1(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M1", 0)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEvent("M2", 0)
	runAsserts(t, ts, err)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestManagerBasic2(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
}

func TestStartMeasurementWithoutStarting(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := StartMeasuringEvent("M1", 0)
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	ts, err = StartMeasuringEventWithParent(&TimeStamp{}, "parent", 0)
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	ts, err = StartMeasuringEventByPath("a/path", 0)
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestStopMeasurementWithoutStarting(t *testing.T) {
	ts, err := StopMeasurement()
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	ts, err = StopMeasurementSpecific(&TimeStamp{})
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	ts, err = StopMeasurementByPath("a/path")
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestNilParent(t *testing.T) {
	var nilTS *TimeStamp = nil
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventWithParent(nilTS, "nil", 0)
	assert.EqualError(t, err, "invalid timestamp parent, can't add sub-step 'nil'")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopRoot(t *testing.T) {
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})
}

func TestStopIsActiveNode(t *testing.T) {
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, root, err)
	time.Sleep(10 * time.Millisecond)
	err = EndTiming()
	assert.NoError(t, err)
	ts, err := ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", false, false)
	runAsserts(t, ts, err)
	newActive, err := GetActiveTimeNode()
	runAsserts(t, newActive, err)
	assert.True(t, timestampHasEquivalentTiming(*root, *newActive))
	err = EndTiming()
	assert.NoError(t, err)
}

func TestStopMiddleNode(t *testing.T) {
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	// root
	//  |
	//  A----------------
	//  |           |   |
	//  B1-------   B2  B3
	//  |   |   |
	//  C1  C2  C3

	// Stop B1, but leave the rest orphaned

	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	assert.NotEqual(t, -1.0, root.ElapsedSeconds)
	assert.Equal(t, root.EndTime, a.EndTime)
	assert.Equal(t, root.EndTime, b2.EndTime)
	assert.Equal(t, root.EndTime, b3.EndTime)
}

func TestGetActiveNode(t *testing.T) {
	EndTiming() // Make sure we aren't running a timing manager
	ts, err := GetActiveTimeNode()
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, &TimeStamp{}, ts)

	ts, err = BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	assert.EqualError(t, err, "timestamping not initialized yet, can't record data")
	assert.NotNil(t, ts)
	assert.Equal(t, &TimeStamp{}, ts)

	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, root, err)
	a, err := StartMeasuringEvent("A", 1)
	runAsserts(t, a, err)
	c, err := StartMeasuringEventByPath(t.Name()+"/A/B/C///", 3)
	runAsserts(t, c, err)
	assert.Equal(t, t.Name()+"/A/B/C", c.Path())

	new_a, err := GetNodeByPath(t.Name() + "/A")
	runAsserts(t, new_a, err)
	assert.Equal(t, a, new_a)
	new_c, err := GetNodeByPath(t.Name() + "/A/B/C")
	runAsserts(t, new_c, err)
	assert.Equal(t, 3.0, new_c.ExpectedWeight)

	ts, err := StopMeasurementByPath(t.Name() + "/A/B/C")
	runAsserts(t, ts, err)
	assert.NotNil(t, new_c.EndTime)
	assert.GreaterOrEqual(t, new_c.ElapsedSeconds, 0.0)

	ts, err = StopMeasurementByPath("invalid/path")
	assert.EqualError(t, err, "could not find measurement 'invalid/path' by path")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, &TimeStamp{})

	assert.Equal(t, c.ExpectedWeight, 3.0)

	err = EndTiming()
	assert.NoError(t, err)
}

func TestAddByPathMutipleRecordings(t *testing.T) {
	path := "./testout/" + t.Name() + ".json"
	ts, err := BeginTiming(t.Name(), path, 0, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventByPath(t.Name()+"/A", 0)
	runAsserts(t, ts, err)
	ts, err = StopMeasurementByPath(t.Name() + "/A")
	runAsserts(t, ts, err)

	//Need to manually clear the locks here since we didn't end timing normally
	FlushData()
	unlockFileLock(StampMgr.dataFileDescriptor)
	StampMgr = nil

	ts, err = ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", false, false)
	runAsserts(t, ts, err)
	ts, err = StartMeasuringEventByPath(t.Name()+"/B", 0)
	runAsserts(t, ts, err)
	// Intentionally don't stop /B

	//Need to manually clear the locks here since we didn't end timing normally
	FlushData()
	unlockFileLock(StampMgr.dataFileDescriptor)
	StampMgr = nil

	ts, err = ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", false, false)
	runAsserts(t, ts, err)
	c, err := StartMeasuringEventByPath(t.Name()+"/C", 0)
	runAsserts(t, c, err)
	ts, err = StopMeasurementByPath(t.Name() + "/C")
	runAsserts(t, ts, err)

	a, err := GetNodeByPath(t.Name() + "/A")
	runAsserts(t, a, err)
	b, err := GetNodeByPath(t.Name() + "/B")
	runAsserts(t, b, err)
	assert.True(t, a.finished)
	assert.False(t, b.finished)
	assert.True(t, c.finished)

	err = EndTiming()
	assert.NoError(t, err)
}

func TestWriteAndRecover(t *testing.T) {
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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

	root2, err := ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", false, false)
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

func TestResumeEmptyFile(t *testing.T) {
	ts, err := ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", false, false)
	assert.EqualError(t, err, "can't read existing timing file (./testout/TestResumeEmptyFile.json): open ./testout/TestResumeEmptyFile.json: no such file or directory")
	assert.NotNil(t, ts)
	assert.ErrorIs(t, err, fs.ErrNotExist)
}

func TestResumeEmptyFileCreate(t *testing.T) {
	ts, err := ResumeTiming(t.Name(), "./testout/"+t.Name()+".json", true, false)
	runAsserts(t, ts, err)
	err = EndTiming()
	assert.NoError(t, err)
}

func TestReadTiming(t *testing.T) {
	ts, err := ReadTimingData("./testdata/time.json")
	runAsserts(t, ts, err)
	assert.Equal(t, "1A", ts.Name)
}

func TestReadTimingMissing(t *testing.T) {
	ts, err := ReadTimingData("not_a_file.json")
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "can't read existing timing file (not_a_file.json): open not_a_file.json: no such file or directory")
}

func TestReadParallel(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	a, err := StartMeasuringEvent("A", 0)
	runAsserts(t, a, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)

	FlushData()

	ts, err = ReadTimingData("./testout/" + t.Name() + ".json")
	runAsserts(t, ts, err)

	assert.True(t, timestampHasEquivalentTiming(*a, *ts.Steps[0]))

	err = EndTiming()
	assert.NoError(t, err)
}

func TestFlush(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
	runAsserts(t, ts, err)
	err = FlushData()
	assert.NoError(t, err)

	err = EndTiming()
	assert.NoError(t, err)
}

func TestCheckExists(t *testing.T) {
	return
}

func TestReadBlocking(t *testing.T) {
	ts, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, true)
	runAsserts(t, ts, err)

	ts, err = ReadTimingData("./testout/" + t.Name() + ".json")
	assert.NotNil(t, ts)
	assert.EqualError(t, err, "failed to secure timing data lock after 250 milliseconds- resource temporarily unavailable")

	err = EndTiming()
	assert.NoError(t, err)

	ts, err = ReadTimingData("./testout/" + t.Name() + ".json")
	runAsserts(t, ts, err)

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
	root, err := BeginTiming(t.Name(), "./testout/"+t.Name()+".json", 0, false)
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
		Name:           "1A",
		StartTime:      &now,
		EndTime:        nil,
		ExpectedWeight: 3.0,
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
		Name:           "1A",
		StartTime:      &now,
		EndTime:        nil,
		ExpectedWeight: 3.0,
	}
	fmt.Printf("ts: %+v \n", ts)

	err := jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps = append(ts.Steps, &TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2})
	err = jsonutils.WriteJSONFile("./testout/"+t.Name()+".json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps[0].Steps = append(ts.Steps[0].Steps, &TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2})
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
	ts := TimeStamp{StartTime: &now, EndTime: nil, Weight: 1.0}

	ts.ExpectedWeight = 4.0
	ts.Steps = []*TimeStamp{
		{StartTime: &now, EndTime: &future, Weight: 1.0},
		{StartTime: &now, EndTime: &future, Weight: 1.0}}
	assert.Equal(t, 0.5, ts.Progress())
}

// Test when ExpectedWeight and actual steps don't align.
func TestProgressBadGuess(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil}

	ts.ExpectedWeight = 1.0
	ts.Steps = []*TimeStamp{
		{StartTime: &now, EndTime: &future, Weight: 1.0},
		{StartTime: &now, EndTime: nil, Weight: 1.0}}
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
	ts := TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2.0, Weight: 1.0} // 1st layer has 2 steps
	ts.Steps = append(ts.Steps,
		&TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2.0, Weight: 1.0}) // 1st step on 2nd layer has 2 steps
	ts.Steps[0].Steps = append(ts.Steps[0].Steps,
		&TimeStamp{StartTime: &now, EndTime: &future, ExpectedWeight: 0.0, Weight: 1.0}) // 2nd step on 2nd layer has 0 steps and is already done
	assert.Equal(t, 0.25, ts.Progress())
}

func TestWeights(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2.0, Weight: 1.0} // 1st layer has 2 steps
	ts.Steps = append(ts.Steps,
		&TimeStamp{StartTime: &now, EndTime: nil, ExpectedWeight: 2.0, Weight: 2}) // 1st step on 2nd layer has 2 steps
	ts.Steps[0].Steps = append(ts.Steps[0].Steps,
		&TimeStamp{StartTime: &now, EndTime: &future, ExpectedWeight: 0.0, Weight: 1}) // 2nd step on 2nd layer has 0 steps and is already done

	ts.Steps = append(ts.Steps,
		&TimeStamp{StartTime: &now, EndTime: &future, ExpectedWeight: 2.0, Weight: 6}) // 2st step on 2nd layer is done
	assert.Equal(t, (7.0 / 8.0), ts.Progress())
}

const expectedCSVOut = `tool,path_1,path_2,path_3,time
A,90.000000
A,B,66.000000
A,C,0.000000
A,C,D,0.000000
A,C,D,E,0.000000
A,C,D,E/F,44.000000
`

func TestCSV(t *testing.T) {
	//const YYYMMDDHHMMSS = "2022"

	files := []string{
		"/home/damcilva/temp/timestamp/build_mariner_toolchain.json",
		"/home/damcilva/temp/timestamp/chroot.json",
		"/home/damcilva/temp/timestamp/create_toolchain_in_container.json",
		"/home/damcilva/temp/timestamp/graph_cache.json",
		"/home/damcilva/temp/timestamp/grapher.json",
		"/home/damcilva/temp/timestamp/imageconfigvalidator.json",
		"/home/damcilva/temp/timestamp/imagepkgfetcher.json",
		"/home/damcilva/temp/timestamp/imager.json",
		"/home/damcilva/temp/timestamp/roast.json",
		"/home/damcilva/temp/timestamp/scheduler.json",
		"/home/damcilva/temp/timestamp/specreader.json",
		"/home/damcilva/temp/timestamp/srpm_packer.json",
		"/home/damcilva/temp/timestamp/srpm_toolchain_packer.json",
	}

	ts, err := ReadTimingData("./testdata/to_csv.json")
	runAsserts(t, ts, err)

	var buf bytes.Buffer
	ConvertToCSV([]*TimeStamp{ts}, &buf)

	assert.Equal(t, expectedCSVOut, buf.String())

	err = WriteToCSV([]*TimeStamp{ts}, "./testout/test.csv")
	assert.NoError(t, err)

	roots := []*TimeStamp{}
	for _, f := range files {
		root, err := ReadTimingData(f)
		runAsserts(t, root, err)
		roots = append(roots, root)
	}
	outName := filepath.Join(".", "test.csv")
	WriteToCSV(roots, outName)
}
