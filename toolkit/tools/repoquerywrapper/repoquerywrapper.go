// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"io/ioutil"
	"os"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/sirupsen/logrus"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	QueryCmdFindPresent = "find-present"
)

var (
	app = kingpin.New("repoquerywrapper", "Runs queries against RPMs repo in bulk.")

	logFlags      = exe.SetupLogFlags(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()

	repoUrls  = app.Flag("repo-url", "URLs of the repos to download from.").Strings()
	repoFiles = app.Flag("repo-file", "Files containing URLs of the repos to download from.").ExistingFiles()
	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	buildDir  = app.Flag("worker-dir", "Directory to store chroot while running repo query.").Required().String()

	queryCmd        = app.Flag("query-cmd", "The query commands to run. Available command is: 'find-present'.").Required().String()
	queryInputFile  = app.Flag("query-input-file", "Path to a file with the query input data.").Required().String()
	queryOutputFile = app.Flag("query-output-file", "Path to a file for the query output data.").Required().String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("repoquerywrapper", *timestampFile)
	defer timestamp.CompleteTiming()

	packagesAvailableFromRepos, err := repoutils.GetAllRepoData(*repoUrls, *repoFiles, *workerTar, *buildDir, "")
	if err != nil {
		logger.PanicOnError(err)
	}

	// cmd         : 'find-present'
	// query input : a file where each line is the name of an rpm to search for.
	// query output: a file where each line is the name of an rpm that is
	//               present on the repo.
	if *queryCmd == QueryCmdFindPresent {

		inputRpmNames, err := readFileLines(*queryInputFile)
		if err != nil {
			logger.PanicOnError(err)
		}

		var outputRpmNames []string
		for _, inputRpmName := range inputRpmNames {
			inputRpmBaseName := strings.TrimSuffix(inputRpmName, ".rpm")
			_, exists := packagesAvailableFromRepos[inputRpmBaseName]
			if exists {
				outputRpmNames = append(outputRpmNames, inputRpmName)
			}
		}

		err = writeFileLines(outputRpmNames, *queryOutputFile)
		if err != nil {
			logger.PanicOnError(err)
		}
	}

	if logger.Log.IsLevelEnabled(logrus.DebugLevel) {
		for i, pkg := range packagesAvailableFromRepos {
			logger.Log.Debugf("Found package: %s, %s", i, pkg)
		}
	}
}

func readFileLines(fileName string) (lines []string, err error) {
	content, err := ioutil.ReadFile(fileName)
	if err != nil {
		logger.Log.Errorf("Error reading file: %v", err)
		return nil, err
	}

	return strings.Split(string(content), "\n"), nil
}

func writeFileLines(lines []string, fileName string) (err error) {
	content := strings.Join(lines, "\n")
	err = ioutil.WriteFile(fileName, []byte(content), 0644)
	if err != nil {
		logger.Log.Errorf("Error writing file: %v", err)
		return err
	}
	return nil
}
