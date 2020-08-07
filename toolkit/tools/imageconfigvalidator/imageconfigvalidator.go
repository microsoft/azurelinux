// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// An image configuration validator

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

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
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	inPath, err := filepath.Abs(*input)
	logger.PanicOnError(err, "Error when calculating input path")

	logger.Log.Infof("Reading configuration file (%s)", inPath)
	config, err := configuration.Load(inPath)
	logger.PanicOnError(err, "Failed loading image configuration")

	err = validateConfiguration(config)
	if err != nil {
		const returnCodeOnError = 1
		// Log an error here as opposed to panicing to keep the output simple
		// and only contain the error with the config file.
		logger.Log.Errorf("Invalid configuration: %s", err)
		os.Exit(returnCodeOnError)
	}

	return
}

func validateConfiguration(config configuration.Config) (err error) {
	err = validateDisks(config.Disks)
	if err != nil {
		return
	}

	err = validateSystemConfigs(config.SystemConfigs)
	return
}

func validateDisks(disks []configuration.Disk) (err error) {
	numberOfDisks := len(disks)

	for i, disk := range disks {
		logger.Log.Infof("Validating disk [%d/%d]", (i + 1), numberOfDisks)
		err = validatePartitionTableType(disk)
		if err != nil {
			return
		}
	}

	return
}

func validatePartitionTableType(disk configuration.Disk) (err error) {
	switch disk.PartitionTableType {
	case "gpt", "mbr", "":
	default:
		return fmt.Errorf("invalid partition table type (%s)", disk.PartitionTableType)
	}

	return
}

func validateSystemConfigs(systemConfigs []configuration.SystemConfig) (err error) {
	numberOfConfigs := len(systemConfigs)
	if numberOfConfigs == 0 {
		return fmt.Errorf("config file must provide at least one system configuration inside the [SystemConfigs] field")
	}

	defaultFound := false
	for i, config := range systemConfigs {
		logger.Log.Infof("Validating system configuration [%d/%d] (%s) ", (i + 1), numberOfConfigs, config.Name)
		if strings.TrimSpace(config.Name) == "" {
			return fmt.Errorf("missing [Name] field")
		}

		if config.IsDefault {
			if defaultFound {
				return fmt.Errorf("config file must have no more than one default system configuration. Please remove redundant [IsDefault] fields")
			}
			defaultFound = true
		}

		if len(config.PackageLists) == 0 {
			return fmt.Errorf("system configuration must provide at least one package list inside the [PackageLists] field")
		}

		// Enforce that any non-rootfs configuration has a default kernel.
		if len(config.PartitionSettings) != 0 {
			// Ensure that default option is always present
			if _, ok := config.KernelOptions["default"]; !ok {
				return fmt.Errorf("system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]")
			}
			// Ensure that non-comment options are not blank
			for name, kernelName := range config.KernelOptions {
				// Skip comments
				if name[0] == '_' {
					continue
				}
				if strings.TrimSpace(kernelName) == "" {
					return fmt.Errorf("empty kernel entry found in the [KernelOptions] field (%s); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", name)
				}
			}
		}
	}
	return
}
