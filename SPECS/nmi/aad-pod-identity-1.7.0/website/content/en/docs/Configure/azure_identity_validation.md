---
title: "Azure Identity Validation using Gatekeeper"
linkTitle: "Azure Identity Validation using Gatekeeper"
weight: 4
description: >
  This will help validate various CRDs and the azure resources used in aad-pod-identity. Currently validation of User assigned MSI format in Azure Identity is supported.
---

## Introduction

This will help validate various CRDs and the azure resources used in aad-pod-identity.
Currently validation of User assigned MSI format in Azure Identity is supported.

[Gatekeeper](https://github.com/open-policy-agent/gatekeeper) - Policy Controller for Kubernetes, is used to validate the resources.
  * It is a validating webhook that enforces CRD based policies
  * Provides admission system which allows to configure policy and rule as constraint

#### Prerequisite Gatekeeper Installation

Run the following to deploy a release version of Gatekeeper in your cluster or refer to [Gatekeeper Installation](https://github.com/open-policy-agent/gatekeeper#installation-instructions) for detailed instructions.

```sh
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
```

## Azure Identity Format Validation

Policy can be configured as Gatekeeper constraint to ensure the validity of the Resource ID format in the given identity.Request will be rejected by admission controller in case of any violation of the configured constraint.

Following are the two major resources to enable this check.

   * Constraint Template
   * Constraint

### Constraint Template

`ConstraintTemplate` describes both the [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) that enforces the constraint and the schema of the constraint.

   * User assigned MSI is expected to have Resource ID in the given format.

   ```
   /subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>
   ```

   The same can be validate using the following regex pattern. Resource ID that does not match this pattern is considered invalid.

   ```
   (?i)/subscriptions/(.+?)/resourcegroups/(.+?)/providers/Microsoft.ManagedIdentity/(.+?)/(.+)
   ```

   * Policy to ensure Resource ID is following expected pattern can be described via following Constraint template

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: azureidentityformat
spec:
  crd:
    spec:
      names:
        kind: azureidentityformat
        listKind: azureidentityformatList
        plural: azureidentityformat
        singular: azureidentityformat
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package azureidentityformat
        violation[{"msg": msg}] {
         input.review.kind.kind == "AzureIdentity"
         # format of resourceId is checked only for user-assigned MSI
         input.review.object.spec.type == 0
         resourceId := input.review.object.spec.resourceID
         result := re_match(`(?i)/subscriptions/(.+?)/resourcegroups/(.+?)/providers/Microsoft.ManagedIdentity/(.+?)/(.+)`,resourceId)
         result == false
         msg := sprintf(`The identity resourceId '%v' is invalid.It must be of the following format: '/subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>'`,[resourceId])
         }
```

You can install this ConstraintTemplate with the following command:

```sh
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/validation/gatekeeper/azureidentityformat_template.yaml
```

### Constraint

Constraint is used to inform Gatekeeper that the admin wants azureidentityformat ConstraintTemplate to be enforced.

If the constraint is violated by any request on Kind `AzureIdentity` in apiGroup `aadpodidentity.k8s.io`, request will be rejected via the admission controller.

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: azureidentityformat
metadata:
  name: azureidentityformatconstraint
spec:
  match:
    kinds:
      - apiGroups: ["aadpodidentity.k8s.io"]
        kinds: ["AzureIdentity"]
```

You can install this Constraint with the following command:

```sh
kubectl apply -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/validation/gatekeeper/azureidentityformat_constraint.yaml
```

### Examples

   * Following identity will pass the constraint and request will be accepted, as the resource ID is in the correct format.

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: testidentityvalid
spec:
  type: 0
  resourceID: /subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/testidentity
  clientID: 00000000-0000-0000-0000-000000000000
```

   * Following identity will violate the constraint and request will be rejected,  as resource ID is not of correct format (`resourcegroups/<resourcegroup>` is missing in resourceID).

```yaml
apiVersion: "aadpodidentity.k8s.io/v1"
kind: AzureIdentity
metadata:
  name: testidentityinvalid
spec:
  type: 0
  resourceID: /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myidentity
  clientID: 00000000-0000-0000-0000-000000000000
```

```sh
 kubectl apply -f aadpodidentity_test_invalid.yaml
Error from server ([denied by azureidentityformatconstraint] The identity resourceId '/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myidentity' is invalid.It must be of the following format: '/subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>'): error when creating "aadpodidentity_test_invalid.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [denied by azureidentityformatconstraint] The identity resourceId '/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myidentity' is invalid.It must be of the following format: '/subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>'
```


### Uninstallation

#### Uninstall Constraint Template & Constraint

   * Delete instances of the constraint resource
   * Delete the ConstraintTemplate` resource

Run the following to uninstall / disable validation.

```sh
kubectl delete -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/validation/gatekeeper/azureidentityformat_constraint.yaml

kubectl delete -f https://raw.githubusercontent.com/Azure/aad-pod-identity/master/validation/gatekeeper/azureidentityformat_template.yaml
```