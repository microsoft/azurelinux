# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Chroot Utilities

######## CHROOT TOOLS ########

chroot_worker = $(BUILD_DIR)/worker/worker_chroot.tar.gz

.PHONY: chroot-tools clean-chroot-tools validate-chroot
##help:target:chroot-tools=Create the chroot working from the toolchain RPMs.
chroot-tools: $(chroot_worker)

clean: clean-chroot-tools
clean-chroot-tools:
	rm -f $(chroot_worker)
	@echo Verifying no mountpoints present in $(BUILD_DIR)/worker/
	$(SCRIPTS_DIR)/safeunmount.sh "$(BUILD_DIR)/worker/" && \
	$(SCRIPTS_DIR)/safeunmount.sh "$(BUILD_DIR)/validatechroot/" && \
	rm -rf $(BUILD_DIR)/worker && \
	rm -rf $(BUILD_DIR)/validatechroot

# Worker chroot manifest is a file corresponding to the TOOLCHAIN_MANIFEST name.
toolchain_config_name=$(notdir $(TOOLCHAIN_MANIFEST))
worker_manifest_name=$(shell echo "$(toolchain_config_name)" | sed -E 's:^toolchain:pkggen_core:' )
worker_chroot_manifest = $(TOOLCHAIN_MANIFESTS_DIR)/$(worker_manifest_name)
#$(TOOLCHAIN_MANIFESTS_DIR)/pkggen_core_$(build_arch).txt
# Find the *.rpm corresponding to each of the entries in the manifest
# regex operation: (.*\.([^\.]+)\.rpm) extracts *.(<arch>).rpm" to determine
# the exact path of the required rpm
# Outputs: $(TOOLCHAIN_RPMS_DIR)/<arch>/<name>.<arch>.rpm
sed_regex_full_path = 's`(.*\.([^\.]+)\.rpm)`$(TOOLCHAIN_RPMS_DIR)/\2/\1`p'
worker_chroot_rpm_paths := $(shell sed -nr $(sed_regex_full_path) < $(worker_chroot_manifest))

# The worker chroot depends on specific toolchain RPMs, the $(toolchain_rpms): target in toolchain.mk knows how
# to update these RPMs if required.
worker_chroot_deps := \
	$(worker_chroot_manifest) \
	$(worker_chroot_rpm_paths) \
	$(PKGGEN_DIR)/worker/create_worker_chroot.sh

ifeq ($(REFRESH_WORKER_CHROOT),y)
$(chroot_worker): $(worker_chroot_deps) $(depend_REBUILD_TOOLCHAIN) $(depend_TOOLCHAIN_ARCHIVE)
else
$(chroot_worker):
endif
	$(PKGGEN_DIR)/worker/create_worker_chroot.sh $(BUILD_DIR)/worker $(worker_chroot_manifest) $(TOOLCHAIN_RPMS_DIR) $(LOGS_DIR)

validate-chroot: $(go-validatechroot) $(chroot_worker)
	$(go-validatechroot) \
	--rpm-dir="$(TOOLCHAIN_RPMS_DIR)" \
	--tmp-dir="$(BUILD_DIR)/validatechroot" \
	--worker-chroot="$(chroot_worker)" \
	--worker-manifest="$(worker_chroot_manifest)" \
	--log-file="$(LOGS_DIR)/worker/validate.log" \
	--log-level="$(LOG_LEVEL)"

######## MACRO TOOLS ########

macro_rpmrc = $(RPMRC_DIR)/rpmrc

macro_manifest = $(TOOLCHAIN_MANIFESTS_DIR)/macro_packages.txt

.PHONY: macro-tools clean-macro-tools
##help:target:macro-tools=Create the directory with expanded rpm macros.
macro-tools: $(macro_rpmrc)

$(macro_rpmrc): $(toolchain_rpms)
	$(SCRIPTS_DIR)/preparemacros.sh $(MACRO_DIR) $(CACHED_RPMS_DIR)/cache $(macro_manifest)

clean: clean-macro-tools
clean-macro-tools:
	rm -rf $(MACRO_DIR)
