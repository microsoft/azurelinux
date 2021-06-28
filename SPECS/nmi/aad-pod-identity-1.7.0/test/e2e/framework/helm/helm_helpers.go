// +build e2e

package helm

import (
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

const (
	chartName = "aad-pod-identity"
)

// InstallInput is the input for Install.
type InstallInput struct {
	Config         *framework.Config
	NamespacedMode bool
}

// Install installs aad-pod-identity via Helm 3.
func Install(input InstallInput) {
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for Helm.Install")

	cwd, err := os.Getwd()
	Expect(err).To(BeNil())

	// Change current working directory to repo root
	// Before installing aad-pod identity through Helm
	os.Chdir("../..")
	defer os.Chdir(cwd)

	args := append([]string{
		"install",
		chartName,
		"manifest_staging/charts/aad-pod-identity",
		"--wait",
		fmt.Sprintf("--namespace=%s", framework.NamespaceKubeSystem),
		"--debug",
	})
	args = append(args, generateValueArgs(input.Config)...)

	err = helm(args)
	Expect(err).To(BeNil())
}

// Uninstall uninstalls aad-pod-identity via Helm 3.
func Uninstall() {
	args := []string{
		"uninstall",
		chartName,
		fmt.Sprintf("--namespace=%s", framework.NamespaceKubeSystem),
		"--debug",
	}

	// ignore error to allow cleanup completion
	_ = helm(args)
}

// UpgradeInput is the input for Upgrade.
type UpgradeInput struct {
	Config *framework.Config
}

// Upgrade upgrades aad-pod-identity via Helm 3.
func Upgrade(input UpgradeInput) {
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for Helm.Upgrade")

	cwd, err := os.Getwd()
	Expect(err).To(BeNil())

	// Change current working directory to repo root
	// Before installing aad-pod identity through Helm
	os.Chdir("../..")
	defer os.Chdir(cwd)

	args := append([]string{
		"upgrade",
		chartName,
		"manifest_staging/charts/aad-pod-identity",
		"--wait",
		fmt.Sprintf("--namespace=%s", framework.NamespaceKubeSystem),
		"--debug",
	})
	args = append(args, generateValueArgs(input.Config)...)

	err = helm(args)
	Expect(err).To(BeNil())
}

func generateValueArgs(config *framework.Config) []string {
	args := []string{
		fmt.Sprintf("--set=image.repository=%s", config.Registry),
		fmt.Sprintf("--set=mic.tag=%s", config.MICVersion),
		fmt.Sprintf("--set=nmi.tag=%s", config.NMIVersion),
	}

	if config.ImmutableUserMSIs != "" {
		args = append(args, fmt.Sprintf("--set=mic.immutableUserMSIs=%s", config.ImmutableUserMSIs))
	}

	if config.NMIMode == "managed" {
		args = append(args, fmt.Sprintf("--set=operationMode=%s", "managed"))
	}

	if config.BlockInstanceMetadata {
		args = append(args, fmt.Sprintf("--set=nmi.blockInstanceMetadata=%t", config.BlockInstanceMetadata))
	}

	if config.IdentityReconcileInterval != 0 {
		args = append(args, fmt.Sprintf("--set=mic.identityAssignmentReconcileInterval=%s", config.IdentityReconcileInterval))
	}

	return args
}

func helm(args []string) error {
	By(fmt.Sprintf("helm %s", strings.Join(args, " ")))

	cmd := exec.Command("helm", args...)
	stdoutStderr, err := cmd.CombinedOutput()
	fmt.Printf("%s", stdoutStderr)

	return err
}
