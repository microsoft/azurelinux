// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"fmt"
	"strings"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/shell"
)

const (
	// BuildRequiresArgument specifies the build requires argument to be used with rpm tools
	BuildRequiresArgument = "--buildrequires"

	// QueryHeaderArgument specifies the srpm argument to be used with rpm tools
	QueryHeaderArgument = "--srpm"

	// DistTagDefine specifies the dist tag option for rpm tool commands
	DistTagDefine = "dist"

	// DistroReleaseVersionDefine specifies the distro release version option for rpm tool commands
	DistroReleaseVersionDefine = "mariner_release_version"

	// DistroBuildNumberDefine specifies the distro build number option for rpm tool commands
	DistroBuildNumberDefine = "mariner_build_number"

	// SourceDirDefine specifies the source directory option for rpm tool commands
	SourceDirDefine = "_sourcedir"

	// TopDirDefine specifies the top directory option for rpm tool commands
	TopDirDefine = "_topdir"

	// WithCheckDefine specifies the with_check option for rpm tool commands
	WithCheckDefine = "with_check"

	// NoCompatibleArchError specifies the error message when processing a SPEC written for a different architecture.
	NoCompatibleArchError = "error: No compatible architectures found for build"
)

const (
	rpmProgram      = "rpm"
	rpmSpecProgram  = "rpmspec"
	rpmBuildProgram = "rpmbuild"
)

// SetMacroDir adds RPM_CONFIGDIR=$(newMacroDir) into the shell's environment for the duration of a program.
// To restore the environment the caller can use shell.SetEnvironment() with the returned origenv.
// On an empty string argument return success immediately and do not modify the environment.
func SetMacroDir(newMacroDir string) (origenv []string, err error) {
	origenv = shell.CurrentEnvironment()
	if newMacroDir == "" {
		return
	}
	exists, err := file.DirExists(newMacroDir)
	if err != nil || exists == false {
		err = fmt.Errorf("Directory %s does not exist", newMacroDir)
		return
	}

	env := append(shell.CurrentEnvironment(), fmt.Sprintf("RPM_CONFIGDIR=%s", newMacroDir))
	shell.SetEnvironment(env)

	return
}

// sanitizeOutput will take the raw output from an RPM command and split by new line,
// trimming whitespace and removing blank lines.
func sanitizeOutput(rawResults string) (sanitizedOutput []string) {
	rawSplitOutput := strings.Split(rawResults, "\n")

	for _, line := range rawSplitOutput {
		trimmedLine := strings.TrimSpace(line)
		if trimmedLine == "" {
			continue
		}

		sanitizedOutput = append(sanitizedOutput, trimmedLine)
	}

	return
}

// formatCommand will generate an RPM command to execute.
func formatCommandArgs(extrArgs []string, file, queryFormat string, defines map[string]string) (commandArgs []string) {
	commandArgs = append(commandArgs, extrArgs...)
	commandArgs = append(commandArgs, file)

	if queryFormat != "" {
		commandArgs = append(commandArgs, "--qf", queryFormat)
	}

	for k, v := range defines {
		commandArgs = append(commandArgs, "-D", fmt.Sprintf(`%s %s`, k, v))
	}

	return
}

// executeRpmCommand will execute an RPM command and return its output split
// by new line and whitespace trimmed.
func executeRpmCommand(program string, args ...string) (results []string, err error) {
	stdout, stderr, err := shell.Execute(program, args...)
	if err != nil {
		// When dealing with a SPEC/package intended for a different architecture, explicitly set the error message
		// to a known value so the invoker can check for it.
		//
		// All other errors will be treated normally.
		if strings.Contains(stderr, NoCompatibleArchError) {
			logger.Log.Debug(stderr)
			err = fmt.Errorf(NoCompatibleArchError)
		} else {
			logger.Log.Warn(stderr)
		}

		return
	}

	results = sanitizeOutput(stdout)
	return
}

// DefaultDefines returns a new map of default defines that can be used during RPM queries.
func DefaultDefines() map[string]string {
	const defaultWithCheck = "1"

	return map[string]string{
		WithCheckDefine: defaultWithCheck,
	}
}

// QuerySPEC queries a SPEC file with queryFormat. Returns the output split by line and trimmed.
func QuerySPEC(specFile, sourceDir, queryFormat string, defines map[string]string, extraArgs ...string) (result []string, err error) {
	const queryArg = "-q"

	var allDefines map[string]string

	extraArgs = append(extraArgs, queryArg)

	// To query some SPECs the source directory must be set
	// since the SPEC file may use `%include` on a source file
	if sourceDir == "" {
		allDefines = defines
	} else {
		allDefines = make(map[string]string)
		for k, v := range defines {
			allDefines[k] = v
		}

		allDefines[SourceDirDefine] = sourceDir
	}

	args := formatCommandArgs(extraArgs, specFile, queryFormat, allDefines)
	return executeRpmCommand(rpmSpecProgram, args...)
}

// QuerySPECForBuiltRPMs queries a SPEC file with queryFormat. Returns only the subpackages, which generate a .rpm file.
func QuerySPECForBuiltRPMs(specFile, sourceDir, queryFormat string, defines map[string]string) (result []string, err error) {
	const builtRPMsSwitch = "--builtrpms"

	return QuerySPEC(specFile, sourceDir, queryFormat, defines, builtRPMsSwitch)
}

// QueryPackage queries an RPM or SRPM file with queryFormat. Returns the output split by line and trimmed.
func QueryPackage(packageFile, queryFormat string, defines map[string]string, extraArgs ...string) (result []string, err error) {
	const queryArg = "-q"

	extraArgs = append(extraArgs, queryArg)
	args := formatCommandArgs(extraArgs, packageFile, queryFormat, defines)

	return executeRpmCommand(rpmProgram, args...)
}

// BuildRPMFromSRPM builds an RPM from the given SRPM file
func BuildRPMFromSRPM(srpmFile string, defines map[string]string, extraArgs ...string) (err error) {
	const (
		queryFormat  = ""
		squashErrors = true
	)

	extraArgs = append(extraArgs, "--rebuild", "--nodeps")

	args := formatCommandArgs(extraArgs, srpmFile, queryFormat, defines)
	return shell.ExecuteLive(squashErrors, rpmBuildProgram, args...)
}

// GenerateSRPMFromSPEC generates an SRPM for the given SPEC file
func GenerateSRPMFromSPEC(specFile, topDir string, defines map[string]string) (err error) {
	const (
		generateSRPMArg = "-bs"
		queryFormat     = ""
	)

	var allDefines map[string]string
	extraArgs := []string{generateSRPMArg}

	if topDir == "" {
		allDefines = defines
	} else {
		allDefines = make(map[string]string)
		for k, v := range defines {
			allDefines[k] = v
		}

		allDefines[TopDirDefine] = topDir
	}

	args := formatCommandArgs(extraArgs, specFile, queryFormat, allDefines)
	_, stderr, err := shell.Execute(rpmBuildProgram, args...)
	if err != nil {
		logger.Log.Warn(stderr)
	}

	return
}

// InstallRPM installs the given RPM or SRPM
func InstallRPM(rpmFile string) (err error) {
	const installOption = "-ihv"

	logger.Log.Debugf("Installing RPM (%s)", rpmFile)

	_, stderr, err := shell.Execute(rpmProgram, installOption, rpmFile)
	if err != nil {
		logger.Log.Warn(stderr)
	}

	return
}
