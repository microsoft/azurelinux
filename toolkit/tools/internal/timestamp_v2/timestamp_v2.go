// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package timestamp_v2

import (
	"fmt"
	"math"
	"strings"
	"time"
)

type TimeStamp struct {
	// Name of this step
	Name string `json:"Name"`
	// Time we started this step, NIL if step hasn't started
	StartTime *time.Time `json:"StartTime"`
	// Time we ended this step, NIL if step hasn't ended
	EndTime *time.Time `json:"EndTime"`
	// Calculated once completed, should be -1 if uninitialized. To the nearest 10 milliseconds
	ElapsedSeconds float64 `json:"ElapsedSeconds"`

	// Roughly how many sub-steps do we expect this step to take?
	// Can use this to estimate the progress bar. If its wrong... just update
	// it as we go along.
	ExpectedSteps int `json:"ExpectedSteps"`
	// Sub-steps. This timestamp reaches 100% when it has both a start & end time,
	// and all the sub steps are also completed.
	Steps []*TimeStamp `json:"Steps"`
	// Maybe we can scale each sub-step somehow?
	// Weight float32 `json:"Weight"`

	parent   *TimeStamp
	finished bool
}

var (
	pathSeparator string = "/"
)

// createTimeStamp will validate input and create a new timestamp object with the requested values
func createTimeStamp(name string, startTime time.Time, expectedSteps int) (newTS *TimeStamp, err error) {
	if strings.Contains(name, pathSeparator) {
		err = fmt.Errorf("can't create a timestamp object with a path containing %s", pathSeparator)
		return
	}

	if expectedSteps < 0 {
		err = fmt.Errorf("can't create a timestamp object with negative expected steps")
		return
	}

	ts := TimeStamp{Name: name, StartTime: &startTime, EndTime: nil, ExpectedSteps: expectedSteps, ElapsedSeconds: -1, finished: false}
	return &ts, err
}

// AddStep adds a sub-step to a specific parent step while guessing how many sub-steps there will be
func (t *TimeStamp) addStepWithExpected(name string, startTime time.Time, expectedSteps int) (newTS *TimeStamp, err error) {
	if t.finished {
		return &TimeStamp{}, fmt.Errorf("parent timestamp has already completed measurement, can't add another substep")
	}

	newTS, err = createTimeStamp(name, startTime, expectedSteps)
	if err == nil {
		newTS.parent = t
		t.Steps = append(t.Steps, newTS)
	} else {
		newTS = &TimeStamp{}
	}
	return
}

func (t *TimeStamp) completeTimeStamp(stopTime time.Time) {
	t.EndTime = &stopTime
	t.finished = true
	if t.StartTime != nil {
		t.ElapsedSeconds = t.EndTime.Sub(*t.StartTime).Round(time.Millisecond * 10).Seconds()
	}
}

func (t *TimeStamp) searchSubSteps(name string) (match *TimeStamp) {
	for _, subStep := range t.Steps {
		if name == subStep.Name {
			return subStep
		}
	}
	return nil
}

func (t *TimeStamp) Path() string {
	path := t.Name
	node := t
	for node.parent != nil {
		path = node.parent.Name + "/" + path
		node = node.parent
	}
	return path
}

func (t *TimeStamp) Progress() float64 {
	progress := 0.0
	maxProgress := math.Max(float64(t.ExpectedSteps), float64(len(t.Steps)))

	if t.StartTime == nil {
		return 0.0
	}

	if t.EndTime != nil {
		return 1.0
	}

	for _, step := range t.Steps {
		progress += step.Progress()
	}

	if maxProgress == 0.0 {
		return 0.0
	} else {
		// We don't want to mark complete until we have an end time for this
		//   step, just max it out at 95%
		return math.Min(progress/maxProgress, 0.95)
	}
}
