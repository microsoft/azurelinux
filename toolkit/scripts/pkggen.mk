# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Package dependency calculations
#	- Package builds

$(call create_folder,$(RPMS_DIR))
$(call create_folder,$(CACHED_RPMS_DIR))
$(call create_folder,$(PKGBUILD_DIR))
$(call create_folder,$(CHROOT_DIR))

######## PACKAGE DEPENDENCY CALCULATIONS ########

# Resources
pkggen_local_repo           = $(MANIFESTS_DIR)/package/local.repo
graphpkgfetcher_cloned_repo = $(MANIFESTS_DIR)/package/fetcher.repo

# SPECs and Built RPMs
build_specs     = $(shell find $(BUILD_SPECS_DIR)/ -type f -name '*.spec')
build_spec_dirs = $(foreach spec,$(build_specs),$(dir $(spec)))
pkggen_rpms     = $(shell find $(RPMS_DIR)/*  2>/dev/null )

# Pkggen workspace
cache_working_dir      = $(PKGBUILD_DIR)/tdnf_cache_worker
rpm_cache_files        = $(shell find $(CACHED_RPMS_DIR)/)
validate-pkggen-config = $(STATUS_FLAGS_DIR)/validate-image-config-pkggen.flag

# Outputs
specs_file        = $(PKGBUILD_DIR)/specs.json
graph_file        = $(PKGBUILD_DIR)/graph.dot
optimized_file    = $(PKGBUILD_DIR)/scrubbed_graph.dot
cached_file       = $(PKGBUILD_DIR)/cached_graph.dot
workplan          = $(PKGBUILD_DIR)/workplan.mk

logging_command = --log-file=$(LOGS_DIR)/pkggen/workplan/$(notdir $@).log --log-level=$(LOG_LEVEL)
$(call create_folder,$(LOGS_DIR)/pkggen/workplan)
$(call create_folder,$(LOGS_DIR)/pkggen/rpmbuilding)

.PHONY: workplan clean-workplan clean-cache graph-cache
workplan: $(workplan)
graph-cache: $(cached_file)
clean: clean-workplan clean-cache
clean-workplan:
	rm -rf $(PKGBUILD_DIR)
	rm -rf $(LOGS_DIR)/pkggen/workplan
clean-cache:
	rm -rf $(CACHED_RPMS_DIR)
	rm -f $(validate-pkggen-config)
	@echo Verifying no mountpoints present in $(cache_working_dir)
	$(SCRIPTS_DIR)/safeunmount.sh "$(cache_working_dir)" && \
	rm -rf $(cache_working_dir)

# Parse all specs in $(BUILD_SPECS_DIR) and generate a specs.json file encoding all dependency information
$(specs_file): $(BUILD_SPECS_DIR) $(build_specs) $(build_spec_dirs) $(go-specreader)
	$(go-specreader) \
		--dir $(BUILD_SPECS_DIR) \
		--srpm-dir $(BUILD_SRPMS_DIR) \
		--dist-tag $(DIST_TAG) \
		$(logging_command) \
		--output $@

# Convert the dependency information in the json file into a graph structure
$(graph_file): $(specs_file) $(go-grapher)
	$(go-grapher) \
		--input $(specs_file) \
		$(logging_command) \
		--output $@

graphoptimizer_extra_flags :=
ifeq ($(REBUILD_DEP_CHAINS), y)
graphoptimizer_extra_flags += --rebuild-missing-dep-chains
endif

# Remove any packages which don't need to be built, and flag any for rebuild if
# their dependencies are updated.
ifneq ($(CONFIG_FILE),)
# If an optional config file is passed, validate it and any files it includes. The target should always depend
# on the value of $(CONFIG_FILE) however, so keep $(depend_CONFIG_FILE) always.
# Actual validation is handled in imggen.mk
$(optimized_file): $(validate-pkggen-config)
endif
$(optimized_file): $(graph_file) $(go-graphoptimizer) $(depend_PACKAGE_BUILD_LIST) $(depend_PACKAGE_REBUILD_LIST) $(depend_PACKAGE_IGNORE_LIST) $(toolchain_rpms) $(pkggen_rpms) $(CONFIG_FILE) $(depend_CONFIG_FILE)
	$(go-graphoptimizer) \
		--input $(graph_file) \
		--rpm-dir $(RPMS_DIR) \
		--dist-tag $(DIST_TAG) \
		--packages "$(PACKAGE_BUILD_LIST)" \
		--rebuild-packages="$(PACKAGE_REBUILD_LIST)" \
		--ignore-packages="$(PACKAGE_IGNORE_LIST)" \
		--image-config-file="$(CONFIG_FILE)" \
		$(if $(CONFIG_FILE),--base-dir=$(CONFIG_BASE_DIR)) \
		$(logging_command) \
		$(graphoptimizer_extra_flags) \
		--output $@

# We want to detect changes in the RPM cache, but we are not responsible for directly rebuilding any missing files.
$(CACHED_RPMS_DIR)/%: ;

graphpkgfetcher_extra_flags :=
ifeq ($(DISABLE_UPSTREAM_REPOS),y)
graphpkgfetcher_extra_flags += --disable-upstream-repos
endif

ifeq ($(USE_UPDATE_REPO),y)
graphpkgfetcher_extra_flags += --use-update-repo
endif

ifeq ($(USE_PREVIEW_REPO),y)
graphpkgfetcher_extra_flags += --use-preview-repo
endif

# Compare files via checksum (-c) instead of timestamp so unchanged RPMs are left intact without updating the timestamp of the directories
$(cached_file): $(optimized_file) $(go-graphpkgfetcher) $(chroot_worker) $(pkggen_local_repo) $(depend_REPO_LIST) $(REPO_LIST) $(shell find $(CACHED_RPMS_DIR)/) $(pkggen_rpms)
	mkdir -p $(CACHED_RPMS_DIR)/cache && \
	$(go-graphpkgfetcher) \
		--input=$(optimized_file) \
		--output-dir=$(CACHED_RPMS_DIR)/cache \
		--rpm-dir=$(RPMS_DIR) \
		--tmp-dir=$(cache_working_dir) \
		--tdnf-worker=$(chroot_worker) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		$(foreach repo, $(pkggen_local_repo) $(graphpkgfetcher_cloned_repo) $(REPO_LIST),--repo-file=$(repo) ) \
		$(graphpkgfetcher_extra_flags) \
		$(logging_command) \
		--input-summary-file=$(PACKAGE_CACHE_SUMMARY) \
		--output-summary-file=$(PKGBUILD_DIR)/graph_external_deps.json \
		--output=$(cached_file) && \
	touch $@

# Generate a workplan from the graph which will build all the packages in order
$(workplan): $(cached_file) $(go-unravel) $(depend_STOP_ON_PKG_FAIL)
	$(go-unravel) \
		--input $(cached_file) \
		--format makefile \
		--run-check $(RUN_CHECK) \
		--dist-tag $(DIST_TAG) \
		--cache-dir $(CACHED_RPMS_DIR)/cache \
		--distro-release-version $(RELEASE_VERSION) \
		--distro-build-number $(BUILD_NUMBER) \
		--retry-attempts="$(PACKAGE_BUILD_RETRIES)" \
		$(if $(filter y,$(STOP_ON_PKG_FAIL)),--stop-on-failure) \
		$(logging_command) \
		--output $@

######## PACKAGE BUILD ########

pkggen_archive	= $(OUT_DIR)/rpms.tar.gz
srpms_archive  	= $(OUT_DIR)/srpms.tar.gz

.PHONY: build-packages clean-build-packages hydrate-rpms compress-rpms clean-compress-rpms compress-srpms clean-compress-srpms

# Execute the build plan encoded in the workplan makefile.
build-packages: $(RPMS_DIR)

clean: clean-build-packages clean-compress-rpms clean-compress-srpms
clean-build-packages:
	rm -rf $(RPMS_DIR)
	rm -rf $(LOGS_DIR)/pkggen/failures.txt
	rm -rf $(LOGS_DIR)/pkggen/rpmbuilding
	rm -rf $(STATUS_FLAGS_DIR)/build-rpms.flag
	@echo Verifying no mountpoints present in $(CHROOT_DIR)
	$(SCRIPTS_DIR)/safeunmount.sh "$(CHROOT_DIR)" && \
	rm -rf $(CHROOT_DIR)
clean-compress-rpms:
	rm -rf $(pkggen_archive)
clean-compress-srpms:
	rm -rf $(srpms_archive)

ifeq ($(REBUILD_PACKAGES),y)
$(RPMS_DIR): $(STATUS_FLAGS_DIR)/build-rpms.flag
	@touch $@
	@echo Finished updating $@
else
$(RPMS_DIR):
	@touch $@
endif

$(STATUS_FLAGS_DIR)/build-rpms.flag: $(workplan) $(chroot_worker) $(go-pkgworker)
ifeq ($(RUN_CHECK),y)
	$(warning Make argument 'RUN_CHECK' set to 'y', running package tests. Will add the 'ca-certificates' package and enable networking for package builds.)
endif
	@rm -f $(LOGS_DIR)/pkggen/failures.txt && \
	$(MAKE) --silent -f $(workplan) go-pkgworker=$(go-pkgworker) CHROOT_DIR=$(CHROOT_DIR) chroot_worker=$(chroot_worker) SRPMS_DIR=$(SRPMS_DIR) RPMS_DIR=$(RPMS_DIR) pkggen_local_repo=$(pkggen_local_repo) LOGS_DIR=$(LOGS_DIR) TOOLCHAIN_MANIFESTS_DIR=$(TOOLCHAIN_MANIFESTS_DIR) GOAL_PackagesToBuild && \
	{ [ ! -f $(LOGS_DIR)/pkggen/failures.txt ] || \
		$(call print_error,Failed to build: $$(cat $(LOGS_DIR)/pkggen/failures.txt)); } && \
	touch $@

# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-rpms:
	tar -I $(ARCHIVE_TOOL) -cvp -f $(BUILD_DIR)/temp_rpms_tarball.tar.gz -C $(RPMS_DIR)/.. $(notdir $(RPMS_DIR))
	mv $(BUILD_DIR)/temp_rpms_tarball.tar.gz $(pkggen_archive)

# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-srpms:
	tar -I $(ARCHIVE_TOOL) -cvp -f $(BUILD_DIR)/temp_srpms_tarball.tar.gz -C $(SRPMS_DIR)/.. $(notdir $(SRPMS_DIR))
	mv $(BUILD_DIR)/temp_srpms_tarball.tar.gz $(srpms_archive)

# Seed the RPMs folder with the any missing files from the archive.
hydrate-rpms:
	$(if $(PACKAGE_ARCHIVE),,$(error Must set PACKAGE_ARCHIVE=))
	@echo Unpacking RPMs from $(PACKAGE_ARCHIVE) into $(RPMS_DIR)
	tar -xf $(PACKAGE_ARCHIVE) -C $(RPMS_DIR) --strip-components 1 --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
