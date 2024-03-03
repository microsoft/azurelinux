// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkgjson

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/versioncompare"
)

const (
	packageWithVersionNameIndex       = 1
	packageWithVersionConditionIndex  = 2
	packageWithVersionVersionIndex    = 3
	packageWithVersionExpectedMatches = 4
)

var (
	knownConditions = map[string]bool{
		"":   true,
		"=":  true,
		"<":  true,
		"<=": true,
		">":  true,
		">=": true,
	}
	// Regular expression to correctly split a string with the package name and an optional version constraint.
	// Examples:
	//	gcc ->       "gcc" "" ""
	//	gcc=9.1.0 -> "gcc" "=" "1.9.0"
	packageWithVersionRegex = regexp.MustCompile(`^\s*([^><=\s]+)\s*(?:((?:[<>]=)|(?:[<>=]))\s*([^<>=\s]+))?\s*$`)
)

// PackageRepo contains an array of SRPMs and relational dependencies
type PackageRepo struct {
	Repo []*Package `json:"Repo"`
}

// PackageVer is a representation of a package with name and version information
type PackageVer struct {
	Name       string `json:"Name"`       // Name of the package
	Version    string `json:"Version"`    // Version number of the package
	Condition  string `json:"Condition"`  // Condition to place on the version number ("<", "=<", "=", ">=", ">")
	SVersion   string `json:"SVersion"`   // Secondary version number to express bounded versions for dependencies
	SCondition string `json:"SCondition"` // Secondary version condition to express bounded versions for dependencies
}

// PackageVerInterval encodes the version interval a given PackageVer struct represents
type PackageVerInterval struct {
	LowerBound     *versioncompare.TolerantVersion // Lower bound on the range of valid versions
	UpperBound     *versioncompare.TolerantVersion // Upper bound on the range of valid versions
	LowerInclusive bool                            // Does the lower bound actually include the indicated version (< vs <=)
	UpperInclusive bool                            // Does the upper bound actually include the indicated version (< vs <=)
}

// Package is a representation of a package with name and version information
type Package struct {
	Provides      *PackageVer   `json:"Provides"`      // Version information and name of package
	SrpmPath      string        `json:"SrpmPath"`      // Reconstructed name of the SRPM the spec is from
	RpmPath       string        `json:"RpmPath"`       // Reconstructed name of the RPM the package comes from
	SourceDir     string        `json:"SourceDir"`     // The path to the directory of sources for this package
	SpecPath      string        `json:"SpecPath"`      // The path to the spec file that builds this package
	Architecture  string        `json:"Architecture"`  // The architecture of the package
	Requires      []*PackageVer `json:"Requires"`      // List of targets this spec requires to install
	BuildRequires []*PackageVer `json:"BuildRequires"` // List of targets this spec requires to build
	TestRequires  []*PackageVer `json:"TestRequires"`  // List of targets this spec requires to run tests.
	IsToolchain   bool          `json:"IsToolchain"`   // Is this package part of the toolchain
	RunTests      bool          `json:"RunTests"`      // Should we run tests for this package.
}

// ParsePackageJSON reads a package list json file
func (pkg *PackageRepo) ParsePackageJSON(path string) (err error) {
	logger.Log.Infof("Opening %s", path)

	return jsonutils.ReadJSONFile(path, &pkg)
}

// IsImplicitPackage returns true if a PackageVer represents an implicit provide.
func (pkgVer *PackageVer) IsImplicitPackage() bool {
	// Auto generated provides will contain "(" and ")".
	if strings.Contains(pkgVer.Name, "(") && strings.Contains(pkgVer.Name, ")") {
		return true
	}

	// File paths will start with a "/" are implicitly provided by an rpm that contains that file.
	if strings.HasPrefix(pkgVer.Name, "/") {
		return true
	}

	return false
}

