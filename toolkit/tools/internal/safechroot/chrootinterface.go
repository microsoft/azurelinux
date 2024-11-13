// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safechroot

type ChrootInterface interface {
	RootDir() string
	Run(toRun func() error) error
	UnsafeRun(toRun func() error) error
	AddFiles(filesToCopy ...FileToCopy) error
}
