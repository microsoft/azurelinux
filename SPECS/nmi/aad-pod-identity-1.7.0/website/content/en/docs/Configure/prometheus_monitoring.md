---
title: "Monitoring Pod Identity with Prometheus"
linkTitle: "Monitoring Pod Identity with Prometheus"
weight: 7
description: >
  Prometheus is a systems and service monitoring system. It collects metrics from configured targets at given intervals, evaluates rule expressions,displays the results, and can trigger alerts if some condition is observed to be true.
---

## Introduction  

AAD pod identity is a foundational service that other applications depend upon, it is recommended to monitor the same.

Liveliness probe and Prometheus metrics are available in both Managed Identity Controller (MIC) and the Node Managed Identity (NMI) components.
  
## Liveliness Probe

MIC and NMI exposes /healthz endpoint with content of "Active/Not Active" state.
State "Active" is being returned if the component has started successfully and "Not Active" otherwise.  

## Prometheus Metrics 

[Prometheus](https://github.com/prometheus/prometheus) is a systems and service monitoring system. It collects metrics from configured targets at given intervals, evaluates rule expressions,displays the results, and can trigger alerts if some condition is observed to be true.

The following [OpenCensus](https://opencensus.io/) metrics are exposed in AAD pod identity system via prometheus exporter.  

**1. aadpodidentity_assigned_identity_addition_duration_seconds**

Histogram that tracks the duration (in seconds) it takes for Assigned identity addition operations.

**2. aadpodidentity_assigned_identity_addition_count**

Counter that tracks the cumulative number of assigned identity addition operations.

**3. aadpodidentity_assigned_identity_deletion_duration_seconds**

Histogram that tracks the duration (in seconds) it takes for Assigned identity deletion operations.

**4. aadpodidentity_assigned_identity_deletion_count**

Counter that tracks the cumulative number of assigned identity deletion operations.

**5. aadpodidentity_nmi_operations_duration_seconds**

Histogram that tracks the latency (in seconds) of NMI operations to complete. Broken down by operation type, status code.

**6. aadpodidentity_mic_cycle_duration_seconds**

Histogram that tracks the duration (in seconds) it takes for a single cycle in MIC.

**7. aadpodidentity_mic_cycle_count**

Counter that tracks the number of cycles executed in MIC.

**8. aadpodidentity_mic_new_leader_election_count**

Counter that tracks the cumulative number of new leader election in MIC.

**9. aadpodidentity_cloud_provider_operations_errors_count**

Counter that tracks the cumulative number of cloud provider operations errors. Broken down by operation type.

**10. aadpodidentity_cloud_provider_operations_duration_seconds**

Histogram that tracks the duration (in seconds) it takes for cloud provider operations. Broken down by operation type.

**11. aadpodidentity_kubernetes_api_operations_errors_count**

Counter that tracks the cumulative number of kubernetes api operations errors. Broken down by operation type.

**12. aadpodidentity_imds_operations_errors_count**

Counter that tracks the cumulative number of imds token operation errors. Broken down by operation type.

**13. aadpodidentity_imds_operations_duration_seconds**

Histogram that tracks the duration (in seconds) it takes for IMDS token operations. Broken down by operation type.

### Prometheus Metrics Endpoints

| Component | Default Metric Port | Metric Path |
|:---------:|---------------------|-------------|
| `NMI`     | `9090`              | `/metrics`   |
| `MIC`     | `8888`              | `/metrics`   |