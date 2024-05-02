// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/grub"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

var (
	// Finds the SELinux mode line in the /etc/selinux/config file.
	selinuxConfigModeRegex = regexp.MustCompile(`(?m)^SELINUX=(\w+)$`)
)

const (
	// The index of the SELinux mode value.
	selinuxConfigModeRegexSELinuxMode = 1
)

// Looks for a command with the provided name and ensures there is only 1 such command.
// Returns the line of the found command.
func findSingularGrubCommand(inputGrubCfgContent string, commandName string) ([]grub.Token, error) {
	grubTokens, err := grub.TokenizeGrubConfig(inputGrubCfgContent)
	if err != nil {
		return nil, err
	}

	grubLines := grub.SplitTokensIntoLines(grubTokens)
	lines := grub.FindCommandAll(grubLines, commandName)
	if len(lines) < 1 {
		return nil, fmt.Errorf("failed to find the '%s' command in grub config", commandName)
	}
	if len(lines) > 1 {
		return nil, fmt.Errorf("more than one '%s' command in grub config", commandName)
	}

	line := lines[0]
	return line, nil
}

// Finds the search command and replaces it.
func replaceSearchCommand(inputGrubCfgContent string, searchCommand string) (outputGrubCfgContent string, err error) {
	searchLine, err := findSingularGrubCommand(inputGrubCfgContent, "search")
	if err != nil {
		return "", err
	}

	start := searchLine[0].Loc.Start.Index
	end := searchLine[len(searchLine)-1].Loc.Start.Index
	outputGrubCfgContent = inputGrubCfgContent[:start] + searchCommand + inputGrubCfgContent[end:]

	return outputGrubCfgContent, nil
}

func replaceToken(inputGrubCfgContent string, oldToken string, newToken string) (outputGrubCfgContent string, err error) {

	// escape special characters that would interfer with defining the regular
	// expression correctly.
	tokenRegexpString := regexp.QuoteMeta(oldToken)

	// ensure the string is preceeded with separator (\t or a ' ') and create
	// a group.
	tokenRegexpString = "(?m)[\\t ](" + tokenRegexpString + ")[\\t ]"

	// create the regular expression
	tokenReplacementPath, err := regexp.Compile(tokenRegexpString)
	if err != nil {
		return "", fmt.Errorf("failed to compile regular expression (%s)", tokenRegexpString)
	}

	match := tokenReplacementPath.FindStringSubmatchIndex(inputGrubCfgContent)
	if match == nil {
		return inputGrubCfgContent, nil
	}
	for i := 2; i+1 < len(match); i = i + 2 {
		start := match[i]
		end := match[i+1]

		outputGrubCfgContent = inputGrubCfgContent[:start] + newToken + inputGrubCfgContent[end:]
	}
	return outputGrubCfgContent, nil
}

// Find the linux command within the grub config file.
func findLinuxLine(inputGrubCfgContent string) ([]grub.Token, error) {
	linuxLine, err := findSingularGrubCommand(inputGrubCfgContent, "linux")
	if err != nil {
		return nil, err
	}

	if len(linuxLine) < 2 {
		return nil, fmt.Errorf("grub config 'linux' command is missing file path arg")
	}

	return linuxLine, nil
}

// Overrides the path of the kernel binary of the linux command within a grub config file.
func setLinuxPath(inputGrubCfgContent string, linuxPath string) (outputGrubCfgContent string, oldKernelPath string, err error) {
	quotedLinuxPath := grub.QuoteString(linuxPath)

	linuxLine, err := findLinuxLine(inputGrubCfgContent)
	if err != nil {
		return "", "", err
	}

	linuxFilePathToken := linuxLine[1]
	start := linuxFilePathToken.Loc.Start.Index
	end := linuxFilePathToken.Loc.End.Index

	oldKernelPath = inputGrubCfgContent[start:end]
	outputGrubCfgContent = inputGrubCfgContent[:start] + quotedLinuxPath + inputGrubCfgContent[end:]

	return outputGrubCfgContent, oldKernelPath, nil
}

