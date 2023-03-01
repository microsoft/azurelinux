// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Manages reading and writing of timing data for active tools.
// General flow should be as follows:
//
// Basic automatic stack based...
///
//    timestamp_v2.BeginTiming("tool", 4) //User readable tool name, and expected number of sub steps
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
)

var (
	StampMgr *TimeStampManager = nil // A shared TimeInfo object that is by default nil. Library will log an warning if the empty object is called.
)

const (
	writeCooldownMilliseconds = 1000 // How often to write data back to file
)

// A TimeStampManager tracks an active set of timing measurements, allowing nested sub-steps to be added easily. The root of the timing tree
// is stored in `root`. The most recent node added through StartMeasuringEvent() is recorded in `activeNode`.
type TimeStampManager struct {
	root               *TimeStamp // Root of the timing tree
	activeNode         *TimeStamp // Last automatically positioned node
	dataFilePath       string     // Path to the output .json file
	dataFileDescriptor *os.File   // Used to coordinate access to the file via flock
	lock               sync.Mutex // Mutex for controlling writes to the data from cooperating threads (cooperating threads will share a file descriptor which means they can't use flock)
	isAtomic           bool       // This manager is operating in exclusive mode, no other manager may edit its file while it exists
	lastUpdate         time.Time  // When was the data last writtent to file
	shouldWrite        bool       // Should we actually write to file next time we try
}

// newStampMgr creates a new instance of the global stamp manager object with a root timing node `rootNode`. The root node may
//	already contain timing information and nested steps if resuming from disk.
//
//	The currently active node will always point to the root node upon creation, regardless of any pre-existing data branching from the root.
func newStampMgr(rootNode *TimeStamp, outputFilePath string, outputFileDescriptor *os.File, atomicMode bool) (newMgr *TimeStampManager) {
	newMgr = &TimeStampManager{
		dataFilePath:       outputFilePath,
		dataFileDescriptor: outputFileDescriptor,
		root:               rootNode,
		isAtomic:           atomicMode,
		shouldWrite:        true,
		lastUpdate:         time.Now(),
	}
	newMgr.activeNode = newMgr.root
	return
}

func ensureNoManager() (err error) {
	if StampMgr != nil {
		err = fmt.Errorf("already recording timing data for a tool into file (%s)", StampMgr.dataFilePath)
		failsafeLoggerWarnf(err.Error())
	}
	return
}

func ensureExistsManager() (err error) {
	if StampMgr == nil {
		err = fmt.Errorf("timestamping not initialized yet, can't record data")
		failsafeLoggerWarnf(err.Error())
	}
	return
}

// establishWriteLocks checks if a write should be performed, and locks the file if so
func (mgr *TimeStampManager) establishWriteLocks() (err error) {
	mgr.lock.Lock()

	// Check if we should attempt to write to disk now. updateFile() will reset this flag after
	// a successful write.
	if !mgr.shouldWrite {
		cooldown := time.Duration(writeCooldownMilliseconds) * time.Millisecond
		mgr.shouldWrite = mgr.lastUpdate.Add(cooldown).Before(time.Now())
	}

	if mgr.shouldWrite {
		return ensureExclusiveFileLockOnFile(mgr.dataFileDescriptor)
	} else {
		return nil
	}
}

// releaseWriteLocks resets the write lock back to normal. If the manager is in atomic mode it will maintain exclusive rights to the lock.
func (mgr *TimeStampManager) releaseWriteLocks() (err error) {
	// If we are in atomic mode we will never release the file lock until the manager is torn down or the thread ends
	if !StampMgr.isAtomic {
		// Make sure we never try to write to disk without the lock established.
		mgr.shouldWrite = false
		err = relaxToSharedLock(StampMgr.dataFileDescriptor)
	}
	mgr.lock.Unlock()
	return
}

// updateFile will write the current state of the manager's timing data back to file. It expects the file to be locked prior to writing.
// The write may be skipped based on writeCooldownMilliseconds.
// Use FlushData() to explicitly write data back to disk immediately.
func (mgr *TimeStampManager) updateFile() {
	// mgr.shouldWrite is controlled by establishWriteLocks()
	if mgr.shouldWrite {
		err := jsonutils.WriteJSONDescriptor(mgr.dataFileDescriptor, &(mgr.root))
		if err != nil {
			failsafeLoggerWarnf("Failed to store timestamp data into file '%s': %s", mgr.dataFilePath, err)
		}
		mgr.dataFileDescriptor.Sync()
		if err != nil {
			failsafeLoggerWarnf("Failed to store timestamp data into file '%s': %s", mgr.dataFilePath, err)
		}
		mgr.lastUpdate = time.Now()
		mgr.shouldWrite = false
	}
}

