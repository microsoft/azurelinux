
# Developer Tools

## containerized-rpmbuild

This [tool](./../../scripts/containerized-build/) enables the user to build/test a single Mariner package. It creates a Mariner container, either using the worker chroot as the fs or using upstream Mariner container (depending on the mode), and mounts SPECs, INTERMEDIATE_SRPMS, and out/RPMs from Mariner repository at repo_path (or the current Mariner repo). The user can choose whether to use locally built RPMs or upstream RPMs to satisfy build and runtime dependencies. One can use native rpm commands to build packages. Changes made to SPECS/ are synced to the host

```bash
cd CBL-Mariner/toolkit
sudo make containerized-rpmbuild

# To see optional arguments and usage
sudo make containerized-rpmbuild-help
```
