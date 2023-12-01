package marinertoolusers

import (
	"fmt"
	"io/fs"
	"os"
	"os/user"
	"path/filepath"
	"strconv"
	"syscall"
	"testing"
)

// Mariner builder user environment variable may be set or not, so we need to handle both cases
// in all tests. Assume the user is not set, and if it is, save the current value and restore it

var (
	oldEnvValue string
)

// Skips tests if we don't have two users we can test with (we generally will be running as sudo, so we should have
// 'root', 'nobody' and '$SUDO_USER' available)
func checkIfTestUsersAvailable(t *testing.T) {
	t.Helper()
	if os.Geteuid() != 0 {
		t.Fatal("Need a second user to transfer files, skipping since we aren't root and can't pretend to be other users")
	}
	sudoUser, err := getCurrentUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get current user: %v", err)
	}
	if sudoUser.Uid == "0" {
		t.Fatal("Need a second user to transfer files, skipping since we are ACTUALLY root instead of using sudo")
	}

	_, err = getNobodyUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get nobody user: %v", err)
	}
}

// Make sure that MARINER_BUILDER_USER is set to the current user (helps if running tests outside the makefile).
// Will restore the environment variable to its original value after the test
func prepEnv(t *testing.T, envName string) {
	t.Helper()
	t.Cleanup(func() {
		t.Log("Cleaning up environment variable")
		os.Setenv(envName, oldEnvValue)
	})
	oldEnvValue = os.Getenv(envName)
	currentUser, err := getCurrentUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get current user: %v", err)
	}
	currentEnvName := currentUser.Username
	os.Setenv(envName, currentEnvName)
}

func getCurrentUserHelper(t *testing.T) (currentUser *user.User, err error) {
	t.Helper()
	currentUser, err = user.Current()
	if err != nil {
		err = fmt.Errorf("unable to get current user:\n%w", err)
		return
	}
	if currentUser == nil {
		err = fmt.Errorf("unable to get current user")
		return
	}
	// Try to find a non-root user if we are root
	if currentUser.Uid == "0" {
		// Check if we can pull SUDO_USER
		sudoUser := os.Getenv("SUDO_USER")
		if sudoUser != "" {
			currentUser, err = user.Lookup(sudoUser)
			if err != nil {
				err = fmt.Errorf("unable to get current user:\n%w", err)
				return
			}
		} else {
			err = fmt.Errorf("unable to get current user")
			return
		}
	}
	return
}

func getNobodyUserHelper(t *testing.T) (nobodyUser *user.User, err error) {
	t.Helper()
	nobodyUser, err = user.Lookup("nobody")
	if err != nil {
		err = fmt.Errorf("unable to get nobody user:\n%w", err)
		return
	}
	if nobodyUser == nil {
		err = fmt.Errorf("unable to get nobody user")
		return
	}
	return
}

func getIDsHelper(t *testing.T, user *user.User) (uid int, gid int) {
	t.Helper()
	if user == nil {
		t.Fatalf("User is nil")
	}
	uid, err := strconv.Atoi(user.Uid)
	if err != nil {
		t.Fatalf("Failed to convert UID to int: %v", err)
	}
	gid, err = strconv.Atoi(user.Gid)
	if err != nil {
		t.Fatalf("Failed to convert GID to int: %v", err)
	}
	return
}

func getOwnerHelper(t *testing.T, file *os.File, info *fs.FileInfo) (uid int, gid int) {
	// Sanity check that we set the ownership correctly
	var err error
	if info == nil {
		if file == nil {
			t.Fatalf("Both file and info are nil")
		}
		name := file.Name()
		newInfo, err := os.Stat(name)
		if err != nil {
			t.Fatalf("Failed to stat file: %v", err)
		}
		info = &newInfo
	}
	stat, ok := (*info).Sys().(*syscall.Stat_t)
	if !ok {
		t.Fatalf("Failed to get syscall.Stat_t: %v", err)
	}
	uid = int(stat.Uid)
	gid = int(stat.Gid)
	return
}

func TestUnsetUser(t *testing.T) {
	prepEnv(t, userEnvName)

	// Override by unsetting the environment variable
	os.Unsetenv(userEnvName)

	user := GetMarinerBuildUser()
	if user != nil {
		t.Errorf("Expected nil user, but got %v", user)
	}
}

func TestGetMarinerBuildUser(t *testing.T) {
	prepEnv(t, userEnvName)

	currentUser, err := getCurrentUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get current user: %v", err)
	}

	user := GetMarinerBuildUser()
	if user == nil {
		t.Errorf("Expected non-nil user, but got nil")
	} else {
		if user.Username != currentUser.Username {
			t.Errorf("Expected username 'root', but got %s", user.Username)
		}
	}
}