// Overrides the path of the initramfs file of the initrd command within a grub config file.
func setInitrdPath(inputGrubCfgContent string, initrdPath string) (outputGrubCfgContent string, oldInitrdPath string, err error) {
	quotedInitrdPath := grub.QuoteString(initrdPath)

	line, err := findSingularGrubCommand(inputGrubCfgContent, "initrd")
	if err != nil {
		return "", "", err
	}

	if len(line) < 2 {
		return "", "", fmt.Errorf("grub config 'initrd' command is missing file path arg")
	}

	initrdFilePathToken := line[1]
	start := initrdFilePathToken.Loc.Start.Index
	end := initrdFilePathToken.Loc.End.Index

	oldInitrdPath = inputGrubCfgContent[start:end]
	outputGrubCfgContent = inputGrubCfgContent[:start] + quotedInitrdPath + inputGrubCfgContent[end:]

	return outputGrubCfgContent, oldInitrdPath, nil
}

// Appends kernel command-line args to the linux command within a grub config file.
func appendKernelCommandLineArguments(inputGrubCfgContent string, extraCommandLine string) (outputGrubCfgContent string, err error) {
	_, insertAtToken, err := getLinuxCommandLineArgs(inputGrubCfgContent)
	if err != nil {
		return "", err
	}

	// Insert args at the end of the line.
	insertPoint := insertAtToken.Loc.Start.Index
	outputGrubCfgContent = inputGrubCfgContent[:insertPoint] + extraCommandLine + " " + inputGrubCfgContent[insertPoint:]
	return outputGrubCfgContent, nil
}

type grubConfigLinuxArg struct {
	// The tokenizer token for the arg.
	Token grub.Token
	// The name of the argument.
	Name string
	// The value of the argument.
	Value string
	// If the argument's value has a variable expansion (e.g. $a).
	ValueHasVarExpansion bool
}

// Finds the linux command within a grub config and returns a list of kernel command-line arguments.
//
// Returns:
// - args: A list of kernel command-line arguments.
// - insertToken: A tokenizer token that represents an appropriate insert point for any new args.
func getLinuxCommandLineArgs(grub2Config string) ([]grubConfigLinuxArg, grub.Token, error) {
	linuxLine, err := findLinuxLine(grub2Config)
	if err != nil {
		return nil, grub.Token{}, err
	}

	// Skip the "linux" command and the kernel binary path arg.
	argTokens := linuxLine[2:]

	args := []grubConfigLinuxArg(nil)
	insertAtToken := (*grub.Token)(nil)

	for i := range argTokens {
		argToken := argTokens[i]
		if argToken.Type != grub.WORD {
			return nil, grub.Token{}, fmt.Errorf("unexpected token (%s) in grub config linux command",
				grub.TokenTypeString(argToken.Type))
		}

		if len(argToken.SubWords) == 1 &&
			argToken.SubWords[0].Type == grub.VAR_EXPANSION &&
			argToken.SubWords[0].Value == "kernelopts" {
			// Found the $kernelopts arg.
			// Any new args to be inserted, will be inserted immediately before this token.
			insertAtToken = &argToken
		}

		hasVarExpansion := false
		argStringBuilder := strings.Builder{}

	subWordsLoop:
		for _, subword := range argToken.SubWords {
			switch subword.Type {
			case grub.KEYWORD_STRING, grub.STRING:
				argStringBuilder.WriteString(subword.Value)

			case grub.QUOTED_VAR_EXPANSION, grub.VAR_EXPANSION:
				// There is a variable expansion (e.g. $a) in the arg.
				// Stop here because we don't know what value to fill in for the variable.
				hasVarExpansion = true
				break subWordsLoop
			}
		}

		argString := argStringBuilder.String()
		name, value, foundEqSymbol := strings.Cut(argString, "=")
		if !foundEqSymbol && hasVarExpansion {
			// Arg has a variable expansion (e.g. $a) that is part of the arg name.
			// There isn't any easy way to handle such args. So, just ignore them.
			continue
		}

		if hasVarExpansion {
			// The arg string value isn't known because it contains a variable expansion.
			value = ""
		}

		arg := grubConfigLinuxArg{
			Token:                argToken,
			Name:                 name,
			Value:                value,
			ValueHasVarExpansion: hasVarExpansion,
		}
		args = append(args, arg)
	}

	if insertAtToken == nil {
		return nil, grub.Token{}, fmt.Errorf("failed to find $kernelopts in linux command line")
	}

	return args, *insertAtToken, nil
}