// BeginTiming will begin collecting fresh timing data for a high level component 'toolName' into the file at `outputFile`.
// This function synchronizes with ReadTimingData(), ResumeTiming(), EndTiming() to ensure there is no data partially
// written to the file. Expected weight is used to inform the dashboarding tools how many substeps the root node is expecting to have.
// The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func BeginTiming(toolName, outputFile string, expectedWeight float64, atomicOperation bool) (node *TimeStamp, err error) {
	if err = ensureNoManager(); err != nil {
		return StampMgr.activeNode, err
	}

	// Create a file to write data to
	outFileDescriptor, err := os.OpenFile(outputFile, os.O_CREATE|os.O_RDWR, 0664)
	if err != nil {
		err = fmt.Errorf("unable to create file %s: %w", outputFile, err)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}
	// We will not close the file handle here unless there is an error, we will use it for synchronization going forwards.

	// We will keep a shared lock on this file until we are done with timing. Grab in exclusive mode for now while we initialize the file
	if err = ensureExclusiveFileLockOnFile(outFileDescriptor); err != nil {
		outFileDescriptor.Close()
		return &TimeStamp{}, err
	}

	// Create a new instance of the StampMgr global and initialize it with an empty root node.
	root, err := createTimeStamp(toolName, time.Now(), expectedWeight)
	if err != nil {
		err = fmt.Errorf("unable to initialize timing root %s: %w", toolName, err)
		failsafeLoggerWarnf(err.Error())
		// Need to release the lock and file before we fail out
		unlockFileLock(outFileDescriptor)
		outFileDescriptor.Close()
		return &TimeStamp{}, err
	}

	StampMgr = newStampMgr(root, outputFile, outFileDescriptor, atomicOperation)
	// We already have the flock, make sure to grab the mutex as well so we can gracefully unlock it later
	StampMgr.lock.Lock()
	StampMgr.updateFile()
	if err = StampMgr.releaseWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("could not begin timing: %w", err)
	}
	return StampMgr.activeNode, err
}

// ResumeTiming will begin appending timing data for a high level component 'toolName' into the file at `outputFile`.
// This function synchronizes with ReadTimingData(), BeginTiming(), EndTiming()  to ensure there is no data partially
// written to the file. The function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty
// timestamp object instead. This function will NOT update the currently active node, it will remain pointing to the root node.
func ResumeTiming(toolName, existingTimingFile string, createIfMissing bool, atomicOperation bool) (node *TimeStamp, err error) {
	var existingroot *TimeStamp = &TimeStamp{}

	if err = ensureNoManager(); err != nil {
		return StampMgr.activeNode, err
	}

	flags := os.O_RDWR
	if createIfMissing {
		flags |= os.O_CREATE
	}

	// Recover an existing timing
	outFileDescriptor, err := os.OpenFile(existingTimingFile, flags, 0664)
	if err != nil {
		err = fmt.Errorf("can't read existing timing file (%s): %w", existingTimingFile, err)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}
	// We will not close the file handle here unless there is an error, we will use it for synchronization going forwards.

	if err = ensureExclusiveFileLockOnFile(outFileDescriptor); err != nil {
		outFileDescriptor.Close()
		return &TimeStamp{}, err
	}

	replaceCorruptedData := false
	err = jsonutils.ReadJSONDescriptor(outFileDescriptor, existingroot)
	if err != nil {
		// JSON library doesn't use static errors, must check message for equivalence instead of errors.Is()
		if err.Error() == "unexpected end of JSON input" && createIfMissing {
			replaceCorruptedData = true
			err = nil
		} else {
			err = fmt.Errorf("can't recover existing timing data (%s): %w", existingTimingFile, err)
			failsafeLoggerWarnf(err.Error())

			// Need to release the lock and file before we fail out
			unlockFileLock(outFileDescriptor)
			outFileDescriptor.Close()
			return &TimeStamp{}, err
		}
	}

	if replaceCorruptedData {
		// We couldn't load the node from JSON, make a new one
		existingroot, err = createTimeStamp(toolName, time.Now(), 1)
		if err != nil {
			err = fmt.Errorf("unable to initialize timing root %s: %w", toolName, err)
			failsafeLoggerWarnf(err.Error())

			// Need to release the lock and file before we fail out
			unlockFileLock(outFileDescriptor)
			outFileDescriptor.Close()
			return &TimeStamp{}, err
		}
	} else {
		// We are keeping the node we loaded from JSON.
		existingroot.restoreNode()
	}

	StampMgr = newStampMgr(existingroot, existingTimingFile, outFileDescriptor, atomicOperation)
	// We already have the flock, make sure to grab the mutex as well so we can gracefully unlock it later
	StampMgr.lock.Lock()
	if err = StampMgr.releaseWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("could not resume timing: %w", err)
	}
	return StampMgr.activeNode, err
}

