---
title: "Block Diagram and Design"
linkTitle: "Block Diagram and Design"
weight: 7
date: 2020-11-03
description: >
  An overview of all the Kubernetes components and their relationship.
---

![Block Diagram](../block-diagram.png)

## AAD and Kubernetes

The relationship between kubernetes and AAD is covered in three main areas:

1. **Cluster Identity**: The identity used by the cloud provider running in various kubernetes components to perform operations against Azure, typically against Azure's resource group where the cluster lives. This identity is set during the cluster bring up process. This is not included in the scope of this proposal.

2. **User Identity**: What enables user/operator to authenticate against AAD using AAD before using `kubectl` commands. This is not included in the scope of this proposal.

3. **Application Identities**: Identities that are used by applications running on kubernetes to access any resources that uses AAD as identity provider. These resources can be ARM, Applications running on the same cluster, on azure, or anywhere else. Managing, assigning these identities is the scope of this document.

> This proposal does not cover how application can be configured to use AAD as identity/authentication provider.

## Use cases

1. Kubernetes applications depending on other applications that use AAD as an identity provider. These applications include Azure first party services such as ARM, Azure SQL, and Azure KeyVault.

> Azure 1st party services are all moving to use AAD as the primary identity provider.

2. Delegating authorization to tools such as AAD group memberships.

3. Enable identity rotation without application interruption.

> Example: rotating a service principal password/cert without having to edit secrets assigned directly to applications.

4. Provide a framework to enable time-boxed identity assignment. Manually triggered or automated. The same framework can be used for (jit sudo style access with automation tools).

> Example: a front end application can have access to centralized data store between midnight and 1 AM during business days only.

## Guiding Principles

1. Favor little to no change to how users currently write applications against various editions of [ADAL](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-authentication-libraries). Favor committing changes to SDKs and don't ask users to change applications that are written for Kubernetes.

2. Favor little to no change in the way users create kubernetes application specs (favor declarative approach). This enables users to focus their development and debugging experience in code they wrote, not code imposed on them.

> Example: favor annotation and labels over side-cars (even dynamically injected).

3. Separate identities from `identity assignment` applications enables users to swap identities used by the applications.

## Processes

### AAD Identity Management and Assignment (within cluster)

- Cluster operators create instances of `crd:azureIdentity`. Each instance is a kubernetes object representing Azure AAD identity that can be EMSI or service principal (with password).

- Cluster operators create instances of `crd:azureIdentityBinding`. Each instance represents binding between `pod` and `crd:azureIdentity`.

- A Controller will run to create `crd:azureAssignedIdentity` based on `crd:azureIdentityBinding` linking `pod` with `crd:azureIdentity`.

### Acquiring Tokens

> for reference please read [Azure VM Managed Service Identity (MSI)](https://docs.microsoft.com/en-us/azure/active-directory/managed-service-identity/how-to-use-vm-token) and [Assign a Managed Service Identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/howto-assign-access-portal)

1. Kubernetes applications (pods) will default to use MSI endpoint.

2. All traffic to MSI endpoint is routed via `iptables` to a daemon-set that will use `sourceIp` to identify pod, then find an appropriate `crd:azureIdentityBinding`. The daemon-set mimics all the REST API offered by MSI endpoint. All tokens are presented to pods on MSI endpoint irrespective of the identity used to back this request (EMSI or service principal).

3. All token issuance will be logged as events attached to `crd:azureIdentityBinding` for audit purposes.