// Filters a list of kernel command-line args to only those that match the provides list of names.
func findMatchingCommandLineArgs(args []grubConfigLinuxArg, names []string) []grubConfigLinuxArg {
	matching := []grubConfigLinuxArg(nil)

argsLoop:
	for _, arg := range args {
		for _, name := range names {
			if arg.Name == name {
				matching = append(matching, arg)
				continue argsLoop
			}
		}
	}

	return matching
}

// Tries to find the specified kernel CLI arg. Does not fail if the arg is not found.
//
// Returns:
// - value: The value of the arg. Or "" if not found.
func findKernelCommandLineArgValue(args []grubConfigLinuxArg, name string) (string, error) {
	foundArgs := findMatchingCommandLineArgs(args, []string{name})
	if len(foundArgs) <= 0 {
		return "", nil
	}

	lastArg := foundArgs[len(foundArgs)-1]
	if lastArg.ValueHasVarExpansion {
		return "", fmt.Errorf("kernel arg (%s) has variable expansion in value", name)
	}

	return lastArg.Value, nil
}

// Finds an existing kernel command-line arg and replaces its value.
func replaceKernelCommandLineArgumentValue(inputGrubCfgContent string, name string, value string,
) (outputGrubCfgContent string, oldValue string, err error) {
	newArg := fmt.Sprintf("%s=%s", name, value)
	quotedNewArg := grub.QuoteString(newArg)

	args, _, err := getLinuxCommandLineArgs(inputGrubCfgContent)
	if err != nil {
		return "", "", err
	}

	foundArgs := findMatchingCommandLineArgs(args, []string{name})
	if len(foundArgs) < 1 {
		return "", "", fmt.Errorf("failed to find kernel arg (%s)", name)
	}
	if len(foundArgs) > 1 {
		return "", "", fmt.Errorf("too many instances of kernel arg found (%s)", name)
	}

	arg := foundArgs[0]
	start := arg.Token.Loc.Start.Index
	end := arg.Token.Loc.End.Index

	outputGrubCfgContent = inputGrubCfgContent[:start] + quotedNewArg + inputGrubCfgContent[end:]

	return outputGrubCfgContent, oldValue, nil
}

// Inserts new kernel command-line args into the grub config file.
func addKernelCommandLine(kernelExtraArguments imagecustomizerapi.KernelExtraArguments,
	imageChroot *safechroot.Chroot,
) error {
	var err error

	extraCommandLine := strings.TrimSpace(string(kernelExtraArguments))
	if extraCommandLine == "" {
		// Nothing to do.
		return nil
	}

	logger.Log.Infof("Setting KernelCommandLine.ExtraCommandLine")

	grub2ConfigFile, err := readGrub2ConfigFile(imageChroot)
	if err != nil {
		return err
	}

	newGrub2ConfigFile, err := appendKernelCommandLineArguments(grub2ConfigFile, extraCommandLine)
	if err != nil {
		return err
	}

	// Update grub.cfg file.
	err = writeGrub2ConfigFile(newGrub2ConfigFile, imageChroot)
	if err != nil {
		return err
	}

	return nil
}

// Updates the kernel command-line args with the new SELinux mode.
//
// See, installutils.setGrubCfgSELinux()
func updateSELinuxCommandLine(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Updating SELinux kernel command-line args")

	grub2Config, err := readGrub2ConfigFile(imageChroot)
	if err != nil {
		return err
	}

	newGrub2Config, err := updateSELinuxCommandLineHelper(grub2Config, selinuxMode)
	if err != nil {
		return err
	}

	// Update grub.cfg file.
	err = writeGrub2ConfigFile(newGrub2Config, imageChroot)
	if err != nil {
		return err
	}

	return nil
}

// Finds all the kernel command-line args that match the provided names, then insert replacement arg(s).
func updateKernelCommandLineArguments(grub2Config string, argsToRemove []string, newArgs []string) (string, error) {
	newArgsQuoted := grubArgsToString(newArgs)

	args, insertAtToken, err := getLinuxCommandLineArgs(grub2Config)
	if err != nil {
		return "", err
	}

	foundArgs := findMatchingCommandLineArgs(args, argsToRemove)

	grub2ConfigBuilder := strings.Builder{}
	nextIndex := 0

	if len(foundArgs) > 0 {
		// Rewrite the grub config with all the found args removed.
		for _, arg := range foundArgs {
			start := arg.Token.Loc.Start.Index
			end := arg.Token.Loc.End.Index
			grub2ConfigBuilder.WriteString(grub2Config[nextIndex:start])
			nextIndex = end
		}

		// Insert the new arg at the location of the last arg.
		grub2ConfigBuilder.WriteString(newArgsQuoted)
	} else {
		// Write out the grub config to the point where the new arg will be inserted.
		insertAt := insertAtToken.Loc.Start.Index
		grub2ConfigBuilder.WriteString(grub2Config[nextIndex:insertAt])
		nextIndex = insertAt

		// Insert the new arg.
		grub2ConfigBuilder.WriteString(newArgsQuoted)
		grub2ConfigBuilder.WriteString(" ")
	}

	// Write out the remainder of the grub config.
	grub2ConfigBuilder.WriteString(grub2Config[nextIndex:])

	grub2Config = grub2ConfigBuilder.String()
	return grub2Config, nil
}

