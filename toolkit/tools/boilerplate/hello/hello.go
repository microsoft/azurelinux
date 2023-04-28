// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package hello

import "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"

// World is a sample public (starts with a capital letter, must be commented) function.
func World() string {
	// timestamp_v2.StartMeasuringEvent("hello world", 0)
	// defer timestamp_v2.StopMeasurement()
	ts, _ := timestamp.StartEvent("hello world", nil)
	defer timestamp.StopEvent(ts)

	return "Hello, world!"
}

func Name(name string) string {
	ts, _ := timestamp.StartEvent("hello name", nil)
	defer timestamp.StopEvent(ts)

	return name
}
