// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package timestamp_v2

import (
	"fmt"
	"os"
	"path/filepath"
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

func cleanupFiles() {
	files, err := filepath.Glob("./testout/*.json")
	if err != nil {
		logger.Log.Panicf("Failed to tidy up timestamp tests: '%s'", err.Error())
	}
	for _, file := range files {
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

func TestInitManagerDoubleStart(t *testing.T) {
	ts, err := StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	runAsserts(t, ts, err)
	ts, err = StartTiming(t.Name(), "./testout/"+t.Name()+".json", 0)
	assert.EqualError(t, err, "already recording timing data for tool 'TestInitManagerDoubleStart' into file (./testout/"+t.Name()+".json)")
	assert.NotNil(t, ts)
	assert.Equal(t, ts, StampMgr.Root)
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
	progress := StampMgr.Root.Progress()
	assert.Equal(t, 2.0/3.0, progress)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	ts, err = StopMeasurement()
	runAsserts(t, ts, err)
	progress = StampMgr.Root.Progress()
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
	assert.Equal(t, ts, StampMgr.Root)

	assert.Equal(t, 0.95, StampMgr.Root.Progress())
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
