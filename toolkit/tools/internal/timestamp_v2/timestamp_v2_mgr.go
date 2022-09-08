// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Manages reading and writing of timing data for active tools.
// General flow should be as follows:
//
// Basic automatic stack based...
///
//    timestamp_v2.StartTiming("tool", 4) //User readable tool name, and expected number of sub steps
//    timestamp_v2.StampMgr.StartMeasuringEvent("step", 1)			//starts measuring 'tool/step'
//        ...
//        timestamp_v2.StampMgr.StartMeasuringEvent("substep", 1)	//starts measuring 'tool/step/substep'
//        defer timestamp_v2.StampMgr.StopMeasurement()				//stops measuring 'tool/step/substep' on return from function
//        ...
//    timestamp_v2.StampMgr.StopMeasurement()						//stops measuring 'tool/step'
//
// Advanced handling for workers etc...
//
//    func worker(parent *TimeStamp, task string) {
//        ts, _ := timestamp_v2.StampMgr.StartMeasuringEventWithParent(parent, task, 0)			// Records 'tool/scheduler/<TASK>'
//        defer timestamp_v2.StampMgr.StopMeasurementSpecific(ts)
//    }
//
//    schedulerTS,_ := timestamp_v2.StampMgr.StartMeasuringEvent("scheduler", getNumTasks())	//starts measuring 'tool/scheduler'
//    for task := range allTasks {
//        go worker(schedulerTS, task)															// Each worker will add a substep under 'tool/scheduler'
//    }
//    defer timestamp_v2.StampMgr.StopMeasurement()												//stops measuring 'tool/scheduler'
//
//
//
package timestamp_v2

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"golang.org/x/sys/unix"
)

var (
	StampMgr *TimeStampManager = nil // A shared TimeInfo object that is by default empty; will log an warning if the empty object is called.
)

// A TimeStampManager tracks an active set of timing measurements, allowing nested sub-steps to be added easily. The root of the timing tree
// is stored in `root`. The most recent node added through StartMeasuringEvent() is recorded in `activeNode`.
type TimeStampManager struct {
	root               *TimeStamp // Root of the timing tree
	activeNode         *TimeStamp // Last automatically positioned node
	dataFilePath       string     // Path to the output .json file
	dataFileDescriptor *os.File   // Used to coordinate access to the file via flock
	lock               sync.Mutex // Mutex for controlling writes to the data
}

// newStampMgr creates a new instance of the global stamp manager object with a root timing node `rootNode`. The root node may
//	already contain timing information and nested steps if resuming from disk.
//
//	The currently active node will always point to the root node upon creation, regardless of any pre-existing data branching from the root.
func newStampMgr(rootNode *TimeStamp, outputFilePath string, outputFileDescriptor *os.File) (newMgr *TimeStampManager) {
	newMgr = &TimeStampManager{
		dataFilePath:       outputFilePath,
		dataFileDescriptor: outputFileDescriptor,
		root:               rootNode,
	}
	newMgr.activeNode = newMgr.root
	return
}

// waitOnFileLock will synchronize access to the file `fileToLock` across processes/threads, blocking for at most `blockMillis` milliseconds.
// On managing to aquire the lock it will return a file descriptor which must be used to release the lock on the file using unlockFileLock().
// If the lock could not be acquired the function will return a nil file descriptor. The function will create a *.lock file adjacent to the
// locked file. Cleaning up this file if required is the responsibility of the caller.
func waitOnFileLock(flockFile *os.File, blockMillis int64) (err error) {
	lockMode := unix.LOCK_EX | unix.LOCK_NB
	if flockFile == nil {
		err = fmt.Errorf("failed to open timing data lock on nil file descriptor")
		return
	}

	start := time.Now()
	for {
		err = unix.Flock(int(flockFile.Fd()), lockMode)
		if err == nil || time.Since(start).Milliseconds() > blockMillis {
			break
		}
		time.Sleep(time.Millisecond * 5)
	}

	if err != nil {
		err = fmt.Errorf("failed to secure timing data lock after %d milliseconds- %w", blockMillis, err)
		flockFile.Close()
		flockFile = nil
	}

	return
}

