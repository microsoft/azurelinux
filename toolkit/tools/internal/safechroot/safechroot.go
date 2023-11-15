// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safechroot

import (
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/systemdependency"

	"github.com/moby/sys/mountinfo"
	"github.com/sirupsen/logrus"
	"golang.org/x/sys/unix"
)

// BindMountPointFlags is a set of flags to do a bind mount.
const BindMountPointFlags = unix.MS_BIND | unix.MS_MGC_VAL

// FileToCopy represents a file to copy into a chroot using AddFiles. Dest is relative to the chroot directory.
type FileToCopy struct {
	Src         string
	Dest        string
	Permissions *os.FileMode
}

// MountPoint represents a system mount point used by a Chroot.
// It is guaranteed to be unmounted on application exit even on a SIGTERM so long as registerSIGTERMCleanup is invoked.
// The fields of MountPoint mirror those of the `mount` syscall.
type MountPoint struct {
	source string
	target string
	fstype string
	flags  uintptr
	data   string

	isMounted           bool
	mountBeforeDefaults bool
}

// Chroot represents a Chroot environment with automatic synchronization protections
// and guaranteed cleanup code even on SIGTERM so long as registerSIGTERMCleanup is invoked.
type Chroot struct {
	rootDir     string
	mountPoints []*MountPoint

	isExistingDir bool
}

// inChrootMutex guards against multiple Chroots entering their respective Chroots
// and running commands. Only a single Chroot can be active at a given time.
//
// activeChrootsMutex guards activeChroots reads and writes.
//
// activeChroots is slice of Initialized Chroots that should be cleaned up iff
// registerSIGTERMCleanup has been invoked. Use a slice instead of a map
// to ensure chroots can be cleaned up in LIFO order incase any are interdependent.
// Note:
//   - Docker based build doesn't need to maintain activeChroots because chroot come from
//     a pre-existing pool of chroots
//     (as opposed to regular build which create a new chroot each time a spec is built)
var (
	inChrootMutex      sync.Mutex
	activeChrootsMutex sync.Mutex
	activeChroots      []*Chroot
)

