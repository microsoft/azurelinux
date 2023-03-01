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
	"encoding/csv"
	"fmt"
	"io"
	"math"
	"os"
	"sort"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	maxHierarchyLevel = 4
	header            = []string{"path", "time"}
)

type CSVTimeStamp struct {
	path            []string
	unaccountedTime string
}

func buildCSVOpbject(path string, time float64) (csvObj CSVTimeStamp) {
	pathComponents := strings.Split(path, "/")
	for i, p := range pathComponents {
		if i < maxHierarchyLevel {
			csvObj.path = append(csvObj.path, p)
		} else {
			// Just join all the paths together
			logger.Log.Warnf("Path too long: '%s", path)
			csvObj.path[maxHierarchyLevel-1] = csvObj.path[maxHierarchyLevel-1] + "/" + p
		}
	}
	csvObj.unaccountedTime = fmt.Sprintf("%f", time)
	return csvObj
}

func (csv CSVTimeStamp) format() []string {
	return append(csv.path, csv.unaccountedTime)
}

// convertNode will transform a tree into a set of CVS entries of the form: <PATH/OF/TIMESTAMP, TOTAL TIME>. Each node
// will be made up of a set of child nodes such that the sum of all child trees should equal the parent nodes total time.
// This does not map well to multithreaded flows, instead it shows single core data.
// Similar entires will be merged together (ie 'A/B,10' + 'A/B,20' will be a single entry of 'A/B,30')
func convertNode(node *TimeStamp, timingLookup map[string]float64) {
	accountedTime := 0.0
	for _, subStep := range node.Steps {
		convertNode(subStep, timingLookup)
		accountedTime += subStep.ElapsedSeconds
	}

	unaccountedSeconds := math.Max(0, node.ElapsedSeconds-accountedTime)
	timingLookup[node.Path()] = timingLookup[node.Path()] + unaccountedSeconds
}

func addHeader(csvWriter *csv.Writer) error {
	header := []string{}
	header = append(header, "tool")
	for i := 1; i < maxHierarchyLevel; i++ {
		header = append(header, "path_"+fmt.Sprintf("%d", i))
	}
	header = append(header, "time")
	return csvWriter.Write(header)
}

func writeInSortedOrder(csvWriter *csv.Writer, timingLookup map[string]float64) (err error) {
	sortedPaths := make([]string, 0, len(timingLookup))
	for path, _ := range timingLookup {
		sortedPaths = append(sortedPaths, path)
	}
	sort.Strings(sortedPaths)

	for _, path := range sortedPaths {
		err = csvWriter.Write(buildCSVOpbject(path, timingLookup[path]).format())
		if err != nil {
			return err
		}
	}
	return nil
}

func ConvertToCSV(roots []*TimeStamp, output io.Writer) (err error) {
	csvWriter := csv.NewWriter(output)
	defer csvWriter.Flush()
	err = addHeader(csvWriter)
	if err != nil {
		return err
	}

	timingLookup := map[string]float64{}
	for _, root := range roots {
		convertNode(root, timingLookup)
	}

	return writeInSortedOrder(csvWriter, timingLookup)
}

func WriteToCSV(roots []*TimeStamp, filepath string) (err error) {
	outFile, err := os.Create(filepath)
	if err != nil {
		return
	}
	defer outFile.Close()

	return ConvertToCSV(roots, outFile)
}
