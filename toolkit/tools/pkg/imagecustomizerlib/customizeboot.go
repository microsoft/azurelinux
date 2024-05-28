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
	// The index of the SELinux mode value.
	selinuxConfigModeRegexSELinuxMode = 1
)

// Looks for a command with the provided name and ensures there is only 1 such command.
// Returns the line of the found command.
func findSingularGrubCommand(inputGrubCfgContent string, commandName string) ([]grub.Token, error) {
	grubTokens, err := grub.TokenizeConfig(inputGrubCfgContent)
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

func findGrubCommand(inputGrubCfgContent string, commandName string) ([][]grub.Token, error) {
	grubTokens, err := grub.TokenizeConfig(inputGrubCfgContent)
	if err != nil {
		return nil, err
	}

	grubLines := grub.SplitTokensIntoLines(grubTokens)
	lines := grub.FindCommandAll(grubLines, commandName)
	if len(lines) < 1 {
		return nil, fmt.Errorf("failed to find the '%s' command in grub config", commandName)
	}

	return lines, nil
}

// Finds the search command and replaces it.
func replaceSearchCommands(inputGrubCfgContent string, newSearchCommand string) (outputGrubCfgContent string, err error) {
	searchLines, err := findGrubCommand(inputGrubCfgContent, "search")
	if err != nil {
		return "", err
	}

	logger.Log.Debugf("---- new search string: (%s)", newSearchCommand)
	outputGrubCfgContent = inputGrubCfgContent

	if len(searchLines) > 0 {
		logger.Log.Debugf("---- found: %d lines", len(searchLines))
		for i := len(searchLines) - 1; i >= 0; i = i - 1 {
			start := searchLines[i][0].Loc.Start.Index
			end := searchLines[i][len(searchLines[i])-1].Loc.End.Index

			logger.Log.Debugf("---- line: %d {%d-%d}", i, start, end)
			logger.Log.Debugf("---- line:    start: (%s)", searchLines[i][0].RawContent)
			logger.Log.Debugf("---- line:    end  : (%s)", searchLines[i][len(searchLines[i])-1].RawContent)

			outputGrubCfgContent = outputGrubCfgContent[:start] + newSearchCommand + outputGrubCfgContent[end:]
		}
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

func findLinuxLines(inputGrubCfgContent string) ([][]grub.Token, error) {
	linuxLines, err := findGrubCommand(inputGrubCfgContent, "linux")
	if err != nil {
		return nil, err
	}

	if len(linuxLines) > 0 {
		logger.Log.Debugf("---- found linux: %d lines", len(linuxLines))
		for i := len(linuxLines) - 1; i >= 0; i = i - 1 {
			if len(linuxLines[i]) < 2 {
				return nil, fmt.Errorf("grub config 'linux' command is missing file path arg")
			}
		}
	}

	return linuxLines, nil
}

func findInitrdLines(inputGrubCfgContent string) ([][]grub.Token, error) {
	initrdLines, err := findGrubCommand(inputGrubCfgContent, "initrd")
	if err != nil {
		return nil, err
	}

	if len(initrdLines) > 0 {
		logger.Log.Debugf("---- found initrd: %d lines", len(initrdLines))
		for i := len(initrdLines) - 1; i >= 0; i = i - 1 {
			if len(initrdLines[i]) < 2 {
				return nil, fmt.Errorf("grub config 'initrd' command is missing file path arg")
			}
		}
	}

	return initrdLines, nil
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

// Overrides the path of the kernel binary of the linux command within a grub config file.
func setLinuxPaths(inputGrubCfgContent string, linuxPath string) (outputGrubCfgContent string, oldKernelPaths []string, err error) {
	quotedLinuxPath := grub.QuoteString(linuxPath)

	logger.Log.Debugf("---- new linux path: %s", linuxPath)

	linuxLines, err := findLinuxLines(inputGrubCfgContent)
	if err != nil {
		return "", nil, err
	}

	logger.Log.Debugf("---- found linux: %d lines", len(linuxLines))
	outputGrubCfgContent = inputGrubCfgContent
	if len(linuxLines) > 0 {
		for i := len(linuxLines) - 1; i >= 0; i = i - 1 {
			linuxFilePathToken := linuxLines[i][1]
			start := linuxFilePathToken.Loc.Start.Index
			end := linuxFilePathToken.Loc.End.Index

			logger.Log.Debugf("---- line: %d {%d-%d}", i, start, end)
			logger.Log.Debugf("---- line:    token: (%s)", linuxFilePathToken.RawContent)

			oldKernelPaths = append(oldKernelPaths, inputGrubCfgContent[start:end])
			outputGrubCfgContent = outputGrubCfgContent[:start] + quotedLinuxPath + outputGrubCfgContent[end:]
		}
	}

	return outputGrubCfgContent, oldKernelPaths, nil
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

func setInitrdPaths(inputGrubCfgContent string, initrdPath string) (outputGrubCfgContent string, oldInitrdPaths []string, err error) {
	quotedInitrdPath := grub.QuoteString(initrdPath)

	logger.Log.Debugf("---- new initrd path: %s", initrdPath)

	initrdLines, err := findInitrdLines(inputGrubCfgContent)
	if err != nil {
		return "", nil, err
	}

	logger.Log.Debugf("---- found initrd: %d lines", len(initrdLines))
	outputGrubCfgContent = inputGrubCfgContent
	if len(initrdLines) > 0 {
		for i := len(initrdLines) - 1; i >= 0; i = i - 1 {
			initrdFilePathToken := initrdLines[i][1]
			start := initrdFilePathToken.Loc.Start.Index
			end := initrdFilePathToken.Loc.End.Index

			logger.Log.Debugf("---- line: %d {%d-%d}", i, start, end)
			logger.Log.Debugf("---- line:    token: (%s)", initrdFilePathToken.RawContent)

			oldInitrdPaths = append(oldInitrdPaths, inputGrubCfgContent[start:end])
			outputGrubCfgContent = outputGrubCfgContent[:start] + quotedInitrdPath + outputGrubCfgContent[end:]
		}
	}

	return outputGrubCfgContent, oldInitrdPaths, nil
}

// Appends kernel command-line args to the linux command within a grub config file.
func appendKernelCommandLineArgs(inputGrubCfgContent string, extraCommandLine string) (outputGrubCfgContent string, err error) {
	_, insertAt, err := getLinuxCommandLineArgs(inputGrubCfgContent)
	if err != nil {
		return "", err
	}

	// Insert args at the end of the line.
	outputGrubCfgContent = inputGrubCfgContent[:insertAt] + extraCommandLine + " " + inputGrubCfgContent[insertAt:]
	return outputGrubCfgContent, nil
}

func appendKernelCommandLineArgsAll(inputGrubCfgContent string, extraCommandLine string) (outputGrubCfgContent string, err error) {

	linuxLines, err := findLinuxLines(inputGrubCfgContent)
	if err != nil {
		return "", err
	}

	outputGrubCfgContent = inputGrubCfgContent
	if len(linuxLines) > 0 {
		for i := len(linuxLines) - 1; i >= 0; i = i - 1 {
			// Skip the "linux" command and the kernel binary path arg.
			argTokens := linuxLines[i][2:]

			insertAt, err := findCommandLineInsertAt(argTokens, true /*forgiving*/)
			if err != nil {
				return "", err
			}

			// Insert args at the end of the line.
			outputGrubCfgContent = outputGrubCfgContent[:insertAt] + extraCommandLine + " " + outputGrubCfgContent[insertAt:]
		}
	}

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
//   - args: A list of kernel command-line arguments.
//   - insertAt: An index that represents an appropriate insert point for any new args.
//     For Azure Linux 2.0 images, this points to the index of the $kernelopts token.
func getLinuxCommandLineArgs(grub2Config string) ([]grubConfigLinuxArg, int, error) {
	linuxLine, err := findLinuxLine(grub2Config)
	if err != nil {
		return nil, 0, err
	}

	// Skip the "linux" command and the kernel binary path arg.
	argTokens := linuxLine[2:]

	insertAt, err := findCommandLineInsertAt(argTokens, false /*forgiving*/)
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
// Specifically, it looks for the index of the $kernelopts args.
func findCommandLineInsertAt(argTokens []grub.Token, forgiving bool) (int, error) {
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
		if forgiving && len(argTokens) > 0 {
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

// Finds an existing kernel command-line arg and replaces its value.
//
// Params:
// - inputGrubCfgContent: The string contents of the grub.cfg file.
// - name: The name of the command-line arg to replace.
// - value: The value to set the command-line arg to.
//
// Returns:
// - outputGrubCfgContent: The new string contents of the grub.cfg file.
// - oldValue: The previous value of the arg.
func replaceKernelCommandLineArgValue(inputGrubCfgContent string, name string, value string,
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

func replaceKernelCommandLineArgValueAll(inputGrubCfgContent string, name string, value string,
) (outputGrubCfgContent string, oldValue []string, err error) {
	newArg := fmt.Sprintf("%s=%s", name, value)
	quotedNewArg := grub.QuoteString(newArg)

	linuxLines, err := findLinuxLines(inputGrubCfgContent)
	if err != nil {
		return "", nil, err
	}

	logger.Log.Debugf("---- found linux: %d lines", len(linuxLines))
	oldValues := []string{}
	outputGrubCfgContent = inputGrubCfgContent
	if len(linuxLines) > 0 {
		for i := len(linuxLines) - 1; i >= 0; i = i - 1 {
			// Skip the "linux" command and the kernel binary path arg.
			args, err := parseCommandLineArgs(linuxLines[i][2:])
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
	}

	return outputGrubCfgContent, oldValues, nil
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
	args, insertAtToken, err := getLinuxCommandLineArgs(grub2Config)
	if err != nil {
		return "", err
	}

	grub2Config, err = updateKernelCommandLineArgsHelper(grub2Config, args, insertAtToken, argsToRemove, newArgs)
	if err != nil {
		return "", err
	}

	return grub2Config, nil
}

func updateKernelCommandLineArgsAll(grub2Config string, argsToRemove []string, newArgs []string) (string, error) {

	linuxLines, err := findLinuxLines(grub2Config)
	if err != nil {
		return "", err
	}

	if len(linuxLines) > 0 {
		logger.Log.Debugf("---- found linux: %d lines", len(linuxLines))
		for i := len(linuxLines) - 1; i >= 0; i = i - 1 {

			// Skip the "linux" command and the kernel binary path arg.
			argTokens := linuxLines[i][2:]

			insertAtToken, err := findCommandLineInsertAt(argTokens, true /*forgiving*/)
			if err != nil {
				return "", err
			}

			args, err := parseCommandLineArgs(argTokens)
			if err != nil {
				return "", err
			}

			// return args, insertAt, nil
			grub2Config, err = updateKernelCommandLineArgsHelper(grub2Config, args, insertAtToken, argsToRemove, newArgs)
			if err != nil {
				return "", err
			}

		}
	}

	return grub2Config, nil
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
		newSELinuxArgs = nil

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
func updateSELinuxCommandLineHelper(grub2Config string, selinuxMode imagecustomizerapi.SELinuxMode) (string, error) {
	newSELinuxArgs, err := selinuxModeToArgs(selinuxMode)
	if err != nil {
		return "", err
	}

	grub2Config, err = updateKernelCommandLineArgs(grub2Config, selinuxArgNames, newSELinuxArgs)
	if err != nil {
		return "", err
	}

	return grub2Config, nil
}

func updateSELinuxCommandLineHelperAll(grub2Config string, selinuxMode imagecustomizerapi.SELinuxMode) (string, error) {
	newSELinuxArgs, err := selinuxModeToArgs(selinuxMode)
	if err != nil {
		return "", err
	}

	grub2Config, err = updateKernelCommandLineArgsAll(grub2Config, selinuxArgNames, newSELinuxArgs)
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

// Reads the /boot/grub2/grub.cfg file.
func readGrub2ConfigFile(imageChroot *safechroot.Chroot) (string, error) {
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
func writeGrub2ConfigFile(grub2Config string, imageChroot *safechroot.Chroot) error {
	logger.Log.Debugf("Writing grub.cfg file")

	grub2ConfigFilePath := getGrub2ConfigFilePath(imageChroot)

	// Update grub.cfg file.
	err := file.Write(grub2Config, grub2ConfigFilePath)
	if err != nil {
		return fmt.Errorf("failed to write grub2 config file (%s):\n%w", installutils.GrubCfgFile, err)
	}

	return nil
}

func getGrub2ConfigFilePath(imageChroot *safechroot.Chroot) string {
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
