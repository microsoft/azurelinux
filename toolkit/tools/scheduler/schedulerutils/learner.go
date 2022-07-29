// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"encoding/json"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
)

type LearnerResult struct {
	Name      string
	BuildTime float32
	Unblocks  []string
}

type Learner struct {
	Results []LearnerResult
}

func NewLearner() (l *Learner) {
	return &Learner{
		Results: make([]LearnerResult, 0),
	}
}

func (l *Learner) RecordBuildResult(res *BuildResult) {
	if res.Node.Type == pkggraph.TypeBuild {
		lr := LearnerResult{
			Name:      res.Node.RpmPath,
			BuildTime: res.BuildTime,
			Unblocks:  []string{"vim"},
		}
	
		l.Results = append(l.Results, lr)
		logger.Log.Debugf("debuggy: %f", res.BuildTime)
	}
}

func (l *Learner) Dump(path string) {
	j, err := json.MarshalIndent(l, "", "  ")
	if err != nil {
		logger.Log.Error(err)
	}
	file, err := os.Create(path)
	if err != nil {
		logger.Log.Error(err)
	}
	defer file.Close()
	_, err = file.Write(j)

	file.Sync()
}
