package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/gosuri/uiprogress"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/demo"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	ts demo.TimeStamp
	dashboardProgress = uiprogress.New()
	progressName []string
	progressValue []int
	progressLevel []int
	waitTime = time.Millisecond * 500
)

func CheckProgress(ts *demo.TimeStamp, level int) {
	progressName = append(progressName, ts.Name)
	progressValue = append(progressValue, int(ts.Progress()*100))
	progressLevel = append(progressLevel, level)
	for _, step := range ts.Steps {
		progress := step.Progress()
		if progress != 0.0 && progress != 1.0 {
			CheckProgress(&step, level+1)
		}
	}
}

func main() {
	logger.InitStderrLog()
	dashboardProgress.Start()

	currDir, err := os.Getwd()
	parentDir := filepath.Dir(currDir)

	for {
		err = jsonutils.ReadJSONFile(parentDir+"/demodata/time_demo.json", &ts)
		if err != nil {
			fmt.Printf("%s\n", err)
			return
		}

		progressName = []string{}
		progressValue = []int{}
		progressLevel = []int{}
		CheckProgress(&ts, 0)

		for i := 0; i < len(progressName); i++ {
			name := progressName[i]
			value := progressValue[i]
			level := progressLevel[i]
			indent := ""
			for i := 0; i < level; i++ {
				indent += "  "
			}
			bar := dashboardProgress.AddBar(100)
			bar.AppendCompleted()
			bar.PrependFunc(func(b *uiprogress.Bar) string {
				return name + indent
			})
			bar.Set(value)
			// wg.Add(1)
		}
		time.Sleep(waitTime)
		for i := 0; i < len(progressName); i++ {
			dashboardProgress.Bars = dashboardProgress.Bars[:len(dashboardProgress.Bars)-1]
		}
		time.Sleep(waitTime)
	}

}

func StartProgress() {
	dashboardProgress.Start()
}

func StopProgress() {
	dashboardProgress.Stop()
}

func AddProgressBar(total int) *uiprogress.Bar {
	return dashboardProgress.AddBar(total)
}

func ListenProgress() {
	dashboardProgress.Listen()
}
