---
name: kql-queries
description: "KQL query templates for Koji container logs, pod errors, restarts, Kubernetes events, build job activity, and node resource usage via Log Analytics."
---

# Koji KQL Log Queries

## Tools

| Tool | Purpose |
|------|---------|
| `monitor_workspace_log_query` | KQL queries across entire Log Analytics workspace |
| `monitor_resource_log_query` | KQL queries scoped to a specific resource |
| `monitor_table_list` | List available tables in the workspace |

## Koji pod namespace

Koji pods run in the **`default`** namespace. Always filter:
- `Namespace == "default"` (KubePodInventory, KubeEvents)
- `PodNamespace == "default"` (ContainerLogV2)
- Combine with: `Name startswith "koji-"` or `PodName startswith "koji-"`

## Query reference

### Pod health and status
```kql
KubePodInventory
| where Namespace == "default"
| where Name startswith "koji-"
| summarize arg_max(TimeGenerated, *) by Name
| project TimeGenerated, Name, ContainerStatus, ContainerRestartCount, PodRestartCount
| order by Name asc
```

### Container errors (all Koji pods)
```kql
ContainerLogV2
| where PodNamespace == "default"
| where PodName startswith "koji-"
| where LogLevel == "error" or LogMessage contains "ERROR" or LogMessage contains "Traceback"
| project TimeGenerated, PodName, LogMessage
| order by TimeGenerated desc
| take 50
```

### Koji Hub logs
```kql
ContainerLogV2
| where PodNamespace == "default"
| where PodName startswith "koji-hub"
| project TimeGenerated, PodName, LogMessage
| order by TimeGenerated desc
| take 100
```

### Koji Builder logs
```kql
ContainerLogV2
| where PodNamespace == "default"
| where PodName startswith "koji-builder"
| project TimeGenerated, PodName, LogMessage
| order by TimeGenerated desc
| take 100
```

### Node resource usage
```kql
Perf
| where ObjectName == "K8SNode"
| where CounterName in ("cpuUsageNanoCores", "cpuCapacityNanoCores", "memoryWorkingSetBytes", "memoryCapacityBytes")
| summarize AvgValue=avg(CounterValue) by Computer, CounterName
| evaluate pivot(CounterName, take_any(AvgValue))
| extend CPUPercent = round(cpuUsageNanoCores / cpuCapacityNanoCores * 100, 1),
         MemPercent = round(memoryWorkingSetBytes / memoryCapacityBytes * 100, 1),
         MemUsedGB = round(memoryWorkingSetBytes / 1073741824, 1),
         MemCapGB = round(memoryCapacityBytes / 1073741824, 1)
| project Computer, CPUPercent, MemPercent, MemUsedGB, MemCapGB
| order by Computer asc
```

### Pod restarts
```kql
KubePodInventory
| where Namespace == "default"
| where Name startswith "koji-"
| summarize MaxRestarts = max(ContainerRestartCount) by Name, ContainerName, ContainerStatus
| where MaxRestarts > 0
| order by MaxRestarts desc
```

### Kubernetes warning events
```kql
KubeEvents
| where Namespace == "default"
| where Name startswith "koji-"
| where Reason in ("BackOff", "Unhealthy", "Failed", "Killing", "OOMKilling")
| project TimeGenerated, Name, Reason, Message
| order by TimeGenerated desc
| take 50
```
> KubeEvents may be empty under Group-Default DCR preset. Fall back to KubePodInventory restart counts.

### Build job activity
```kql
ContainerLogV2
| where PodNamespace == "default"
| where PodName startswith "koji-builder"
| where LogMessage contains "build" or LogMessage contains "task"
| project TimeGenerated, PodName, LogMessage
| order by TimeGenerated desc
| take 100
```
