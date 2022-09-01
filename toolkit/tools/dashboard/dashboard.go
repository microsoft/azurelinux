package main

import (
	"bufio"
	"fmt"
	"io/fs"
	"os"
	"path"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gosuri/uiprogress"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"gopkg.in/alecthomas/kingpin.v2"
)

type stampedFile struct {
	fileName     string
	currLine     int32
	totalLine    int32
	bar          *uiprogress.Bar
	lastStepDesc string
}

var (
	app     = kingpin.New("dashboard", "A tool that monitors a CBL-Mariner build live.")
	dirPath = app.Flag("build-dir", "The build directory of the CBL-Mariner build to track.").Required().ExistingDir()

	wg                sync.WaitGroup
	dashboardProgress = uiprogress.New()
	barWidth          = 30
	currProgress      = int32(0) // chose int32 instead of int to use the atomic package
	totalProgress     = int32(24)
	isInit            = false // set to true the first time we detec the "init" file in build/timestamp folder.
	targetDir         string
	targetCSV         = []*stampedFile{
		&stampedFile{
			fileName:     "create_worker_chroot.sh.csv",
			currLine:     0,
			totalLine:    5,
			lastStepDesc: "",
		},
		&stampedFile{
			fileName:     "imageconfigvalidator.csv",
			currLine:     0,
			totalLine:    2,
			lastStepDesc: "",
		},
		&stampedFile{
			fileName:     "imagepkgfetcher.csv",
			currLine:     0,
			totalLine:    9,
			lastStepDesc: "",
		},
		&stampedFile{
			fileName:     "imager.csv",
			currLine:     0,
			totalLine:    4,
			lastStepDesc: "",
		},
		&stampedFile{
			fileName:     "roast.csv",
			currLine:     0,
			totalLine:    3,
			lastStepDesc: "",
		},
	}
	// targetJSON = []string{} // for future version
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	targetDir = path.Join(*dirPath, "timestamp")

	fmt.Println("Starting dashboard")
	fmt.Println("Will scan for:")
	for _, f := range targetCSV {
		path := path.Join(targetDir, f.fileName)
		fmt.Println(path)
	}
	dashboardProgress.Start()
	bar := AddProgressBar(int(totalProgress)).AppendCompleted()
	bar.Width = barWidth

	bar.PrependFunc(func(b *uiprogress.Bar) string {
		return fmt.Sprintf("%15s: %-25s", "Total", "")
	})

	SetSubBar()

	// fmt.Println("Proceeding to for loop")
	// fmt.Printf("%+v \n", dashboardProgress)

	for {
		time.Sleep(1 * time.Second)
		// fmt.Printf("%d \n", int(currProgress))
		bar.Set(int(currProgress))

		// Check if the target directory exists. Assume we only need to check one directory for now.
		_, err := os.Stat(targetDir)
		if os.IsNotExist(err) {
			continue
		}

		// Check if build has started; if so, add a timestamp to init.csv
		if isInit == false {
			// fmt.Printf("incrementing in checkinit() \n")
			checkInit()
		}

		// Check update for each target file.
		for i, _ := range targetCSV {
			currFile := targetCSV[i]
			path := path.Join(targetDir, currFile.fileName)
			// Check if the file exists.
			currStat, err := os.Stat(path)
			if os.IsNotExist(err) {
				continue
			}

			// If the file exists, check if there has been any updates since we last visited.
			go currFile.getUpdate(currStat)
		}
	}

}

// Check if the file has been updated, and get updated contents if it did.
// Assumption: the file and its parent directories of the file have been created.
func (file *stampedFile) getUpdate(currStat fs.FileInfo) {
	currNumLines := file.getNumLines()
	if currNumLines != file.currLine {
		atomic.AddInt32(&currProgress, currNumLines-file.currLine)

		file.currLine = currNumLines
		file.bar.Set(int(currNumLines))

		// pop one task off the queue when it's done
		if currNumLines == file.totalLine {
			wg.Done()
			dashboardProgress.Bars = dashboardProgress.Bars[:len(dashboardProgress.Bars)-1]
		}
	}
}

func (file *stampedFile) getNumLines() int32 {
	currfile, _ := os.Open(targetDir + file.fileName)
	fileScanner := bufio.NewScanner(currfile)
	count := int32(0)
	stepDesc := ""

	for fileScanner.Scan() {
		count += 1
		stepDesc = strings.Split(fileScanner.Text(), ",")[1]
		if count > file.currLine {
			// fmt.Printf("[%d / %d] in %s: %s \n", count, targetCSV[filepath][1], filepath, fileScanner.Text())
		}
	}

	file.lastStepDesc = stepDesc

	return count
}

// Checks if the build has started, and update the progress bar if it did start.
func checkInit() {
	_, err := os.Stat(targetDir + "/init")
	if os.IsNotExist(err) {
		return
	}
	isInit = true
	atomic.AddInt32(&currProgress, 1)
}

func SetSubBar() {
	// fmt.Println("Within SetSubBar")

	for i, _ := range targetCSV {
		currFile := targetCSV[i]
		currFile.bar = AddProgressBar(int(currFile.totalLine)).AppendCompleted()
		currFile.bar.Width = barWidth
		currFile.bar.PrependFunc(func(b *uiprogress.Bar) string {
			var tempFileName, tempLastStep string
			tempFileName = currFile.fileName[:len(currFile.fileName)-4]
			if len(currFile.fileName) > 15 {
				tempFileName = tempFileName[:13] + ".."
			}
			if len(currFile.lastStepDesc) > 25 {
				tempLastStep = currFile.lastStepDesc[:23] + ".."
			} else {
				tempLastStep = currFile.lastStepDesc
			}
			return fmt.Sprintf("%15s: %-25s", tempFileName, tempLastStep)
		})
		wg.Add(1)
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