func grubArgsToString(args []string) string {
	builder := strings.Builder{}
	for i, arg := range args {
		if i != 0 {
			builder.WriteString(" ")
		}

		quotedArg := grub.QuoteString(arg)
		builder.WriteString(quotedArg)
	}

	combinedString := builder.String()
	return combinedString
}

// Update the SELinux kernel command-line args.
func updateSELinuxCommandLineHelper(grub2Config string, selinuxMode imagecustomizerapi.SELinuxMode) (string, error) {
	newSELinuxArgs := []string(nil)
	switch selinuxMode {
	case imagecustomizerapi.SELinuxModeDisabled:
		newSELinuxArgs = nil

	case imagecustomizerapi.SELinuxModeForceEnforcing:
		newSELinuxArgs = []string{installutils.CmdlineSELinuxSecurityArg, installutils.CmdlineSELinuxEnabledArg,
			installutils.CmdlineSELinuxEnforcingArg}

	case imagecustomizerapi.SELinuxModePermissive, imagecustomizerapi.SELinuxModeEnforcing:
		newSELinuxArgs = []string{installutils.CmdlineSELinuxSecurityArg, installutils.CmdlineSELinuxEnabledArg}

	default:
		return "", fmt.Errorf("unknown SELinux mode (%s)", selinuxMode)
	}

	grub2Config, err := updateKernelCommandLineArguments(grub2Config, []string{"security", "selinux", "enforcing"},
		newSELinuxArgs)
	if err != nil {
		return "", err
	}

	return grub2Config, nil
}

// Finds a set command that sets the variable with the provided name and then change the value that is set.
func replaceSetCommandValue(grub2Config string, varName string, newValue string) (string, error) {
	quotedNewValue := grub.QuoteString(newValue)

	grubTokens, err := grub.TokenizeGrubConfig(grub2Config)
	if err != nil {
		return "", err
	}

	grubLines := grub.SplitTokensIntoLines(grubTokens)
	setLines := grub.FindCommandAll(grubLines, "set")

	// Search for all the set commands that set the variable.
	setVarLines := [][]grub.Token(nil)
	for _, line := range setLines {
		if len(line) < 2 {
			return "", fmt.Errorf("grub config has a set command that has zero args")
		}

		argToken := line[1]
		argStringBuilder := strings.Builder{}

		// Get the name of the variable being set.
	subWordsLoop:
		for _, subword := range argToken.SubWords {
			switch subword.Type {
			case grub.KEYWORD_STRING, grub.STRING:
				argStringBuilder.WriteString(subword.Value)

			case grub.QUOTED_VAR_EXPANSION, grub.VAR_EXPANSION:
				// There is a variable expansion (e.g. $a) in the arg.
				// If the variable is only in the value portion (i.e. after the = symbol), then the set command can
				// still be replaced.
				break subWordsLoop
			}
		}

		argValue := argStringBuilder.String()
		name, _, foundEq := strings.Cut(argValue, "=")
		if !foundEq {
			return "", fmt.Errorf("grub config has a set command that doesn't have an equals symbol")
		}

		// Check if the name matches.
		if name == varName {
			setVarLines = append(setVarLines, line)
		}
	}

	// Ensure there is only 1 set command.
	if len(setVarLines) < 1 {
		return "", fmt.Errorf("failed to find grub config set command for variable (%s)", varName)
	}
	if len(setVarLines) > 1 {
		return "", fmt.Errorf("grub config has more than 1 set command for variable (%s)", varName)
	}

	setVarLine := setVarLines[0]

	// Override set command.
	argToken := setVarLine[1]
	start := argToken.Loc.Start.Index
	end := argToken.Loc.End.Index
	grub2Config = fmt.Sprintf("%s%s=%s%s", grub2Config[:start], varName, quotedNewValue, grub2Config[end:])

	return grub2Config, nil
}

