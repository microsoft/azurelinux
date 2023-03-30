// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"fmt"
	"regexp"
	"runtime"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/sliceutils"
)

const (
	// TargetArgument specifies to build for a target platform (i.e., aarch64-mariner-linux)
	TargetArgument = "--target"

	// BuildRequiresArgument specifies the build requires argument to be used with rpm tools
	BuildRequiresArgument = "--buildrequires"

	// QueryHeaderArgument specifies the srpm argument to be used with rpm tools
	QueryHeaderArgument = "--srpm"

	// QueryBuiltRPMHeadersArgument specifies that only rpm packages that would be built from a given spec should be queried.
	QueryBuiltRPMHeadersArgument = "--builtrpms"

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

	// MarinerModuleLdflagsDefine specifies the variable used to enable linking ELF binaries with module_info.ld metadata.
	MarinerModuleLdflagsDefine = "mariner_module_ldflags"

	// MarinerCCacheDefine enables ccache in the Mariner build system
	MarinerCCacheDefine = "mariner_ccache_enabled"
)

const (
	installedRPMRegexRPMIndex = 1

	rpmProgram      = "rpm"
	rpmSpecProgram  = "rpmspec"
	rpmBuildProgram = "rpmbuild"
)

var (
	goArchToRpmArch = map[string]string{
		"amd64": "x86_64",
		"arm64": "aarch64",
	}

	// Output from 'rpm' prints installed RPMs in a line with the following format:
	//
	//	D: ========== +++ [name]-[version]-[release].[distribution] [architecture]-linux [hex_value]
	//
	// Example:
	//
	//	D: ========== +++ systemd-devel-239-42.cm2 x86_64-linux 0x0
	installedRPMRegex = regexp.MustCompile(`^D: =+ \+{3} (\S+).*$`)
)

