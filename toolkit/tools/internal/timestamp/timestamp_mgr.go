// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Manages reading and writing of timing data for active tools
// General flow should be as folllows:
//
// Basic automatic stack based:
//
//  timestamp.BeginTiming("tool", "/path/to/output/file.jsonl")
//  timestamp.StartEvent("step-A", nil)                 // starts recording step-A
//    ...
//    timestamp.StartEvent("sub-step-of-step-A", nil)   // starts recording sub-step-of-step-A
//    timestamp.StopEvent(nil)                          // stops recording sub-step-of-step-A
//    ...
//  timestamp.StopEvent(nil)                            // stops recording step-A
//  timestamp.CompleteTiming()
//
// Advanced handling for workers:
//
//  func worker(parent *TimeStamp, task string) {
//    ts, _ := timestamp.StartEvent(task, parent)             // starts recording "tool/scheduler/<task>"
//    defer timestamp.StopEvent(ts)
//  }
//
//  schedulerTS, _ := timestamp.StartEvent("scheduler", nil   // starts recording "tool/scheduler"
//  defer timestamp.StopEvent(schedulerTS)                    // stops recording "tool/scheduler" later
//  for task := range allTasks {
//    go worker(schedulerTS, task)                            // each worker will add a substep under "tool/scheduler"
//  }

package timestamp

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"os"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

type EventType int

// Types of event for a timestamped step. E.g start, stop
const (
	EventStart EventType = iota
	EventStop
	EventPause
	EventResume
)

const (
	writeCooldownMilliseconds = 1000          // How often to write data back to file
	maxID                     = math.MaxInt64 // max value to use for timestamp ID
)

var (
	timestampMgr *TimeStampManager = nil
)

// Represents an event during recording of a timestamped step
type TimeStampRecord struct {
	EventType EventType `json:"EventType"`
	*TimeStamp
	time time.Time
}

// The write manager is responsible for holding a write buffer and flushing it to file periodically. It is supposed
// to be running in a separate goroutine so the main build process performance is not affected.
type TimeStampWriteManager struct {
	filePath       string    // absolute path to the file recording timestamp events
	fileDescriptor *os.File  // file descriptor of the file to write to
	writeBuffer    [][]byte  // write buffer, each element in the buffer represents a single line
	lastWrite      time.Time // last time the buffer is flushed to disk
}

// The read manager is responsible for holding an in-memory data structure for the timestamps, starting from the root
// node. Read manager provides interface for querying the current state of the timestamps.
type TimeStampReadManager struct {
	root        *TimeStamp           // root timestamp, usually represents the tool being tracked
	nodes       map[int64]*TimeStamp // map of timestamp ID -> timestamp object for fast access
	lastVisited *TimeStamp           // helper pointer, useful for providing easy-to-use interface
}

// The TimeStampManager provides the main interface for actions taken on timestamp objects.
type TimeStampManager struct {
	EventQueue             chan *TimeStampRecord // events to be processed and recorded to file
	eventProcessorFinished chan bool             // signal to terminate the processor when no more events will be added to queue
	currentMaxID           int64

	TimeStampWriteManager // interface to handle all file writing
	TimeStampReadManager  // interface to handle all in-memory structures
}

// Initializes a new write manager object
func newTimeStampWriteManager() *TimeStampWriteManager {
	return &TimeStampWriteManager{
		lastWrite: time.Now(),
	}
}

// Initializes a new read manager object
func newTimeStampReadManager() *TimeStampReadManager {
	return &TimeStampReadManager{
		root:        nil,
		nodes:       make(map[int64]*TimeStamp),
		lastVisited: nil,
	}
}

// Initializes a new manager object
func newTimeStampManager() *TimeStampManager {
	return &TimeStampManager{
		EventQueue:             make(chan *TimeStampRecord, 256),
		eventProcessorFinished: make(chan bool, 1),
		TimeStampWriteManager:  *newTimeStampWriteManager(),
		TimeStampReadManager:   *newTimeStampReadManager(),
	}
}

// Initializes the global timestamp manager of the module
func initTimeStampManager() {
	timestampMgr = newTimeStampManager()
}

func ensureManagerExists() error {
	if timestampMgr == nil {
		return errors.New("timestamping has not been initialized. Make sure BeginTiming is called first")
	}
	return nil
}

