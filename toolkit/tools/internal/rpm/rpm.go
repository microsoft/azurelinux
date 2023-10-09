// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"errors"
	"fmt"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
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

	// MaxCPUDefine specifies the max number of CPUs to use for parallel build
	MaxCPUDefine = "_smp_ncpus_max"
)

const (
	installedRPMRegexRPMIndex        = 1
	installedRPMRegexArchIndex       = 2
	installedRPMRegexExpectedMatches = 3

	rpmProgram      = "rpm"
	rpmSpecProgram  = "rpmspec"
	rpmBuildProgram = "rpmbuild"
)

var (
	goArchToRpmArch = map[string]string{
		"amd64": "x86_64",
		"arm64": "aarch64",
	}

	// checkSectionRegex is used to determine if a SPEC file has a '%check' section.
	// It works multi-line strings containing the whole file content, thus the need for the 'm' flag.
	checkSectionRegex = regexp.MustCompile(`(?m)^\s*%check`)

	// Output from 'rpm' prints installed RPMs in a line with the following format:
	//
	//	D: ========== +++ [name]-[version]-[release].[distribution] [architecture]-linux [hex_value]
	//
	// Example:
	//
	//	D: ========== +++ systemd-devel-239-42.cm2 x86_64-linux 0x0
	installedRPMRegex = regexp.MustCompile(`^D: =+ \+{3} (\S+) (\S+)-linux.*$`)
)

// GetRpmArch converts the GOARCH arch into an RPM arch
func GetRpmArch(goArch string) (rpmArch string, err error) {
	rpmArch, ok := goArchToRpmArch[goArch]
	if !ok {
		err = fmt.Errorf("unknown GOARCH detected (%s)", goArch)
	}
	return
}

func GetBasePackageNameFromSpecFile(specPath string) (basePackageName string, err error) {

	baseName := filepath.Base(specPath)
	if baseName == "" {
		return "", errors.New(fmt.Sprintf("Cannot extract file name from specPath (%s).", specPath))
	}

	fileExtension := filepath.Ext(baseName)
	if fileExtension == "" {
		return "", errors.New(fmt.Sprintf("Cannot extract file extension from file name (%s).", baseName))
	}

	basePackageName = baseName[:len(baseName)-len(fileExtension)]

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
		err = fmt.Errorf("directory %s does not exist", newMacroDir)
		return
	}

	env := append(shell.CurrentEnvironment(), fmt.Sprintf("RPM_CONFIGDIR=%s", newMacroDir))
	shell.SetEnvironment(env)

	return
}

// ExtractNameFromRPMPath strips the version from an RPM file name. i.e. pkg-name-1.2.3-4.cm2.x86_64.rpm -> pkg-name
func ExtractNameFromRPMPath(rpmFile string) (strippedFile string, err error) {
	baseName := filepath.Base(rpmFile)

	// If the path is invalid, return empty string. We consider any string that has at least 1 '-' characters valid.
	if !strings.Contains(baseName, "-") {
		err = fmt.Errorf("invalid RPM file name '%s', can't extract name", rpmFile)
		return
	}

	rpmFileSplit := strings.Split(baseName, "-")
	strippedFile = strings.Join(rpmFileSplit[:len(rpmFileSplit)-2], "-")
	return
}

// getCommonBuildArgs will generate arguments to pass to 'rpmbuild'.
func getCommonBuildArgs(outArch, srpmFile string, defines map[string]string) (buildArgs []string, err error) {
	const (
		os          = "linux"
		queryFormat = ""
		vendor      = "mariner"
	)

	buildArgs = []string{"--nodeps"}

	// buildArch is the arch of the build machine
	// outArch is the arch of the machine that will run the resulting binary
	buildArch, err := GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	if buildArch != outArch && outArch != "noarch" {
		tuple := outArch + "-" + vendor + "-" + os
		logger.Log.Debugf("Applying RPM target tuple (%s)", tuple)
		buildArgs = append(buildArgs, TargetArgument, tuple)
	}

	return formatCommandArgs(buildArgs, srpmFile, queryFormat, defines), nil
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

	if queryFormat != "" {
		commandArgs = append(commandArgs, "--qf", queryFormat)
	}

	for k, v := range defines {
		commandArgs = append(commandArgs, "-D", fmt.Sprintf(`%s %s`, k, v))
	}

	commandArgs = append(commandArgs, file)

	return
}

