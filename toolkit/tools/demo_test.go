// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package demo2

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

func PrintProgress(ts *TimeStamp) {
	println("Step", ts.Name, ":", ts.Progress())
	for _, step := range ts.Steps {
		if step.Progress() != 0.0 {
			PrintProgress(&step)
		}
	}

}

func TestProgressBarData(t *testing.T) {
	logger.InitStderrLog()

	var ts TimeStamp
	err := jsonutils.ReadJSONFile("./time.json", &ts)
	assert.NoError(t, err)
	if err != nil {
		return
	}

	PrintProgress(&ts)
}

func TestProgressZero(t *testing.T) {
	var ts TimeStamp
	assert.Nil(t, ts.StartTime)
	assert.Nil(t, ts.EndTime)
	assert.Equal(t, 0.0, ts.Progress())
}

func TestProgressFull(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: &future}

	ts.StartTime = &now
	ts.EndTime = &future

	assert.Equal(t, 1.0, ts.Progress())
}

func TestProgressHalf(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil}

	ts.ExpectedSteps = 4
	ts.Steps = []TimeStamp{{StartTime: &now, EndTime: &future},
		{StartTime: &now, EndTime: &future}}
	assert.Equal(t, 0.5, ts.Progress())
}

func TestProgressBadGuess(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil}

	ts.ExpectedSteps = 1
	ts.Steps = []TimeStamp{{StartTime: &now, EndTime: &future},
		{StartTime: &now, EndTime: nil}}
	assert.Equal(t, 0.5, ts.Progress())

	ts.Steps[1].EndTime = &future
	assert.Equal(t, 0.95, ts.Progress())

	ts.EndTime = &future
	assert.Equal(t, 1.0, ts.Progress())
}

func TestProgressNested(t *testing.T) {
	now := time.Now()
	future := now.Add(time.Minute * 5)
	ts := TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2}
	ts.Steps = append(ts.Steps,
		TimeStamp{StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	ts.Steps[0].Steps = append(ts.Steps[0].Steps,
		TimeStamp{StartTime: &now, EndTime: &future, ExpectedSteps: 0})
	assert.Equal(t, 0.25, ts.Progress())
}
