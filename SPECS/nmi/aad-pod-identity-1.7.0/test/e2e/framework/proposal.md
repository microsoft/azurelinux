# AAD Pod Identity E2E Framework

## The Current State of E2E Tests

- It's flaky and it's hard to get a consistent test signal;

- It's hard to develop due to technical debt;

- Contributors are discouraged to write E2E tests for their pull requests due to the difficulty of understanding the test suite codebase, causing a decrease in test coverage.

## Goals

- Reduce test duration and technical debt by using various libraries instead of bash commands and Go-template-based deployments;

- Make the e2e test suite easier to develop and run by following a similar approach to how Kubernetes and Kubernetes-related projects write their e2e framework and test cases. This will encourage more developers to write e2e tests when they open PRs;

- Enhance log dump / collection so we can debug test failures easier.

## Framework Interface

The new test framework for AAD Pod Identity is inspired by [Cluster API's E2E test framework](https://github.com/kubernetes-sigs/cluster-api/tree/master/test/framework). Instead of using kubectl, the test suite communicates with the Kubernetes cluster via [`ClusterProxy`](./cluster_proxy.go), which uses the [client-go](https://github.com/kubernetes/client-go) library under the hood to create, delete, and modify Kubernetes resources, including CRDs like AzureIdentities, AzureIdentityBindings and AzureIdentityPodExceptions.

Helper functions of each resources are created under `./test/e2e/framework/<Resourcename>/<ResourceName>_helpers.go`, and each function takes an input struct to create or modify the resources. This is done so that we can avoid adding additional parameters in the function signature, instead, we can simply add new fields to the struct if we want to include additional parameters for the operation.

Below is an example Go file named `crd_helpers.go`, which includes a function that creates a `CRD` resource based on the input struct.

```go
package crd

type CreateInput struct {
	Creator      Creator
	Name         string
	Namespace    string
}

func Create(input CreateInput) *crdv1.CRD {
	Expect(input.Creator).NotTo(BeNil(), "input.Creator is required for CreateCRD")
	Expect(input.Name).NotTo(BeEmpty(), "input.Name is required for CreateCRD")
	Expect(input.Namespace).NotTo(BeEmpty(), "input.Namespace is required for CreateCRD")

	crd := &crdv1.CRD{
		ObjectMeta: metav1.ObjectMeta{
			Name:      input.Name,
			Namespace: input.Namespace,
		},
		Spec: crdv1.CRDSpec{
            ...
        },
	}
	Eventually(func() error {
		return input.Creator.Create(context.TODO(), crd)
	}, 10 * time.Second, 1 * time.Second).Should(Succeed())

	return crd
}
```

`Creator` in `CreateInput` is an interface that is responsible for sending a create request to the Kubernetes API server. There are also [interfaces](./interfaces.go) such as `Deleter`, `Listor`, and `Getter` available for developers to use. This is done so that we can limit the scope of actions in each helper function. Note that the controller-runtime client in `ClusterProxy` mentioned implements the `Creator`, `Deleter`, `Listor`, and `Getter` interfaces. So to invoke `crd.Create`:

```go

import "github.com/Azure/aad-pod-identity/test/e2e/framework/crd"

...
crd := crd.Create(crd.CreateInput{
    Creator: clusterProxy.GetClient(),
    Name: "my-crd",
    Namespace: "my-namespace",
})
...
```
