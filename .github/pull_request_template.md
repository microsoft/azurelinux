###### Summary
<!-- Which release is this snapshot for? -->

###### Test Methodology
<!-- Pipeline build / verification used to derive the timestamp. -->
- Pipeline build id:

###### Checklist
- [ ] Added `release-repo-snapshot/releases/<release>.json` for the new release
- [ ] Bumped `release-repo-snapshot/latest.json` to match
- [ ] `azurelinux_release` field matches the corresponding `<release>-3.0` tag
- [ ] `repo_snapshot_timestamp` is a UNIX epoch (seconds)