// Gets the current SELinux mode of an image.
func getCurrentSELinuxMode(imageChroot *safechroot.Chroot) (imagecustomizerapi.SELinuxMode, error) {
	logger.Log.Debugf("Get existing SELinux mode")

	grub2Config, err := readGrub2ConfigFile(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	args, _, err := getLinuxCommandLineArgs(grub2Config)
	if err != nil {
		return "", err
	}

	// Try to find any existing SELinux args.
	securityValue, err := findKernelCommandLineArgValue(args, "security")
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	selinuxValue, err := findKernelCommandLineArgValue(args, "selinux")
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	enforcingValue, err := findKernelCommandLineArgValue(args, "enforcing")
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	// Check if SELinux is disabled.
	if securityValue != "selinux" || selinuxValue != "1" {
		return imagecustomizerapi.SELinuxModeDisabled, nil
	}

	// Check if SELinux is in forced enforcing mode.
	if enforcingValue == "1" {
		return imagecustomizerapi.SELinuxModeForceEnforcing, nil
	}

	selinuxMode, err := getSELinuxModeFromConfigFile(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	return selinuxMode, nil
}

func getSELinuxModeFromConfigFile(imageChroot *safechroot.Chroot) (imagecustomizerapi.SELinuxMode, error) {
	selinuxConfigFilePath := filepath.Join(imageChroot.RootDir(), installutils.SELinuxConfigFile)

	// Read the SELinux config file.
	selinuxConfig, err := file.Read(selinuxConfigFilePath)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, fmt.Errorf("failed to read SELinux config file (%s):\n%w",
			installutils.SELinuxConfigFile, err)
	}

	match := selinuxConfigModeRegex.FindStringSubmatch(selinuxConfig)
	if match == nil {
		return imagecustomizerapi.SELinuxModeDefault, fmt.Errorf("failed to find SELinux mode in (%s) file",
			installutils.SELinuxConfigFile)
	}

	selinuxConfigMode := match[selinuxConfigModeRegexSELinuxMode]

	switch selinuxConfigMode {
	case installutils.SELinuxConfigEnforcing:
		return imagecustomizerapi.SELinuxModeEnforcing, nil

	case installutils.SELinuxConfigPermissive:
		return imagecustomizerapi.SELinuxModePermissive, nil

	case installutils.SELinuxConfigDisabled:
		return imagecustomizerapi.SELinuxModeDisabled, nil

	default:
		return imagecustomizerapi.SELinuxModeDefault, fmt.Errorf("unknown SELinux mode (%s) found in (%s) file",
			selinuxConfigMode, installutils.SELinuxConfigFile)
	}
}

func readGrub2ConfigFile(imageChroot *safechroot.Chroot) (string, error) {
	logger.Log.Debugf("Reading grub.cfg file")

	grub2ConfigFilePath := getGrub2ConfigFilePath(imageChroot)

	// Read the existing grub.cfg file.
	grub2Config, err := file.Read(grub2ConfigFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to read existing grub2 config file (%s):\n%w", installutils.GrubCfgFile, err)
	}

	return grub2Config, nil
}

func writeGrub2ConfigFile(grub2Config string, imageChroot *safechroot.Chroot) error {
	logger.Log.Debugf("Writing grub.cfg file")

	grub2ConfigFilePath := getGrub2ConfigFilePath(imageChroot)

	// Update grub.cfg file.
	err := os.WriteFile(grub2ConfigFilePath, []byte(grub2Config), 0)
	if err != nil {
		return fmt.Errorf("failed to write new grub2 config file (%s):\n%w", installutils.GrubCfgFile, err)
	}

	return nil
}

func getGrub2ConfigFilePath(imageChroot *safechroot.Chroot) string {
	return filepath.Join(imageChroot.RootDir(), installutils.GrubCfgFile)
}

func regenerateInitrd(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Regenerate initramfs file")

	err := imageChroot.Run(func() error {
		return shell.ExecuteLiveWithErr(1, "mkinitrd")
	})
	if err != nil {
		return fmt.Errorf("failed to rebuild initramfs file:\n%w", err)
	}

	return nil
}
