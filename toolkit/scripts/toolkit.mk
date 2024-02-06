# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Toolkit Creation

######## TOOLKIT CREATION ########

# Toolkit Components
toolkit_component_extra_files = \
	$(PROJECT_ROOT)/CONTRIBUTING.md \
	$(PROJECT_ROOT)/LICENSES-AND-NOTICES/LICENSE.md \
	$(toolkit_root)/.gitignore

mariner_repos_dir = $(PROJECT_ROOT)/SPECS/mariner-repos
mariner_repos_files = $(wildcard $(mariner_repos_dir)/*.repo)
rpms_snapshot_name = rpms_snapshot.json
specs_dir_name = $(notdir $(SPECS_DIR))
toolkit_remove_archive = $(OUT_DIR)/toolkit-*.tar*
toolkit_root_files = $(wildcard $(toolkit_root)/*)
toolkit_version   = $(RELEASE_VERSION)-$(build_arch)

# Build files
rpms_snapshot_dir_name = rpms_snapshots
rpms_snapshot_build_dir = $(BUILD_DIR)/$(rpms_snapshot_dir_name)
rpms_snapshot_logs_path = $(LOGS_DIR)/$(rpms_snapshot_dir_name)/rpms_snapshot.log
rpms_snapshot_per_specs = $(rpms_snapshot_build_dir)/$(specs_dir_name)_$(rpms_snapshot_name)

valid_arch_spec_names_build_dir = $(BUILD_DIR)/valid_arch_spec_names
valid_arch_spec_names           = $(valid_arch_spec_names_build_dir)/valid_arch_spec_names.txt
valid_arch_spec_names_logs_path = $(LOGS_DIR)/valid_arch_spec_names/valid_arch_spec_names.log

toolkit_build_dir   = $(BUILD_DIR)/toolkit_prep
toolkit_archive   = $(toolkit_build_dir)/toolkit.tar
toolkit_archive_versioned   = $(toolkit_build_dir)/toolkit_versioned.tar

toolkit_prep_dir = $(toolkit_build_dir)/toolkit
toolkit_release_file = $(toolkit_prep_dir)/version.txt
toolkit_release_file_relative_path = $(toolkit_release_file:$(toolkit_build_dir)/%=%)
toolkit_rpms_snapshot_file = $(toolkit_prep_dir)/$(rpms_snapshot_name)
toolkit_rpms_snapshot_file_relative_path = $(toolkit_rpms_snapshot_file:$(toolkit_build_dir)/%=%)
toolkit_repos_dir = $(toolkit_prep_dir)/repos
toolkit_tools_dir = $(toolkit_prep_dir)/tools/toolkit_bins

$(call create_folder,"$(rpms_snapshot_build_dir)")
$(call create_folder,"$(toolkit_prep_dir)")

# Outputs
toolkit_archive_versioned_compressed   = $(OUT_DIR)/toolkit-$(toolkit_version).tar.gz
rpms_snapshot = $(OUT_DIR)/$(rpms_snapshot_name)

.PHONY: package-toolkit rpms-snapshot clean-package-toolkit clean-rpms-snapshot

clean: clean-package-toolkit clean-rpms-snapshot

clean-package-toolkit:
	rm -f $(toolkit_remove_archive)
	rm -rf $(toolkit_build_dir)

clean-rpms-snapshot:
	rm -f $(rpms_snapshot)
	@echo Verifying no mountpoints present in $(rpms_snapshot_build_dir)
	$(SCRIPTS_DIR)/safeunmount.sh "$(rpms_snapshot_build_dir)" && \
	rm -rf $(rpms_snapshot_build_dir)
	rm -f $(rpms_snapshot_logs_path)

##help:target:package-toolkit=Create this toolkit.
package-toolkit: $(toolkit_archive_versioned_compressed)
	@echo "Toolkit packed under '$(toolkit_archive_versioned_compressed)'."

$(toolkit_archive_versioned_compressed): $(toolkit_archive) $(rpms_snapshot) $(depend_SPECS_DIR)
	cp $(toolkit_archive) $(toolkit_archive_versioned) && \
	echo "$(toolkit_version)" > $(toolkit_release_file) && \
	cp $(rpms_snapshot) $(toolkit_rpms_snapshot_file) && \
	tar --update -f $(toolkit_archive_versioned) -C $(toolkit_build_dir) $(toolkit_release_file_relative_path) $(toolkit_rpms_snapshot_file_relative_path) && \
	$(ARCHIVE_TOOL) --best -c $(toolkit_archive_versioned) > $(toolkit_archive_versioned_compressed)

$(toolkit_archive): $(go_tool_targets) $(mariner_repos_files) $(toolkit_component_extra_files) $(toolkit_root_files)
	rm -rf $(toolkit_prep_dir) && \
	mkdir -p $(toolkit_prep_dir) && \
	mkdir -p $(toolkit_repos_dir) && \
	mkdir -p $(toolkit_tools_dir) && \
	cp -r $(toolkit_root_files) $(toolkit_prep_dir) && \
	cp $(mariner_repos_files) $(toolkit_repos_dir) && \
	cp $(toolkit_component_extra_files) $(toolkit_prep_dir) && \
	cp $(go_tool_targets) $(toolkit_tools_dir) && \
	rm -rf $(toolkit_prep_dir)/out && \
	tar -cvp -f $(toolkit_archive) -C $(dir $(toolkit_prep_dir)) $(notdir $(toolkit_prep_dir))

rpms-snapshot: $(rpms_snapshot)
	@echo "RPMs snapshot generated under '$(rpms_snapshot)'."

$(rpms_snapshot): $(rpms_snapshot_per_specs) $(depend_SPECS_DIR)
	cp $(rpms_snapshot_per_specs) $(rpms_snapshot)

$(rpms_snapshot_per_specs): $(go-rpmssnapshot) $(chroot_worker) $(local_specs) $(local_spec_dirs) $(SPECS_DIR)
	@mkdir -p "$(rpms_snapshot_build_dir)"
	$(go-rpmssnapshot) \
		--input="$(SPECS_DIR)" \
		--output="$(rpms_snapshot_per_specs)" \
		--build-dir="$(rpms_snapshot_build_dir)" \
		--dist-tag=$(DIST_TAG) \
		--worker-tar="$(chroot_worker)" \
		--log-level=$(LOG_LEVEL) \
		--log-file="$(rpms_snapshot_logs_path)" \
		--log-color="$(LOG_COLOR)""

print-build-summary:
	sed -E -n 's:^.+level=info msg="Built \(([^\)]+)\) -> \[(.+)\].+$:\1\t\2:gp' $(LOGS_DIR)/pkggen/rpmbuilding/* | tee $(LOGS_DIR)/pkggen/build-summary.csv

# This will run the spec arch checker and generate a list of valid spec names suitable for passing to PACKAGE_BUILD_LIST et. al.
.PHONY: run-specarchchecker
run-specarchchecker: $(valid_arch_spec_names)
	@cat $(valid_arch_spec_names) && echo "" # File doesn't have a newline at the end, so add one via echo.
	@echo "Valid arch spec names generated under '$(valid_arch_spec_names)'."

$(valid_arch_spec_names): $(go-specarchchecker) $(chroot_worker) $(local_specs) $(local_spec_dirs) $(SPECS_DIR) $(depend_PACKAGE_BUILD_LIST) $(depend_PACKAGE_REBUILD_LIST) 
	$(go-specarchchecker) \
		--input="$(SPECS_DIR)" \
		--output="$@" \
		--packages="$(PACKAGE_BUILD_LIST)" \
		--rebuild-packages="$(PACKAGE_REBUILD_LIST)" \
		--build-dir="$(valid_arch_spec_names_build_dir)" \
		$(if $(filter y,$(RUN_CHECK)),--test-only) \
		--dist-tag=$(DIST_TAG) \
		--worker-tar="$(chroot_worker)" \
		--log-level=$(LOG_LEVEL) \
		--log-file="$(valid_arch_spec_names_logs_path)" \
		--log-color="$(LOG_COLOR)"