// Begins collecting timing data for a high level component 'toolName' into the file at 'outputFile'
func BeginTiming(toolName, outputFile string) (*TimeStamp, error) {
	if outputFile == "" {
		err := fmt.Errorf("timestamp output file is not specified, the feature will be turned off for %s", toolName)
		logger.Log.Info(err.Error())
		return &TimeStamp{}, err
	}

	initTimeStampManager()

	outputFileDescriptor, err := os.OpenFile(outputFile, os.O_CREATE|os.O_WRONLY, 0664)
	if err != nil {
		err = fmt.Errorf("unable to create file %s: %v", outputFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}

	timestampMgr.filePath = outputFile
	timestampMgr.fileDescriptor = outputFileDescriptor
	_, err = StartEvent(toolName, nil)
	if err != nil {
		err = fmt.Errorf("unable to initialize root TimeStamp object for %s: %v", toolName, err)
		logger.Log.Warn(err.Error())
		timestampMgr.eventProcessorFinished <- true
		FlushAndCleanUpResources()
		return &TimeStamp{}, err
	}

	go timestampMgr.processEventsInQueue()
	logger.Log.Debugf("Begin recording timestamp for %s", toolName)
	return timestampMgr.root, err
}

// Begins appending timing data for a high level component 'toolName' into the file at 'outputFile'
func ResumeTiming(toolName, outputFile string) error {
	if outputFile == "" {
		err := fmt.Errorf("timestamp output file is not specified, the feature will be turned off for %s", toolName)
		logger.Log.Info(err.Error())
		return err
	}

	initTimeStampManager()

	outputFileDescriptor, err := os.OpenFile(outputFile, os.O_RDWR, 0664)
	if err != nil {
		err = fmt.Errorf("unable to open file %s: %v", outputFile, err)
		logger.Log.Warn(err.Error())
		return err
	}

	timestampMgr.filePath = outputFile
	timestampMgr.fileDescriptor = outputFileDescriptor
	timestampMgr.buildTreeFromFile()
	timestampMgr.fileDescriptor.Seek(0, 2)

	go timestampMgr.processEventsInQueue()
	logger.Log.Debugf("Resume recording timestamp for %s", toolName)
	return nil
}

// Marks the end of collecting timing data. Perform any cleanup needed by the timestamp manager object
func CompleteTiming() (err error) {
	if err = ensureManagerExists(); err != nil {
		return
	}

	StopEvent(timestampMgr.root)
	FlushAndCleanUpResources()
	logger.Log.Debugf("Completed recording timestamp, results written to %s", timestampMgr.filePath)
	timestampMgr = nil
	return
}

// Close the event queue, wait for the processor to finish and flush the remaining buffered data to disk
func FlushAndCleanUpResources() {
	close(timestampMgr.EventQueue)
	<-timestampMgr.eventProcessorFinished
	timestampMgr.flush()
	timestampMgr.fileDescriptor.Close()
}

// Add an event that marks the start of a timestamped step, if parentTS is nil, use lastVisited as parentTS
func StartEvent(name string, parentTS *TimeStamp) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	ts, err = newTimeStamp(name, parentTS)
	if err != nil {
		err = fmt.Errorf("failed to create a timestamp object %s: %v", name, err)
		return &TimeStamp{}, err
	}
	ts.ID = timestampMgr.nextID()
	timestampMgr.submitEvent(EventStart, ts)
	return
}

// Add an event that marks the start of a timestamped step using full name
func StartEventByPath(path string) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	ts, err = newTimeStampByPath(timestampMgr.root, path)
	ts.ID = timestampMgr.nextID()
	if err != nil {
		err = fmt.Errorf("failed to create a timestamp object %s: %v", path, err)
		return &TimeStamp{}, err
	}
	timestampMgr.submitEvent(EventStart, ts)
	return
}

// Add an event that marks the end of a timestamped step, if ts is nil, use lastVisited as ts
func StopEvent(ts *TimeStamp) (*TimeStamp, error) {
	if err := ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventStop, ts)
	return ts, nil
}

// Add an event that marks the end of a timestamped step using full name
func StopEventByPath(path string) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	components := strings.Split(path, pathSeparator)
	if components[0] != timestampMgr.root.Name {
		err = fmt.Errorf("timestamp root mismatch ('%s', expected '%s')", components[0], timestampMgr.root.Name)
		return
	}
	ts, err = getTimeStampFromPath(timestampMgr.root, components, 1)
	if err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventStop, ts)
	return
}

// Pause a step
func PauseEvent(ts *TimeStamp) (*TimeStamp, error) {
	if err := ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventPause, ts)
	return ts, nil
}

// Resume a step
func ResumeEvent(ts *TimeStamp) (*TimeStamp, error) {
	if err := ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventResume, ts)
	return ts, nil
}

