// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package demo

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

// Test if we can read an existing json file, add lines to it, then write it out
func TestLoadDemo(t *testing.T) {
	// Need to create logger since the json tools use it, will just
	// print to console for errors.
	logger.InitStderrLog()

	var timestamp TimeStamp
	err := jsonutils.ReadJSONFile("./time.json", &timestamp)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	now := time.Now()
	future := now.Add(time.Minute * 5)
	timestamp.StartTime = &now
	timestamp.EndTime = &future

	err = jsonutils.WriteJSONFile("./time_out.json", &timestamp)
	assert.NoError(t, err)
	if err != nil {
		return
	}
}

func TestRewriteMultipleTimes(t *testing.T) {
	logger.InitStderrLog()
	now := time.Now()
	ts := TimeStamp{
		Name:          "1A",
		StartTime:     &now,
		EndTime:       nil,
		ExpectedSteps: 3,
	}
	fmt.Printf("ts: %+v \n", ts)

	err := jsonutils.WriteJSONFile("./time_test_1.json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	var ts1 TimeStamp
	err = jsonutils.ReadJSONFile("./time_test_1.json", &ts1)
	assert.NoError(t, err)
	if err != nil {
		return
	}
	fmt.Printf("ts1: %+v \n", ts1)

	// Some precision for time is always lost after we write to json for the first time, but the rest of the struct is the same.
	// assert.Equal(t, ts, ts1) // false

	err = jsonutils.WriteJSONFile("./time_test_1.json", &ts1)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	var ts2 TimeStamp
	err = jsonutils.ReadJSONFile("./time_test_1.json", &ts2)
	assert.NoError(t, err)
	if err != nil {
		return
	}
	fmt.Printf("ts2: %+v \n", ts2)

	// If we write json with a struct that was read from a json, rewriting it wouldn't change it anymore.
	assert.Equal(t, ts1, ts2)
}

func TestUpdateJson(t *testing.T) {
	logger.InitStderrLog()
	now := time.Now()
	ts := TimeStamp{
		Name:          "1A",
		StartTime:     &now,
		EndTime:       nil,
		ExpectedSteps: 3,
	}
	fmt.Printf("ts: %+v \n", ts)

	err := jsonutils.WriteJSONFile("./time_test_1.json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps = append(ts.Steps, TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	err = jsonutils.WriteJSONFile("./time_test_2.json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	time.Sleep(time.Millisecond * 100)
	ts.Steps[0].Steps = append(ts.Steps[0].Steps, TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	err = jsonutils.WriteJSONFile("./time_test_1.json", &ts)
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
	ts.Steps = []TimeStamp{
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
	ts.Steps = []TimeStamp{
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
		TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2}) // 1st step on 2nd layer has 2 steps
	ts.Steps[0].Steps = append(ts.Steps[0].Steps,
		TimeStamp{StartTime: &now, EndTime: &future, ExpectedSteps: 0}) // 2nd step on 2nd layer has 0 steps and is already done
	assert.Equal(t, 0.25, ts.Progress())
}

func TestHomeDirs(t *testing.T) {
	currDir, err := os.Getwd()
	fmt.Printf(currDir)
	parentDir := filepath.Dir(currDir)
	fmt.Printf(parentDir)
	if err != nil {
		return
	}
}