// executeRpmCommand will execute an RPM command and return its output split
// by new line and whitespace trimmed.
func executeRpmCommand(program string, args ...string) (results []string, err error) {
	stdout, err := executeRpmCommandRaw(program, args...)

	return sanitizeOutput(stdout), err
}

// executeRpmCommandRaw will execute an RPM command and return stdout in form of unmodified strings.
func executeRpmCommandRaw(program string, args ...string) (stdout string, err error) {
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
	}

	return
}

// DefaultDefinesWithDist returns a new map of default defines that can be used during RPM queries that also includes
// the dist tag.
func DefaultDefinesWithDist(runChecks bool, distTag string) map[string]string {
	defines := DefaultDefines(runChecks)
	defines[DistTagDefine] = distTag
	return defines
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

	extraArgs = append(extraArgs, queryArg)

	// Apply --target arch argument
	extraArgs = append(extraArgs, TargetArgument, arch)

	allDefines := updateSourceDirDefines(defines, sourceDir)

	args := formatCommandArgs(extraArgs, specFile, queryFormat, allDefines)
	return executeRpmCommand(rpmSpecProgram, args...)
}

// QuerySPECForBuiltRPMs queries a SPEC file with queryFormat. Returns only the subpackages, which generate a .rpm file.
func QuerySPECForBuiltRPMs(specFile, sourceDir, arch string, defines map[string]string) (result []string, err error) {
	const queryFormat = "%{nevra}\n"

	return QuerySPEC(specFile, sourceDir, queryFormat, arch, defines, QueryBuiltRPMHeadersArgument)
}

// QueryPackage queries an RPM or SRPM file with queryFormat. Returns the output split by line and trimmed.
func QueryPackage(packageFile, queryFormat string, defines map[string]string, extraArgs ...string) (result []string, err error) {
	const queryArg = "-q"

	extraArgs = append(extraArgs, queryArg)
	args := formatCommandArgs(extraArgs, packageFile, queryFormat, defines)

	return executeRpmCommand(rpmProgram, args...)
}

// BuildRPMFromSRPM builds an RPM from the given SRPM file but does not run its '%check' section.
func BuildRPMFromSRPM(srpmFile, outArch string, defines map[string]string) (err error) {
	const squashErrors = true

	commonBuildArgs, err := getCommonBuildArgs(outArch, srpmFile, defines)
	if err != nil {
		return
	}

	args := []string{"--nocheck", "--rebuild"}
	args = append(args, commonBuildArgs...)

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
		if len(matches) == installedRPMRegexExpectedMatches {
			rpmName := fmt.Sprintf("%s.%s", matches[installedRPMRegexRPMIndex], matches[installedRPMRegexArchIndex])
			uniqueResolvedRPMs[rpmName] = true
		}
	}

	resolvedRPMs = sliceutils.SetToSlice(uniqueResolvedRPMs)
	return
}

// SpecExclusiveArchIsCompatible verifies the "ExclusiveArch" tag is compatible with the current machine's architecture.
func SpecExclusiveArchIsCompatible(specfile, sourcedir, arch string, defines map[string]string) (isCompatible bool, err error) {
	const (
		exclusiveArchIndex = 0
		exclusiveArchQuery = "[%{EXCLUSIVEARCH} ]"
	)

	// Sanity check that this SPEC is meant to be built for the current machine architecture
	queryOutput, err := QuerySPEC(specfile, sourcedir, exclusiveArchQuery, arch, defines, QueryHeaderArgument)
	if err != nil {
		logger.Log.Warnf("Failed to query SPEC (%s), error: %s", specfile, err)
		return
	}

	// Empty result means the package is buildable for all architectures.
	if len(queryOutput) == 0 {
		isCompatible = true
		return
	}

	isCompatible = strings.Contains(queryOutput[exclusiveArchIndex], arch)

	return
}

