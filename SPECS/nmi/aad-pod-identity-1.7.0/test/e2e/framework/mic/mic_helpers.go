// +build e2e

package mic

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/Azure/aad-pod-identity/test/e2e/framework"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	corev1 "k8s.io/api/core/v1"
	rl "k8s.io/client-go/tools/leaderelection/resourcelock"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// GetLeaderInput is the input for GetLeader.
type GetLeaderInput struct {
	Getter framework.Getter
}

// GetLeader returns the MIC pod which won the leader election.
func GetLeader(input GetLeaderInput) *corev1.Pod {
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for MIC.GetLeader")

	By("Getting MIC Leader")

	leaderPod := &corev1.Pod{}
	endpoints := &corev1.Endpoints{}
	Expect(input.Getter.Get(context.TODO(), client.ObjectKey{Name: "aad-pod-identity-mic", Namespace: corev1.NamespaceDefault}, endpoints)).Should(Succeed())

	leRecord := &rl.LeaderElectionRecord{}
	Expect(json.Unmarshal([]byte(endpoints.ObjectMeta.Annotations["control-plane.alpha.kubernetes.io/leader"]), leRecord)).Should(Succeed())

	leaderName := leRecord.HolderIdentity
	Expect(input.Getter.Get(context.TODO(), client.ObjectKey{Name: leaderName, Namespace: framework.NamespaceKubeSystem}, leaderPod)).Should(Succeed())

	return leaderPod
}

// DeleteLeaderInput is the input for DeleteLeader.
type DeleteLeaderInput struct {
	Getter  framework.Getter
	Deleter framework.Deleter
}

// DeleteLeader deletes the MIC pod which won the leader election.
func DeleteLeader(input DeleteLeaderInput) {
	Expect(input.Getter).NotTo(BeNil(), "input.Getter is required for MIC.DeleteLeader")
	Expect(input.Deleter).NotTo(BeNil(), "input.Deleter is required for MIC.DeleteLeader")

	leader := GetLeader(GetLeaderInput{
		Getter: input.Getter,
	})

	By(fmt.Sprintf("Deleting MIC Leader \"%s\"", leader.Name))
	Expect(input.Deleter.Delete(context.TODO(), leader)).Should(Succeed())
}
