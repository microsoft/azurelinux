// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"strings"
	"path/filepath"
	"io/ioutil"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func enableVerityPartition(Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) error {
	var err error

	// Ensure the VerityPartition value is one of the supported types: 'root' or 'user'.
	if Verity.VerityTab != "root" && Verity.VerityTab != "user" {
		return fmt.Errorf("invalid VerityPartition: %s. It should be either 'root' or 'user'", Verity.VerityTab)
	}

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	err = buildDracutModule(systemdVerityDracutModule, imageChroot) 
	if err != nil {
		return err
	}

	// Update mariner config file with the new generated initramfs file.
	err = updateMarinerCfgWithInitramfs(imageChroot)
	if err != nil {
		return err
	}

	/*
	// Calculate the root hash using veritysetup
	rootHash, salt, err := calculateRootHash(Verity, imageChroot)
	if err != nil {
		return err
	}

	// Update grub.cfg with the new kernel command-line arguments.
	err = updateGrubConfigWithVerityArgs(rootHash, salt, Verity, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to update grub.cfg with verity arguments: %w", err)
	}
	*/

	return nil
}

func buildDracutModule(dracutModuleName string, imageChroot *safechroot.Chroot) error {
	var err error

	buildDracutModuleArgs := []string{
		// TODO: debug kernel version mismatch here.
		"dracut", "-f", "--kver", "5.15.131.1-2.cm2", "-a",
		//"dracut", "-f", "-a",
		// Placeholder for dracut module name.
		"",
	}

	buildDracutModuleArgs[len(buildDracutModuleArgs)-1] = dracutModuleName

	fmt.Println("Executing command:", "sudo", strings.Join(buildDracutModuleArgs, " "))
	err = imageChroot.Run(func() error {
		stdout, stderr, err := shell.Execute("pwd")
		fmt.Println("Stdout:", stdout)
		fmt.Println("Stderr:", stderr)

		stdout, stderr, err = shell.Execute("sudo", buildDracutModuleArgs...)
		fmt.Println("Stdout:", stdout)
		fmt.Println("Stderr:", stderr)
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to build dracut module - (%s):\n%w", dracutModuleName, err)
	}

	// Define the initramfs path
    initrdPath := "/boot/initramfs-5.15.131.1-2.cm2.img"

	// Arguments to run lsinitrd
    lsinitrdArgs := []string{"lsinitrd", initrdPath, " | grep dm_mod"}

    fmt.Println("Executing command:", "sudo", strings.Join(lsinitrdArgs, " "))

	// Run lsinitrd to verify the initramfs contents
    err = imageChroot.Run(func() error {
        stdout, stderr, err := shell.Execute("sudo", lsinitrdArgs...)
        fmt.Println("Stdout:", stdout)
        fmt.Println("Stderr:", stderr)
        if err != nil {
            return fmt.Errorf("failed to execute lsinitrd on the initramfs image - (%s):\n%w", initrdPath, err)
        }

		// Now let's check the systemd version
		systemdVersionCmd := []string{"systemctl", "--version"}
		systemdStdout, systemdStderr, systemdErr := shell.Execute("sudo", systemdVersionCmd...)
		fmt.Println("systemd Version Stdout:", systemdStdout)
		if systemdErr != nil {
			fmt.Println("systemd Version Stderr:", systemdStderr)
			return fmt.Errorf("failed to get systemd version - (%s):\n%w", systemdStderr, systemdErr)
		}

		/*
        // Check if dm_mod is included in the initramfs
        if !strings.Contains(stdout, "dm_mod") {
            return fmt.Errorf("dm_mod is not found in the initramfs image - (%s)", initrdPath)
        }
		*/

        return nil // No error occurred, and dm_mod is found
    })

    if err != nil {
        return fmt.Errorf("failed to verify dm_mod in initramfs - (%s):\n%w", initrdPath, err)
    }

	return nil
}

func updateMarinerCfgWithInitramfs(imageChroot *safechroot.Chroot) error {
	// Construct path for the initramfs file inside the chroot environment.
	initramfsPath := filepath.Join("boot", "initramfs-*")

	// Fetch the initramfs file name.
	var initramfsFiles []string
	err := imageChroot.Run(func() error {
		var innerErr error
		initramfsFiles, innerErr = filepath.Glob(initramfsPath)
		return innerErr
	})
	if err != nil {
		return fmt.Errorf("failed to list initramfs file: %w", err)
	}

	// Ensure an initramfs file is found.
	if len(initramfsFiles) != 1 {
		return fmt.Errorf("expected one initramfs file, but found %d", len(initramfsFiles))
	}

	newInitramfs := filepath.Base(initramfsFiles[0])

	// Construct path for mariner.cfg inside the chroot environment.
	cfgPath := filepath.Join("boot", "mariner.cfg")

	// Update mariner.cfg to reference the new initramfs.
	err = imageChroot.Run(func() error {
		input, innerErr := ioutil.ReadFile(cfgPath)
		if innerErr != nil {
			return fmt.Errorf("failed to read mariner.cfg: %w", innerErr)
		}

		lines := strings.Split(string(input), "\n")
		for i, line := range lines {
			if strings.HasPrefix(line, "mariner_initrd=") {
				lines[i] = "mariner_initrd=" + newInitramfs
			}
		}
		output := strings.Join(lines, "\n")
		return ioutil.WriteFile(cfgPath, []byte(output), 0644)
	})

	// Print the updated contents
	//command := fmt.Sprintf("%s %s", "cat", cfgPath)
	err = imageChroot.Run(func() error {
		stdout, stderr, err := shell.Execute("cat", cfgPath)
		fmt.Println("Stdout:", stdout)
		fmt.Println("Stderr:", stderr)
		return err
	})

	// Printing current directory.
	fmt.Println("Right after mariner.cfg update printing current working directory:")
	stdout, stderr, err := shell.Execute("pwd")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return fmt.Errorf("failed to execute pwd: %w", err)
	}

	return nil
}

