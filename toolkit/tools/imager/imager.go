// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to create and install images

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/image/imager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagegen/installutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app             = kingpin.New("imager", "Tool to create and install images.")
	buildDir        = app.Flag("build-dir", "Directory to store temporary files while building.").ExistingDir()
	configFile      = exe.InputFlag(app, "Path to the image config file.")
	localRepo       = app.Flag("local-repo", "Path to local RPM repo").ExistingDir()
	tdnfTar         = app.Flag("tdnf-worker", "Path to tdnf worker tarball").ExistingFile()
	repoFile        = app.Flag("repo-file", "Full path to local.repo.").ExistingFile()
	assets          = app.Flag("assets", "Path to assets directory.").ExistingDir()
	baseDirPath     = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	outputDir       = app.Flag("output-dir", "Path to directory to place final image.").ExistingDir()
	liveInstallFlag = app.Flag("live-install", "Enable to perform a live install to the disk specified in config file.").Bool()
	emitProgress    = app.Flag("emit-progress", "Write progress updates to stdout, such as percent complete and current action.").Bool()
	logFile         = exe.LogFileFlag(app)
	logLevel        = exe.LogLevelFlag(app)
)

func populateImagerConfig() *imager.Config {
	const defaultSystemConfig = 0

	return &imager.Config{
		BuildDir:        *buildDir,
		ConfigFile:      *configFile,
		LocalRepo:       *localRepo,
		TdnfTar:         *tdnfTar,
		RepoFile:        *repoFile,
		Assets:          *assets,
		BaseDirPath:     *baseDirPath,
		OutputDir:       *outputDir,
		LiveInstallFlag: *liveInstallFlag,
		EmitProgress:    *emitProgress,
		SystemConfig:    defaultSystemConfig,
	}
}

func main() {
	const defaultSystemConfig = 0

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)

	if *emitProgress {
		installutils.EnableEmittingProgress()
	}

	cfg := populateImagerConfig()
	err := cfg.BuildSysConfig(defaultSystemConfig)
	logger.PanicOnError(err, "Failed to build system configuration")
}
