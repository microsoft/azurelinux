// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"bufio"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/attendedinstaller"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"

	"golang.org/x/sys/unix"
	"gopkg.in/alecthomas/kingpin.v2"
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
	logColor  = exe.LogColorFlag(app)
)

// Every valid mouse event handler will follow the format:
// H: Handlers=eventX mouseX
var mouseEventHandlerRegex = regexp.MustCompile(`^H:\s+Handlers=(\w+)\s+mouse\d+`)

type imagerArguments struct {
	imagerTool   string
	configFile   string
	buildDir     string
	baseDirPath  string
	emitProgress bool
	logFile      string
	logLevel     string
}

type installationDetails struct {
	installationQuit bool
	finalConfig      configuration.Config
}

func handleCtrlC(signals chan os.Signal) {
	<-signals
	logger.Log.Error("Installation in progress, please wait until finished.")
}

func main() {
	const imagerLogFile = "/var/log/imager.log"

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel, *logColor)

	// Prevent a SIGINT (Ctr-C) from stopping liveinstaller while an installation is in progress.
	// It is the responsibility of the installer's user interface (terminal installer or Calamares) to handle quit requests from the user.
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, unix.SIGINT)
	go handleCtrlC(signals)

	// Imager's stdout/stderr will be combined with this tool's, so it will automatically be logged to the current log file
	args := imagerArguments{
		imagerTool:  *imagerTool,
		buildDir:    *buildDir,
		baseDirPath: *baseDirPath,
		logLevel:    logger.Log.GetLevel().String(),
		logFile:     imagerLogFile,
	}

	installFunc := installerFactory(*forceAttended, *configFile, *templateConfigFile)
	installDetails, err := installFunc(args)
	if installDetails.installationQuit {
		logger.Log.Error("User quit installation")
		// Return a non-zero exit code to drop the user to shell
		os.Exit(1)
	}

	logger.PanicOnError(err)

	// Change the boot order by either changing the EFI boot order or ejecting CDROM.
	updateBootOrder(installDetails)
	ejectDisk()
}

func installerFactory(forceAttended bool, configFile, templateConfigFile string) (installFunc func(imagerArguments) (installationDetails, error)) {
	isAttended := false

	// Determine if the attended installer should be shown
	if forceAttended {
		logger.Log.Info("`attended` flag set, using attended installation")
		isAttended = true
	} else {
		unattendedExists, _ := file.PathExists(configFile)

		if !unattendedExists {
			logger.Log.Infof("Config file (%s) does not exist, using attended installation", configFile)
			isAttended = true
		}
	}

	if isAttended {
		templateExists, _ := file.PathExists(templateConfigFile)
		if !templateExists {
			logger.Log.Panicf("Attended installation requires a template config file. Specified template (%s) does not exist.", templateConfigFile)
		}
	}

	if isAttended {
		installFunc = func(args imagerArguments) (installationDetails, error) {
			return terminalUIAttendedInstall(templateConfigFile, args)
		}
	} else {
		installFunc = func(args imagerArguments) (installationDetails, error) {
			return unattendedInstall(configFile, args)
		}
	}

	return
}

func updateBootOrder(installDetails installationDetails) (err error) {
	if installDetails.finalConfig.DefaultSystemConfig.BootType != "efi" {
		logger.Log.Info("No BootType of 'efi' detected. Not attempting to set EFI boot order.")
		return
	}

	err = removeOldMarinerBootTargets()
	if err != nil {
		return
	}

	logger.Log.Info("Setting Boot Order")
	err = runBootEntryCreationCommand(installDetails)
	if err != nil {
		return
	}

	return
}

func runBootEntryCreationCommand(installDetails installationDetails) (err error) {
	const squashErrors = false
	program := "efibootmgr"
	cfg := installDetails.finalConfig
	bootPartIdx, bootPart := cfg.GetBootPartition()
	bootDisk := cfg.GetDiskContainingPartition(bootPart)
	commandArgs := []string{
		"-c",                            // Create a new bootnum and place it in the beginning of the boot order
		"-d", bootDisk.TargetDisk.Value, // Specify which disk the boot file is on
		"-p", fmt.Sprintf("%d", bootPartIdx+1), // Specify which partition the boot file is on
		"-l", "'\\EFI\\BOOT\\bootx64.efi'", // Specify the path for where the boot file is located on the partition
		"-L", "Mariner", // Specify what label you would like to give this boot entry
		"-v", // Be verbose
	}
	err = shell.ExecuteLive(squashErrors, program, commandArgs...)
	return
}

