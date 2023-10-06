// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package diskutils

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"golang.org/x/sys/unix"
)

type MountFlags uintptr

type FstabEntry struct {
	Source    string     `json:"source"`
	Target    string     `json:"target"`
	FsType    string     `json:"fstype"`
	Options   MountFlags `json:"vfs-options"`
	FsOptions string     `json:"fs-options"`
	Freq      int        `json:"freq"`
	PassNo    int        `json:"passno"`
}

type findmntOutput struct {
	FileSystems []FstabEntry `json:"filesystems"`
}

func (f *MountFlags) UnmarshalJSON(b []byte) (err error) {
	var stringValue string
	err = json.Unmarshal(b, &stringValue)
	if err != nil {
		return fmt.Errorf("failed to parse MountFlags:\n%w", err)
	}

	var value MountFlags
	options := strings.Split(stringValue, ",")
	for _, option := range options {
		switch option {
		case "async":
			value |= unix.MS_ASYNC

		case "atime":
			value &= ^MountFlags(unix.MS_NOATIME)

		case "noatime":
			value |= unix.MS_NOATIME

		case "dev":
			value &= ^MountFlags(unix.MS_NODEV)

		case "nodev":
			value |= unix.MS_NODEV

		case "diratime":
			value &= ^MountFlags(unix.MS_NODIRATIME)

		case "nodiratime":
			value |= unix.MS_NODIRATIME

		case "dirsync":
			value |= unix.MS_DIRSYNC

		case "exec":
			value &= ^MountFlags(unix.MS_NOEXEC)

		case "noexec":
			value |= unix.MS_NOEXEC

		case "iversion":
			value |= unix.MS_I_VERSION

		case "mand":
			value |= unix.MS_MANDLOCK

		case "nomand":
			value &= ^MountFlags(unix.MS_MANDLOCK)

		case "relatime":
			value |= unix.MS_RELATIME

		case "norelatime":
			value &= ^MountFlags(unix.MS_RELATIME)

		case "strictatime":
			value |= unix.MS_STRICTATIME

		case "nostrictatime":
			value &= ^MountFlags(unix.MS_STRICTATIME)

		case "suid":
			value &= ^MountFlags(unix.MS_NOSUID)

		case "nosuid":
			value |= unix.MS_NOSUID

		case "remount":
			value |= unix.MS_REMOUNT

		case "ro":
			value |= unix.MS_RDONLY

		case "rw":
			value &= ^MountFlags(unix.MS_RDONLY)

		case "sync":
			value |= unix.MS_SYNC

		// These options are only relevant for the fstab file.
		case "owner", "user", "nouser", "users", "group", "auto", "noauto", "nofail", "_netdev", "_rnetdev":

		// There isn't a fixed set of defaults. So, no easy way to support this.
		case "defaults":
			return fmt.Errorf("unsupported mount flag (%s)", option)

		// Ignore empty options.
		case "":

		default:
			return fmt.Errorf("unknown mount flag (%s)", option)
		}
	}

	*f = value
	return nil
}

func ReadFstabFile(fstabPath string) ([]FstabEntry, error) {
	// Read the fstab file.
	// The `findmnt` command provides a convenient JSON output. In addition, it helpfully splits the
	// common vfs options from the filesystem specific options.
	jsonString, _, err := shell.Execute("findmnt", "--fstab", "--tab-file", fstabPath,
		"--json", "--output", "source,target,fstype,vfs-options,fs-options,freq,passno")
	if err != nil {
		return nil, fmt.Errorf("failed to read fstab file (%s):\n%w", fstabPath, err)
	}

	var output findmntOutput
	err = json.Unmarshal([]byte(jsonString), &output)
	if err != nil {
		return nil, fmt.Errorf("failed to read fstab file (%s): json parse error:\n%w", fstabPath, err)
	}

	return output.FileSystems, nil
}