// ReadTimingData will read out any existing timing data contained in the json file. This function synchronizes with
// BeginTiming(), ResumeTiming(), EndTiming() to ensure there is no data partially written to the file. The tool will NEVER return
// a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
// This function is read-only and will not affect the currently active StampMgr instance in any way. The  Manager does not
// need to be started to call this function.
func ReadTimingData(existingTimingFile string) (node *TimeStamp, err error) {
	var existingroot TimeStamp
	// Recover an existing timing
	file, err := os.Open(existingTimingFile)
	if err != nil {
		err = fmt.Errorf("can't read existing timing file (%s): %w", existingTimingFile, err)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}
	defer file.Close()

	// We will hold a shared lock only while reading the data, then release it completely
	if err = waitOnFileLock(file, blockTimeMilliseconds, false); err != nil {
		return &TimeStamp{}, err
	}
	defer func() {
		if deferErr := unlockFileLock(file); deferErr != nil {
			failsafeLoggerErrorf("ReadTimingData: %s", deferErr.Error())
		}
	}()

	err = jsonutils.ReadJSONDescriptor(file, &existingroot)
	if err != nil {
		err = fmt.Errorf("can't recover existing timing data (%s): %w", existingTimingFile, err)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}
	existingroot.restoreNode()
	return &existingroot, nil
}

// End timing will finalize a set of measurements into the file used to start the measurements. Any nodes that are currently
// still incomplete will be recursively completed based on their parent's end time. This function synchronizes with
// ReadTimingData(), BeginTiming(), ResumeTiming()  to ensure there is no data partially written to the file. Timing
// may be picked back up again by calling ResumeTiming(), however the active timestamp node WILL be reset back to the root.
func EndTiming() (err error) {
	if err = ensureExistsManager(); err != nil {
		return err
	}

	// We are tearing down, flus any data now
	StampMgr.shouldWrite = true

	// Will manually tear down locks at the end of this function
	StampMgr.establishWriteLocks()

	// Clean up any dangling timing
	StampMgr.root.completeTimeStamp(time.Now())
	err = StampMgr.root.FinishAllMeasurements()
	if err != nil {
		failsafeLoggerWarnf(err.Error())
		return err
	}

	StampMgr.updateFile()

	// Completely releasing the file lock now.
	err = unlockFileLock(StampMgr.dataFileDescriptor)
	if err != nil {
		failsafeLoggerErrorf("EndTiming: %s", err.Error())
		return
	}
	StampMgr.dataFileDescriptor.Close()
	StampMgr.lock.Unlock()
	StampMgr = nil

	return
}