func removeOldMarinerBootTargets() (err error) {
	const squashErrors = false
	logger.Log.Info("Removing pre-existing 'Mariner' boot targets from efibootmgr")
	program := "efibootmgr" // Default behavior when piped or called without options is to print current boot order in a human-readable format
	commandArgs := []string{
		"|", "grep", "\"Mariner\"", // Filter boot order for Mariner boot targets
		"|", "sed", "'s/* Mariner//g'", // Pruning for just the bootnum
		"|", "sed", "'s/Boot*//g'", // Pruning for just the bootnum
		"|", "xargs", "-t", "-i", "efibootmgr", "-b", "{}", "-B", // Calling efibootmgr --delete-bootnum (aka `-B`) on each pre-existing bootnum with a Mariner label
	}
	err = shell.ExecuteLive(squashErrors, program, commandArgs...)
	return
}

func ejectDisk() (err error) {
	logger.Log.Info("Ejecting CD-ROM.")
	_, _, err = shell.Execute("eject", "--cdrom")

	if err != nil {
		// If there was an error ejecting the CD-ROM, assume this is a USB installation and prompt the user
		// to remove the USB device before rebooting.
		logger.Log.Info("==================================================================================")
		logger.Log.Info("Installation Complete. Please Remove USB installation media and reboot if present.")
		logger.Log.Info("==================================================================================")
	}
	return
}

func findMouseHandlers() (handlers string, err error) {
	const (
		deviceHandlerFile   = "/proc/bus/input/devices"
		eventPrefix         = "/dev/input"
		handlerDelimiter    = ":"
		absoluteInputEvents = "abs"
		eventMatchGroup     = 1
	)

	devicesFile, err := os.Open(deviceHandlerFile)
	if err != nil {
		return
	}
	defer devicesFile.Close()

	// Gather a list of all mouse event handlers from the devices file
	eventHandlers := []string{}
	scanner := bufio.NewScanner(devicesFile)
	for scanner.Scan() {
		matches := mouseEventHandlerRegex.FindStringSubmatch(scanner.Text())
		if len(matches) == 0 {
			continue
		}

		eventPath := filepath.Join(eventPrefix, matches[eventMatchGroup])
		eventHandlers = append(eventHandlers, eventPath)
	}

	err = scanner.Err()
	if err != nil {
		return
	}

	if len(eventHandlers) == 0 {
		err = fmt.Errorf("no mouse handler detected")
		return
	}

	// Add the the absolute input modifier to the handler list as mouse events are absolute.
	// QT's default behavior is to take in relative events.
	eventHandlers = append(eventHandlers, absoluteInputEvents)

	// Join all mouse event handlers together so they all function inside QT
	handlers = strings.Join(eventHandlers, handlerDelimiter)

	return
}

func calamaresInstall(templateConfigFile string, args imagerArguments) (err error) {
	const (
		squashErrors = false
		calamaresDir = "/etc/calamares"
	)

	args.emitProgress = true
	args.configFile = filepath.Join(calamaresDir, "unattended_config.json")

	launchScript := filepath.Join(calamaresDir, "mariner-install.sh")
	skuDir := filepath.Join(calamaresDir, "mariner-skus")

	bootType := configuration.SystemBootType()
	logger.Log.Infof("Boot type detected: %s", bootType)

	mouseHandlers, err := findMouseHandlers()
	if err != nil {
		// Not finding a mouse isn't fatal as the installer can instead be driven with
		// a keyboard only.
		logger.Log.Warnf("No mouse detected: %v", err)
	}

	logger.Log.Infof("Using (%s) for mouse input", mouseHandlers)
	newEnv := append(shell.CurrentEnvironment(), fmt.Sprintf("QT_QPA_EVDEV_MOUSE_PARAMETERS=%s", mouseHandlers))
	shell.SetEnvironment(newEnv)

	// Generate the files needed for calamares
	err = os.MkdirAll(skuDir, os.ModePerm)
	if err != nil {
		return
	}

	err = generateCalamaresLaunchScript(launchScript, args)
	if err != nil {
		return
	}

	// Generate the partial JSONs for SKUs
	err = generateCalamaresSKUs(templateConfigFile, skuDir, bootType)
	if err != nil {
		return
	}

	return shell.ExecuteLive(squashErrors, "calamares", "-platform", "linuxfb")
}