func calculateRootHash(Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) (string, string, error) {
	var rootHash, salt string
	cmd := "veritysetup format /dev/loop19p3 /dev/loop19p6"

	// Printing current devices using lsblk
	fmt.Println("Printing current block devices using lsblk:")
	stdout, stderr, err := shell.Execute("lsblk")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to execute lsblk: %w", err)
	}

	// Printing current directory.
	fmt.Println("Printing current working directory:")
	stdout, stderr, err = shell.Execute("pwd")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to execute lsblk: %w", err)
	}

	fmt.Println("Executing command:", cmd)
	rootHashOutput, stderr, err := shell.Execute("sh", "-c", cmd)
	fmt.Println("Stdout:", rootHashOutput)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to calculate root hash: %w", err)
	}
	lines := strings.Split(rootHashOutput, "\n")
	for _, line := range lines {
		if strings.Contains(line, "Root hash:") {
			rootHash = strings.Fields(line)[2]
		}
		if strings.Contains(line, "Salt:") {
			salt = strings.Fields(line)[1]
		}
	}

	rootHash = strings.TrimSpace(rootHash)
	salt = strings.TrimSpace(salt)

	if rootHash == "" {
		return "", "", fmt.Errorf("failed to extract root hash from veritysetup output")
	}
	if salt == "" {
		return "", "", fmt.Errorf("failed to extract salt from veritysetup output")
	}

	return rootHash, salt, nil
}

func calculateExtraRootHash(Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot, salt string) (string, string, error) {
	var rootHash string
	cmdlineTemplate := "veritysetup format --salt=%s /dev/loop19p3 /dev/loop19p6"
	cmd := fmt.Sprintf(cmdlineTemplate, salt)

	// Printing current devices using lsblk
	fmt.Println("Printing current block devices using lsblk:")
	stdout, stderr, err := shell.Execute("lsblk")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to execute lsblk: %w", err)
	}

	// Printing current directory.
	fmt.Println("Printing current working directory:")
	stdout, stderr, err = shell.Execute("pwd")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to execute lsblk: %w", err)
	}

	fmt.Println("Executing command:", cmd)
	rootHashOutput, stderr, err := shell.Execute("sh", "-c", cmd)
	fmt.Println("Stdout:", rootHashOutput)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return "", "", fmt.Errorf("failed to calculate root hash: %w", err)
	}
	lines := strings.Split(rootHashOutput, "\n")
	for _, line := range lines {
		if strings.Contains(line, "Root hash:") {
			rootHash = strings.Fields(line)[2]
		}
		if strings.Contains(line, "Salt:") {
			salt = strings.Fields(line)[1]
		}
	}

	rootHash = strings.TrimSpace(rootHash)
	salt = strings.TrimSpace(salt)

	if rootHash == "" {
		return "", "", fmt.Errorf("failed to extract root hash from veritysetup output")
	}
	if salt == "" {
		return "", "", fmt.Errorf("failed to extract salt from veritysetup output")
	}

	return rootHash, salt, nil
}

func updateGrubConfigWithVerityArgs(rootHash string, salt string, Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) error {
	const grubCfgPath = "/boot/grub2/grub.cfg"
	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=panic-on-corruption,salt=%s"
	const rootDevicePattern = "set rootdevice=PARTUUID="
    const replacement = "set rootdevice=/dev/mapper/root"

	// Printing current directory.
	fmt.Println("At the beginning of grub.cfg update printing current working directory:")
	stdout, stderr, err := shell.Execute("pwd")
	fmt.Println("Stdout:", stdout)
	fmt.Println("Stderr:", stderr)
	if err != nil {
		return fmt.Errorf("failed to execute pwd: %w", err)
	}

	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, Verity.VerityDevice, Verity.HashDevice, salt)

	var updatedLines []string

	err = imageChroot.Run(func() error {
		lines, err := ioutil.ReadFile(grubCfgPath)
		if err != nil {
			return err
		}

		for _, line := range strings.Split(string(lines), "\n") {
			trimmedLine := strings.TrimSpace(line)
			if strings.HasPrefix(trimmedLine, "linux ") {
				line += " " + newArgs
			}
			/*
			if strings.HasPrefix(trimmedLine, rootDevicePattern) {
				line = replacement
			}
			*/
			updatedLines = append(updatedLines, line)
		}

		// Write the updated content back to grub.cfg
		err = ioutil.WriteFile(grubCfgPath, []byte(strings.Join(updatedLines, "\n")), 0644)
		if err != nil {
			return err
		}

		// Print the updated content of grub.cfg
		fmt.Println("Updated grub.cfg content:")
		fmt.Println(strings.Join(updatedLines, "\n"))

		return nil
	})

	if err != nil {
		return fmt.Errorf("failed to update grub.cfg: %w", err)
	}

	return nil
}
