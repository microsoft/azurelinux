// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package main

import (
	"fmt"
	"math"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	// Shared TimeStamp struct.
	ts TimeStamp
)

type TimeStamp struct {
	// Name of this step
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

func main() {
	logger.InitStderrLog()
	now := time.Now()

	ts = TimeStamp{Name: "1A", StartTime: &now, EndTime: nil, ExpectedSteps: 3}

	err := jsonutils.WriteJSONFile("./time_test_1.json", &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}

	appendStep(&ts.Steps, 100, "2A", 2, "./time_test_2.json")
	// time.Sleep(time.Millisecond * 100)
	// ts.Steps = append(ts.Steps, TimeStamp{Name: "2A", StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	// err = jsonutils.WriteJSONFile("./time_test_2.json", &ts)
	// if err != nil {
	// 	fmt.Printf("unable to write to json file\n")
	// 	return
	// }
	
	appendStep(&ts.Steps[0].Steps, 100, "3A", 0, "./time_test_2.json")
	// time.Sleep(time.Millisecond * 100)
	// ts.Steps[0].Steps = append(ts.Steps[0].Steps, TimeStamp{Name: "3A", StartTime: &now, EndTime: nil, ExpectedSteps: 0})
	// err = jsonutils.WriteJSONFile("./time_test_2.json", &ts)
	// if err != nil {
	// 	fmt.Printf("unable to write to json file\n")
	// 	return
	// }

	appendStep(&ts.Steps[0].Steps, 100, "3B", 2, "./time_test_2.json")
	// time.Sleep(time.Millisecond * 100)
	// ts.Steps[0].Steps = append(ts.Steps[0].Steps, TimeStamp{Name: "3B", StartTime: &now, EndTime: nil, ExpectedSteps: 2})
	// err = jsonutils.WriteJSONFile("./time_test_2.json", &ts)
	// if err != nil {
	// 	fmt.Printf("unable to write to json file\n")
	// 	return
	// }

	appendStep(&ts.Steps[0].Steps[1].Steps, 100, "4A", 0, "./time_test_3.json")
	appendStep(&ts.Steps[0].Steps[1].Steps, 100, "4B", 0, "./time_test_3.json")
	appendStep(&ts.Steps, 100, "2B", 2, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps, 100, "3C", 2, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps[0].Steps, 100, "4A", 0, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps[0].Steps, 100, "4B", 0, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps, 100, "3D", 1, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps[1].Steps, 100, "4C", 0, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps[1].Steps, 100, "4D", 1, "./time_test_4.json")
	appendStep(&ts.Steps[1].Steps[1].Steps[0].Steps, 100, "5A", 0, "./time_test_4.json")
	appendStep(&ts.Steps, 100, "2C", 1, "./time_test_4.json")
	appendStep(&ts.Steps[2].Steps, 100, "50", 2, "./time_test_4.json")

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

func appendStep(steps *[]TimeStamp, unitTime int, name string, expectedSteps int, fileName string){ 
	time.Sleep(time.Millisecond * time.Duration(unitTime))
	now := time.Now()
	*steps = append(*steps, TimeStamp{Name: name, StartTime: &now, EndTime: nil, ExpectedSteps: expectedSteps})
	err := jsonutils.WriteJSONFile(fileName, &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}
}
