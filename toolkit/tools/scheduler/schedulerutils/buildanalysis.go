// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

type BuildAnalysis struct {
	TotalBuildTime float32
	IdleTime       float32
	WastedTime     float32
}

func NewBuildAnalysis() (l *BuildAnalysis) {
	return &BuildAnalysis{
		TotalBuildTime: 0.0,
		IdleTime:       0.0,
		WastedTime:     0.0,
	}
}

func (b *BuildAnalysis) RecordTotalBuildTime(buildTime float32) {
	b.TotalBuildTime = buildTime
}