// GetRpmArch converts the GOARCH arch into an RPM arch
func GetRpmArch(goArch string) (rpmArch string, err error) {
	rpmArch, ok := goArchToRpmArch[goArch]
	if !ok {
		err = fmt.Errorf("Unknown GOARCH detected (%s)", goArch)
	}
	return
}

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
func formatCommandArgs(extraArgs []string, file, queryFormat string, defines map[string]string) (commandArgs []string) {
	commandArgs = append(commandArgs, extraArgs...)
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
func DefaultDefines(runCheck bool) map[string]string {
	// "with_check" definition should align with the RUN_CHECK Make variable whenever possible
	withCheckSetting := "0"
	if runCheck {
		withCheckSetting = "1"
	}

	return map[string]string{
		WithCheckDefine: withCheckSetting,
	}
}

// GetInstalledPackages returns a string list of all packages installed on the system
// in the "[name]-[version]-[release].[distribution].[architecture]" format.
// Example: tdnf-2.1.0-4.cm1.x86_64
func GetInstalledPackages() (result []string, err error) {
	const queryArg = "-qa"

	return executeRpmCommand(rpmProgram, queryArg)
}

// QuerySPEC queries a SPEC file with queryFormat. Returns the output split by line and trimmed.
func QuerySPEC(specFile, sourceDir, queryFormat, arch string, defines map[string]string, extraArgs ...string) (result []string, err error) {
	const queryArg = "-q"

	var allDefines map[string]string

	extraArgs = append(extraArgs, queryArg)

	// Apply --target arch argument
	extraArgs = append(extraArgs, TargetArgument, arch)

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
func QuerySPECForBuiltRPMs(specFile, sourceDir, arch string, defines map[string]string) (result []string, err error) {
	const queryFormat = "%{nvra}\n"

	return QuerySPEC(specFile, sourceDir, queryFormat, arch, defines, QueryBuiltRPMHeadersArgument)
}

// QueryPackage queries an RPM or SRPM file with queryFormat. Returns the output split by line and trimmed.
func QueryPackage(packageFile, queryFormat string, defines map[string]string, extraArgs ...string) (result []string, err error) {
	const queryArg = "-q"

	extraArgs = append(extraArgs, queryArg)
	args := formatCommandArgs(extraArgs, packageFile, queryFormat, defines)

	return executeRpmCommand(rpmProgram, args...)
}

// BuildRPMFromSRPM builds an RPM from the given SRPM file
func BuildRPMFromSRPM(srpmFile, outArch string, defines map[string]string, extraArgs ...string) (err error) {
	const (
		queryFormat  = ""
		squashErrors = true
		vendor       = "mariner"
		os           = "linux"
	)

	extraArgs = append(extraArgs, "--rebuild", "--nodeps")

	// buildArch is the arch of the build machine
	// outArch is the arch of the machine that will run the resulting binary
	buildArch, err := GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	if buildArch != outArch && "noarch" != outArch {
		tuple := outArch + "-" + vendor + "-" + os
		logger.Log.Debugf("Applying RPM target tuple (%s)", tuple)
		extraArgs = append(extraArgs, TargetArgument, tuple)
	}

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

// QueryRPMProvides returns what an RPM file provides.
// This includes any provides made by a generator and files provided by the rpm.
func QueryRPMProvides(rpmFile string) (provides []string, err error) {
	const queryProvidesOption = "-qlPp"

	logger.Log.Debugf("Querying RPM provides (%s)", rpmFile)
	stdout, stderr, err := shell.Execute(rpmProgram, queryProvidesOption, rpmFile)
	if err != nil {
		logger.Log.Warn(stderr)
		return
	}

	provides = sanitizeOutput(stdout)
	return
}

// ResolveCompetingPackages takes in a list of RPMs and returns only the ones, which would
// end up being installed after resolving outdated, obsoleted, or conflicting packages.
func ResolveCompetingPackages(rootDir string, rpmPaths ...string) (resolvedRPMs []string, err error) {
	const (
		queryFormat  = ""
		squashErrors = true
	)

	args := []string{
		"-Uvvh",
		"--replacepkgs",
		"--nodeps",
		"--root",
		rootDir,
		"--test",
	}
	args = append(args, rpmPaths...)

	// Output of interest is printed to stderr.
	_, stderr, err := shell.Execute(rpmProgram, args...)
	if err != nil {
		logger.Log.Warn(stderr)
		return
	}

	splitStdout := strings.Split(stderr, "\n")
	uniqueResolvedRPMs := map[string]bool{}
	for _, line := range splitStdout {
		matches := installedRPMRegex.FindStringSubmatch(line)
		if len(matches) != 0 {
			uniqueResolvedRPMs[matches[installedRPMRegexRPMIndex]] = true
		}
	}

	resolvedRPMs = sliceutils.StringsSetToSlice(uniqueResolvedRPMs)
	return
}

// SpecExclusiveArchIsCompatible verifies the "ExclusiveArch" tag is compatible with the current machine's architecture.
func SpecExclusiveArchIsCompatible(specfile, sourcedir, arch string, defines map[string]string) (isCompatible bool, err error) {
	const queryExclusiveArch = "%{ARCH}\n[%{EXCLUSIVEARCH} ]\n"

	const (
		machineArchField   = iota
		exclusiveArchField = iota
		minimumFieldsCount = iota
	)

	// Sanity check that this SPEC is meant to be built for the current machine architecture
	exclusiveArchList, err := QuerySPEC(specfile, sourcedir, queryExclusiveArch, arch, defines, QueryHeaderArgument)
	if err != nil {
		logger.Log.Warnf("Failed to query SPEC (%s), error: %s", specfile, err)
		return
	}

	// If the list does not return enough lines then there is no exclusive arch set
	if len(exclusiveArchList) < minimumFieldsCount {
		isCompatible = true
		return
	}

	if strings.Contains(exclusiveArchList[exclusiveArchField], exclusiveArchList[machineArchField]) {
		isCompatible = true
		return
	}

	return
}

// SpecExcludeArchIsCompatible verifies the "ExcludeArch" tag is compatible with the current machine's architecture.
func SpecExcludeArchIsCompatible(specfile, sourcedir, arch string, defines map[string]string) (isCompatible bool, err error) {
	const queryExclusiveArch = "%{ARCH}\n[%{EXCLUDEARCH} ]\n"

	const (
		machineArchField   = iota
		excludeArchField   = iota
		minimumFieldsCount = iota
	)

	excludedArchList, err := QuerySPEC(specfile, sourcedir, queryExclusiveArch, arch, defines, QueryHeaderArgument)
	if err != nil {
		logger.Log.Warnf("Failed to query SPEC (%s), error: %s", specfile, err)
		return
	}

	// If the list does not return enough lines then there is no excluded architectures set.
	if len(excludedArchList) < minimumFieldsCount {
		isCompatible = true
		return
	}

	isCompatible = !strings.Contains(excludedArchList[excludeArchField], excludedArchList[machineArchField])

	return
}

// SpecArchIsCompatible verifies the spec is buildable on the current machine's architecture.
func SpecArchIsCompatible(specfile, sourcedir, arch string, defines map[string]string) (isCompatible bool, err error) {
	isCompatible, err = SpecExclusiveArchIsCompatible(specfile, sourcedir, arch, defines)
	if err != nil {
		return
	}

	if isCompatible {
		return SpecExcludeArchIsCompatible(specfile, sourcedir, arch, defines)
	}

	return
}
