---
title: Mariner's Container Host 2.0
type: post
classes: wide
published: false
status: draft
categories:
- Microsoft
- Linux
tags:
- Microsoft
- Azure
- Linux
author: henry_beberman
comments: false
---

Last fall we released Mariner on Azure Kubernetes Service (AKS) as a container host for internal Microsoft services. Since then, we have been hard at work on Mariner 2.0 and improving the next generation of our container host.

The biggest new feature we are looking forward to bringing into AKS with Mariner 2.0 is A/B updates with an immutable host OS. Today we are delivering similar technologies on the edge with EFLOW (Edge for Linux on Windows) and AKS-HCI. While the concept of A/B updates isn't new, and certainly exists in other distributions, we're working to establish a consistent implementation in Mariner powered products in Azure and at the edge.

This approach has several advantages for our internal customer’s utilization of their cluster. By performing most of the update while the node is still running, we will be able to minimize the time a node is unavailable to customer containers, maximizing the work a customer gets out of their cluster. Additionally, the customer's container images are preserved on disk across an OS update, eliminating the need to redownload them before work resumes.

Applying the updates to the inactive partition while the node is still running allows us to comprehend and control the update natively in Kubernetes using Custom Resource Definitions, Operators, and DaemonSets. This opens a huge design space for managing updates and exposes them through mechanisms that are already familiar to Kubernetes cluster owners.

For example, an operator could implement safe deployment practices by specifying a set of health checks for a host OS update rollout. The update operator would ensure that their service passes these health checks on the new host version before committing to the change and gradually rolling it out to more nodes in their cluster. However, if these health checks detected an issue, the update operator could simply reboot the failed node, which would roll it back to the previous partition placing it back into a known working configuration.


