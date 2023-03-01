// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package timestamp_v2

import (
	"fmt"
	"os"
	"time"

	"golang.org/x/sys/unix"
)

const (
	blockTimeMilliseconds        = 250 // Maximum time to wait for a contested file
	blockPollingTimeMilliseconds = 10  // How often to check if the lock is available
)

// waitOnFileLock will synchronize access to the file `fileToLock` across processes/threads, blocking for at most `blockMillis` milliseconds.
// The lock may be acquired in either shared or exclusive mode. Multiple callers may hold the lock in shared mode.
// Each file descriptor may only be locked once, this is used to coordinate multiple readers/writers across independent processes rather than
// threads inside a single program.
func waitOnFileLock(flockFile *os.File, blockMillis int64, exclusive bool) (err error) {
	lockMode := unix.LOCK_NB
	if exclusive {
		lockMode |= unix.LOCK_EX
	} else {
		lockMode |= unix.LOCK_SH
	}
	if flockFile == nil {
		err = fmt.Errorf("failed to open timing data lock on nil file descriptor")
		return
	}

	start := time.Now()
	for {
		err = unix.Flock(int(flockFile.Fd()), lockMode)
		if err == nil || time.Since(start).Milliseconds() > blockMillis {
			break
		}
		time.Sleep(time.Millisecond * blockPollingTimeMilliseconds)
	}

	if err != nil {
		err = fmt.Errorf("failed to secure timing data lock after %d milliseconds- %w", blockMillis, err)
	} else {
		if exclusive {
			failsafeLoggerTracef("waitOnFileLock: LOCK EXCLUSIVE\n")
		} else {
			failsafeLoggerTracef("waitOnFileLock: LOCK SHARED\n")
		}
	}

	return
}

// relaxToSharedLock will set the lock to shared. Setting a shared lock to shared has no additional effect.
func relaxToSharedLock(flockFile *os.File) (err error) {
	err = unix.Flock(int(flockFile.Fd()), unix.LOCK_SH)
	if err != nil {
		failsafeLoggerErrorf("failed to relax timing data lock - %s", err.Error())
	} else {
		failsafeLoggerTracef("relaxToSharedLock: RELAX TO SHARED\n")
	}
	return
}

// unlockFileLock will release the synchronization lock around a file. Generally the manager should keep the
// lock in shared mode however.
func unlockFileLock(flockFile *os.File) (err error) {
	lockMode := unix.LOCK_UN

	err = unix.Flock(int(flockFile.Fd()), lockMode)
	if err != nil {
		failsafeLoggerErrorf("failed to release timing data lock - %s", err.Error())
	} else {
		failsafeLoggerTracef("unlockFileLock: RELEASE")
	}
	return
}

// ensureExclusiveFileLock grabs an exclusive lock on a file descriptor
func ensureExclusiveFileLockOnFile(fd *os.File) (err error) {
	err = waitOnFileLock(fd, blockTimeMilliseconds, true)
	if err != nil {
		err = fmt.Errorf("can't lock timestamp file: %w", err)
		failsafeLoggerWarnf(err.Error())
	}
	return
}