var defaultChrootEnv = []string{
	"USER=root",
	"HOME=/root",
	fmt.Sprintf("SHELL=%s", os.Getenv("SHELL")),
	fmt.Sprintf("TERM=%s", os.Getenv("TERM")),
	"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

const (
	unmountTypeLazy   = true
	unmountTypeNormal = !unmountTypeLazy
)

// init will always be called if this package is loaded
func init() {
	registerSIGTERMCleanup()
	logrus.RegisterExitHandler(cleanupAllChroots)
}

// NewMountPoint creates a new MountPoint struct to be created by a Chroot
func NewMountPoint(source, target, fstype string, flags uintptr, data string) (mountPoint *MountPoint) {
	return &MountPoint{
		source: source,
		target: target,
		fstype: fstype,
		flags:  flags,
		data:   data,
	}
}

// NewPreDefaultsMountPoint creates a new MountPoint struct to be created by a Chroot but before the default mount points.
func NewPreDefaultsMountPoint(source, target, fstype string, flags uintptr, data string) (mountPoint *MountPoint) {
	return &MountPoint{
		source:              source,
		target:              target,
		fstype:              fstype,
		flags:               flags,
		data:                data,
		mountBeforeDefaults: true,
	}
}

// NewOverlayMountPoint creates a new MountPoint struct and extra directories slice configured for a given overlay
func NewOverlayMountPoint(chrootDir, source, target, lowerDir, upperDir, workDir string) (mountPoint *MountPoint, extaDirsNeeds []string) {
	const (
		overlayFlags  = 0
		overlayFsType = "overlay"
	)

	upperDirInChroot := filepath.Join(chrootDir, upperDir)
	workDirInChroot := filepath.Join(chrootDir, workDir)

	overlayData := fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", lowerDir, upperDirInChroot, workDirInChroot)

	extaDirsNeeds = []string{upperDir, workDir}
	mountPoint = &MountPoint{
		source: source,
		target: target,
		fstype: overlayFsType,
		flags:  overlayFlags,
		data:   overlayData,
	}

	return
}

// NewChroot creates a new Chroot struct
func NewChroot(rootDir string, isExistingDir bool) *Chroot {
	// get chroot folder
	chrootDir, err := buildpipeline.GetChrootDir(rootDir)
	if err != nil {
		logger.Log.Panicf("Failed to get chroot dir - %s", err.Error())
		return nil
	}

	// create new safechroot
	c := new(Chroot)
	c.rootDir = chrootDir
	if buildpipeline.IsRegularBuild() {
		c.isExistingDir = isExistingDir
	} else {
		// Docker based pipeline recycle chroot =>
		// - chroot always exists
		// - chroot must be cleaned-up before being used
		c.isExistingDir = true
		buildpipeline.CleanupDockerChroot(c.rootDir)
	}
	return c
}

// Initialize initializes a Chroot, creating directories and mount points.
//   - tarPath is an optional path to a tar file that will be extracted at the root of the chroot.
//   - extraDirectories is an optional slice of additional directories that should be created before attempting to
//     mount inside the chroot.
//   - extraMountPoints is an optional slice of additional mount points that should be created inside the chroot,
//     they will automatically be unmounted on a Chroot Close.
//
// This call will block until the chroot initializes successfully.
// Only one Chroot will initialize at a given time.
func (c *Chroot) Initialize(tarPath string, extraDirectories []string, extraMountPoints []*MountPoint) (err error) {
	// On failed initialization, cleanup all chroot files
	const leaveChrootOnDisk = false

	// Acquire a lock on the global activeChrootsMutex to ensure SIGTERM
	// teardown doesn't happen mid-initialization.
	activeChrootsMutex.Lock()
	defer activeChrootsMutex.Unlock()

	if c.isExistingDir {
		_, err = os.Stat(c.rootDir)
		if os.IsNotExist(err) {
			err = fmt.Errorf("chroot directory (%s) does not exist", c.rootDir)
			return
		}
	} else {
		// Prevent a Chroot from being made on top of an existing directory.
		// Chroot cleanup involves deleting the rootdir, so assume Chroot
		// has exclusive ownership of it.
		_, err = os.Stat(c.rootDir)
		if !os.IsNotExist(err) {
			err = fmt.Errorf("chroot directory (%s) already exists", c.rootDir)
			return
		}

		// Create new root directory
		err = os.MkdirAll(c.rootDir, os.ModePerm)
		if err != nil {
			logger.Log.Warnf("Could not create chroot directory (%s)", c.rootDir)
			return
		}
	}

	// Defer cleanup after it has been confirmed rootDir will not
	// overwrite an existing directory when isExistingDir is set to false.
	defer func() {
		if err != nil {
			if buildpipeline.IsRegularBuild() {
				// mount/unmount is only supported in regular pipeline
				// Best effort cleanup in case mountpoint creation failed mid-way through. We will not try again so treat as final attempt.
				cleanupErr := c.unmountAndRemove(leaveChrootOnDisk, unmountTypeLazy)
				if cleanupErr != nil {
					logger.Log.Warnf("Failed to cleanup chroot (%s) during failed initialization. Error: %s", c.rootDir, cleanupErr)
				}
			} else {
				// release chroot dir
				cleanupErr := buildpipeline.ReleaseChrootDir(c.rootDir)
				if cleanupErr != nil {
					logger.Log.Warnf("Failed to release chroot (%s) during failed initialization. Error: %s", c.rootDir, cleanupErr)
				}
			}
		}
	}()

	// Extract a given tarball if necessary
	if tarPath != "" {
		err = extractWorkerTar(c.rootDir, tarPath)
		if err != nil {
			logger.Log.Warnf("Could not extract worker tar (%s)", err)
			return
		}
	}

	// Create extra directories
	for _, dir := range extraDirectories {
		err = os.MkdirAll(filepath.Join(c.rootDir, dir), os.ModePerm)
		if err != nil {
			logger.Log.Warnf("Could not create extra directory inside chroot (%s)", dir)
			return
		}
	}

	// mount is only supported in regular pipeline
	if buildpipeline.IsRegularBuild() {
		// Create kernel mountpoints
		allMountPoints := []*MountPoint{}

		for _, mountPoint := range extraMountPoints {
			if mountPoint.mountBeforeDefaults {
				allMountPoints = append(allMountPoints, mountPoint)
			}
		}

		allMountPoints = append(allMountPoints, defaultMountPoints()...)

		for _, mountPoint := range extraMountPoints {
			if !mountPoint.mountBeforeDefaults {
				allMountPoints = append(allMountPoints, mountPoint)
			}
		}

		// Assign to `c.mountPoints` now since `Initialize` will call `unmountAndRemove` if an error occurs.
		c.mountPoints = allMountPoints

		// Mount with the original unsorted order. Assumes the order of mounts is important.
		err = c.createMountPoints()
		if err != nil {
			logger.Log.Warn("Error creating mountpoints for chroot")
			return
		}

		// Mark this chroot as initialized, allowing it to be cleaned up on SIGTERM
		// if requested.
		activeChroots = append(activeChroots, c)
	}

	return
}

// AddFiles copies each file 'Src' to the relative path chrootRootDir/'Dest' in the chroot.
func (c *Chroot) AddFiles(filesToCopy ...FileToCopy) (err error) {
	for _, f := range filesToCopy {
		dest := filepath.Join(c.rootDir, f.Dest)
		logger.Log.Debugf("Copying '%s' to worker '%s'", f.Src, dest)

		if f.Permissions != nil {
			err = file.CopyAndChangeMode(f.Src, dest, os.ModePerm, *f.Permissions)
		} else {
			err = file.Copy(f.Src, dest)
		}

		if err != nil {
			logger.Log.Errorf("Error provisioning worker with '%s'", f.Src)
			return
		}
	}
	return
}

// CopyOutFile copies file 'srcPath' in the chroot to the host at 'destPath'
func (c *Chroot) CopyOutFile(srcPath string, destPath string) (err error) {
	srcPathFull := filepath.Join(c.rootDir, srcPath)
	err = file.Copy(srcPathFull, destPath)
	if err != nil {
		logger.Log.Errorf("Error copying file '%s'", err)
		return
	}
	return
}

// MoveOutFile moves file 'srcPath' in the chroot to the host at 'destPath', deleting the 'srcPath' file.
func (c *Chroot) MoveOutFile(srcPath string, destPath string) (err error) {
	srcPathFull := filepath.Join(c.rootDir, srcPath)
	err = file.Move(srcPathFull, destPath)
	if err != nil {
		logger.Log.Errorf("Error moving file '%s'", err)
		return
	}
	return
}

// Run runs a given function inside the Chroot. This function will synchronize
// with all other Chroots to ensure only one Chroot command is executed at a given time.
func (c *Chroot) Run(toRun func() error) (err error) {
	// Only a single chroot can be active at a given time for a single GO application.
	// acquire a global mutex to ensure this behavior.
	inChrootMutex.Lock()
	defer inChrootMutex.Unlock()

	// Alter the environment variables while inside the chroot, upon exit restore them.
	originalEnv := shell.CurrentEnvironment()
	shell.SetEnvironment(defaultChrootEnv)
	defer shell.SetEnvironment(originalEnv)

	err = c.UnsafeRun(toRun)

	return
}

// UnsafeRun runs a given function inside the Chroot. This function will not synchronize
// with other Chroots. The invoker is responsible for ensuring safety.
func (c *Chroot) UnsafeRun(toRun func() error) (err error) {
	const fsRoot = "/"

	originalRoot, err := os.Open(fsRoot)
	if err != nil {
		return
	}
	defer originalRoot.Close()

	cwd, err := os.Getwd()
	if err != nil {
		return
	}
	originalWd, err := os.Open(cwd)
	if err != nil {
		return
	}
	defer originalWd.Close()

	logger.Log.Debugf("Entering Chroot: '%s'", c.rootDir)
	err = unix.Chroot(c.rootDir)
	if err != nil {
		return
	}
	defer c.restoreRoot(originalRoot, originalWd)

	err = os.Chdir(fsRoot)
	if err != nil {
		return
	}

	err = toRun()
	return
}

// RootDir returns the Chroot's root directory.
func (c *Chroot) RootDir() string {
	return c.rootDir
}

// Close will unmount the chroot and cleanup its files.
// This call will block until the chroot cleanup runs.
// Only one Chroot will close at a given time.
func (c *Chroot) Close(leaveOnDisk bool) (err error) {
	// Acquire a lock on the global activeChrootsMutex to ensure SIGTERM
	// teardown doesn't happen mid-close.
	activeChrootsMutex.Lock()
	defer activeChrootsMutex.Unlock()

	if buildpipeline.IsRegularBuild() {
		index := -1
		for i, chroot := range activeChroots {
			if chroot == c {
				index = i
				break
			}
		}

		if index < 0 {
			// Already closed.
			return
		}

		// mount is only supported in regular pipeline
		err = c.unmountAndRemove(leaveOnDisk, unmountTypeNormal)
		if err != nil {
			logger.Log.Warnf("Chroot cleanup failed, will retry with lazy unmount. Error: %s", err)
			err = c.unmountAndRemove(leaveOnDisk, unmountTypeLazy)
		}
		if err == nil {
			const emptyLen = 0
			// Remove this chroot from the list of active ones since it has now been cleaned up.
			// Create a new slice that is -1 capacity of the current activeChroots.
			newActiveChroots := make([]*Chroot, emptyLen, len(activeChroots)-1)
			newActiveChroots = append(newActiveChroots, activeChroots[:index]...)
			newActiveChroots = append(newActiveChroots, activeChroots[index+1:]...)
			activeChroots = newActiveChroots
		}
	} else {
		// release chroot dir
		err = buildpipeline.ReleaseChrootDir(c.rootDir)
	}

	return
}

// registerSIGTERMCleanup will register SIGTERM handling to force all Chroots
// to Close before exiting the application.
func registerSIGTERMCleanup() {
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, unix.SIGINT, unix.SIGTERM)
	go cleanupAllChrootsOnSignal(signals)
}

