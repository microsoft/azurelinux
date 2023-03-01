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
	// Roughly how many sub-steps do we expect this step to take, and how much
	// weight should they have.
	// We can use this to estimate the progress bar. If its wrong just use the actual
	// data we have as we go along. We assume the default weight per step is 1.
	ExpectedWeight float64 `json:"ExpectedWeight"`
	// Sub-steps. This timestamp reaches 100% when it has both a start & end time.
	// Otherwise, progress is calculated by summing each sub steps' Progress() * Weight / ExpectedWeight
	Steps []*TimeStamp `json:"Steps"`
	// How much relative weight this step has compared to others. Default is 1.0
	Weight float64 `json:"Weight"`

	parent   *TimeStamp
	finished bool
}

var (
	pathSeparator string = "/"
)

// createTimeStamp will validate input and create a new timestamp object with the requested values
func createTimeStamp(name string, startTime time.Time, expectedWeight float64) (newTS *TimeStamp, err error) {
	if strings.Contains(name, pathSeparator) {
		err = fmt.Errorf("can't create a timestamp object with a path containing %s", pathSeparator)
		return
	}

	if expectedWeight < 0 {
		err = fmt.Errorf("can't create a timestamp object with negative expected weight")
		return
	}

	ts := TimeStamp{Name: name, StartTime: &startTime, EndTime: nil, ExpectedWeight: expectedWeight, Weight: 1.0, ElapsedSeconds: -1, finished: false}
	return &ts, err
}

// AddStep adds a sub-step to this step .The expected weight of the new step will be used to estimate progress. '1.0' is a good default weight.
func (t *TimeStamp) addStep(name string, startTime time.Time, expectedWeight float64) (newTS *TimeStamp, err error) {
	if t.finished {
		return &TimeStamp{}, fmt.Errorf("parent timestamp has already completed measurement, can't add another substep")
	}

	newTS, err = createTimeStamp(name, startTime, expectedWeight)
	if err == nil {
		newTS.parent = t
		t.Steps = append(t.Steps, newTS)
	} else {
		newTS = &TimeStamp{}
	}
	return
}

// Marks the timestamp as completed. Will not allow additional sub-steps to be added after.
func (t *TimeStamp) completeTimeStamp(stopTime time.Time) {
	t.EndTime = &stopTime
	t.finished = true
	if t.StartTime != nil {
		t.ElapsedSeconds = t.EndTime.Sub(*t.StartTime).Round(time.Millisecond * 10).Seconds()
	}
}

func (node *TimeStamp) implementInheritMeasurements() *time.Time {
	for _, subStep := range node.Steps {
		candidate := subStep.implementInheritMeasurements()
		// Only makes sense to update if we have a measurement
		if candidate != nil {
			if node.EndTime == nil || candidate.After(*node.EndTime) {
				node.EndTime = candidate
			}
		}
	}
	return node.EndTime
}

// InheritMeasurements is the opposite of FinishAllMeasurements(). Each step will inherit the longest end time from the
// substeps nested at it.
func (node *TimeStamp) InheritMeasurements() (err error) {
	time := node.implementInheritMeasurements()
	if time == nil {
		err = fmt.Errorf("could not inherit time, no substeps are completed")
	}
	return
}

// SetWeight sets a steps relative weight to a custom value rather than the default 1.0. Progress is calculated based on the sum of all sub-steps' weights.
func (node *TimeStamp) SetWeight(weight float64) {
	if weight > 0 {
		node.Weight = weight
	}
}

// FinishAllMeasurements will recursively scan the timing data tree starting from `node` and ensure that all child nodes
// have a finish time. This finish time will be inherited from its parent if it is currently nil. A warning message will
// be printed about any such node that is found. The initial node passed in must either have a valid end time, or have a
// parent with one.
func (node *TimeStamp) FinishAllMeasurements() (err error) {
	if node.EndTime == nil {
		if node.parent.EndTime == nil {
			return fmt.Errorf("could not finalize orphaned times for node '%s' since it has no parent with an end time", node.Name)
		} else {
			failsafeLoggerWarnf("Found orphaned node '%s' with incomplete timing", node.Path())
			node.completeTimeStamp(*node.parent.EndTime)
		}
	}
	for _, subStep := range node.Steps {
		err = subStep.FinishAllMeasurements()
		if err != nil {
			return err
		}
	}
	return
}

func (t *TimeStamp) searchSubSteps(name string) (match *TimeStamp) {
	for _, subStep := range t.Steps {
		if name == subStep.Name {
			return subStep
		}
	}
	return nil
}

// restoreNode recursively re-establishes the child -> parent links for nodes read from disk
func (ts *TimeStamp) restoreNode() {
	ts.finished = ts.StartTime != nil && ts.EndTime != nil
	for _, child := range ts.Steps {
		child.parent = ts
		child.restoreNode()
	}
}

// Path returns the full path of the step
func (t *TimeStamp) Path() string {
	path := t.Name
	node := t
	for node.parent != nil {
		path = node.parent.Name + "/" + path
		node = node.parent
	}
	return path
}

// Progress estimates the progress of a step from  0.0 to 1.0 based on ExpectedWeight and currently
// completed substeps. It will never report above 95% until the current node is actually completed.
func (t *TimeStamp) Progress() float64 {
	progress := 0.0
	// We assume each sub-step has weight 1.0 unless we find otherwise.

	if t.StartTime == nil {
		return 0.0
	}

	if t.EndTime != nil {
		return 1.0
	}

	totalWeight := 0.0
	for _, step := range t.Steps {
		weight := math.Max(step.Weight, 0.0)
		totalWeight += weight
		progress += step.Progress() * weight
	}

	totalWeight = math.Max(totalWeight, t.ExpectedWeight)

	if totalWeight == 0.0 {
		return 0.0
	} else {
		// We don't want to mark complete until we have an end time for this
		//   step, just max it out at 95%
		return math.Min(progress/totalWeight, 0.95)
	}
}