// Interval returns a PackageVerInterval struct which has been sanitized. The interval represents the range of versions a PackageVer
// structure considers valid.
func (pkgVer *PackageVer) Interval() (interval PackageVerInterval, err error) {
	var (
		lowerBound, upperBound         *versioncompare.TolerantVersion
		lowerCond, upperCond           string
		lowerInclusive, upperInclusive bool
	)

	c1 := pkgVer.Condition
	c2 := pkgVer.SCondition
	v1 := versioncompare.New(pkgVer.Version)
	v2 := versioncompare.New(pkgVer.SVersion)

	if err = pkgVer.validatedIntervals(); err != nil {
		err = fmt.Errorf("invalid intervals for '%s': %v", pkgVer.Name, err)
		return
	}

	switch {
	case pkgVer.Version == "" && pkgVer.SVersion == "":
		// No version information
		lowerBound = versioncompare.NewMin()
		upperBound = versioncompare.NewMax()
		upperInclusive = true
		lowerInclusive = true
	case pkgVer.Version == "" && pkgVer.SVersion != "",
		pkgVer.Version != "" && pkgVer.SVersion == "",
		pkgVer.Version == pkgVer.SVersion && pkgVer.Condition == pkgVer.SCondition:
		// Only one version set, or duplicated version data
		if pkgVer.Version == "" {
			v1 = v2
			c1 = c2
		}

		switch c1 {
		case ">=":
			lowerInclusive = true
			fallthrough
		case ">":
			lowerBound = v1
			upperBound = versioncompare.NewMax()
			upperInclusive = true
		case "<=":
			upperInclusive = true
			fallthrough
		case "<":
			lowerBound = versioncompare.NewMin()
			upperBound = v1
			lowerInclusive = true
		case "", "=":
			lowerBound = v1
			upperBound = v1
			lowerInclusive = true
			upperInclusive = true
		}
	case pkgVer.Version != "" && pkgVer.SVersion != "":
		// Explicit version information for both (duplicate version data is handled above)
		if v1.Compare(v2) == versioncompare.LessThan {
			lowerBound, lowerCond = v1, c1
			upperBound, upperCond = v2, c2
		} else {
			lowerBound, lowerCond = v2, c2
			upperBound, upperCond = v1, c1
		}

		switch {
		case conditionEquals(lowerCond):
			lowerInclusive = true
			upperInclusive = true
			upperBound = lowerBound
		case conditionEquals(upperCond):
			lowerInclusive = true
			upperInclusive = true
			lowerBound = upperBound
		case conditionUpperBound(lowerCond):
			upperBound = lowerBound
			lowerBound = versioncompare.NewMin()
			upperInclusive = conditionCanEqual(lowerCond)
			lowerInclusive = true
		case conditionLowerBound(upperCond):
			lowerBound = upperBound
			upperBound = versioncompare.NewMax()
			lowerInclusive = conditionCanEqual(upperCond)
			upperInclusive = true
		default:
			upperInclusive = conditionCanEqual(upperCond)
			lowerInclusive = conditionCanEqual(lowerCond)
		}
	default:
		err = fmt.Errorf("unexpected conditions interval: %s", pkgVer)
		return
	}

	interval = PackageVerInterval{
		UpperBound:     upperBound,
		LowerBound:     lowerBound,
		UpperInclusive: upperInclusive,
		LowerInclusive: lowerInclusive,
	}

	return
}

func (pkgVer *PackageVer) validatedIntervals() error {
	c1 := pkgVer.Condition
	c2 := pkgVer.SCondition

	if _, known := knownConditions[c1]; !known {
		return fmt.Errorf("unknown condition (%s)", c1)
	}

	if _, known := knownConditions[c2]; !known {
		return fmt.Errorf("unknown condition (%s)", c2)
	}

	if pkgVer.Version == "" && c1 != "" {
		return fmt.Errorf("invalid empty version and condition (%s) combination", c1)
	}

	if pkgVer.SVersion == "" && c2 != "" {
		return fmt.Errorf("invalid empty version and condition (%s) combination", c2)
	}

	if (pkgVer.Version == "" && c1 == "") ||
		(pkgVer.SVersion == "" && c2 == "") {
		return nil
	}

	sameDirection := conditionsHaveSameDirection(c1, c2)
	if sameDirection {
		if conditionEquals(c1) && pkgVer.Version != pkgVer.SVersion {
			return fmt.Errorf("found contradicting package version requirements: %s", pkgVer)
		}

		return nil
	}

	v1 := versioncompare.New(pkgVer.Version)
	v2 := versioncompare.New(pkgVer.SVersion)

	comparisonResult := v1.Compare(v2)
	if (comparisonResult == versioncompare.LessThan && (conditionUpperBound(c1) || (conditionEquals(c1) && !conditionUpperBound(c2)))) ||
		(comparisonResult == versioncompare.EqualTo && (!conditionCanEqual(c1) || !conditionCanEqual(c2))) ||
		(comparisonResult == versioncompare.GreatherThan && (conditionUpperBound(c2) || (conditionEquals(c2) && !conditionUpperBound(c1)))) {
		return fmt.Errorf("version bounds (%s) don't overlap", pkgVer)
	}

	return nil
}

