// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// An image configuration validator

package main

import (
	"os"
	"path/filepath"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
)

var (
	app = kingpin.New("imageconfigvalidator", "A tool for validating image configuration files")

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	input = exe.InputStringFlag(app, "Path to the image config file.")
)

func main() {
	const returnCodeOnError = 1

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	inPath, err := filepath.Abs(*input)
	logger.PanicOnError(err, "Error when calculating input path")

	logger.Log.Infof("Reading configuration file (%s)", inPath)
	config, err := configuration.Load(inPath)
	if err != nil {
		logger.Log.Fatalf("Failed while loading image configuration '%s': %s", inPath, err)
	}

	// Basic validation will occur during load, but we can add additional checking here.
	err = ValidateConfiguration(config)
	if err != nil {
		// Log an error here as opposed to panicing to keep the output simple
		// and only contain the error with the config file.
		logger.Log.Fatalf("Invalid configuration '%s': %s", inPath, err)
	}

	return
}

// ValidateConfiguration will run sanity checks on a configuration structure
func ValidateConfiguration(config configuration.Config) (err error) {
	err = config.IsValid()
	return
}