// SpecExcludeArchIsCompatible verifies the "ExcludeArch" tag is compatible with the current machine's architecture.
func SpecExcludeArchIsCompatible(specfile, sourcedir, arch string, defines map[string]string) (isCompatible bool, err error) {
	const (
		excludeArchIndex = 0
		excludeArchQuery = "[%{EXCLUDEARCH} ]"
	)

	queryOutput, err := QuerySPEC(specfile, sourcedir, excludeArchQuery, arch, defines, QueryHeaderArgument)
	if err != nil {
		logger.Log.Warnf("Failed to query SPEC (%s), error: %s", specfile, err)
		return
	}

	// Empty result means the package is buildable for all architectures.
	if len(queryOutput) == 0 {
		isCompatible = true
		return
	}

	isCompatible = !strings.Contains(queryOutput[excludeArchIndex], arch)

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

// SpecHasCheckSection verifies if the spec has the '%check' section.
func SpecHasCheckSection(specFile, sourceDir, arch string, defines map[string]string) (hasCheckSection bool, err error) {
	const (
		parseSwitch = "--parse"
		queryFormat = ""
	)

	basicArgs := []string{
		parseSwitch,
		TargetArgument,
		arch,
	}
	allDefines := updateSourceDirDefines(defines, sourceDir)
	args := formatCommandArgs(basicArgs, specFile, queryFormat, allDefines)

	stdout, err := executeRpmCommandRaw(rpmSpecProgram, args...)

	return checkSectionRegex.MatchString(stdout), err
}

// BuildCompatibleSpecsList builds a list of spec files in a directory that are compatible with the build arch. Paths
// are relative to the 'baseDir' directory. This function should generally be used from inside a chroot to ensure the
// correct defines are available.
func BuildCompatibleSpecsList(baseDir string, inputSpecPaths []string, defines map[string]string) (filteredSpecPaths []string, err error) {
	var specPaths []string
	if len(inputSpecPaths) > 0 {
		specPaths = inputSpecPaths
	} else {
		specPaths, err = buildAllSpecsList(baseDir)
		if err != nil {
			return
		}
	}

	return filterCompatibleSpecs(specPaths, defines)
}

// TestRPMFromSRPM builds an RPM from the given SRPM and runs its '%check' section SRPM file
// but it does not generate any RPM packages.
func TestRPMFromSRPM(srpmFile, outArch string, defines map[string]string) (err error) {
	const squashErrors = true

	commonBuildArgs, err := getCommonBuildArgs(outArch, srpmFile, defines)
	if err != nil {
		return
	}

	args := []string{"-ri"}
	args = append(args, commonBuildArgs...)

	return shell.ExecuteLive(squashErrors, rpmBuildProgram, args...)
}

// buildAllSpecsList builds a list of all spec files in the directory. Paths are relative to the base directory.
func buildAllSpecsList(baseDir string) (specPaths []string, err error) {
	specFilesGlob := filepath.Join(baseDir, "**", "*.spec")

	specPaths, err = filepath.Glob(specFilesGlob)
	if err != nil {
		logger.Log.Errorf("Failed while trying to enumerate all spec files with (%s). Error: %v.", specFilesGlob, err)
	}

	return
}

// filterCompatibleSpecs filters a list of spec files in the chroot's SPECs directory that are compatible with the build arch.
func filterCompatibleSpecs(inputSpecPaths []string, defines map[string]string) (filteredSpecPaths []string, err error) {
	var specCompatible bool

	buildArch, err := GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	type specArchResult struct {
		compatible bool
		path       string
		err        error
	}
	resultsChannel := make(chan specArchResult, len(inputSpecPaths))

	for _, specFilePath := range inputSpecPaths {
		specDirPath := filepath.Dir(specFilePath)

		go func(pathIter string) {
			specCompatible, err = SpecArchIsCompatible(pathIter, specDirPath, buildArch, defines)
			if err != nil {
				err = fmt.Errorf("failed while querrying spec (%s). Error: %v.", pathIter, err)
			}
			resultsChannel <- specArchResult{
				compatible: specCompatible,
				path:       pathIter,
				err:        err,
			}
		}(specFilePath)
	}

	for i := 0; i < len(inputSpecPaths); i++ {
		result := <-resultsChannel
		if result.err != nil {
			err = result.err
			return
		}
		if result.compatible {
			filteredSpecPaths = append(filteredSpecPaths, result.path)
		}
	}

	return
}

// updateSourceDirDefines adds the source directory to the defines map if it is not empty.
// To query some SPECs the source directory must be set
// since the SPEC file may use `%include` on a source file.
func updateSourceDirDefines(defines map[string]string, sourceDir string) (updatedDefines map[string]string) {
	updatedDefines = make(map[string]string)
	for key, value := range defines {
		updatedDefines[key] = value
	}

	if sourceDir != "" {
		updatedDefines[SourceDirDefine] = sourceDir
	}

	return
}
