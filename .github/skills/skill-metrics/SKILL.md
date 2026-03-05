---
name: metrics
description: "Query Azure Monitor metrics for Koji AKS node CPU, memory, disk usage, pod readiness, and PostgreSQL database performance."
---

# Koji Azure Monitor Metrics

## Tools

| Tool | Purpose |
|------|---------|
| `monitor_metrics_definitions` | Discover available metrics for a resource |
| `monitor_metrics_query` | Query metric time-series values |

## Key metric namespaces

### AKS (`Microsoft.ContainerService/managedClusters`)
| Metric | Description |
|--------|-------------|
| `node_cpu_usage_percentage` | Node CPU utilization |
| `node_memory_working_set_percentage` | Node memory utilization |
| `kube_pod_status_ready` | Pod readiness count |
| `node_disk_usage_percentage` | Node disk utilization |

## Common query patterns

Use `aggregation: "Average"` and `interval: "PT1H"` for hourly trends, `interval: "PT5M"` for granular views.

Example: Query AKS node CPU and memory over the last 24 hours:
- `resource`: AKS cluster name from deployment summary
- `metric-names`: `node_cpu_usage_percentage,node_memory_working_set_percentage`
- `metric-namespace`: `Microsoft.ContainerService/managedClusters`
- `aggregation`: `Average`
- `interval`: `PT1H`