// unlockFileLock will release the synchronization lock around a file. The file descriptor passed in should be created by calling
// waitOnFileLock().
func unlockFileLock(flockFile *os.File) {
	lockMode := unix.LOCK_UN

	err := unix.Flock(int(flockFile.Fd()), lockMode)
	if err != nil {
		logger.Log.Errorf("failed to release timing data lock - %s", err.Error())
		return
	}
}

// updateFile will write the current state of the manager's timing data back to file. It locks the file prior to writing.
func (mgr *TimeStampManager) updateFile() {
	err := waitOnFileLock(mgr.dataFileDescriptor, 100)

	if err != nil {
		logger.Log.Warnf("Failed to secure timestamp file '%s' ('%s')", mgr.dataFilePath, err)
	} else {
		defer unlockFileLock(mgr.dataFileDescriptor)
	}
	err = jsonutils.WriteJSONDescriptor(mgr.dataFileDescriptor, &(mgr.root))
	if err != nil && logger.Log != nil {
		logger.Log.Warnf("Failed to store timestamp data into file '%s' ('%s')", mgr.dataFilePath, err)
	}
}

// pathSearchInternal checks if a node exists based  on a path like '/Path/To/Time Stamp'.
// The manager lock MUST be held when running this code.
func pathSearchInternal(path string) (node *TimeStamp) {
	path = strings.Trim(path, pathSeparator)
	pathComponents := strings.Split(path, pathSeparator)
	// Check the root first
	cur := StampMgr.root
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
	return
}

