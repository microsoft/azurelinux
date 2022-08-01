// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package demo

import (
	"math"
	"time"
)

type TimeStamp struct {
	Name string `json:"Name"`
	// Time we started this step, NIL if step hasn't started
	StartTime *time.Time `json:"StartTime"`
	// Time we ended this step, NIL if step hasn't ended
	EndTime *time.Time `json:"EndTime"`
	// Roughly how many sub-steps do we expect this step to take?
	// Can use this to estimate the progress bar. If its wrong... just update
	// it as we go along.
	ExpectedSteps int `json:"ExpectedSteps"`
	// Sub-steps. This timestamp reaches 100% when it has both a start & end time,
	// and all the sub steps are also completed.
	Steps []TimeStamp `json:"Steps"`
	// Maybe we can scale each sub-step somehow?
	// Weight float32 `json:"Weight"`
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
