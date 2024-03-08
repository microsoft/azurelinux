// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Timestamp data structure and utilities

package timestamp

import (
	"fmt"
	"strings"
	"time"
)

type TimeStamp struct {
	ID              int64                 `json:"ID"`             // Unique ID for timestamp object
	Name            string                `json:"Name"`           // Name of the step
	StartTime       *time.Time            `json:"StartTime"`      // Start time of the step
	EndTime         *time.Time            `json:"EndTime"`        // End time of the step
	ElapsedSeconds  float64               `json:"ElapsedSeconds"` // Total elapsed time in seconds
	ParentID        int64                 `json:"ParentID"`       // ID of the parent step
	parentTimestamp *TimeStamp            // Pointer to parent step
	subSteps        map[string]*TimeStamp // Map of step name -> timestamp of substep
}

const (
	pathSeparator string = "/"
)

// Calculates the elapsed time of a step, returns -1 if the end time is not yet available
func (ts *TimeStamp) ElapsedTime() time.Duration {
	if ts.EndTime == nil {
		return time.Duration(-1)
	}
	return ts.EndTime.Sub(*ts.StartTime)
}

// Returns full name of the step starting from the root, i.e A/B/C
func (ts *TimeStamp) DisplayName() string {
	if ts == nil {
		return ""
	}
	if ts.parentTimestamp == nil {
		return ts.Name
	}
	return ts.parentTimestamp.DisplayName() + pathSeparator + ts.Name
}

// Creates a new timestamp object with optional parent ID
func newTimeStamp(name string, parent *TimeStamp) (ts *TimeStamp, err error) {
	if strings.Contains(name, pathSeparator) {
		err = fmt.Errorf("can't create a timestamp object with a path containing %s", pathSeparator)
		return
	}

	ts = &TimeStamp{Name: name, StartTime: nil, EndTime: nil, subSteps: make(map[string]*TimeStamp), ParentID: -1}
	if parent != nil {
		ts.parentTimestamp = parent
		ts.ParentID = parent.ID
	}
	return
}

// Creates a new timestamp object in the timestamp tree using full path name
func newTimeStampByPath(root *TimeStamp, path string) (ts *TimeStamp, err error) {
	components := strings.Split(path, pathSeparator)
	if components[0] != root.Name {
		err = fmt.Errorf("timestamp root mismatch ((%s), expected (%s))", components[0], root.Name)
		return
	}
	parent, err := getTimeStampFromPath(root, components[:len(components)-1], 1)
	if err != nil {
		return &TimeStamp{}, err
	}
	ts, err = newTimeStamp(components[len(components)-1], parent)
	return
}

// Returns timestamp node starting from the root using full path name
func getTimeStampFromPath(root *TimeStamp, path []string, nextIndex int) (ts *TimeStamp, err error) {
	if nextIndex == len(path) {
		return root, nil
	}
	nextNode, present := root.subSteps[path[nextIndex]]
	if !present {
		err = fmt.Errorf("node at index (%d) does not exist in the path from root: %v", nextIndex, path)
		return &TimeStamp{}, err
	}
	return getTimeStampFromPath(nextNode, path, nextIndex+1)
}

// Adds a substep to the current timestamp node
func (ts *TimeStamp) addSubStep(subStep *TimeStamp) {
	ts.subSteps[subStep.Name] = subStep
	subStep.parentTimestamp = ts
	subStep.ParentID = ts.ID
}

// Marks the end of a timestamped step with endTime
func (ts *TimeStamp) complete(endTime time.Time) {
	ts.EndTime = &endTime
	ts.ElapsedSeconds = ts.ElapsedTime().Seconds()
}
