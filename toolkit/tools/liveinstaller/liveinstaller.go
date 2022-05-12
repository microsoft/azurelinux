// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"gopkg.in/alecthomas/kingpin.v2"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/image/liveinstaller"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
)

var (
	app = kingpin.New("liveinstaller", "A tool to download a provided list of packages into a given directory.")

	// Take in strings for the config and template config file, as they may not exist on disk
	configFile         = exe.InputStringFlag(app, "Path to the image config file.")
	templateConfigFile = app.Flag("template-config", "Path to the template config file.").String()
	forceAttended      = app.Flag("attended", "Use the attended installer regardless if a config file is present.").Bool()
	imagerTool         = app.Flag("imager", "Path to the imager tool.").Required().ExistingFile()
	buildDir           = app.Flag("build-dir", "Directory to store temporary files while building.").Required().ExistingDir()
	baseDirPath        = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populateLiveinstallerConfig() *liveinstaller.Config {
	const imagerLogFile = "/var/log/imager.log"
	return &liveinstaller.Config{
		ConfigFile:         *configFile,
		TemplateConfigFile: *templateConfigFile,
		ForceAttended:      *forceAttended,
		ImagerTool:         *imagerTool,
		BuildDir:           *buildDir,
		BaseDirPath:        *baseDirPath,
		ImagerLogFile:      imagerLogFile,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateLiveinstallerConfig()
	err := cfg.Install()
	logger.PanicOnError(err)
}