// StartTiming will begin collecting fresh timing data for a high level component 'toolName' into the file at `outputFile`.
// This function synchronizes with ReadOnlyTimingData(), ResumeTiming(), EndTiming() to ensure there is no data partially
// written to the file. Expected steps is used to inform the dashboarding tools how many substeps the root node is expecting to have.
// The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StartTiming(toolName, outputFile string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr != nil {
		err = fmt.Errorf("already recording timing data for tool '%s' into file (%s)", toolName, outputFile)
		logger.Log.Warn(err.Error())
		return StampMgr.activeNode, err
	}

	// Create a new instance of the StampMgr global and initialize it with an empty root node.
	root, err := createTimeStamp(toolName, time.Now(), expectedSteps)
	if err != nil {
		err = fmt.Errorf("unable to initialize timing root %s: %s", toolName, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}

	// Create a file to write data to
	outFileDescriptor, err := os.OpenFile(outputFile, os.O_CREATE|os.O_RDWR, 0664)
	if err != nil {
		err = fmt.Errorf("unable to create file %s: %s", outputFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}

	StampMgr = newStampMgr(root, outputFile, outFileDescriptor)
	StampMgr.updateFile()
	return StampMgr.activeNode, err
}

// ReadOnlyTimingData will read out any existing timing data contained in the json file. This function synchronizes with
// StartTiming(), ResumeTiming(), EndTiming() to ensure there is no data partially written to the file. The tool will NEVER return
// a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
// This function is read-only and will not affect the currently active StampMgr instance in any way. The  Manager does not
// need to be started to call this function.
func ReadOnlyTimingData(existingTimingFile string) (node *TimeStamp, err error) {
	var existingroot TimeStamp
	// Recover an existing timing
	file, err := os.Open(existingTimingFile)
	if err != nil {
		err = fmt.Errorf("can't read timing file (%s): %w", existingTimingFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}
	defer file.Close()

	err = waitOnFileLock(file, 100)
	if err != nil {
		err = fmt.Errorf("can't lock timing file (%s): %w", existingTimingFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}
	defer unlockFileLock(file)

	err = jsonutils.ReadJSONDescriptor(file, &existingroot)
	if err != nil {
		err = fmt.Errorf("can't recover existing timing data (%s): %w", existingTimingFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}
	return &existingroot, nil
}

// ResumeTiming will begin appending timing data for a high level component 'toolName' into the file at `outputFile`.
// This function synchronizes with ReadOnlyTimingData(), StartTiming(), EndTiming()  to ensure there is no data partially
// written to the file. The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty
// timestamp object instead. This function will NOT update the currently active node, it will remain pointing to the root node.
func ResumeTiming(existingTimingFile string) (node *TimeStamp, err error) {
	var existingroot TimeStamp

	if StampMgr != nil {
		err = fmt.Errorf("already recording timing data for a tool into file (%s)", existingTimingFile)
		logger.Log.Warn(err.Error())
		return StampMgr.activeNode, err
	}

	// Recover an existing timing
	outFileDescriptor, err := os.OpenFile(existingTimingFile, os.O_CREATE|os.O_RDWR, 0664)
	if err != nil {
		err = fmt.Errorf("can't read timing file (%s)", existingTimingFile)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}
	// We will not close the file handle here, we will use it for synchronization going forwards.

	err = waitOnFileLock(outFileDescriptor, 100)
	if err != nil {
		err = fmt.Errorf("can't lock timing file (%s)", existingTimingFile)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}
	defer unlockFileLock(outFileDescriptor)

	err = jsonutils.ReadJSONDescriptor(outFileDescriptor, &existingroot)
	if err != nil {
		err = fmt.Errorf("can't recover existing timing data (%s): %w", existingTimingFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}

	StampMgr = newStampMgr(&existingroot, existingTimingFile, outFileDescriptor)
	return StampMgr.activeNode, err
}

// finishAllMeasurements will recursively scan the timing data tree starting from `node` and ensure that all child nodes
// have a finish time. This finish time will be inherited from its parent if it is currently nil. A warning message will
// be printed about any such node that is found. The initial node passed in must either have a valid end time, or have a
// parent with one.
func finishAllMeasurements(node *TimeStamp) (err error) {
	if node.EndTime == nil {
		if node.parent.EndTime == nil {
			return fmt.Errorf("could not finalize orphaned times for node '%s' since it has no parent with an end time", node.Name)
		} else {
			logger.Log.Warnf("Found orphaned node '%s' with incomplete timing", node.Path())
			node.completeTimeStamp(*node.parent.EndTime)
		}
	}
	for _, subStep := range node.Steps {
		err = finishAllMeasurements(subStep)
		if err != nil {
			return err
		}
	}
	return
}

// End timing will finalize a set of measurements into the file used to start the measurements. Any nodes that are currently
// still incomplete will be recursively completed based on their parent's end time. This function synchronizes with
// ReadOnlyTimingData(), StartTiming(), ResumeTiming()  to ensure there is no data partially written to the file. Timing
// may be picked back up again by calling ResumeTiming(), however the active timestamp node WILL be reset back to the root.
func EndTiming() (err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't stop timing")
		logger.Log.Warn(err.Error())
		return err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	StampMgr.root.completeTimeStamp(time.Now())
	err = finishAllMeasurements(StampMgr.root)
	if err != nil {
		logger.Log.Warn(err.Error())
		return err
	}

	StampMgr.updateFile()

	StampMgr.dataFileDescriptor.Close()
	StampMgr = nil

	return
}

// StartMeasuringEvent will create and return a new sub-step under the currently active measurement (StampMgr.GetActiveTimeNode()
// will return this node). The new node will start recording time immediately. Expected steps may be used to inform the
// dashboarding tool how many nested substeps are to be expected, use 0 if unknown or there are no substeps. The name
// may not include the character "/" since that is used to parse path based timing commands. The function will return
// the newly created timestamp. This function will also update the currently active node in the manager. The function will
// NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StartMeasuringEvent(name string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	currentParent := StampMgr.activeNode
	newNode, err := currentParent.addStepWithExpected(name, time.Now(), expectedSteps)
	if err != nil {
		err = fmt.Errorf("failed to create a timestamp object '%s': %s", name, err)
		return &TimeStamp{}, err
	}
	StampMgr.activeNode = newNode
	StampMgr.updateFile()
	return StampMgr.activeNode, err
}

// StartMeasuringEventWithParent behaves similarly to StartMeasuringEvent() with two differences:
// 1) Instead of creating the substep under the currently active node, it will create it under `parent` instead.
// 2) It will NEVER update the manager's currently active node, even if the parent is the active node.
// The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object
// instead.
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
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	node, err = parent.addStepWithExpected(name, time.Now(), expectedSteps)
	StampMgr.updateFile()
	return node, err
}

// StartMeasuringEventByPath behaves similarly to StartMeasuringEvent() with two differences:
// 1) Instead of creating the substep under the currently active node, it will create each missing node listed in the
//    path until it reaches the last node in the path. The root of the path MUST correspond the the root nodes name (the
//    name of the tool used to initialize the manager)
// 2) It will NEVER update the manager's currently active node, even if the parent is the active node.
// The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object
// instead.
func StartMeasuringEventByPath(path string, expectedSteps int) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't get search for node '%s'", path)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	path = strings.Trim(path, pathSeparator)
	pathComponents := strings.Split(path, pathSeparator)
	// Check the root first

	node = nil

	if pathComponents[0] != StampMgr.root.Name {
		err = fmt.Errorf("timestamp root miss-match ('%s', expected '%s')", pathComponents[0], StampMgr.root.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	// Now loop through the tree and see if we can find a node
	cur := StampMgr.root
	for i, pathComponent := range pathComponents[1:] {
		// Convert A/B////C into A/B/C by skipping empty steps
		if pathComponent == "" {
			continue
		}
		next := cur.searchSubSteps(pathComponent)
		if next == nil {
			thisNodeExpectedSteps := 0
			if i == len(pathComponents)-2 {
				thisNodeExpectedSteps = expectedSteps
			}
			next, err = cur.addStepWithExpected(pathComponent, time.Now(), thisNodeExpectedSteps)
			if err != nil {
				logger.Log.Warnf(err.Error())
				return &TimeStamp{}, err
			}
		}
		cur = next
	}
	StampMgr.updateFile()
	return cur, err
}

// StopMeasurement will stop StampMgr's currently active measurement and record the results. The active node will then
// become the stopped measurements' parent. This function will not stop measuring the root node, use EndTiming() instead.
// Will return the newly updated active node. The function will NEVER return a nil TimeStamp pointer, in event of an
// error it will return an empty timestamp object instead.
func StopMeasurement() (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data")
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	// We don't want to ever stop measuring the root until we call EndTiming().
	if StampMgr.activeNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		logger.Log.Warnf(err.Error())
		return StampMgr.root, err
	}

	StampMgr.activeNode.completeTimeStamp(time.Now())
	StampMgr.activeNode = StampMgr.activeNode.parent
	StampMgr.updateFile()

	return StampMgr.activeNode, err
}

// StopMeasurementSpecific behaves similarly to StopMeasurement() except instead of completing the currently active node,
// it will complete the specific node passed in. If the currently active node matches the node passed in, this function
// WILL update the managers active node. Will return the (possibly updated) active node. The function will NEVER return a
// nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StopMeasurementSpecific(currentNode *TimeStamp) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", currentNode.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	// We don't want to ever stop measuring the root until we call EndTiming().
	if currentNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	if currentNode == StampMgr.activeNode {
		StampMgr.activeNode.completeTimeStamp(time.Now())
		StampMgr.activeNode = StampMgr.activeNode.parent
	} else {
		currentNode.completeTimeStamp(time.Now())
	}
	StampMgr.updateFile()
	return StampMgr.activeNode, err
}

// StopMeasurementByPath behaves similarly to StopMeasurement() except instead of completing the currently active node,
// it will first search for a node based on a path. If the currently active node matches this, the function WILL update
// the managers active node. Will return the (possibly updated) active node. The function will NEVER return a nil
// TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StopMeasurementByPath(path string) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data for '%s'", path)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	currentNode := pathSearchInternal(path)
	if currentNode == nil {
		err = fmt.Errorf("could not find measurement '%s' by path", path)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	// We don't want to ever stop measuring the root until we call EndTiming().
	if currentNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}

	if currentNode == StampMgr.activeNode {
		StampMgr.activeNode.completeTimeStamp(time.Now())
		StampMgr.activeNode = StampMgr.activeNode.parent
	} else {
		currentNode.completeTimeStamp(time.Now())
	}
	StampMgr.updateFile()
	return StampMgr.activeNode, err
}

// GetActiveTimeNode returns the node that should next have sub-steps added to it for single threaded operations. The
// function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object
// instead.
func GetActiveTimeNode() (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't get active node")
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	return StampMgr.activeNode, err
}

// GetNodeByPath returns the node that matches the path passed in. The function will NEVER return a nil TimeStamp pointer,
// in event of an error it will return an empty timestamp object instead.
func GetNodeByPath(path string) (node *TimeStamp, err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't get search for node '%s'", path)
		logger.Log.Warnf(err.Error())
		return &TimeStamp{}, err
	}
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	node = pathSearchInternal(path)

	if node == nil {
		err = fmt.Errorf("could not find node for path '%s'", path)
	}
	return
}