func generateCalamaresLaunchScript(launchScriptPath string, args imagerArguments) (err error) {
	const executionPerm = 0755

	// Generate the script calamares will invoke to install
	scriptFile, err := os.OpenFile(launchScriptPath, os.O_CREATE|os.O_RDWR, executionPerm)
	if err != nil {
		return
	}
	defer scriptFile.Close()

	logger.Log.Infof("Generating install script (%s)", launchScriptPath)
	program, commandArgs := formatImagerCommand(args)

	scriptFile.WriteString("#!/bin/bash\n")
	scriptFile.WriteString(fmt.Sprintf("%s %s", program, strings.Join(commandArgs, " ")))
	scriptFile.WriteString("\n")

	return
}

func generateCalamaresSKUs(templateConfigFile, skuDir, bootType string) (err error) {
	// Parse template config
	templateConfig, err := configuration.Load(templateConfigFile)
	if err != nil {
		return
	}

	// Generate JSON snippets for each SKU
	for _, sysConfig := range templateConfig.SystemConfigs {
		sysConfig.BootType = bootType
		err = generateSingleCalamaresSKU(sysConfig, skuDir)
		if err != nil {
			return
		}
	}

	return
}

func generateSingleCalamaresSKU(sysConfig configuration.SystemConfig, skuDir string) (err error) {
	skuFilePath := filepath.Join(skuDir, sysConfig.Name+".json")
	logger.Log.Infof("Generating SKU option (%s)", skuFilePath)

	// Write the individual system config to a file.
	return jsonutils.WriteJSONFile(skuFilePath, sysConfig)
}

func terminalUIAttendedInstall(templateConfigFile string, args imagerArguments) (installDetails installationDetails, err error) {
	const configFileName = "attendedconfig.json"

	// Parse template config
	templateConfig, err := configuration.Load(templateConfigFile)
	if err != nil {
		return
	}

	// Store the config file generated by the attended installer under the build dir
	err = os.MkdirAll(args.buildDir, os.ModePerm)
	if err != nil {
		return
	}

	args.configFile = filepath.Join(args.buildDir, configFileName)
	attendedInstaller, err := attendedinstaller.New(templateConfig,
		// Terminal-UI based installation
		func(cfg configuration.Config, progress chan int, status chan string) (err error) {
			return terminalAttendedInstall(cfg, progress, status, args)
		},

		// Calamares based installation
		func() (err error) {
			return calamaresInstall(templateConfigFile, args)
		})

	if err != nil {
		return
	}

	finalConfig, installationQuit, err := attendedInstaller.Run()
	installDetails.finalConfig = finalConfig
	installDetails.installationQuit = installationQuit
	return
}

func terminalAttendedInstall(cfg configuration.Config, progress chan int, status chan string, args imagerArguments) (err error) {
	defer close(progress)
	defer close(status)

	logger.Log.Infof("Writing temporary config file to (%s)", args.configFile)
	err = jsonutils.WriteJSONFile(args.configFile, cfg)
	if err != nil {
		return
	}

	onStdout := func(args ...interface{}) {
		const (
			progressPrefix = "progress:"
			actionPrefix   = "action:"
		)

		if len(args) == 0 {
			return
		}

		line := args[0].(string)

		if strings.HasPrefix(line, progressPrefix) {
			reportedProgress, err := strconv.Atoi(strings.TrimPrefix(line, progressPrefix))
			if err != nil {
				logger.Log.Warnf("Failed to convert progress to an integer (%s). Error: %v", line, err)
				return
			}

			progress <- reportedProgress
		} else if strings.HasPrefix(line, actionPrefix) {
			status <- strings.TrimPrefix(line, actionPrefix)
		}
	}

	args.emitProgress = true
	program, commandArgs := formatImagerCommand(args)
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, false, program, commandArgs...)

	return
}

func unattendedInstall(configFile string, args imagerArguments) (installDetails installationDetails, err error) {
	const squashErrors = false

	args.configFile = configFile

	installDetails.finalConfig, err = configuration.Load(configFile)
	if err != nil {
		installDetails.installationQuit = true
		return
	}
	program, commandArgs := formatImagerCommand(args)
	err = shell.ExecuteLive(squashErrors, program, commandArgs...)
	return
}

func formatImagerCommand(args imagerArguments) (program string, commandArgs []string) {
	program = args.imagerTool

	commandArgs = []string{
		"--live-install",
		fmt.Sprintf("--input=%s", args.configFile),
		fmt.Sprintf("--build-dir=%s", args.buildDir),
		fmt.Sprintf("--base-dir=%s", args.baseDirPath),
		fmt.Sprintf("--log-file=%s", args.logFile),
		fmt.Sprintf("--log-level=%s", args.logLevel),
	}

	if args.emitProgress {
		commandArgs = append(commandArgs, "--emit-progress")
	}

	return
}
