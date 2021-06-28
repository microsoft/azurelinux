// +build e2e

package identityvalidator

import (
	"context"
	"fmt"
	"sync"

	aadpodv1 "github.com/Azure/aad-pod-identity/pkg/apis/aadpodidentity/v1"
	"github.com/Azure/aad-pod-identity/test/e2e/framework"
	"github.com/Azure/aad-pod-identity/test/e2e/framework/exec"

	"github.com/Azure/go-autorest/autorest/to"
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// CreateInput is the input for Create.
type CreateInput struct {
	Creator         framework.Creator
	Config          *framework.Config
	Namespace       string
	IdentityBinding string
	InitContainer   bool
	NodeName        string
	PodLabels       map[string]string
}

// Create creates an identity-validator pod.
func Create(input CreateInput) *corev1.Pod {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for IdentityValidator.Create")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for IdentityValidator.Create")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for IdentityValidator.Create")

	if input.IdentityBinding == "" {
		By("Creating an identity-validator pod with no label")
	} else {
		By(fmt.Sprintf("Creating an identity-validator pod with \"%s\" label", input.IdentityBinding))
	}

	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			GenerateName: "identity-validator-",
			Namespace:    input.Namespace,
			Labels: map[string]string{
				aadpodv1.CRDLabelKey: input.IdentityBinding,
			},
		},
		Spec: corev1.PodSpec{
			TerminationGracePeriodSeconds: to.Int64Ptr(int64(0)),
			Containers: []corev1.Container{
				{
					Name:            "identity-validator",
					Image:           fmt.Sprintf("%s/identityvalidator:%s", input.Config.Registry, input.Config.IdentityValidatorVersion),
					Command:         getIdentityValidatorCommand(input.Config),
					Args:            getIdentityValidatorArgs(input.Config),
					ImagePullPolicy: corev1.PullAlways,
					Env: []corev1.EnvVar{
						{
							Name: "E2E_TEST_POD_NAME",
							ValueFrom: &corev1.EnvVarSource{
								FieldRef: &corev1.ObjectFieldSelector{
									FieldPath: "metadata.name",
								},
							},
						},
						{
							Name: "E2E_TEST_POD_NAMESPACE",
							ValueFrom: &corev1.EnvVarSource{
								FieldRef: &corev1.ObjectFieldSelector{
									FieldPath: "metadata.namespace",
								},
							},
						},
						{
							Name: "E2E_TEST_POD_IP",
							ValueFrom: &corev1.EnvVarSource{
								FieldRef: &corev1.ObjectFieldSelector{
									FieldPath: "status.podIP",
								},
							},
						},
					},
				},
			},
		},
	}

	if input.InitContainer {
		pod.Spec.InitContainers = []corev1.Container{
			{
				Name:  "init-myservice",
				Image: "microsoft/azure-cli:latest",
				Command: []string{
					"sh",
					"-c",
					"az login --identity",
				},
			},
		}
	}

	if input.NodeName != "" {
		pod.Spec.NodeName = input.NodeName
	}

	if len(input.PodLabels) > 0 {
		for k, v := range input.PodLabels {
			pod.ObjectMeta.Labels[k] = v
		}
	}

	Expect(input.Creator.Create(context.TODO(), pod)).Should(Succeed())

	return pod
}

// CreateBatchInput is the input for CreateBatch.
type CreateBatchInput struct {
	Creator          framework.Creator
	Config           *framework.Config
	Namespace        string
	IdentityBindings []*aadpodv1.AzureIdentityBinding
}

// CreateBatch creates a batch of identity-validator in parallel.
func CreateBatch(input CreateBatchInput) []*corev1.Pod {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for IdentityValidator.CreateBatch")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for IdentityValidator.CreateBatch")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for IdentityValidator.CreateBatch")
	Expect(len(input.IdentityBindings) > 0).To(BeTrue(), "input.IdentityBindings must not be empty for IdentityValidator.CreateBatch")

	var wg sync.WaitGroup
	identityValidators := make([]*corev1.Pod, len(input.IdentityBindings))
	for i := 0; i < len(input.IdentityBindings); i++ {
		wg.Add(1)
		go func(i int) {
			identityValidators[i] = Create(CreateInput{
				Creator:         input.Creator,
				Config:          input.Config,
				Namespace:       input.Namespace,
				IdentityBinding: input.IdentityBindings[i].Spec.Selector,
			})
			wg.Done()
		}(i)
	}
	wg.Wait()

	return identityValidators
}

// UpdateInput is the input for Update.
type UpdatePodLabelInput struct {
	Getter          framework.Getter
	Updater         framework.Updater
	Namespace       string
	PodName         string
	UpdatedPodLabel string
}

