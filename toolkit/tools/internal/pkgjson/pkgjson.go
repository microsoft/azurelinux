// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkgjson

import (
	"fmt"
	"regexp"
	"sort"
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

//cmp func(a, b E) int

func PackageLess(a, b PackageVer) bool {
	if a.Name < b.Name {
		return true
	} else if a.Name == b.Name {
		v1 := versioncompare.New(a.Version)
		v2 := versioncompare.New(b.Version)
		if v1.LT(v2) {
			return true
		}
	}

	return false
}

func SortPackageList(packages []*Package) {

	sort.Slice(packages, func(i, j int) bool {
		return PackageLess(*packages[i].Provides, *packages[j].Provides)
	})

	// For each package, also sort the package lists
	for _, pkg := range packages {
		sort.Slice(pkg.Requires, func(i, j int) bool {
			return PackageLess(*pkg.Requires[i], *pkg.Requires[j])
		})
		sort.Slice(pkg.BuildRequires, func(i, j int) bool {
			return PackageLess(*pkg.BuildRequires[i], *pkg.BuildRequires[j])
		})
		sort.Slice(pkg.TestRequires, func(i, j int) bool {
			return PackageLess(*pkg.TestRequires[i], *pkg.TestRequires[j])
		})
	}
}

// ParsePackageJSON reads a package list json file
func (pkg *PackageRepo) ParsePackageJSON(path string) (err error) {
	logger.Log.Infof("Opening %s", path)

	if err = jsonutils.ReadJSONFile(path, &pkg); err != nil {
		return err
	}

	// Ensure deterministic ordering of the package list
	SortPackageList(pkg.Repo)

	return nil
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
		if v1.LT(v2) {
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

	if (v1.LT(v2) && (conditionUpperBound(c1) || (conditionEquals(c1) && !conditionUpperBound(c2)))) ||
		(v1.EQ(v2) && (!conditionCanEqual(c1) || !conditionCanEqual(c2))) ||
		(v1.GT(v2) && (conditionUpperBound(c2) || (conditionEquals(c2) && !conditionUpperBound(c1)))) {
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

	if interval.LowerBound.LT(other.LowerBound) {
		return lessThan
	}
	if interval.LowerBound.GT(other.LowerBound) {
		return greatherThan
	}
	if interval.LowerBound.EQ(other.LowerBound) {
		if interval.LowerInclusive && !other.LowerInclusive {
			return lessThan
		}
		if !interval.LowerInclusive && other.LowerInclusive {
			return greatherThan
		}
	}

	if interval.UpperBound.LT(other.UpperBound) {
		return lessThan
	}
	if interval.UpperBound.GT(other.UpperBound) {
		return greatherThan
	}
	if interval.UpperBound.EQ(other.UpperBound) {
		if interval.UpperInclusive && !other.UpperInclusive {
			return greatherThan
		}
		if !interval.UpperInclusive && other.UpperInclusive {
			return lessThan
		}
	}
	return equalTo
}

// Contains checks if the interval fully contains the query range
func (interval *PackageVerInterval) contains(queryInterval *PackageVerInterval) (contains bool) {
	lowerBoundValid := false
	upperBoundValid := false

	// Check if the each bound of the query is within the interval, or if it is the same as the bound of the interval
	// and the bound is inclusive.
	if interval.LowerBound.LT(queryInterval.LowerBound) ||
		(interval.LowerBound.EQ(queryInterval.LowerBound) && interval.LowerInclusive) ||
		(interval.LowerBound.EQ(queryInterval.LowerBound) && (interval.LowerInclusive == queryInterval.LowerInclusive)) {
		lowerBoundValid = true
	}

	if interval.UpperBound.GT(queryInterval.UpperBound) ||
		(interval.UpperBound.EQ(queryInterval.UpperBound) && interval.UpperInclusive) ||
		(interval.UpperBound.EQ(queryInterval.UpperBound) && (interval.UpperInclusive == queryInterval.UpperInclusive)) {
		upperBoundValid = true
	}

	return lowerBoundValid && upperBoundValid
}

func (interval *PackageVerInterval) intersects(queryInterval *PackageVerInterval) (intersects bool) {
	if interval.LowerBound.GT(queryInterval.UpperBound) || interval.UpperBound.LT(queryInterval.LowerBound) {
		// No overlap at all
		return false
	}

	// Handle equal versions but open intervals
	if interval.LowerBound.EQ(queryInterval.UpperBound) && (!interval.LowerInclusive || !queryInterval.UpperInclusive) {
		return false
	}

	if interval.UpperBound.EQ(queryInterval.LowerBound) && (!interval.UpperInclusive || !queryInterval.LowerInclusive) {
		return false
	}

	return true
}

// GuaranteedSatisfies returns true if every version in the interval is guaranteed to satisfy the query. A pair of
// intervals may overlap, but not guarantee that the query interval is satisfied.
// i.e., interval: [1, 3], query: [2, 4] will overlap, but the valid version '1' does not satisfy the query.
func (interval *PackageVerInterval) GuaranteedSatisfies(queryInterval *PackageVerInterval) (valid bool) {
	return queryInterval.contains(interval)
}

// Satisfies returns true if there exists some version in the interval that satisfies the query interval.
func (interval *PackageVerInterval) Satisfies(queryInterval *PackageVerInterval) (valid bool) {
	return interval.intersects(queryInterval)
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
