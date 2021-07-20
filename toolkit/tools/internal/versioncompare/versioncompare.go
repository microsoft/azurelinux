// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package versioncompare

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

const (
	LessThan     = -1
	EqualTo      = 0
	GreatherThan = 1
)

var (
	componentRegex      = regexp.MustCompile(`(\d+|[a-z]+)`)
	epochComponentRegex = regexp.MustCompile(`^(\d+|[a-z])\:`)
)

// TolerantVersion is a flexible version representation
type TolerantVersion struct {
	versionComponents []uint64
	releaseComponents []uint64
	isMaxVer          bool
	isMinVer          bool
	original          string
}

// New returns new TolerantVersion
func New(versionString string) *TolerantVersion {
	v := &TolerantVersion{original: versionString}
	v.parse(versionString)
	return v
}

// NewMax returns a special version which is always greater than any other version
func NewMax() *TolerantVersion {
	return &TolerantVersion{original: "MAX_VER", isMaxVer: true}
}

// NewMin returns a special version which is always less than any other version
func NewMin() *TolerantVersion {
	return &TolerantVersion{original: "MIN_VER", isMinVer: true}
}

// CompareWithConditional evaluates a conditional statement
func (v *TolerantVersion) CompareWithConditional(condition string, b *TolerantVersion) (valid bool, err error) {
	// Validate the operator
	switch condition {
	case "<":
		return v.Compare(b) < 0, nil
	case "<=":
		return v.Compare(b) <= 0, nil
	case ">":
		return v.Compare(b) > 0, nil
	case ">=":
		return v.Compare(b) >= 0, nil
	case "=":
		return v.Compare(b) == 0, nil
	default:
		return false, fmt.Errorf("unknown conditional operator %s", condition)
	}
}

// Compare compares this version and the argument version and returns 1 if the argument's version is higher,
// -1 if argument's version is lower and 0 if they are equal (three-way comparison)
func (v *TolerantVersion) Compare(other *TolerantVersion) int {
	switch {
	case v.isMaxVer && other.isMaxVer:
		fallthrough
	case v.isMinVer && other.isMinVer:
		return EqualTo
	case v.isMaxVer || other.isMinVer:
		return GreatherThan
	case v.isMinVer || other.isMaxVer:
		return LessThan
	}

	for i := range v.versionComponents {
		if i == len(other.versionComponents) {
			return GreatherThan
		}
		if v.versionComponents[i] < other.versionComponents[i] {
			return LessThan
		}
		if v.versionComponents[i] > other.versionComponents[i] {
			return GreatherThan
		}
	}
	if len(v.versionComponents) < len(other.versionComponents) {
		return LessThan
	}

	// Only check the release components if both versions request it.
	if len(v.releaseComponents) > 0 && len(other.releaseComponents) > 0 {
		for i := range v.releaseComponents {
			if i == len(other.releaseComponents) {
				return GreatherThan
			}
			if v.releaseComponents[i] < other.releaseComponents[i] {
				return LessThan
			}
			if v.releaseComponents[i] > other.releaseComponents[i] {
				return GreatherThan
			}
		}
		if len(v.releaseComponents) < len(other.releaseComponents) {
			return LessThan
		}
	}

	return EqualTo
}

// String returns the original string representation of the version
func (v *TolerantVersion) String() string {
	return v.original
}

// parse takes an arbitrary versionString and fills v with the processed version information
func (v *TolerantVersion) parse(versionString string) {
	var (
		versionSubstring, releaseSubstring string
	)
	// Split off any release number if present. '-' is an illegal character for versions so we can split on it
	splitString := strings.Split(versionString, "-")
	versionSubstring = splitString[0]
	if len(splitString) > 1 {
		releaseSubstring = splitString[1]
	} else {
		releaseSubstring = ""
	}

	rawComponents := componentRegex.FindAllString(versionSubstring, -1)

	// If no epoch is set in the version, apply an epoch of 0 so all versions have one.
	if epochComponentRegex.FindString(versionSubstring) == "" {
		rawComponents = append([]string{"0"}, rawComponents...)
	}

	v.versionComponents = make([]uint64, len(rawComponents))
	for i := range rawComponents {
		// Base36 to support lowercase characters
		// 64bits to support at least 12 characters (12 times 'z')
		intComponent, err := strconv.ParseUint(rawComponents[i], 36, 64)
		if err == nil {
			v.versionComponents[i] = intComponent
		}
		// On error keep default value (0)
	}

	// Run again if we have a release version as well
	if releaseSubstring != "" {
		rawComponents = componentRegex.FindAllString(releaseSubstring, -1)
		v.releaseComponents = make([]uint64, len(rawComponents))
		for i := range rawComponents {
			// Base36 to support lowercase characters
			// 64bits to support at least 12 characters (12 times 'z')
			intComponent, err := strconv.ParseUint(rawComponents[i], 36, 64)
			if err == nil {
				v.releaseComponents[i] = intComponent
			}
			// On error keep default value (0)
		}
	}
}
