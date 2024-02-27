
# Developer Tools

## containerized-rpmbuild

This [tool](./../../scripts/containerized-build/) enables the user to build/test a single Mariner package. It creates a Mariner container, either using the worker chroot as the fs or using upstream Mariner container (depending on the mode), and mounts SPECs, INTERMEDIATE_SRPMS, and out/RPMs from Mariner repository at repo_path (or the current Mariner repo) into the container. The user can choose whether to use locally built RPMs or upstream RPMs to satisfy build and runtime dependencies. One can use native rpm commands to build packages. Changes made to SPECS/ are synced to the host. All other changes are lost.

The user can optionally add arguments. REPO_PATH defines directory to use as Mariner repo, default is current directory. MODE can be build (default) or test. Mariner VERSION may be 2.0 (default) or 1.0. MOUNTS specify directories to mount into the container, besides the default ones. BUILD_MOUNT defines directory to mount as build directory into container, default is $REPO_PATH/build. EXTRA_PACKAGES to install into container besides the default ones. ENABLE_REPO to use local RPMs to satisfy build depenedencies. KEEP_CONTAINER to keep container on exit. By default, it is cleaned up upon exit. In addition, user may override any Mariner make definitions e.g. SPECS_DIR, SRPM_PACK_LIST, etc.

```bash
cd CBL-Mariner/toolkit
sudo make containerized-rpmbuild

# To see optional arguments and usage
sudo make containerized-rpmbuild-help
```
