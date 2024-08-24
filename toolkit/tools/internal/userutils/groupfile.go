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

type GroupEntry struct {
	Name     string
	Password string
	GID      int
	UserList []string
}

func ReadGroupFile(rootDir string) ([]GroupEntry, error) {
	lines, err := file.ReadLines(filepath.Join(rootDir, GroupFile))
	if err != nil {
		return nil, fmt.Errorf("failed to read %s file:\n%w", GroupFile, err)
	}

	entries, err := parseGroupFile(lines)
	if err != nil {
		return nil, fmt.Errorf("invalid %s file:\n%w", GroupFile, err)
	}

	return entries, nil
}

func parseGroupFile(lines []string) ([]GroupEntry, error) {
	entries := []GroupEntry(nil)
	for i, line := range lines {
		entry, err := parseGroupFileEntry(line)
		if err != nil {
			return nil, fmt.Errorf("invalid line %d", i)
		}

		entries = append(entries, entry)
	}

	return entries, nil
}

func parseGroupFileEntry(line string) (GroupEntry, error) {
	const (
		numFields = 4
	)

	fields := strings.Split(line, ":")
	if len(fields) != numFields {
		return GroupEntry{}, fmt.Errorf("%d fields instead of %d", len(fields), numFields)
	}

	gidStr := fields[2]
	gid, err := strconv.Atoi(gidStr)
	if err != nil {
		return GroupEntry{}, fmt.Errorf("invalid GID:\n%w", err)
	}

	usersStr := fields[3]
	users := strings.Split(usersStr, ",")

	entry := GroupEntry{
		Name:     fields[0],
		Password: fields[1],
		GID:      gid,
		UserList: users,
	}
	return entry, nil
}

func GetUserGroups(rootDir string, username string) ([]string, error) {
	systemGroups, err := ReadGroupFile(rootDir)
	if err != nil {
		return nil, err
	}

	userGroups := []string(nil)
	for _, group := range systemGroups {
		userInGroup := sliceutils.ContainsValue(group.UserList, username)
		if userInGroup {
			userGroups = append(userGroups, group.Name)
		}
	}

	return userGroups, nil
}
