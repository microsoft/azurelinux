# Warning :warning: 
- If upgrading from versions 1.5.x to 1.7.x of pod-identity, please carefully review this [doc](README.md#v160-breaking-change) before upgrade.
- Pod Identity is disabled by default for Clusters with Kubenet. Please review this [doc](https://azure.github.io/aad-pod-identity/docs/configure/aad_pod_identity_on_kubenet/) before upgrade.


# v1.7.0

### Features
- support JSON logging format ([#839](https://github.com/Azure/aad-pod-identity/pull/839))
- disable aad-pod-identity by default for kubenet ([#842](https://github.com/Azure/aad-pod-identity/pull/842))
- add auxiliary tenant ids for service principal ([#843](https://github.com/Azure/aad-pod-identity/pull/843))

### Bug Fixes
- account for 150+ identity assignment and unassignment ([#847](https://github.com/Azure/aad-pod-identity/pull/847))

### Other Improvements
-  include image scanning as part of CI & set non-root user in Dockerfile ([#803](https://github.com/Azure/aad-pod-identity/pull/803))

### Documentation
- initial layout for static site ([#801](https://github.com/Azure/aad-pod-identity/pull/801))
- update website theme to docsy ([#828](https://github.com/Azure/aad-pod-identity/pull/828))
- update invalid URLs in website ([#832](https://github.com/Azure/aad-pod-identity/pull/832))
- fix casing of "priorityClassName" parameters in README.md ([#856](https://github.com/Azure/aad-pod-identity/pull/856))
- add docs for various topics ([#858](https://github.com/Azure/aad-pod-identity/pull/858))
- s/cluster resource group/node resource group ([#862](https://github.com/Azure/aad-pod-identity/pull/862))
- add docs for configuring in custom cloud ([#863](https://github.com/Azure/aad-pod-identity/pull/863))
- fix broken links and typo ([#864](https://github.com/Azure/aad-pod-identity/pull/864))

### Helm
- remove extra indentation in crd.yaml ([#833](https://github.com/Azure/aad-pod-identity/pull/833))
- make runAsUser conditional for MIC in helm ([#844](https://github.com/Azure/aad-pod-identity/pull/844))

### Test Improvements
- remove aks cluster version in e2e ([#808](https://github.com/Azure/aad-pod-identity/pull/808))
- decrease length of RG name to allow cluster creation in eastus2euap ([#810](https://github.com/Azure/aad-pod-identity/pull/810))
- health check with podIP from the busybox container ([#840](https://github.com/Azure/aad-pod-identity/pull/840))
- add gosec as part of linting ([#850](https://github.com/Azure/aad-pod-identity/pull/850))
- remove --ignore-unfixed for trivy ([#854](https://github.com/Azure/aad-pod-identity/pull/854))
