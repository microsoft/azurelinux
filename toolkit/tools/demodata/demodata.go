// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package main

import (
	"fmt"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/dashboard_v2"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	// Shared TimeStamp struct.
	ts            dashboard_v2.TimeStamp
	fileName      = "./time_demo.json"
	shortInterval = 500
	longInterval  = 1000
)

func main() {
	// structure:
	// 1A	-2A	-3A
	//			\3B	-4A
	//				\4B
	//		\2B	-3C	-4C	-5A
	//				\4D
	//			\3D	-4E
	//				\4F
	//		\2C	-3E

	logger.InitStderrLog()
	now := time.Now()
	ts = dashboard_v2.TimeStamp{Name: "1A", StartTime: &now, EndTime: nil, ExpectedSteps: 3}
	err := jsonutils.WriteJSONFile(fileName, &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}

	appendStep(&ts.Steps, shortInterval, "2A", 2)
	appendStep(&ts.Steps[0].Steps, shortInterval, "3A", 0)
	finishStep(&ts.Steps[0].Steps, longInterval) // 3A
	appendStep(&ts.Steps[0].Steps, shortInterval, "3B", 2)
	appendStep(&ts.Steps[0].Steps[1].Steps, shortInterval, "4A", 0)
	finishStep(&ts.Steps[0].Steps[1].Steps, longInterval) // 4A
	appendStep(&ts.Steps[0].Steps[1].Steps, shortInterval, "4B", 0)
	finishStep(&ts.Steps[0].Steps[1].Steps, longInterval) // 4B
	finishStep(&ts.Steps[0].Steps, shortInterval)         // 3B
	finishStep(&ts.Steps, shortInterval)                  // 2A
	appendStep(&ts.Steps, shortInterval, "2B", 2)
	appendStep(&ts.Steps[1].Steps, shortInterval, "3C", 2)
	appendStep(&ts.Steps[1].Steps[0].Steps, shortInterval, "4C", 0)
	appendStep(&ts.Steps[1].Steps[0].Steps[0].Steps, shortInterval, "5A", 0)
	finishStep(&ts.Steps[1].Steps[0].Steps[0].Steps, longInterval) // 5A
	finishStep(&ts.Steps[1].Steps[0].Steps, longInterval)          // 4C
	appendStep(&ts.Steps[1].Steps[0].Steps, shortInterval, "4D", 0)
	finishStep(&ts.Steps[1].Steps[0].Steps, longInterval) // 4D
	finishStep(&ts.Steps[1].Steps, shortInterval)         // 3C
	appendStep(&ts.Steps[1].Steps, shortInterval, "3D", 1)
	appendStep(&ts.Steps[1].Steps[1].Steps, shortInterval, "4E", 0)
	finishStep(&ts.Steps[1].Steps[1].Steps, longInterval) // 4E
	appendStep(&ts.Steps[1].Steps[1].Steps, shortInterval, "4F", 1)
	finishStep(&ts.Steps[1].Steps[1].Steps, longInterval) // 4F
	finishStep(&ts.Steps[1].Steps, shortInterval)         // 3D
	finishStep(&ts.Steps, shortInterval)                  // 2B
	appendStep(&ts.Steps, shortInterval, "2C", 1)
	appendStep(&ts.Steps[2].Steps, shortInterval, "3E", 2)
	finishStep(&ts.Steps[2].Steps, longInterval) // 3E
	finishStep(&ts.Steps, shortInterval)         // 2C
	now = time.Now()
	ts.EndTime = &now
	err = jsonutils.WriteJSONFile(fileName, &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}

}

func appendStep(steps *[]dashboard_v2.TimeStamp, unitTime int, name string, expectedSteps int) {
	time.Sleep(time.Millisecond * time.Duration(unitTime))
	now := time.Now()
	*steps = append(*steps, dashboard_v2.TimeStamp{Name: name, StartTime: &now, EndTime: nil, ExpectedSteps: expectedSteps})
	err := jsonutils.WriteJSONFile(fileName, &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}
}

func finishStep(steps *[]dashboard_v2.TimeStamp, unitTime int) {
	time.Sleep(time.Millisecond * time.Duration(unitTime))
	now := time.Now()
	(*steps)[len(*steps)-1].EndTime = &now
	err := jsonutils.WriteJSONFile(fileName, &ts)
	if err != nil {
		fmt.Printf("unable to write to json file\n")
		return
	}
}
