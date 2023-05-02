// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Timestamp data structure and utilities

package timestamp

import (
	"fmt"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/uidutils"
)

type TimeStamp struct {
	ID              int64      `json:"ID"`
	Name            string     `json:"Name"`
	StartTime       *time.Time `json:"StartTime"`
	EndTime         *time.Time `json:"EndTime"`
	ElapsedSeconds  float64    `json:"ElapsedSeconds"`
	ParentID        int64      `json:"ParentID"`
	parentTimestamp *TimeStamp
	subSteps        map[string]*TimeStamp
}

const (
	pathSeparator string = "/"
)

func (ts *TimeStamp) ElapsedTime() time.Duration {
	if ts.EndTime == nil {
		return time.Duration(-1)
	}
	return ts.EndTime.Sub(*ts.StartTime)
}

func (ts *TimeStamp) DisplayName() string {
	if ts == nil {
		return ""
	}
	return ts.parentTimestamp.DisplayName() + pathSeparator + ts.Name
}

func newTimeStamp(name string, parent *TimeStamp) (ts *TimeStamp, err error) {
	if strings.Contains(name, pathSeparator) {
		err = fmt.Errorf("Can't create a timestamp object with a path containing %s", pathSeparator)
		return
	}

	ts = &TimeStamp{ID: uidutils.NextUID(), Name: name, StartTime: nil, EndTime: nil, subSteps: make(map[string]*TimeStamp), ParentID: -1}
	if parent != nil {
		ts.parentTimestamp = parent
		ts.ParentID = parent.ID
	}
	return
}

func newTimeStampByPath(root *TimeStamp, path string) (ts *TimeStamp, err error) {
	components := strings.Split(path, pathSeparator)
	if components[0] != root.Name {
		err = fmt.Errorf("Timestamp root mismatch ('%s', expected '%s')", components[0], root.Name)
		return
	}
	parent, err := getTimeStampFromPath(root, components[:len(components)-1], 1)
	if err != nil {
		return &TimeStamp{}, err
	}
	ts, err = newTimeStamp(components[len(components)-1], parent)
	return
}

func getTimeStampFromPath(root *TimeStamp, path []string, nextIndex int) (ts *TimeStamp, err error) {
	if nextIndex == len(path) {
		return root, nil
	}
	nextNode, present := root.subSteps[path[nextIndex]]
	if !present {
		err = fmt.Errorf("Node at index %d does not exist in the path from root: %v", nextIndex, path)
	}
	return getTimeStampFromPath(nextNode, path, nextIndex+1)
}

func (ts *TimeStamp) addSubStep(subStep *TimeStamp) {
	ts.subSteps[subStep.Name] = subStep
	subStep.parentTimestamp = ts
	subStep.ParentID = ts.ID
}

func (ts *TimeStamp) complete(endTime time.Time) {
	ts.EndTime = &endTime
	ts.ElapsedSeconds = ts.ElapsedTime().Seconds()
}