// Update updates an identity-validator resource.
func UpdatePodLabel(input UpdatePodLabelInput) *corev1.Pod {
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for IdentityValidator.Update")
	Expect(input.Updater).NotTo(BeNil(), "input.Updater is required for IdentityValidator.Update")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for IdentityValidator.Update")
	Expect(input.PodName).NotTo(BeEmpty(), "input.PodName is required for IdentityValidator.Update")
	Expect(input.UpdatedPodLabel).NotTo(BeEmpty(), "input.UpdatedPodLabel is required for IdentityValidator.Update")

	identityValidator := &corev1.Pod{}
	Expect(input.Getter.Get(context.TODO(), client.ObjectKey{Name: input.PodName, Namespace: input.Namespace}, identityValidator)).Should(Succeed())

	By(fmt.Sprintf("Changing the pod label of %s from %s to %s", input.PodName, identityValidator.ObjectMeta.Labels[aadpodv1.CRDLabelKey], input.UpdatedPodLabel))
	identityValidator.ObjectMeta.Labels[aadpodv1.CRDLabelKey] = input.UpdatedPodLabel
	Expect(input.Updater.Update(context.TODO(), identityValidator)).Should(Succeed())

	return identityValidator
}

// DeleteInput is the input for Delete.
type DeleteInput struct {
	Deleter           framework.Deleter
	IdentityValidator *corev1.Pod
}

// Delete deletes an identity-validator pod.
func Delete(input DeleteInput) {
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for IdentityValidator.Delete")
	Expect(input.IdentityValidator).NotTo(BeNil(), "input.IdentityValidator is required for IdentityValidator.Delete")

	By(fmt.Sprintf("Deleting pod \"%s\"", input.IdentityValidator.Name))
	Expect(input.Deleter.Delete(context.TODO(), input.IdentityValidator)).Should(Succeed())
}

// ValidateInput is the input for Validate.
type ValidateInput struct {
	Getter             framework.Getter
	Config             *framework.Config
	KubeconfigPath     string
	PodName            string
	Namespace          string
	IdentityClientID   string
	IdentityResourceID string
	ExpectError        bool
	InitContainer      bool
}

// Validate performs validation against an identity-validator pod.
func Validate(input ValidateInput) {
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for IdentityValidator.Validate")
	Expect(input.Config).NotTo(BeNil(), "input.Config is required for IdentityValidator.Validate")
	Expect(input.KubeconfigPath).NotTo(BeEmpty(), "input.KubeconfigPath is required for IdentityValidator.Validate")
	Expect(input.PodName).NotTo(BeEmpty(), "input.PodName is required for IdentityValidator.Validate")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for IdentityValidator.Validate")
	Expect(input.IdentityClientID).NotTo(BeEmpty(), "input.IdentityClientID is required for IdentityValidator.Validate")

	By(fmt.Sprintf("Ensuring Pod \"%s\" is Running", input.PodName))
	Eventually(func() bool {
		pod := &corev1.Pod{}
		Expect(input.Getter.Get(context.TODO(), client.ObjectKey{Name: input.PodName, Namespace: input.Namespace}, pod)).Should(Succeed())

		if pod.Status.Phase == corev1.PodRunning {
			if input.InitContainer {
				By("Ensuring the exit code of init container is 0")
				Expect(len(pod.Status.InitContainerStatuses) > 0).To(BeTrue())
				Expect(pod.Status.InitContainerStatuses[0].State.Terminated.ExitCode == 0).To(BeTrue())
				Expect(pod.Status.InitContainerStatuses[0].State.Terminated.Reason == "Completed").To(BeTrue())
			}
			return true
		}
		return false
	}, framework.Timeout, framework.Polling).Should(BeTrue())

	args := []string{
		"identityvalidator",
		"--subscription-id",
		input.Config.SubscriptionID,
		"--resource-group",
		input.Config.IdentityResourceGroup,
		"--identity-client-id",
		input.IdentityClientID,
		"--keyvault-name",
		input.Config.KeyvaultName,
		"--keyvault-secret-name",
		input.Config.KeyvaultSecretName,
		"--keyvault-secret-version",
		input.Config.KeyvaultSecretVersion,
	}

	if input.IdentityResourceID != "" {
		args = append(args, "--identity-resource-id", input.IdentityResourceID)
	}

	_, err := exec.KubectlExec(input.KubeconfigPath, input.PodName, input.Namespace, args)
	if input.ExpectError {
		By(fmt.Sprintf("Ensuring an error has occurred in %s", input.PodName))
		Expect(err).NotTo(BeNil())
	} else {
		By(fmt.Sprintf("Ensuring an error has not occurred in %s", input.PodName))
		Expect(err).To(BeNil())
	}
}

// getIdentityValidatorCommand returns the command used for identityvalidator pod.
// TODO: remove this when releasing v1.6.4
func getIdentityValidatorCommand(config *framework.Config) []string {
	command := []string{}
	if config.IsSoakTest {
		// Soak test is still using non-distroless identityvalidator image
		// which allows us to run the 'sleep' command
		command = append(command, "sleep", "3600")
	}
	return command
}

// getIdentityValidatorCommand returns the args used for identityvalidator pod.
// TODO: remove this when releasing v1.6.4
func getIdentityValidatorArgs(config *framework.Config) []string {
	args := []string{}
	if !config.IsSoakTest {
		// Non-soak test is using a distroless identityvalidator image
		// which does not allow us to run the 'sleep' command.
		// enable the sleep flag to allow identityvalidator to sleep forever.
		args = append(args, "--sleep")
	}
	return args
}
