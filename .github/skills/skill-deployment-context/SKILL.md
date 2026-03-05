---
name: deployment-context
description: "Resolve Koji AKS deployment context -- resource group, cluster name, subscription, Log Analytics workspace, and monitoring resource names from deployment_summary.yaml."
---

# Koji Deployment Context Discovery

**Always resolve context before running queries. Never assume resource names.**

## Step 1: Read `deployment_summary.yaml`

This file contains `resource_group`, `aks_cluster_name`, `subscription_id`, and monitoring resource names/IDs. Read it first.

## Step 2: If subscription is missing

Run: `az account show --query id -o tsv`

## Step 3: If deployment does not match the summary

Ask the user for the **resource group** or **AKS cluster name**.

## Step 4: Discover monitoring resources dynamically

```bash
az monitor log-analytics workspace list --resource-group <RG> -o table
az resource list --resource-group <RG> --resource-type Microsoft.Monitor/accounts -o table
az resource list --resource-group <RG> --resource-type Microsoft.Dashboard/grafana -o table
```

## Naming convention

Resources follow `<prefix>-koji-*`:
- Resource group: `<prefix>-koji-rg-<suffix>`
- AKS cluster: `<prefix>-koji-aks`
- Log Analytics: `<prefix>-koji-logs`
- Azure Monitor: `<prefix>-koji-monitor`
- Grafana: `<prefix>-koji-grafana`

## MCP tools for context discovery

| Tool | Purpose |
|------|---------|
| `aks_cluster_get` | List/get AKS cluster details |
| `aks_nodepool_get` | List/get node pool details |
| `monitor_table_list` | List tables in a Log Analytics workspace |

**Prerequisites:** Node.js (`npx`) and an active `az login` session.
