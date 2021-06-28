// +build e2e

package exec

import (
	"fmt"
	"os/exec"
	"strings"

	. "github.com/onsi/ginkgo"
)

// KubectlApply executes "kubectl apply" given a list of arguments.
func KubectlApply(kubeconfigPath, namespace string, args []string) error {
	args = append([]string{
		"apply",
		fmt.Sprintf("--kubeconfig=%s", kubeconfigPath),
		fmt.Sprintf("--namespace=%s", namespace),
	}, args...)

	_, err := kubectl(args)
	return err
}

// KubectlDelete executes "kubectl delete" given a list of arguments.
func KubectlDelete(kubeconfigPath, namespace string, args []string) error {
	args = append([]string{
		"delete",
		fmt.Sprintf("--kubeconfig=%s", kubeconfigPath),
		fmt.Sprintf("--namespace=%s", namespace),
	}, args...)

	_, err := kubectl(args)
	return err
}

// KubectlExec executes "kubectl exec" given a list of arguments.
func KubectlExec(kubeconfigPath, podName, namespace string, args []string) (string, error) {
	args = append([]string{
		"exec",
		fmt.Sprintf("--kubeconfig=%s", kubeconfigPath),
		fmt.Sprintf("--namespace=%s", namespace),
		podName,
		"--",
	}, args...)

	return kubectl(args)
}

func KubectlLogs(kubeconfigPath, podName, namespace string) (string, error) {
	args := []string{
		"logs",
		fmt.Sprintf("--kubeconfig=%s", kubeconfigPath),
		fmt.Sprintf("--namespace=%s", namespace),
		podName,
	}

	return kubectl(args)
}

func kubectl(args []string) (string, error) {
	By(fmt.Sprintf("kubectl %s", strings.Join(args, " ")))

	cmd := exec.Command("kubectl", args...)
	stdoutStderr, err := cmd.CombinedOutput()
	fmt.Printf("%s", stdoutStderr)

	return string(stdoutStderr), err
}
