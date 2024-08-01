// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
)

const (
	sampleGrubCfg20Path     = "bootcfgtests/2.0-grub.cfg"
	sampleDefaultGrub20Path = "bootcfgtests/2.0-default-grub"

	sampleGrubCfg30Path     = "bootcfgtests/3.0-grub.cfg"
	sampleDefaultGrub30Path = "bootcfgtests/3.0-default-grub"
)

func TestBootCustomizerAddKernelCommandLine20(t *testing.T) {
	b := createBootCustomizerFor20(t)
	err := b.AddKernelCommandLine("console=tty0 console=ttyS0")
	assert.NoError(t, err)

	expectedGrubCfdDiff := `22c22
< 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline   $kernelopts
---
> 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline   console=tty0 console=ttyS0 $kernelopts
`
	checkDiffs20(t, b, expectedGrubCfdDiff, "")
}

func TestBootCustomizerAddKernelCommandLine30(t *testing.T) {
	b := createBootCustomizerFor30(t)
	err := b.AddKernelCommandLine("console=tty0 console=ttyS0")
	assert.NoError(t, err)

	expectedDefaultGrubFileDiff := `6c6
< GRUB_CMDLINE_LINUX_DEFAULT=" $kernelopts"
---
> GRUB_CMDLINE_LINUX_DEFAULT="  console=tty0 console=ttyS0 \$kernelopts"
`
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)
}

func TestBootCustomizerSELinuxMode20(t *testing.T) {
	b := createBootCustomizerFor20(t)
	selinuxMode, err := b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDisabled, selinuxMode)

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModePermissive)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDefault, selinuxMode)

	expectedGrubCfgDiff := `22c22
< 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline   $kernelopts
---
> 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline    security=selinux selinux=1 $kernelopts
`
	checkDiffs20(t, b, expectedGrubCfgDiff, "")

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModeForceEnforcing)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeForceEnforcing, selinuxMode)

	expectedGrubCfgDiff = `22c22
< 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline   $kernelopts
---
> 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline     security=selinux selinux=1 enforcing=1 $kernelopts
`
	checkDiffs20(t, b, expectedGrubCfgDiff, "")

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModeDisabled)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDisabled, selinuxMode)

	expectedGrubCfgDiff = `22c22
< 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline   $kernelopts
---
> 	linux $bootprefix/$mariner_linux       rd.auto=1 root=$rootdevice $mariner_cmdline lockdown=integrity sysctl.kernel.unprivileged_bpf_disabled=1 $systemd_cmdline        $kernelopts
`
	checkDiffs20(t, b, expectedGrubCfgDiff, "")
}

func TestBootCustomizerSELinuxMode30(t *testing.T) {
	b := createBootCustomizerFor30(t)
	selinuxMode, err := b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDisabled, selinuxMode)

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModePermissive)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDefault, selinuxMode)

	expectedDefaultGrubFileDiff := `5c5
< GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity "
---
> GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity  security=selinux selinux=1 "
`
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModeForceEnforcing)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeForceEnforcing, selinuxMode)

	expectedDefaultGrubFileDiff = `5c5
< GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity "
---
> GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity   security=selinux selinux=1 enforcing=1 "
`
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)

	err = b.UpdateSELinuxCommandLine(imagecustomizerapi.SELinuxModeDisabled)
	assert.NoError(t, err)

	selinuxMode, err = b.getSELinuxModeFromGrub()
	assert.NoError(t, err)
	assert.Equal(t, imagecustomizerapi.SELinuxModeDisabled, selinuxMode)

	expectedDefaultGrubFileDiff = `5c5
< GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity "
---
> GRUB_CMDLINE_LINUX="      rd.auto=1 net.ifnames=0 lockdown=integrity      "
`
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)
}

func TestBootCustomizerVerity20(t *testing.T) {
	b := createBootCustomizerFor20(t)

	err := b.PrepareForVerity()
	assert.NoError(t, err)

	checkDiffs20(t, b, "", "")
}

func TestBootCustomizerVerity30(t *testing.T) {
	b := createBootCustomizerFor30(t)

	err := b.PrepareForVerity()
	assert.NoError(t, err)

	expectedDefaultGrubFileDiff := `6a7,8
> GRUB_DISABLE_UUID="true"
> GRUB_DISABLE_RECOVERY="true"
`
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)

	// Do it again to make sure there aren't any changes.
	err = b.PrepareForVerity()
	assert.NoError(t, err)
	checkDiffs30(t, b, "", expectedDefaultGrubFileDiff)
}

func checkDiffs20(t *testing.T, b *BootCustomizer, expectedGrubCfgDiff string, expectedDefaultGrubFileDiff string) {
	checkDiffs(t, b, filepath.Join(testDir, sampleGrubCfg20Path), filepath.Join(testDir, sampleDefaultGrub20Path),
		expectedGrubCfgDiff, expectedDefaultGrubFileDiff)
}

func checkDiffs30(t *testing.T, b *BootCustomizer, expectedGrubCfgDiff string, expectedDefaultGrubFileDiff string) {
	checkDiffs(t, b, filepath.Join(testDir, sampleGrubCfg30Path), filepath.Join(testDir, sampleDefaultGrub30Path),
		expectedGrubCfgDiff, expectedDefaultGrubFileDiff)
}

func checkDiffs(t *testing.T, b *BootCustomizer, originalGrubCfgPath string, originalDefaultGrubFilePath string,
	expectedGrubCfgDiff string, expectedDefaultGrubFileDiff string,
) {
	grubCfgDiff := calcDiff(t, originalGrubCfgPath, b.grubCfgContent)
	defaultGrubFileDiff := calcDiff(t, originalDefaultGrubFilePath, b.DefaultGrubFileContent)

	assert.Equal(t, expectedGrubCfgDiff, grubCfgDiff, "diff of grub.cfg file")
	assert.Equal(t, expectedDefaultGrubFileDiff, defaultGrubFileDiff, "diff of /etc/default/grub file")
}

func calcDiff(t *testing.T, oldPath string, newContent string) string {
	diff, _, err := shell.ExecuteWithStdin(newContent, "diff", oldPath, "-")
	if err != nil {
		exitError, isExitError := err.(*exec.ExitError)
		if assert.True(t, isExitError) {
			assert.Equal(t, exitError.ExitCode(), 1)
		}
	}
	return diff
}

func createBootCustomizerFor20(t *testing.T) *BootCustomizer {
	return createBootCustomizer(t, filepath.Join(testDir, sampleGrubCfg20Path),
		filepath.Join(testDir, sampleDefaultGrub20Path), false)
}

func createBootCustomizerFor30(t *testing.T) *BootCustomizer {
	return createBootCustomizer(t, filepath.Join(testDir, sampleGrubCfg30Path),
		filepath.Join(testDir, sampleDefaultGrub30Path), true)
}

func createBootCustomizer(t *testing.T, sampleGrubCfgPath string, sampleDefaultGrubFilePath string, isGrubMkconfig bool,
) *BootCustomizer {
	sampleGrubCfgContent, err := os.ReadFile(sampleGrubCfgPath)
	assert.NoError(t, err, "failed to read sample grub.cfg file")

	sampleDefaultGrubFileContent, err := os.ReadFile(sampleDefaultGrubFilePath)
	assert.NoError(t, err, "failed to read sample /etc/default/grub file")

	b := &BootCustomizer{
		grubCfgContent:         string(sampleGrubCfgContent),
		DefaultGrubFileContent: string(sampleDefaultGrubFileContent),
		isGrubMkconfig:         isGrubMkconfig,
	}
	return b
}