func TestGiveSinglePathToUser(t *testing.T) {
	prepEnv(t, userEnvName)
	checkIfTestUsersAvailable(t)

	// Create a temporary file
	file, err := os.CreateTemp("", "testfile")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	nobody, err := getNobodyUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get nobody user: %v", err)
	}
	nobodyUid, nobodyGid := getIDsHelper(t, nobody)

	// Change ownership to nobody, we will change it back to the current user
	err = os.Chown(file.Name(), nobodyUid, nobodyGid)
	if err != nil {
		t.Fatalf("Failed to change ownership to root: %v", err)
	}

	// Sanity check that we set the ownership correctly
	actualUid, actualGid := getOwnerHelper(t, file, nil)
	if actualUid != nobodyUid || actualGid != nobodyGid {
		t.Fatalf("Expected ownership %s:%s, but got %d:%d", nobody.Uid, nobody.Gid, actualUid, actualGid)
	}

	// Change ownership to mariner builder user
	user := GetMarinerBuildUser()
	err = GiveSinglePathToUser(file.Name(), user)
	if err != nil {
		t.Fatalf("Failed to change ownership to mariner builder user: %v", err)
	}

	// Check ownership
	actualUid, actualGid = getOwnerHelper(t, file, nil)
	// User type uses strings for UID, GID
	userUid, userGid := getIDsHelper(t, user)

	if actualUid != userUid || actualGid != userGid {
		t.Errorf("Expected ownership %s:%s, but got %d:%d", user.Uid, user.Gid, actualUid, actualGid)
	}
}

func TestGiveDirToUserRecursive(t *testing.T) {
	prepEnv(t, userEnvName)
	checkIfTestUsersAvailable(t)

	// Create a temporary directory
	dir, err := os.MkdirTemp("", "testdir")
	if err != nil {
		t.Fatalf("Failed to create temporary directory: %v", err)
	}

	// Create a temporary file in the directory
	file1, err := os.CreateTemp(dir, "testfile1")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	// Create a temporary file in the directory
	file2, err := os.CreateTemp(dir, "testfile2")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	nobody, err := getNobodyUserHelper(t)
	if err != nil {
		t.Fatalf("Failed to get nobody user: %v", err)
	}
	nobodyUid, nobodyGid := getIDsHelper(t, nobody)

	// Change ownership to nobody, we will change it back to the current user
	err = os.Chown(dir, nobodyUid, nobodyGid)
	if err != nil {
		t.Fatalf("Failed to change ownership to nobody: %v", err)
	}
	err = os.Chown(file1.Name(), nobodyUid, nobodyGid)
	if err != nil {
		t.Fatalf("Failed to change ownership to nobody: %v", err)
	}
	err = os.Chown(file2.Name(), nobodyUid, nobodyGid)
	if err != nil {
		t.Fatalf("Failed to change ownership to nobody: %v", err)
	}

	// Sanity check that we set the ownership correctly
	actualUid, actualGid := getOwnerHelper(t, file1, nil)
	if actualUid != nobodyUid || actualGid != nobodyGid {
		t.Fatalf("Expected ownership %s:%s, but got %d:%d", nobody.Uid, nobody.Gid, actualUid, actualGid)
	}
	// Sanity check that we set the ownership correctly
	actualUid, actualGid = getOwnerHelper(t, file2, nil)
	if actualUid != nobodyUid || actualGid != nobodyGid {
		t.Fatalf("Expected ownership %s:%s, but got %d:%d", nobody.Uid, nobody.Gid, actualUid, actualGid)
	}

	// Change ownership to mariner builder user
	user := GetMarinerBuildUser()
	err = GiveDirToUserRecursive(dir, user)
	if err != nil {
		t.Fatalf("Failed to change ownership to mariner builder user: %v", err)
	}

	// User type uses strings for UID, GID
	userUid, err := strconv.Atoi(user.Uid)
	if err != nil {
		t.Fatalf("Failed to convert UID to int: %v", err)
	}
	userGid, err := strconv.Atoi(user.Gid)
	if err != nil {
		t.Fatalf("Failed to convert GID to int: %v", err)
	}

	// Check ownership
	err = filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		actualUid, actualGid := getOwnerHelper(t, nil, &info)

		if actualUid != userUid || actualGid != userGid {
			t.Errorf("Expected ownership %s:%s, but got %d:%d", user.Uid, user.Gid, actualUid, actualGid)
		}
		return nil
	})
	if err != nil {
		t.Fatalf("Failed to walk directory: %v", err)
	}
}

func TestInvalidUserSingle(t *testing.T) {
	prepEnv(t, userEnvName)

	// Create a temporary file
	file, err := os.CreateTemp("", "testfile")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	// Change ownership to mariner builder user
	user := &user.User{
		Uid: "invalid",
		Gid: "invalid",
	}
	err = GiveSinglePathToUser(file.Name(), user)
	if err == nil {
		t.Fatalf("Expected error, but got nil")
	}
}

func TestInvalidUserDir(t *testing.T) {
	prepEnv(t, userEnvName)

	// Create a temporary directory
	dir, err := os.MkdirTemp("", "testdir")
	if err != nil {
		t.Fatalf("Failed to create temporary directory: %v", err)
	}

	// Create a temporary file in the directory
	_, err = os.CreateTemp(dir, "testfile1")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	// Create a temporary file in the directory
	_, err = os.CreateTemp(dir, "testfile2")
	if err != nil {
		t.Fatalf("Failed to create temporary file: %v", err)
	}

	// Change ownership to mariner builder user
	user := &user.User{
		Uid: "invalid",
		Gid: "invalid",
	}
	err = GiveDirToUserRecursive(dir, user)
	if err == nil {
		t.Fatalf("Expected error, but got nil")
	}
}