// StartMeasuringEvent will create and return a new sub-step under the currently active measurement (StampMgr.GetActiveTimeNode()
// will return this node). The new node will start recording time immediately. Expected steps may be used to inform the
// dashboarding tool how many nested substeps are to be expected, use 0 if unknown or there are no substeps. The name
// may not include the character "/" since that is used to parse path based timing commands. The function will return
// the newly created timestamp. This function will also update the currently active node in the manager. The function will
// NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StartMeasuringEvent(name string, expectedWeight float64) (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StartMeasuringEvent: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	currentParent := StampMgr.activeNode
	newNode, err := currentParent.addStep(name, time.Now(), expectedWeight)
	if err != nil {
		err = fmt.Errorf("failed to create a timestamp object '%s': %w", name, err)
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
func StartMeasuringEventWithParent(parent *TimeStamp, name string, expectedWeight float64) (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if parent == nil {
		err = fmt.Errorf("invalid timestamp parent, can't add sub-step '%s'", name)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StartMeasuringEventWithParent: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	node, err = parent.addStep(name, time.Now(), expectedWeight)
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
func StartMeasuringEventByPath(path string, expectedWeight float64) (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StartMeasuringEventByPath: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	path = strings.Trim(path, pathSeparator)
	pathComponents := strings.Split(path, pathSeparator)

	// Check the root first
	node = nil
	if pathComponents[0] != StampMgr.root.Name {
		err = fmt.Errorf("timestamp root miss-match ('%s', expected '%s')", pathComponents[0], StampMgr.root.Name)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}

	// Now loop through the tree and see if we can find a node, omitting the root entry
	cur := StampMgr.root
	for i, pathComponent := range pathComponents[1:] {
		// Convert A/B////C into A/B/C by skipping empty steps
		if pathComponent == "" {
			continue
		}
		next := cur.searchSubSteps(pathComponent)
		if next == nil {
			thisNodeExpectedWeight := 1.0
			// Set a default of 1 for expected weight except for the leaf node which is the (len -2)'th node
			if i == len(pathComponents)-2 {
				thisNodeExpectedWeight = expectedWeight
			}
			next, err = cur.addStep(pathComponent, time.Now(), thisNodeExpectedWeight)
			if err != nil {
				failsafeLoggerWarnf(err.Error())
				err = fmt.Errorf("failed to create a timestamp object '%s': %w", path, err)
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
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StopMeasurement: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	// We don't want to ever stop measuring the root until we call EndTiming().
	if StampMgr.activeNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		failsafeLoggerWarnf(err.Error())
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
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StopMeasurementSpecific: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	// We don't want to ever stop measuring the root until we call EndTiming().
	if currentNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		failsafeLoggerWarnf(err.Error())
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

// pathSearchInternal checks if a node exists based  on a path like '/Path/To/Time Stamp'.
// The manager lock should be held when running this code.
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

// StopMeasurementByPath behaves similarly to StopMeasurement() except instead of completing the currently active node,
// it will first search for a node based on a path. If the currently active node matches this, the function WILL update
// the managers active node. Will return the (possibly updated) active node. The function will NEVER return a nil
// TimeStamp pointer, in event of an error it will return an empty timestamp object instead.
func StopMeasurementByPath(path string) (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	if err = StampMgr.establishWriteLocks(); err != nil {
		return &TimeStamp{}, fmt.Errorf("failed StopMeasurementByPath: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	currentNode := pathSearchInternal(path)
	if currentNode == nil {
		err = fmt.Errorf("could not find measurement '%s' by path", path)
		failsafeLoggerWarnf(err.Error())
		return &TimeStamp{}, err
	}

	// We don't want to ever stop measuring the root until we call EndTiming().
	if currentNode == StampMgr.root {
		err = fmt.Errorf("can't stop measuring the root timestamp '%s', call EndTiming() instead", StampMgr.root.Name)
		failsafeLoggerWarnf(err.Error())
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

// FlushData triggers a manual dump of data to disk if possible.
func FlushData() (err error) {
	if err := ensureExistsManager(); err != nil {
		return err
	}

	StampMgr.shouldWrite = true

	if err = StampMgr.establishWriteLocks(); err != nil {
		return fmt.Errorf("failed FlushData: %w", err)
	}
	defer StampMgr.releaseWriteLocks()

	StampMgr.updateFile()
	return
}

// GetActiveTimeNode returns the node that should next have sub-steps added to it for single threaded operations. The
// function will NEVER return a nil TimeStamp pointer, in event of an error it will return an empty timestamp object
// instead.
func GetActiveTimeNode() (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	// We should already have a shared flock, just grab the mutex to read
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	return StampMgr.activeNode, err
}

// GetNodeByPath returns the node that matches the path passed in. The function will NEVER return a nil TimeStamp pointer,
// in event of an error it will return an empty timestamp object instead.
func GetNodeByPath(path string) (node *TimeStamp, err error) {
	if err = ensureExistsManager(); err != nil {
		return &TimeStamp{}, err
	}

	// We should already have a shared flock, just grab the mutex to read
	StampMgr.lock.Lock()
	defer StampMgr.lock.Unlock()

	node = pathSearchInternal(path)

	if node == nil {
		err = fmt.Errorf("could not find node for path '%s'", path)
	}
	return
}
