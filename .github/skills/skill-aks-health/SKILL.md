---
name: aks-health
description: "Inspect Koji AKS cluster health, node pool status, autoscaling, VM sizes, activity logs, deployment failures, and Azure control-plane operations."
---

# Koji AKS Cluster Health

## Tools

| Tool | Purpose |
|------|---------|
| `aks_cluster_get` | List/get AKS cluster details and provisioning state |
| `aks_nodepool_get` | List/get node pool status, VM size, scaling config |
| `monitor_activitylog_list` | Azure control-plane operations and failures |

## AKS node pools

The Koji AKS cluster has three node pool types:

| Pool | Purpose | Typical VM size |
|------|---------|-----------------|
| System | Core K8s services (coredns, metrics-server) | `Standard_D4s_v6` |
| Infra | Koji hub, web, kojira, jobs | Shared with system or dedicated |
| Builder (x86_64) | x86_64 build workers | `Standard_D4s_v5` |
| Builder (arm64) | ARM64 build workers | `Standard_D4ps_v5` |

Builder pools use **autoscaling** (max count configurable via `AKS_BUILDER_NODE_MAX_COUNT`, default 25).

## Activity logs

Use `monitor_activitylog_list` to check for:
- Failed deployments or provisioning errors
- Scale-up/scale-down events on node pools
- Resource modification operations
- RBAC or permission-related failures

Set `hours` to scope the time window (e.g., 12 or 24).
