// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
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
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

var (
	selinuxArgNames = []string{"security", "selinux", "enforcing"}

	// Finds the SELinux mode line in the /etc/selinux/config file.
	selinuxConfigModeRegex = regexp.MustCompile(`(?m)^SELINUX=(\w+)$`)
)

const (
	linuxCommand  = "linux"
	initrdCommand = "initrd"
	// The index of the SELinux mode value.
	selinuxConfigModeRegexSELinuxMode = 1
)

// Looks for all occurences of a command with the provided name.
// Returns the lines containing the command.
func findGrubCommandAll(inputGrubCfgContent string, commandName string, allowMultiple bool) ([]grub.Line, error) {
	grubTokens, err := grub.TokenizeConfig(inputGrubCfgContent)
	if err != nil {
		return nil, err
	}

	grubLines := grub.SplitTokensIntoLines(grubTokens)
	lines := grub.FindCommandAll(grubLines, commandName)
	if len(lines) < 1 {
		return nil, fmt.Errorf("failed to find the '%s' command in grub config", commandName)
	}
	if !allowMultiple {
		if len(lines) > 1 {
			return nil, fmt.Errorf("more than one '%s' command in grub config", commandName)
		}
	}

	return lines, nil
}

// Finds all search command occurences and replaces them.
func replaceSearchCommandAll(inputGrubCfgContent string, newSearchCommand string) (outputGrubCfgContent string, err error) {
	lines, err := findGrubCommandAll(inputGrubCfgContent, "search", true /*allowMultiple*/)
	if err != nil {
		return "", err
	}
	outputGrubCfgContent = inputGrubCfgContent
	// loop from last to first so that the captured locations from
	// findGrubCommandAll are not invalidated as reconstructing
	// outputGrubCfgContent.
	for i := len(lines) - 1; i >= 0; i-- {
		line := lines[i]
		start := line.Tokens[0].Loc.Start.Index
		end := line.EndToken.Loc.Start.Index
		outputGrubCfgContent = outputGrubCfgContent[:start] + newSearchCommand + outputGrubCfgContent[end:]
	}

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

// Find all occurences of the initrd or kernel command within the grub config file.
func findLinuxOrInitrdLineAll(inputGrubCfgContent string, commandName string, allowMultiple bool) ([]grub.Line, error) {
	lines, err := findGrubCommandAll(inputGrubCfgContent, commandName, allowMultiple)
	if err != nil {
		return nil, err
	}
	for i := 0; i < len(lines); i++ {
		if len(lines[i].Tokens) < 2 {
			return nil, fmt.Errorf("grub config '%s' command is missing file path arg", commandName)
		}
	}

	return lines, nil
}

// Find the linux command within the grub config file.
func findLinuxLine(inputGrubCfgContent string) (grub.Line, error) {
	lines, err := findLinuxOrInitrdLineAll(inputGrubCfgContent, linuxCommand, false /*allowMultiple*/)
	if err != nil {
		return grub.Line{}, err
	}
	return lines[0], nil
}

// Overrides the path of the kernel binary of all the linux commands within a grub config file.
func setLinuxOrInitrdPathAll(inputGrubCfgContent string, commandName string, filePath string, allowMultiple bool) (outputGrubCfgContent string, oldFilePaths []string, err error) {
	quotedFilePath := grub.QuoteString(filePath)

	lines, err := findLinuxOrInitrdLineAll(inputGrubCfgContent, commandName, allowMultiple)
	if err != nil {
		return "", nil, err
	}

	outputGrubCfgContent = inputGrubCfgContent
	// loop from last to first so that the captured locations from
	// findGrubCommandAll are not invalidated as reconstructing
	// outputGrubCfgContent.
	for i := len(lines) - 1; i >= 0; i-- {
		line := lines[i]
		linuxFilePathToken := line.Tokens[1]
		start := linuxFilePathToken.Loc.Start.Index
		end := linuxFilePathToken.Loc.End.Index

		oldFilePaths = append(oldFilePaths, inputGrubCfgContent[start:end])
		outputGrubCfgContent = outputGrubCfgContent[:start] + quotedFilePath + outputGrubCfgContent[end:]
	}

	return outputGrubCfgContent, oldFilePaths, nil
}

// Overrides the path of the kernel binary of the linux command within a grub config file.
func setLinuxPath(inputGrubCfgContent string, linuxPath string) (outputGrubCfgContent string, oldKernelPath string, err error) {
	outputGrubCfgContent, oldKernelPaths, err := setLinuxOrInitrdPathAll(inputGrubCfgContent, linuxCommand, linuxPath, false /*allowMultiple*/)
	if err != nil {
		return "", "", err
	}
	return outputGrubCfgContent, oldKernelPaths[0], nil
}

// Overrides the path of the initramfs file of the initrd command within a grub config file.
func setInitrdPath(inputGrubCfgContent string, initrdPath string) (outputGrubCfgContent string, oldInitrdPath string, err error) {
	outputGrubCfgContent, oldInitrdPaths, err := setLinuxOrInitrdPathAll(inputGrubCfgContent, initrdCommand, initrdPath, false /*allowMultiple*/)
	if err != nil {
		return "", "", err
	}
	return outputGrubCfgContent, oldInitrdPaths[0], nil
}

// Appends kernel command-line args to the linux command within a grub config file.
// If $kernelopts is present, extraCommandLine is inserted before $kernelopts.
// If $kernelopts is not present, extraCommandLine is appended at the end.
func appendKernelCommandLineArgsAll(inputGrubCfgContent string, extraCommandLine string,
	allowMultiple bool, requireKernelOpts bool) (outputGrubCfgContent string, err error) {
	lines, err := findLinuxOrInitrdLineAll(inputGrubCfgContent, linuxCommand, allowMultiple)
	if err != nil {
		return "", err
	}

	outputGrubCfgContent = inputGrubCfgContent
	// loop from last to first so that the captured locations from
	// findGrubCommandAll are not invalidated as reconstructing
	// outputGrubCfgContent.
	for i := len(lines) - 1; i >= 0; i-- {
		line := lines[i]

		// Skip the "linux" command and the kernel binary path arg.
		argTokens := line.Tokens[2:]

		insertAt, err := findCommandLineInsertAt(argTokens, requireKernelOpts)
		if err != nil {
			return "", err
		}

		leadingSpace := " "
		if requireKernelOpts {
			// When requireKernelOpts is true, we are inserting right before
			// kernelOpts, and there is already an empty space.
			leadingSpace = ""
		}
		outputGrubCfgContent = outputGrubCfgContent[:insertAt] + leadingSpace + extraCommandLine + " " + outputGrubCfgContent[insertAt:]
	}

	return outputGrubCfgContent, nil
}

// Appends kernel command-line args to the linux command within a grub config file.
func appendKernelCommandLineArgs(inputGrubCfgContent string, extraCommandLine string) (outputGrubCfgContent string, err error) {
	return appendKernelCommandLineArgsAll(inputGrubCfgContent, extraCommandLine, false /*allow multiple*/, true /*requireKernelOpts*/)
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
//   - args: A list of kernel command-line arguments.
//   - insertAt: An index that represents an appropriate insert point for any new args.
//     For Azure Linux 2.0 images, this points to the index of the $kernelopts token.
func getLinuxCommandLineArgs(grub2Config string, requireKernelOpts bool) ([]grubConfigLinuxArg, int, error) {
	linuxLine, err := findLinuxOrInitrdLineAll(grub2Config, linuxCommand, false /*allowMultiple*/)
	if err != nil {
		return nil, 0, err
	}

	// Skip the "linux" command and the kernel binary path arg.
	argTokens := linuxLine[0].Tokens[2:]

	insertAt, err := findCommandLineInsertAt(argTokens, requireKernelOpts)
	if err != nil {
		return nil, 0, err
	}

	args, err := parseCommandLineArgs(argTokens)
	if err != nil {
		return nil, 0, err
	}

	return args, insertAt, nil
}

// Takes a tokenized grub.cfg file and looks for an appropriate place to insert new args.
// If $kernelopts is present, it returns its location for insertion.
// If $kernelopts is absent,
// - If requireKernelOpts is true, it fails (could not find required $kernelopts).
// - If requireKernelOpts is false, it returns the location after the last token.
func findCommandLineInsertAt(argTokens []grub.Token, requireKernelOpts bool) (int, error) {
	insertAtTokens := []grub.Token(nil)
	for i := range argTokens {
		argToken := argTokens[i]
		if argToken.Type != grub.WORD {
			return 0, fmt.Errorf("unexpected token (%s) in grub config linux command",
				grub.TokenTypeString(argToken.Type))
		}

		if len(argToken.SubWords) == 1 &&
			argToken.SubWords[0].Type == grub.VAR_EXPANSION &&
			argToken.SubWords[0].Value == grubKernelOpts {
			// Found the $kernelopts arg.
			// Any new args to be inserted, will be inserted immediately before this token.
			insertAtTokens = append(insertAtTokens, argToken)
		}
	}

	if len(insertAtTokens) < 1 {
		// Could not find the grubKernelOpts
		if !requireKernelOpts && len(argTokens) > 0 {
			// Try to insert at the very end as long as there are other tokens.
			return argTokens[len(argTokens)-1].Loc.End.Index, nil
		} else {
			return 0, fmt.Errorf("failed to find $%s in linux command line", grubKernelOpts)
		}
	}
	if len(insertAtTokens) > 1 {
		return 0, fmt.Errorf("too many $%s tokens found in linux command line", grubKernelOpts)
	}

	insertAtToken := insertAtTokens[0]
	insertAt := insertAtToken.Loc.Start.Index
	return insertAt, nil
}

// Takes a tokenized grub.cfg file and makes a best effort to extract the kernel command-line args.
func parseCommandLineArgs(argTokens []grub.Token) ([]grubConfigLinuxArg, error) {
	args := []grubConfigLinuxArg(nil)

	for i := range argTokens {
		argToken := argTokens[i]
		if argToken.Type != grub.WORD {
			return nil, fmt.Errorf("unexpected token (%s) in grub config linux command",
				grub.TokenTypeString(argToken.Type))
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
			// The arg string value isn't known in full because it contains a variable expansion.
			// So, clear the value to avoid the value from being misinterpreted.
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

	return args, nil
}

// Filters a list of kernel command-line args to only those that match the provided list of names.
func findMatchingCommandLineArgs(args []grubConfigLinuxArg, names []string) []grubConfigLinuxArg {
	matching := []grubConfigLinuxArg(nil)

	for _, arg := range args {
		matchedName := sliceutils.ContainsValue(names, arg.Name)
		if matchedName {
			matching = append(matching, arg)
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

func replaceKernelCommandLineArgValueAll(inputGrubCfgContent string, name string, value string, allowMultiple bool,
) (outputGrubCfgContent string, oldValues []string, err error) {
	newArg := fmt.Sprintf("%s=%s", name, value)
	quotedNewArg := grub.QuoteString(newArg)

	lines, err := findLinuxOrInitrdLineAll(inputGrubCfgContent, linuxCommand, allowMultiple)
	if err != nil {
		return "", nil, err
	}

	outputGrubCfgContent = inputGrubCfgContent
	// loop from last to first so that the captured locations from
	// findGrubCommandAll are not invalidated as reconstructing
	// outputGrubCfgContent.
	for i := len(lines) - 1; i >= 0; i-- {
		line := lines[i]

		// Skip the "linux" command and the kernel binary path arg.
		argTokens := line.Tokens[2:]

		args, err := parseCommandLineArgs(argTokens)
		if err != nil {
			return "", nil, err
		}

		foundArgs := findMatchingCommandLineArgs(args, []string{name})
		if len(foundArgs) < 1 {
			return "", nil, fmt.Errorf("failed to find kernel arg (%s)", name)
		}
		if len(foundArgs) > 1 {
			return "", nil, fmt.Errorf("too many instances of kernel arg found (%s)", name)
		}

		arg := foundArgs[0]
		start := arg.Token.Loc.Start.Index
		end := arg.Token.Loc.End.Index

		oldValues = append(oldValues, inputGrubCfgContent[start:end])
		outputGrubCfgContent = outputGrubCfgContent[:start] + quotedNewArg + outputGrubCfgContent[end:]
	}

	return outputGrubCfgContent, oldValues, nil
}

func updateKernelCommandLineArgsAll(grub2Config string, argsToRemove []string, newArgs []string,
	allowMultiple bool, requireKernelOpts bool) (string, error) {
	lines, err := findLinuxOrInitrdLineAll(grub2Config, linuxCommand, allowMultiple /*allowMultiple*/)
	if err != nil {
		return "", err
	}

	// loop from last to first so that the captured locations from
	// findGrubCommandAll are not invalidated as reconstructing
	// outputGrubCfgContent.
	for i := len(lines) - 1; i >= 0; i-- {
		line := lines[i]

		// Skip the "linux" command and the kernel binary path arg.
		argTokens := line.Tokens[2:]

		insertAtToken, err := findCommandLineInsertAt(argTokens, requireKernelOpts)
		if err != nil {
			return "", err
		}

		args, err := parseCommandLineArgs(argTokens)
		if err != nil {
			return "", err
		}

		grub2Config, err = updateKernelCommandLineArgsHelper(grub2Config, args, insertAtToken, argsToRemove, newArgs)
		if err != nil {
			return "", err
		}
	}
	return grub2Config, nil
}

// Finds all the kernel command-line args that match the provided names, then insert replacement arg(s).
//
// Params:
// - grub2Config: The string contents of the grub.cfg file.
// - argsToRemove: A list of arg names to remove from the command-line args.
// - newArgs: A list of new arg values to add to the command-line args.
//
// Output:
// - grub2Config: The new string contents of the grub.cfg file.
func updateKernelCommandLineArgs(grub2Config string, argsToRemove []string, newArgs []string) (string, error) {
	return updateKernelCommandLineArgsAll(grub2Config, argsToRemove, newArgs, false /*allowMultiple*/, true /*requireKernelOpts*/)
}

func updateKernelCommandLineArgsHelper(value string, args []grubConfigLinuxArg, insertAt int,
	argsToRemove []string, newArgs []string,
) (string, error) {
	newArgsQuoted := grubArgsToString(newArgs)
	foundArgs := findMatchingCommandLineArgs(args, argsToRemove)

	builder := strings.Builder{}
	nextIndex := 0

	if len(foundArgs) > 0 {
		// Rewrite the grub config with all the found args removed.
		for _, arg := range foundArgs {
			start := arg.Token.Loc.Start.Index
			end := arg.Token.Loc.End.Index
			builder.WriteString(value[nextIndex:start])
			nextIndex = end
		}

		// Insert the new arg at the location of the last arg.
		builder.WriteString(newArgsQuoted)
	} else {
		// Write out the grub config to the point where the new arg will be inserted.
		builder.WriteString(value[nextIndex:insertAt])
		nextIndex = insertAt

		// Insert the new arg.
		builder.WriteString(" ")
		builder.WriteString(newArgsQuoted)
		builder.WriteString(" ")
	}

	// Write out the remainder of the grub config.
	builder.WriteString(value[nextIndex:])

	value = builder.String()
	return value, nil
}

// Takes a list of unescaped and unquoted kernel command-line args and combines them into a single string with
// appropriate quoting for a grub.cfg file.
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

// Converts an SELinux mode into the list of required command-line args for that mode.
func selinuxModeToArgs(selinuxMode imagecustomizerapi.SELinuxMode) ([]string, error) {
	newSELinuxArgs := []string(nil)
	switch selinuxMode {
	case imagecustomizerapi.SELinuxModeDisabled:
		newSELinuxArgs = []string{installutils.CmdlineSELinuxDisabledArg}

	case imagecustomizerapi.SELinuxModeForceEnforcing:
		newSELinuxArgs = []string{installutils.CmdlineSELinuxSecurityArg, installutils.CmdlineSELinuxEnabledArg,
			installutils.CmdlineSELinuxEnforcingArg}

	case imagecustomizerapi.SELinuxModePermissive, imagecustomizerapi.SELinuxModeEnforcing:
		newSELinuxArgs = []string{installutils.CmdlineSELinuxSecurityArg, installutils.CmdlineSELinuxEnabledArg}

	default:
		return nil, fmt.Errorf("unknown SELinux mode (%s)", selinuxMode)
	}

	return newSELinuxArgs, nil
}

// Update the SELinux kernel command-line args.
func updateSELinuxCommandLineHelperAll(grub2Config string, selinuxMode imagecustomizerapi.SELinuxMode, allowMultiple bool, requireKernelOpts bool) (string, error) {
	newSELinuxArgs, err := selinuxModeToArgs(selinuxMode)
	if err != nil {
		return "", err
	}

	grub2Config, err = updateKernelCommandLineArgsAll(grub2Config, selinuxArgNames, newSELinuxArgs, allowMultiple, requireKernelOpts)
	if err != nil {
		return "", err
	}

	return grub2Config, nil
}

// Finds a set command that sets the variable with the provided name and then change the value that is set.
func replaceSetCommandValue(grub2Config string, varName string, newValue string) (string, error) {
	quotedNewValue := grub.QuoteString(newValue)

	grubTokens, err := grub.TokenizeConfig(grub2Config)
	if err != nil {
		return "", err
	}

	grubLines := grub.SplitTokensIntoLines(grubTokens)
	setLines := grub.FindCommandAll(grubLines, "set")

	// Search for all the set commands that set the variable.
	setVarLines := []grub.Line(nil)
	for _, line := range setLines {
		if len(line.Tokens) < 2 {
			return "", fmt.Errorf("grub config has a set command that has zero args")
		}

		argToken := line.Tokens[1]
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
	argToken := setVarLine.Tokens[1]
	start := argToken.Loc.Start.Index
	end := argToken.Loc.End.Index
	grub2Config = fmt.Sprintf("%s%s=%s%s", grub2Config[:start], varName, quotedNewValue, grub2Config[end:])

	return grub2Config, nil
}

// Takes a list of kernel command-line args and calculates the SELinux mode that is set.
// If the command-line args delegate the SELinux mode to the /etc/selinux/config file, then SELinuxModeDefault ("") is
// returned.
func getSELinuxModeFromLinuxArgs(args []grubConfigLinuxArg) (imagecustomizerapi.SELinuxMode, error) {
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

	// The SELinux mode has been left up to the /etc/selinux/config file.
	// Signal this by returning the default ("") value.
	return imagecustomizerapi.SELinuxModeDefault, nil
}

// Gets the SELinux mode set by the /etc/selinux/config file.
func getSELinuxModeFromConfigFile(imageChroot safechroot.ChrootInterface) (imagecustomizerapi.SELinuxMode, error) {
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

// Reads the /boot/grub2/grub.cfg file.
func readGrub2ConfigFile(imageChroot safechroot.ChrootInterface) (string, error) {
	logger.Log.Debugf("Reading grub.cfg file")

	grub2ConfigFilePath := getGrub2ConfigFilePath(imageChroot)

	// Read the existing grub.cfg file.
	grub2Config, err := file.Read(grub2ConfigFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to read grub2 config file (%s):\n%w", installutils.GrubCfgFile, err)
	}

	return grub2Config, nil
}

// Writes the /boot/grub2/grub.cfg file.
func writeGrub2ConfigFile(grub2Config string, imageChroot safechroot.ChrootInterface) error {
	logger.Log.Debugf("Writing grub.cfg file")

	grub2ConfigFilePath := getGrub2ConfigFilePath(imageChroot)

	// Update grub.cfg file.
	err := file.Write(grub2Config, grub2ConfigFilePath)
	if err != nil {
		return fmt.Errorf("failed to write grub2 config file (%s):\n%w", installutils.GrubCfgFile, err)
	}

	return nil
}

func getGrub2ConfigFilePath(imageChroot safechroot.ChrootInterface) string {
	return filepath.Join(imageChroot.RootDir(), installutils.GrubCfgFile)
}

// Regenerates the initramfs file.
func regenerateInitrd(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Regenerate initramfs file")

	err := imageChroot.UnsafeRun(func() error {
		// The 'mkinitrd' command was removed in Azure Linux 3.0 in favor of using 'dracut' directly.
		mkinitrdExists, err := file.CommandExists("mkinitrd")
		if err != nil {
			return fmt.Errorf("failed to search for mkinitrd command:\n%w", err)
		}

		if mkinitrdExists {
			return shell.ExecuteLiveWithErr(1, "mkinitrd")
		} else {
			return shell.ExecuteLiveWithErr(1, "dracut", "--force", "--regenerate-all")
		}
	})
	if err != nil {
		return fmt.Errorf("failed to rebuild initramfs file:\n%w", err)
	}

	return nil
}
