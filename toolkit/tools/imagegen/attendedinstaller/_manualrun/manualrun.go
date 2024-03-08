// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// manualrun is a tool to test the attendedinstaller in the current terminal window.
// It will simply run the UI and print out the final config structure's content.
func main() {
	const (
		assetDirPath      = "./"
		configFileDirPath = "./"
	)

	logger.InitStderrLog()

	// The JSON parser if responsible for filling defaults, since we are
	// using a Go struct need to manually use the defaults.
	verityConfig := configuration.GetDefaultReadOnlyVerityRoot()
	verityConfig.Enable = true

	baseCfg := configuration.Config{
		SystemConfigs: []configuration.SystemConfig{
			configuration.SystemConfig{
				Name: "Core",
				PackageLists: []string{
					"packagelists/core-packages-image.json",
					"packagelists/hyperv-packages.json",
				},
				KernelOptions: map[string]string{
					"default": "kernel",
				},
				AdditionalFiles: map[string]string{
					"/etc/resolv.conf": "/etc/resolv.conf",
					"/root/.bashrc":    "/root/.bashrc",
				},
				PostInstallScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
				FinalizeImageScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
			},
			configuration.SystemConfig{
				Name: "Developer",
				PackageLists: []string{
					"packagelists/developer-packages.json",
					"packagelists/core-packages-image.json",
					"packagelists/hyperv-packages.json",
				},
				KernelOptions: map[string]string{
					"default": "kernel",
				},
				AdditionalFiles: map[string]string{
					"/etc/resolv.conf": "/etc/resolv.conf",
					"/root/.bashrc":    "/root/.bashrc",
				},
				PostInstallScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
				FinalizeImageScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
			},
			configuration.SystemConfig{
				Name: "Read-Only",
				PackageLists: []string{
					"packagelists/core-packages-image.json",
					"packagelists/hyperv-packages.json",
					"packagelists/read-only-root-packages.json",
				},
				KernelOptions: map[string]string{
					"default": "kernel",
				},
				AdditionalFiles: map[string]string{
					"/etc/resolv.conf": "/etc/resolv.conf",
					"/root/.bashrc":    "/root/.bashrc",
				},
				ReadOnlyVerityRoot: verityConfig,
				PostInstallScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
				FinalizeImageScripts: []configuration.InstallScript{
					configuration.InstallScript{
						Path: "arglessScript.sh",
					},
					configuration.InstallScript{
						Path: "thisOneNeedsArguments.sh",
						Args: "--input abc --output cba",
					},
				},
			},
		},
	}

	attendedInstaller, err := attendedinstaller.New(baseCfg, performInstallation, performCalamaresInstallation)
	logger.PanicOnError(err)

	resultingCfg, installationQuit, err := attendedInstaller.Run()
	if installationQuit {
		logger.Log.Error("User quit installation")
		return
	}
	logger.PanicOnError(err)

	// Marshal to JSON to print out a human-readable version of the config
	jsonBytes, err := json.MarshalIndent(resultingCfg, "", "\t")
	logger.PanicOnError(err)

	fmt.Print(string(jsonBytes))
}

// A fake calamares installation method.
func performCalamaresInstallation() (err error) {
	logger.Log.Info("Calamares installation requested")
	return
}

// A fake installation method that will take ~2 seconds to test the ProgressView.
func performInstallation(cfg configuration.Config, progress chan int, status chan string) (err error) {
	const (
		totalLoops              = 200
		msToSleep               = 10
		testPanicInInstallation = false
		testErrorInInstallation = false
	)

	defer close(progress)
	defer close(status)

	for i := 0; i < totalLoops; i++ {
		progress <- (100 * i) / totalLoops
		status <- fmt.Sprintf("%d/%d", i, totalLoops)
		time.Sleep(msToSleep * time.Millisecond)
	}

	if testPanicInInstallation {
		logger.Log.Panicf("Simulated panic during installation, expected behavior is to drop to shell cleanly in terminal mode")
	}

	if testErrorInInstallation {
		err = fmt.Errorf("simulated error")
	}

	return
}