func (mgr *TimeStampManager) nextID() (id int64) {
	if mgr.currentMaxID < maxID {
		id = mgr.currentMaxID
		mgr.currentMaxID++
		return
	}
	panic("Ran out of int64 to assign new ID")
}

func (mgr *TimeStampManager) setMaxID(maxID int64) {
	mgr.currentMaxID = maxID
}

// Submit a recorded event to event queue to be processed
func (mgr *TimeStampManager) submitEvent(eventType EventType, ts *TimeStamp) {
	mgr.EventQueue <- &TimeStampRecord{EventType: eventType, TimeStamp: ts, time: time.Now()}
}

// Process each event submitted to the queue by updating in-memory data structure and recording to file
func (mgr *TimeStampManager) processEventsInQueue() {
	for event := range mgr.EventQueue {
		mgr.updateRead(event)
		mgr.writeToFile(event)
	}
	mgr.eventProcessorFinished <- true
}

// Append a timestamp record to file, and periodically flush to disk
func (writeMgr *TimeStampWriteManager) writeToFile(record *TimeStampRecord) {
	outputBytes, err := json.Marshal(record)
	if err != nil {
		logger.Log.Warnf("Failed to marshal timestamp record: %v", err)
		return
	}
	writeMgr.writeBuffer = append(writeMgr.writeBuffer, outputBytes)

	cooldownDuration := time.Duration(writeCooldownMilliseconds) * time.Millisecond
	if writeMgr.lastWrite.Add(cooldownDuration).After(time.Now()) {
		return
	}

	writeMgr.flush()
	writeMgr.lastWrite = time.Now()
}

// Flush write buffer to disk
func (writeMgr *TimeStampWriteManager) flush() {
	for _, outputBytes := range writeMgr.writeBuffer {
		_, err := writeMgr.fileDescriptor.WriteString(string(outputBytes) + "\n")
		if err != nil {
			logger.Log.Warnf("Failed to write timestamp record to file %s: %v", writeMgr.filePath, err)
			continue
		}
	}
	err := writeMgr.fileDescriptor.Sync()
	if err != nil {
		logger.Log.Warnf("Failed to save file %s to disk: %v", writeMgr.filePath, err)
		return
	}
	writeMgr.writeBuffer = nil
}

// Update the timestamp tree for each event submitted to the event queue
func (mgr *TimeStampManager) updateRead(record *TimeStampRecord) {
	if record.TimeStamp == nil {
		record.TimeStamp = mgr.lastVisited
	}

	switch record.EventType {
	case EventStart:
		ts := record.TimeStamp
		ts.StartTime = &record.time
		mgr.nodes[ts.ID] = ts
		if record.parentTimestamp == nil {
			if mgr.lastVisited == nil {
				mgr.root = ts
			} else {
				mgr.lastVisited.addSubStep(ts)
			}
			mgr.lastVisited = ts
		} else {
			mgr.nodes[ts.ParentID].addSubStep(ts)
			if mgr.lastVisited != nil && mgr.lastVisited.ID == ts.ParentID {
				mgr.lastVisited = ts
			}
		}
	case EventStop, EventPause:
		ts := mgr.nodes[record.ID]
		ts.complete(record.time)
		if mgr.lastVisited != nil && ts.ID == mgr.lastVisited.ID {
			mgr.lastVisited = ts.parentTimestamp
		}
	case EventResume:
		ts := mgr.nodes[record.ID]
		ts.StartTime = &record.time
		ts.EndTime = nil
		if mgr.lastVisited != nil && mgr.lastVisited.ID == ts.ParentID {
			mgr.lastVisited = ts
		}
	}
}

// Read records written to a file and build a (partially) finished timestamp tree. This is useful for resuming
// partial recording progress
func (mgr *TimeStampManager) buildTreeFromFile() (err error) {
	mgr.fileDescriptor.Seek(0, 0)
	scanner := bufio.NewScanner(mgr.fileDescriptor)
	for scanner.Scan() {
		var ts TimeStamp
		err = json.Unmarshal(scanner.Bytes(), &ts)
		if err != nil {
			logger.Log.Warnf("Error reading timestamp object from file %v", err)
			continue
		}
		ts.subSteps = make(map[string]*TimeStamp)
		if ts.ID >= mgr.currentMaxID {
			mgr.setMaxID(ts.ID + 1)
		}
		mgr.nodes[ts.ID] = &ts
		if mgr.root == nil {
			mgr.root = &ts
		} else {
			mgr.nodes[ts.ParentID].addSubStep(&ts)
		}
	}
	if err = scanner.Err(); err != nil {
		logger.Log.Warnf("Error rebuilding timestamp tree from file %v", err)
		return
	}
	return
}
