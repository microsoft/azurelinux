// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package timestamp

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

type EventType int

const (
	EventStart EventType = iota
	EventStop
)

const (
	writeCooldownMilliseconds = 1000 // How often to write data back to file
)

var (
	timestampMgr *TimeStampManager = nil
	initOnce     sync.Once
)

type TimeStampRecord struct {
	EventType EventType `json:"EventType"`
	*TimeStamp
	time time.Time
}

// The write manager is responsible for holding a write buffer and flushing it to file
// periodically. It is supposed to be running in a separate goroutine so the main build
// process performance is not affected.
type TimeStampWriteManager struct {
	filePath       string
	fileDescriptor *os.File
	writeBuffer    [][]byte
	lastWrite      time.Time
}

// The read manager is responsible for holding an in-memory data structure for the timestamps,
// starting from the root node. Read manager provides interface for querying the current state
// of the timestamps
type TimeStampReadManager struct {
	root        *TimeStamp
	nodes       map[int64]*TimeStamp
	lastVisited *TimeStamp
}

// The TimeStampManager provides the main interface for actions taken on timestamp objects.
type TimeStampManager struct {
	EventQueue             chan *TimeStampRecord
	eventProcessorFinished chan bool
	TimeStampWriteManager
	TimeStampReadManager
}

func newTimeStampWriteManager() *TimeStampWriteManager {
	return &TimeStampWriteManager{
		lastWrite: time.Now(),
	}
}

func newTimeStampReadManager() *TimeStampReadManager {
	return &TimeStampReadManager{
		root:        nil,
		nodes:       make(map[int64]*TimeStamp),
		lastVisited: nil,
	}
}

func newTimeStampManager() *TimeStampManager {
	return &TimeStampManager{
		EventQueue:             make(chan *TimeStampRecord, 256),
		eventProcessorFinished: make(chan bool, 1),
		TimeStampWriteManager:  *newTimeStampWriteManager(),
		TimeStampReadManager:   *newTimeStampReadManager(),
	}
}

func initTimeStampManager() {
	timestampMgr = newTimeStampManager()
}

func ensureManagerExists() error {
	if timestampMgr == nil {
		return fmt.Errorf("Timestamping has not been initialized. Make sure BeginTiming is called first.")
	}
	return nil
}

func BeginTiming(toolName, outputFile string) (*TimeStamp, error) {
	initOnce.Do(initTimeStampManager)

	outputFileDescriptor, err := os.OpenFile(outputFile, os.O_CREATE|os.O_WRONLY, 0664)
	if err != nil {
		err = fmt.Errorf("Unable to create file %s: %v", outputFile, err)
		logger.Log.Warn(err.Error())
		return &TimeStamp{}, err
	}

	timestampMgr.filePath = outputFile
	timestampMgr.fileDescriptor = outputFileDescriptor
	_, err = StartEvent(toolName, nil)
	if err != nil {
		err = fmt.Errorf("Unable to initialize root TimeStamp object for %s: %v", toolName, err)
		timestampMgr.eventProcessorFinished <- true
		FlushAndCleanUpResources()
		return &TimeStamp{}, err
	}

	go timestampMgr.processEventsInQueue()
	return timestampMgr.root, err
}

func ResumeTiming(toolName, outputFile string) error {
	initOnce.Do(initTimeStampManager)

	outputFileDescriptor, err := os.OpenFile(outputFile, os.O_RDWR, 0664)
	if err != nil {
		err = fmt.Errorf("Unable to open file %s: %v", outputFile, err)
		logger.Log.Warn(err.Error())
		return err
	}

	timestampMgr.filePath = outputFile
	timestampMgr.fileDescriptor = outputFileDescriptor
	timestampMgr.buildTreeFromFile(timestampMgr.fileDescriptor)
	timestampMgr.fileDescriptor.Seek(0, 2)

	go timestampMgr.processEventsInQueue()
	return nil
}

func CompleteTiming() (err error) {
	if err = ensureManagerExists(); err != nil {
		return
	}

	StopEvent(timestampMgr.root)
	FlushAndCleanUpResources()
	return
}

func FlushAndCleanUpResources() {
	close(timestampMgr.EventQueue)
	<-timestampMgr.eventProcessorFinished
	timestampMgr.flush()
	timestampMgr.fileDescriptor.Close()
}

func StartEvent(name string, parentTS *TimeStamp) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	ts, err = newTimeStamp(name, parentTS)
	if err != nil {
		err = fmt.Errorf("Failed to create a timestamp object %s: %v", name, err)
		return &TimeStamp{}, err
	}
	timestampMgr.submitEvent(EventStart, ts)
	return
}

func StartEventByPath(path string) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	ts, err = newTimeStampByPath(timestampMgr.root, path)
	if err != nil {
		err = fmt.Errorf("Failed to create a timestamp object %s: %v", path, err)
		return &TimeStamp{}, err
	}
	timestampMgr.submitEvent(EventStart, ts)
	return
}

func StopEvent(ts *TimeStamp) (*TimeStamp, error) {
	if err := ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventStop, ts)
	return ts, nil
}

func StopEventByPath(path string) (ts *TimeStamp, err error) {
	if err = ensureManagerExists(); err != nil {
		return &TimeStamp{}, err
	}

	components := strings.Split(path, pathSeparator)
	if components[0] != timestampMgr.root.Name {
		err = fmt.Errorf("Timestamp root mismatch ('%s', expected '%s')", components[0], timestampMgr.root.Name)
		return
	}
	ts, err = getTimeStampFromPath(timestampMgr.root, components, 1)
	if err != nil {
		return &TimeStamp{}, err
	}

	timestampMgr.submitEvent(EventStop, ts)
	return
}

func (mgr *TimeStampManager) submitEvent(eventType EventType, ts *TimeStamp) {
	mgr.EventQueue <- &TimeStampRecord{EventType: eventType, TimeStamp: ts, time: time.Now()}
}

func (mgr *TimeStampManager) processEventsInQueue() {
	for event := range mgr.EventQueue {
		mgr.updateRead(event)
		mgr.writeToFile(event)
	}
	mgr.eventProcessorFinished <- true
}

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
			if mgr.lastVisited.ID == ts.ParentID {
				mgr.lastVisited = ts
			}
		}
	case EventStop:
		ts := mgr.nodes[record.ID]
		ts.complete(record.time)
		if record.EventType == EventStop && ts.ID == mgr.lastVisited.ID {
			mgr.lastVisited = ts.parentTimestamp
		}
	}
	return
}

func (readMgr *TimeStampReadManager) buildTreeFromFile(fd *os.File) (err error) {
	fd.Seek(0, 0)
	scanner := bufio.NewScanner(fd)
	for scanner.Scan() {
		var ts TimeStamp
		err = json.Unmarshal(scanner.Bytes(), &ts)
		if err != nil {
			logger.Log.Warnf("Error reading timestamp object from file %v", err)
			continue
		}
		readMgr.nodes[ts.ID] = &ts
		if readMgr.root == nil {
			readMgr.root = &ts
		} else {
			readMgr.nodes[ts.ParentID].addSubStep(&ts)
		}
	}
	if err = scanner.Err(); err != nil {
		logger.Log.Warnf("Error rebuilding timestamp tree from file %v", err)
		return
	}
	return
}
