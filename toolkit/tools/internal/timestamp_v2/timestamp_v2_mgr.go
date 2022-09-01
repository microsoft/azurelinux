// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package timestamp_v2

import (
	"fmt"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	StampMgr *TimeStampManager = nil // A shared TimeInfo object that is by default empty; will log an warning if the empty object is called.
)

type TimeStampManager struct {
	Root         *TimeStamp
	ActiveNode   *TimeStamp
	DataFilePath string
}

func newStampMgr(rootNode *TimeStamp, outputFilePath string) (newMgr *TimeStampManager) {
	newMgr = &TimeStampManager{
		DataFilePath: outputFilePath,
		Root:         rootNode,
	}
	newMgr.ActiveNode = newMgr.Root
	return
}

func (mgr *TimeStampManager) updateFile() {
	err := jsonutils.WriteJSONFile(mgr.DataFilePath, &(mgr.Root))
	if err != nil && logger.Log != nil {
		logger.Log.Warnf("Failed to store timestamp data into file '%s' ('%s')", mgr.DataFilePath, err)
	}
}

func StartTiming(toolName, completePath string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr != nil {
		return StampMgr.ActiveNode, fmt.Errorf("already recording timing data for tool '%s' into file (%s)", toolName, completePath)
	}
	// Update the global object "StampMgr".
	root, err := createTimeStamp(toolName, time.Now(), expectedSteps)
	if err != nil {
		return &TimeStamp{}, fmt.Errorf("unable to create file %s: %s", completePath, err)
	}

	StampMgr = newStampMgr(root, completePath)
	StampMgr.updateFile()
	return StampMgr.ActiveNode, err
}

func EndTiming() (err error) {
	if StampMgr != nil {
		StampMgr.Root.completeTimeStamp(time.Now())
		StampMgr.updateFile()
		StampMgr = nil
	} else {
		err = fmt.Errorf("timestamping not initialized yet, can't stop timing")
		logger.Log.Warn(err.Error())
	}
	return
}

func StartMeasuringEvent(name string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	currentParent := StampMgr.ActiveNode
	newNode, err := currentParent.addStepWithExpected(name, time.Now(), expectedSteps)
	if err != nil {
		err = fmt.Errorf("failed to create a timestamp object '%s': %s", name, err)
		return &TimeStamp{}, err
	}
	StampMgr.ActiveNode = newNode
	StampMgr.updateFile()
	return StampMgr.ActiveNode, err
}

// NEVER updates active node
func StartMeasuringEventWithParent(parent *TimeStamp, name string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	if parent == nil {
		err = fmt.Errorf("invalid timestamp parent, can't add sub-step '%s'", name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	StampMgr.updateFile()
	return parent.addStepWithExpected(name, time.Now(), expectedSteps)
}

func StopMeasurement() (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data")
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	// We don't want to ever stop measuring the root until we call EndTiming().
	if StampMgr.ActiveNode == StampMgr.Root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.Root.Name)
		logger.Log.Warnf(err.Error())
		return StampMgr.Root, err
	}

	StampMgr.ActiveNode.completeTimeStamp(time.Now())
	StampMgr.ActiveNode = StampMgr.ActiveNode.parent

	StampMgr.updateFile()
	return StampMgr.ActiveNode, err
}

func StopMeasurementSpecific(currentNode *TimeStamp) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", currentNode.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	// We don't want to ever stop measuring the root until we call EndTiming().
	if currentNode == StampMgr.Root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.Root.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	if currentNode == StampMgr.ActiveNode {
		return StopMeasurement()
	}

	currentNode.completeTimeStamp(time.Now())
	StampMgr.updateFile()
	return StampMgr.ActiveNode, err
}

func GetActiveTimeNode() (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't get active node")
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	return StampMgr.ActiveNode, err
}

func GetNodeByPath(path string) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't get search for node '%s'", path)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	pathComponents := strings.Split(path, pathSeparator)
	// Check the root first
	cur := StampMgr.Root
	node = nil
	if pathComponents[0] == cur.Name {
		// Now loop through the tree and see if we can find a node
		for _, pathComponent := range pathComponents[1:] {
			// Convert A/B////C into A/B/C by skipping empty steps
			if pathComponent == "" {
				continue
			}
			cur = cur.searchSubSteps(pathComponent)
			if cur == nil {
				break
			}
		}

		node = cur
	}

	if node == nil {
		err = fmt.Errorf("could not find node for path '%s'", path)
	}
	return
}
