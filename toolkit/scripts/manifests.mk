# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#   - Optional mechanisms for regenerating the toolchain manifests

TOOLCHAIN_MANIFEST           ?= $(TOOLCHAIN_MANIFESTS_DIR)/toolchain_$(build_arch).txt
WORKER_CHROOT_MANIFEST       ?= $(TOOLCHAIN_MANIFESTS_DIR)/pkggen_core_$(build_arch).txt
