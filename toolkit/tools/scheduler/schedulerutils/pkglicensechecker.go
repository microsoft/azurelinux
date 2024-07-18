// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/directory"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck/licensecheckformat"
)

type PackageLicenseCheckerConfig struct {
	BuildDirPath      string                        // The path to the build directory to create the chroot in
	WorkerTarPath     string                        // The path to the worker tarball to extract into the chroot
	NameFilePath      string                        // The path to the file containing the license name regexes
	ExceptionFilePath string                        // The path to the file containing the license exception regexes
	DistTag           string                        // The dist tag to use for the chroot
	Mode              licensecheck.LicenseCheckMode // Control the behavior of the license checker
	ResultsFile       string                        // (optional) Where to save the .json results file
	SummaryFile       string                        // (optional) Where to save the human readable summary file
}

// PackageLicenseChecker is a wrapper around the licensecheck package that provides an interface optimized for use in
// the scheduler. The PackageLicenseChecker is NOT thread safe and should not be shared between goroutines. An instance
// should be created via NewPackageLicenseChecker() and may be reused for multiple calls to CheckPkgLicenses(). Results
// are accumulated across calls to CheckPkgLicenses() and can be saved via SaveResults() if result or summary files are
// given.
type PackageLicenseChecker struct {
	config         PackageLicenseCheckerConfig
	licenseChecker *licensecheck.LicenseChecker

	rpmDirPath  string
	checkerMode licensecheck.LicenseCheckMode
	resultsFile string
	summaryFile string
}

// NewPackageLicenseChecker creates a new PackageLicenseChecker. The license checker will be initialized with the given configuration. The
// initialization of the license checker is deferred until the first call to CheckLicenses that requires scanning RPMs.
// The resulting PackageLicenseChecker instance should be cleaned up with CleanupPackageLicenseChecker() when it is no longer needed.
func NewPackageLicenseChecker(config PackageLicenseCheckerConfig) (p *PackageLicenseChecker, err error) {
	if !licensecheck.IsValidLicenseCheckMode(config.Mode) {
		err = fmt.Errorf("invalid license check mode: %s", config.Mode)
		return nil, err
	}

	if config.Mode == licensecheck.LicenseCheckModeNone {
		return &PackageLicenseChecker{checkerMode: licensecheck.LicenseCheckModeNone}, nil
	}

	rpmCopyDir := filepath.Join(config.BuildDirPath, "rpms_to_scan")
	err = directory.EnsureDirExists(rpmCopyDir)
	if err != nil {
		err = fmt.Errorf("failed to create directory to stage RPMs:\n%w", err)
		return nil, err
	}

	return &PackageLicenseChecker{
		// Lazy initialize the license checker chroot. We can wait until a build is actually done, and has RPMS to scan,
		// before starting it. If we start it now, it will block us starting any graph processing until the chroot is
		// ready.
		licenseChecker: nil,
		config:         config,

		rpmDirPath:  rpmCopyDir,
		checkerMode: config.Mode,
		resultsFile: config.ResultsFile,
		summaryFile: config.SummaryFile,
	}, nil
}

// Initialize the license checker chroot if needed.
func (p *PackageLicenseChecker) startLicenseCheckerChroot() (err error) {
	if p.licenseChecker != nil {
		return nil
	}
	p.licenseChecker, err = licensecheck.New(p.config.BuildDirPath,
		p.config.WorkerTarPath, p.rpmDirPath, p.config.NameFilePath, p.config.ExceptionFilePath, p.config.DistTag)
	if err != nil {
		err = fmt.Errorf("failed to create license checker for use with packages:\n%w", err)
		return err
	}
	return nil
}

func (p *PackageLicenseChecker) CleanupPackageLicenseChecker() error {
	if p.licenseChecker != nil {
		return p.licenseChecker.Cleanup()
	} else {
		return nil
	}
}

// CheckPkgLicenses will check each RPM passed in for license issues by copying them to a dedicated folder and running
// the license checker. This function will initialize the license checker if it has not already been initialized.
// Each call will accumulate the results of the license checks in the license checker instance. After all RPMs have been
// checked, the results can be saved via SaveResults().
func (p *PackageLicenseChecker) CheckPkgLicenses(rpmPaths []string) (hasWarning, hasError bool, err error) {
	if len(rpmPaths) == 0 || p.checkerMode == licensecheck.LicenseCheckModeNone {
		return false, false, nil
	}

	if p.licenseChecker == nil {
		err = p.startLicenseCheckerChroot()
		if err != nil {
			err = fmt.Errorf("failed to start license checker chroot:\n%w", err)
			return false, false, err
		}
	}

	// Clear the RPM directory before copying the new RPMs
	err = file.RemoveDirectoryContents(p.rpmDirPath)
	if err != nil {
		err = fmt.Errorf("failed to clear RPM directory before scan:\n%w", err)
		return false, false, err
	}

	// Copy the RPMs into the check directory
	for _, rpmPath := range rpmPaths {
		err = file.Copy(rpmPath, filepath.Join(p.rpmDirPath, filepath.Base(rpmPath)))
		if err != nil {
			err = fmt.Errorf("failed to copy RPMs to check directory:\n%w", err)
			return false, false, err
		}
	}

	latestResults, err := p.licenseChecker.CheckLicenses(true)
	if err != nil {
		err = fmt.Errorf("failed to check licenses for packages:\n%w", err)
		return false, false, err
	}

	_, warnings, errors := licensecheck.SortAndFilterResults(latestResults, p.checkerMode)

	// Clean up once the scan is done so no .rpm files are left behind unnecessarily
	err = file.RemoveDirectoryContents(p.rpmDirPath)
	if err != nil {
		err = fmt.Errorf("failed to clear RPM directory after scan:\n%w", err)
		return false, false, err
	}

	return len(warnings) > 0, len(errors) > 0, nil
}

func (p *PackageLicenseChecker) GetSummaryFile() string {
	return p.summaryFile
}

func (p *PackageLicenseChecker) SaveResults() (err error) {
	all := []licensecheck.LicenseCheckResult{}
	if p.licenseChecker != nil {
		all, _, _ = p.licenseChecker.GetResults(p.checkerMode)
	}

	// Save the results .json file
	if p.resultsFile != "" {
		err = licensecheck.SaveLicenseCheckResults(p.resultsFile, all)
		if err != nil {
			err = fmt.Errorf("failed to save license check results:\n%w", err)
			return err
		}
	}

	// Save the human readable summary file
	if p.summaryFile != "" {
		summary := licensecheckformat.FormatResults(all, p.checkerMode)
		err = file.Write(summary, p.summaryFile)
		if err != nil {
			err = fmt.Errorf("failed to save license check summary:\n%w", err)
			return err
		}
	}

	return nil
}