// cleanupAllChrootsOnSignal will cleanup all chroots on an os signal.
func cleanupAllChrootsOnSignal(signals chan os.Signal) {
	sig := <-signals
	logger.Log.Error(sig)

	cleanupAllChroots()

	os.Exit(1)
}

// cleanupAllChroots will unmount and cleanup all running chroots.
// *NOTE*: invocation of this method assumes application teardown. It will leave
// Chroot in state where all operations (Initialize/Run/Close) will block indefinitely.
func cleanupAllChroots() {
	// This code blocks all Chroot operations,
	// and frees the underlying OS handles associated with the chroots (unmounting them).
	//
	// However, it does not actually free the Chroot objects created by other goroutines, as they hold reference to them.
	// Thus it could leave other go routines' Chroots in a bad state, where the routine believes the chroot is in-fact initialized,
	// but really it has already been cleaned up.

	const (
		// On cleanup, remove all chroot files
		leaveChrootOnDisk = false
		// On cleanup SIGKILL all children processes.
		stopSignal = unix.SIGKILL
	)

	// Acquire and permanently hold the global activeChrootsMutex to ensure no
	// new Chroots are initialized or unmounted during this teardown routine
	logger.Log.Info("Waiting for outstanding chroot initialization and cleanup to finish")
	activeChrootsMutex.Lock()

	// Acquire and permanently hold the global inChrootMutex lock to ensure this application is not
	// inside any Chroot.
	logger.Log.Info("Waiting for outstanding chroot commands to finish")
	shell.PermanentlyStopAllChildProcesses(stopSignal)
	inChrootMutex.Lock()

	// mount is only supported in regular pipeline
	failedToUnmount := false
	if buildpipeline.IsRegularBuild() {
		// Cleanup chroots in LIFO order incase any are interdependent (e.g. nested safe chroots)
		logger.Log.Info("Cleaning up all active chroots")
		for i := len(activeChroots) - 1; i >= 0; i-- {
			logger.Log.Infof("Cleaning up chroot (%s)", activeChroots[i].rootDir)
			err := activeChroots[i].unmountAndRemove(leaveChrootOnDisk, unmountTypeLazy)
			// Perform best effort cleanup: unmount as many chroots as possible,
			// even if one fails.
			if err != nil {
				logger.Log.Errorf("Failed to unmount chroot (%s)", activeChroots[i].rootDir)
				failedToUnmount = true
			}
		}
	}

	if failedToUnmount {
		logger.Log.Fatalf("Failed to unmount a chroot, manual unmount required. See above errors for details on which mounts failed.")
	} else {
		logger.Log.Info("Cleanup finished")
	}
}