// String prints the contents of the given PackageVer struct.
func (pkgVer *PackageVer) String() string {
	return fmt.Sprintf("%s:C:'%s'V:'%s',C2:'%s'V2:'%s'", pkgVer.Name, pkgVer.Condition, pkgVer.Version, pkgVer.SCondition, pkgVer.SVersion)
}

// PackageStringToPackageVer converts a package string into an instance of PackageVer.
// The string may contain only the name of the package or also include a single package version constraint.
// Examples:
//   - "gcc"
//   - "gcc=9.1.0"
//   - "gcc < 9.1.0"
func PackageStringToPackageVer(packageString string) (pkgVer *PackageVer, err error) {
	matches := packageWithVersionRegex.FindStringSubmatch(packageString)
	if len(matches) != packageWithVersionExpectedMatches {
		err = fmt.Errorf("packages list entry \"%s\" does not match the '[name][optional_condition][optional_version]' format", packageString)
		return
	}

	return &PackageVer{
		Name:      matches[packageWithVersionNameIndex],
		Condition: matches[packageWithVersionConditionIndex],
		Version:   matches[packageWithVersionVersionIndex],
	}, err
}

// String outputs an interval in interval notation
func (interval *PackageVerInterval) String() (s string) {
	var (
		openParens, lower, upper, closeParens string
	)
	if interval.LowerInclusive {
		openParens = "["
	} else {
		openParens = "("
	}
	if interval.UpperInclusive {
		closeParens = "]"
	} else {
		closeParens = ")"
	}
	lower = interval.LowerBound.String()
	upper = interval.UpperBound.String()
	return fmt.Sprintf("%s%s,%s%s", openParens, lower, upper, closeParens)
}

// Equal returns true if two intervals are exactly equivalent
func (interval *PackageVerInterval) Equal(other *PackageVerInterval) (valid bool) {
	return interval.LowerBound.String() == other.LowerBound.String() &&
		interval.UpperBound.String() == other.UpperBound.String() &&
		interval.LowerInclusive == other.LowerInclusive &&
		interval.UpperInclusive == other.UpperInclusive
}

// Compare two intervals based first on their lower bound, then upper bound
func (interval *PackageVerInterval) Compare(other *PackageVerInterval) (result int) {
	const (
		lessThan     = -1
		equalTo      = 0
		greatherThan = 1
	)

	if interval.LowerBound.Compare(other.LowerBound) < 0 {
		return lessThan
	}
	if interval.LowerBound.Compare(other.LowerBound) > 0 {
		return greatherThan
	}
	if interval.LowerBound.Compare(other.LowerBound) == 0 {
		if interval.LowerInclusive && !other.LowerInclusive {
			return lessThan
		}
		if !interval.LowerInclusive && other.LowerInclusive {
			return greatherThan
		}
	}

	if interval.UpperBound.Compare(other.UpperBound) < 0 {
		return lessThan
	}
	if interval.UpperBound.Compare(other.UpperBound) > 0 {
		return greatherThan
	}
	if interval.UpperBound.Compare(other.UpperBound) == 0 {
		if interval.UpperInclusive && !other.UpperInclusive {
			return greatherThan
		}
		if !interval.UpperInclusive && other.UpperInclusive {
			return lessThan
		}
	}
	return equalTo
}

