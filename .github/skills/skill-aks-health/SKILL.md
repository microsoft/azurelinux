---
name: skill-aks-health
description: "[Skill] aks, aks health, cluster health, node pool, activity logs - Inspect Koji AKS cluster health, node pool status, autoscaling, activity logs, deployment failures, and Azure control-plane operations."
user-invocable: false
disable-model-invocation: false
---

# Koji AKS Cluster Health

## Tools

| Tool | Purpose |
|------|---------|
| `aks_cluster_get` | List/get AKS cluster details and provisioning state |
| `aks_nodepool_get` | List/get node pool status, VM size, scaling config |
| `monitor_activitylog_list` | Azure control-plane operations and failures |

## AKS node pools

The Koji AKS cluster has four node pool types:

| Pool | Purpose |
|------|----------|
| System | Core K8s services (coredns, metrics-server) |
| Infra | Koji hub, web, kojira, jobs |
| Builder (x86_64) | x86_64 build workers |
| Builder (arm64) | ARM64 build workers |

Use `aks_nodepool_get` to discover current VM sizes and scaling configuration. Builder pools use **autoscaling** with a configurable maximum node count (check your AKS deployment or IaC configuration for the exact value and defaults).

## Activity logs

Use `monitor_activitylog_list` to check for:
- Failed deployments or provisioning errors
- Scale-up/scale-down events on node pools
- Resource modification operations
- RBAC or permission-related failures

Set `hours` to scope the time window (e.g., 12 or 24).
