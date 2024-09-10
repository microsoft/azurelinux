// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"fmt"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

type FileCopyBuilder struct {
	Src            string
	Dst            string
	DirFileMode    os.FileMode
	ChangeFileMode bool
	FileMode       os.FileMode
	NoDereference  bool
}

func NewFileCopyBuilder(src string, dst string) FileCopyBuilder {
	return FileCopyBuilder{
		Src:            src,
		Dst:            dst,
		DirFileMode:    os.ModePerm,
		ChangeFileMode: false,
		FileMode:       os.ModePerm,
		NoDereference:  false,
	}
}

func (b FileCopyBuilder) SetDirFileMode(dirFileMode os.FileMode) FileCopyBuilder {
	b.DirFileMode = dirFileMode
	return b
}

func (b FileCopyBuilder) SetFileMode(fileMode os.FileMode) FileCopyBuilder {
	b.ChangeFileMode = true
	b.FileMode = fileMode
	return b
}

func (b FileCopyBuilder) SetNoDereference() FileCopyBuilder {
	b.NoDereference = true
	return b
}

func (b FileCopyBuilder) Run() (err error) {
	logger.Log.Debugf("Copying (%s) to (%s)", b.Src, b.Dst)

	if b.NoDereference && b.ChangeFileMode {
		return fmt.Errorf("cannot modify file permissions of symlinks")
	}

	if b.NoDereference {
		isSrcFileOrSymlink, err := IsFileOrSymlink(b.Src)
		if err != nil {
			return err
		}
		if !isSrcFileOrSymlink {
			return fmt.Errorf("source (%s) is not a file or a symlink", b.Src)
		}
	} else {
		isSrcFile, err := IsFile(b.Src)
		if err != nil {
			return err
		}
		if !isSrcFile {
			return fmt.Errorf("source (%s) is not a file", b.Src)
		}
	}

	err = createDestinationDir(b.Dst, b.DirFileMode)
	if err != nil {
		return
	}

	args := []string(nil)
	if b.NoDereference {
		args = append(args, "--no-dereference")
	}

	args = append(args, "--preserve=mode", b.Src, b.Dst)

	err = shell.NewExecBuilder("cp", args...).
		LogLevel(logrus.DebugLevel, logrus.WarnLevel).
		ErrorStderrLines(1).
		Execute()
	if err != nil {
		return
	}

	if b.ChangeFileMode {
		logger.Log.Debugf("Calling chmod on (%s) with the mode (%v)", b.Dst, b.FileMode)
		err = os.Chmod(b.Dst, b.FileMode)
	}

	return
}
