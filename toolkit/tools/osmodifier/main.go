// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"log"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/osmodifierlib"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("osmodifier", "Used to modify os")

	configFile    = app.Flag("config-file", "Path of the os modification config file.").String()
	logFlags      = exe.SetupLogFlags(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	var err error

	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("osmodifier", *timestampFile)
	defer timestamp.CompleteTiming()

	err = modifyImage()
	if err != nil {
		log.Fatalf("os modification failed: %v", err)
	}
}

func modifyImage() error {
	if *configFile == "" {
		err := osmodifierlib.ModifyOSWithoutConfigFile()
		if err != nil {
			return err
		}
	}

	err := osmodifierlib.ModifyOSWithConfigFile(*configFile)
	if err != nil {
		return err
	}

	return nil
}