// versionInInterval returns true if ver is a version in the set of versions represented in interval
func (interval *PackageVerInterval) versionInInterval(ver *versioncompare.TolerantVersion) (valid bool) {
	if ver.Compare(interval.LowerBound) == 0 && interval.LowerInclusive {
		return true
	}
	if ver.Compare(interval.UpperBound) == 0 && interval.UpperInclusive {
		return true
	}
	if ver.Compare(interval.UpperBound) < 0 && ver.Compare(interval.LowerBound) > 0 {
		return true
	}
	return false
}

// Contains checks if the interval fully contains the query range
func (interval *PackageVerInterval) Contains(queryInterval *PackageVerInterval) (contains bool) {
	// Check the lower bound
	lowerBoundValid := interval.versionInInterval(queryInterval.LowerBound)
	upperBoundValid := interval.versionInInterval(queryInterval.UpperBound)

	return lowerBoundValid && upperBoundValid
}

// Satisfies returns true the query interval overlaps the current interval at any point (ie it provides a version of a package
// which satisfied the query)
func (interval *PackageVerInterval) Satisfies(queryInterval *PackageVerInterval) (valid bool) {
	var (
		queryUpperValid, queryLowerValid, superset bool
	)
	if interval.LowerBound.Compare(queryInterval.UpperBound) > 0 || interval.UpperBound.Compare(queryInterval.LowerBound) < 0 {
		// No overlap at all
		return false
	}

	// Check lower bound of the query
	switch {
	case queryInterval.LowerBound.Compare(interval.UpperBound) == 0:
		// Check if the query lower bound touches the interval upper bound exactly
		if interval.UpperInclusive && queryInterval.LowerInclusive {
			queryLowerValid = true
		}
	case queryInterval.LowerBound.Compare(interval.LowerBound) == 0:
		// Check if both lower bounds are the same
		if interval.LowerInclusive || !queryInterval.LowerInclusive {
			queryLowerValid = true
		}
	default:
		// Otherwise simple check
		queryLowerValid = interval.versionInInterval(queryInterval.LowerBound)
	}

	// Check the upper bound of the query
	switch {
	case queryInterval.UpperBound.Compare(interval.LowerBound) == 0:
		// Check if the query upper bound touches the interval lower bound exactly
		if interval.LowerInclusive && queryInterval.UpperInclusive {
			queryUpperValid = true
		}
	case queryInterval.UpperBound.Compare(interval.UpperBound) == 0:
		// Check if both upper bounds are the same
		if interval.UpperInclusive || !queryInterval.UpperInclusive {
			queryLowerValid = true
		}
	default:
		// Otherwise simple check
		queryUpperValid = interval.versionInInterval(queryInterval.UpperBound)
	}

	// Check if the query interval is a superset of the provided interval
	superset = queryInterval.LowerBound.Compare(interval.LowerBound) < 0 && queryInterval.UpperBound.Compare(interval.UpperBound) > 0

	return queryUpperValid || queryLowerValid || superset
}

// conditionCanEqual checks if the input condition allows "equal to" versions.
func conditionCanEqual(condition string) bool {
	return condition == "" || strings.Contains(condition, "=")
}

// conditionEqual checks if the input condition "equal to" versions.
func conditionEquals(condition string) bool {
	return condition == "" || condition == "="
}

// conditionsHaveSameDirection checks if both conditions are either the same
// or create the same boundary direction (greater, equal, or lesser).
func conditionsHaveSameDirection(firstCondition, secondCondition string) bool {
	return (firstCondition == secondCondition) ||
		(firstCondition != "" && secondCondition != "" && firstCondition[0] == secondCondition[0])
}

// conditionLowerBound checks if the input condition is of the ">" or ">=" variation.
func conditionLowerBound(condition string) bool {
	return strings.Contains(condition, ">")
}

// conditionUpperBound checks if the input condition is of the "<" or "<=" variation.
func conditionUpperBound(condition string) bool {
	return strings.Contains(condition, "<")
}