// unmountAndRemove retries to unmount directories that were mounted into
// the chroot until the unmounts succeed or too many failed attempts.
// This is to avoid leaving folders like /dev mounted when the chroot folder is forcefully deleted in cleanup.
// Iff all mounts were successfully unmounted, the chroot's root directory will be removed if requested.
// If doLazyUnmount is true, use the lazy unmount flag which will allow the unmount to succeed even if the mount point is busy.
func (c *Chroot) unmountAndRemove(leaveOnDisk, lazyUnmount bool) (err error) {
	const (
		retryDuration      = time.Second
		totalAttempts      = 3
		unmountFlagsNormal = 0
		// Do a lazy unmount as a fallback. This will allow the unmount to succeed even if the mount point is busy.
		// This is to avoid leaving folders like /dev mounted if the chroot folder is forcefully deleted by the user. Even
		// if the mount is busy at least it will be detached from the filesystem and will not damage the host.
		unmountFlagsLazy = unix.MNT_DETACH
	)
	unmountFlags := unmountFlagsNormal
	if lazyUnmount {
		unmountFlags = unmountFlagsLazy
	}

	// Unmount in the reverse order of mounting to ensure that any nested mounts are unraveled in the correct order.
	for i := len(c.mountPoints) - 1; i >= 0; i-- {
		mountPoint := c.mountPoints[i]

		fullPath := filepath.Join(c.rootDir, mountPoint.target)

		var exists bool
		exists, err = file.PathExists(fullPath)
		if err != nil {
			err = fmt.Errorf("failed to check if mount point (%s) exists. Error: %s", fullPath, err)
			return
		}
		if !exists {
			logger.Log.Debugf("Skipping unmount of (%s) because path doesn't exist", fullPath)
			continue
		}

		var isMounted bool
		isMounted, err = mountinfo.Mounted(fullPath)
		if err != nil {
			err = fmt.Errorf("failed to check if mount point (%s) is mounted. Error: %s", fullPath, err)
			return
		}
		if !isMounted {
			logger.Log.Debugf("Skipping unmount of (%s) because it is not mounted", fullPath)
			continue
		}

		logger.Log.Debugf("Unmounting (%s)", fullPath)

		// Skip mount points if they were not successfully created
		if !mountPoint.isMounted {
			continue
		}

		_, err = retry.RunWithExpBackoff(func() error {
			logger.Log.Debugf("Calling unmount on path(%s) with flags (%v)", fullPath, unmountFlags)
			umountErr := unix.Unmount(fullPath, unmountFlags)
			return umountErr
		}, totalAttempts, retryDuration, 2.0, nil)

		if err != nil {
			logger.Log.Warnf("Failed to unmount (%s). Error: %s", fullPath, err)
			return
		}
	}

	if !leaveOnDisk {
		err = os.RemoveAll(c.rootDir)
	}

	return
}

