// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"fmt"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

type ShadowEntry struct {
	Name                     string
	EncryptedPassword        string
	LastPasswordChange       *int
	MinPasswordAge           *int
	MaxPasswordAge           *int
	PasswordWarningPeriod    *int
	PasswordInactivityPeriod *int
	AccountExpirationDate    *int
}

func ReadShadowFile(rootDir string) ([]ShadowEntry, error) {
	lines, err := file.ReadLines(filepath.Join(rootDir, ShadowFile))
	if err != nil {
		return nil, fmt.Errorf("failed to read %s file:\n%w", ShadowFile, err)
	}

	entries, err := parseShadowFile(lines)
	if err != nil {
		return nil, fmt.Errorf("invalid %s file:\n%w", ShadowFile, err)
	}

	return entries, nil
}

func parseShadowFile(lines []string) ([]ShadowEntry, error) {
	entries := []ShadowEntry(nil)
	for i, line := range lines {
		entry, err := parseShadowFileEntry(line)
		if err != nil {
			return nil, fmt.Errorf("invalid line %d", i)
		}

		entries = append(entries, entry)
	}

	return entries, nil
}

func parseShadowFileEntry(line string) (ShadowEntry, error) {
	const (
		numFields = 9
	)

	fields := strings.Split(line, ":")
	if len(fields) != numFields {
		return ShadowEntry{}, fmt.Errorf("%d fields instead of %d", len(fields), numFields)
	}

	lastPasswordChange, err := parseOptionalInt(fields[2])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid date of last password change:\n%w", err)
	}

	minPasswordAge, err := parseOptionalInt(fields[3])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid minimum password age:\n%w", err)
	}

	maxPasswordAge, err := parseOptionalInt(fields[4])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid maximum password age:\n%w", err)
	}

	passwordWarningPeriod, err := parseOptionalInt(fields[5])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid password warning period:\n%w", err)
	}

	passwordInactivityPeriod, err := parseOptionalInt(fields[6])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid password inactivity period:\n%w", err)
	}

	accountExpirationDate, err := parseOptionalInt(fields[7])
	if err != nil {
		return ShadowEntry{}, fmt.Errorf("invalid account expiration date:\n%w", err)
	}

	entry := ShadowEntry{
		Name:                     fields[0],
		EncryptedPassword:        fields[1],
		LastPasswordChange:       lastPasswordChange,
		MinPasswordAge:           minPasswordAge,
		MaxPasswordAge:           maxPasswordAge,
		PasswordWarningPeriod:    passwordWarningPeriod,
		PasswordInactivityPeriod: passwordInactivityPeriod,
		AccountExpirationDate:    accountExpirationDate,
	}
	return entry, nil
}

func parseOptionalInt(value string) (*int, error) {
	if value == "" {
		return nil, nil
	}

	a, err := strconv.Atoi(value)
	return &a, err
}

func GetShadowFileEntryForUser(rootDir string, user string) (ShadowEntry, error) {
	entries, err := ReadShadowFile(rootDir)
	if err != nil {
		return ShadowEntry{}, err
	}

	entry, found := sliceutils.FindValueFunc(entries, func(entry ShadowEntry) bool {
		return entry.Name == user
	})
	if !found {
		return ShadowEntry{}, fmt.Errorf("failed to find user (%s) in %s file", user, ShadowFile)
	}

	return entry, nil
}
