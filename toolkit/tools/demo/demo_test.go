// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package demo

import (
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