// defaultMountPoints returns a new copy of the default mount points used by a functional chroot
func defaultMountPoints() []*MountPoint {
	return []*MountPoint{
		&MountPoint{
			target: "/dev",
			fstype: "devtmpfs",
		},
		&MountPoint{
			target: "/proc",
			fstype: "proc",
		},
		&MountPoint{
			target: "/sys",
			fstype: "sysfs",
		},
		&MountPoint{
			target: "/run",
			fstype: "tmpfs",
		},
		&MountPoint{
			target: "/dev/pts",
			fstype: "devpts",
			data:   "gid=5,mode=620",
		},
	}
}

// restoreRoot will restore the original root of the GO application, cleaning up
// after the run command. Will panic on error.
func (c *Chroot) restoreRoot(originalRoot, originalWd *os.File) {
	logger.Log.Debugf("Exiting Chroot: '%s'", c.rootDir)

	err := originalRoot.Chdir()
	if err != nil {
		logger.Log.Panicf("Failed to change directory to original root. Error: %s", err)
	}

	err = unix.Chroot(".")
	if err != nil {
		logger.Log.Panicf("Failed to restore original chroot. Error: %s", err)
	}

	err = originalWd.Chdir()
	if err != nil {
		logger.Log.Panicf("Failed to change directory to original root. Error: %s", err)
	}

	return
}

// createMountPoints will create a provided list of mount points
func (c *Chroot) createMountPoints() (err error) {
	for _, mountPoint := range c.mountPoints {
		fullPath := filepath.Join(c.rootDir, mountPoint.target)
		logger.Log.Debugf("Mounting: source: (%s), target: (%s), fstype: (%s), flags: (%#x), data: (%s)",
			mountPoint.source, fullPath, mountPoint.fstype, mountPoint.flags, mountPoint.data)

		err = os.MkdirAll(fullPath, os.ModePerm)
		if err != nil {
			logger.Log.Warnf("Could not create directory (%s)", fullPath)
			return
		}

		err = unix.Mount(mountPoint.source, fullPath, mountPoint.fstype, mountPoint.flags, mountPoint.data)
		if err != nil {
			logger.Log.Errorf("Mount of (%s) to (%s) failed. Error: %s", mountPoint.source, fullPath, err)
			return
		}

		mountPoint.isMounted = true
	}

	return
}

// extractWorkerTar uses tar with gzip or pigz to setup a chroot directory using a rootfs tar
func extractWorkerTar(chroot string, workerTar string) (err error) {
	gzipTool, err := systemdependency.GzipTool()
	if err != nil {
		return err
	}

	logger.Log.Debugf("Using (%s) to extract tar", gzipTool)
	_, _, err = shell.Execute("tar", "-I", gzipTool, "-xf", workerTar, "-C", chroot)
	return
}
