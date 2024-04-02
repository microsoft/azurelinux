// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safechroot

// DummyChroot is a placeholder that implements ChrootInterface.
type DummyChroot struct {
}

func (d *DummyChroot) RootDir() string {
	return "/"
}

func (d *DummyChroot) Run(toRun func() error) (err error) {
	// Only execute the function, no chroot operations
	return toRun()
}

func (d *DummyChroot) UnsafeRun(toRun func() error) (err error) {
	return toRun()
}

func (d *DummyChroot) AddFiles(filesToCopy ...FileToCopy) (err error) {
	return addFilesToDestination(d.RootDir(), filesToCopy...)
}
