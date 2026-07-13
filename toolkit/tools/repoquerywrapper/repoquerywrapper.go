// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"github.com/sirupsen/logrus"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	QueryCmdFindPresent     = "find-present"
	QueryCmdFindNamePresent = "find-name-present"
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

	queryCmd        = app.Flag("query-cmd", "The query commands to run. Available commands are: 'find-present', 'find-name-present'.").Required().String()
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

	// cmd         : 'find-name-present'
	// query input : a file where each line is a bare rpm package name
	//               (no version/release/arch) to search for.
	// query output: a file where each line is a name that has AT LEAST ONE
	//               matching RPM (any version/release/arch) available in the
	//               queried repos.
	//
	// Motivation: image composition uses a fetcher that walks ordered repos
	// first-match; the local toolchain-repo shadows PMC even when PMC has a
	// newer NEVRA for the same package name. Callers use this query to identify
	// which toolchain packages can be safely scrubbed so PMC's copy is used
	// instead. See rpmrepocloner.go and toolkit/resources/manifests/package/local.repo.
	if *queryCmd == QueryCmdFindNamePresent {

		// Build a set of package names present in the queried repos by
		// stripping "-<version>-<release>.<arch>" from each basename.
		presentNames := make(map[string]bool)
		for basename := range packagesAvailableFromRepos {
			name := packageNameFromNEVRA(basename)
			if name != "" {
				presentNames[name] = true
			}
		}

		inputNames, err := readFileLines(*queryInputFile)
		if err != nil {
			logger.PanicOnError(err)
		}

		var outputNames []string
		for _, inputName := range inputNames {
			if inputName == "" {
				continue
			}
			if presentNames[inputName] {
				outputNames = append(outputNames, inputName)
			}
		}

		err = writeFileLines(outputNames, *queryOutputFile)
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
	content, err := os.ReadFile(fileName)
	if err != nil {
		logger.Log.Errorf("Error reading file: %v", err)
		return nil, err
	}

	return strings.Split(string(content), "\n"), nil
}

func writeFileLines(lines []string, fileName string) (err error) {
	content := strings.Join(lines, "\n")
	err = os.WriteFile(fileName, []byte(content), 0644)
	if err != nil {
		logger.Log.Errorf("Error writing file: %v", err)
		return err
	}
	return nil
}

// packageNameFromNEVRA parses an RPM basename of the form
// "<name>-<version>-<release>.<arch>" (with the ".rpm" suffix already stripped)
// and returns just the "<name>" portion. Returns an empty string if the input
// does not have the expected structure.
//
// Per RPM rules, <version> and <release> may not contain '-', but <name> may.
// So we parse from the right: strip ".<arch>", then "-<release>", then
// "-<version>", leaving the name.
func packageNameFromNEVRA(basename string) string {
	lastDot := strings.LastIndex(basename, ".")
	if lastDot < 0 {
		return ""
	}
	nameVerRel := basename[:lastDot]

	lastDash := strings.LastIndex(nameVerRel, "-")
	if lastDash < 0 {
		return ""
	}
	nameVer := nameVerRel[:lastDash]

	lastDash = strings.LastIndex(nameVer, "-")
	if lastDash < 0 {
		return ""
	}
	return nameVer[:lastDash]
}
