# Repo snapshot

Each file under `releases/` records the Azure Linux package set
associated with one official release. `latest.json` is a copy of the
most recent entry.

```json
{
  "repo_snapshot_timestamp": 1700000000,
  "azurelinux_release": "3.0.YYYYMMDD"
}
```

| Field | Meaning |
|---|---|
| `repo_snapshot_timestamp` | UNIX epoch. `tdnf` honors this via the `snapshottime=` config key and filters every repo to packages published at or before this instant. |
| `azurelinux_release` | Azure Linux release tag this snapshot is associated with. The file under `releases/` is named after this tag. See https://github.com/microsoft/azurelinux/releases for the corresponding release notes. |
