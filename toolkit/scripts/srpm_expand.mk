# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- SRPM Expanding

$(call create_folder,$(BUILD_SPECS_DIR))

######## SRPM EXPANDING ########

srpms = $(shell find $(BUILD_SRPMS_DIR)/ -type f -name '*.src.rpm')
srpm_expand_logs_dir = $(LOGS_DIR)/srpm_expand
srpm_expand_log = $(srpm_expand_logs_dir)/srpm_expand.log

$(call create_folder,$(srpm_expand_logs_dir))

.PHONY: expand-specs clean-expand-specs
expand-specs: $(BUILD_SPECS_DIR)

clean: clean-expand-specs
clean-expand-specs:
	rm -rf $(BUILD_SPECS_DIR)
	rm -rf $(STATUS_FLAGS_DIR)/build_specs.flag
	rm -rf $(srpm_expand_logs_dir)

# The directory freshness is tracked with a status flag. The status flag is only updated when all SPECS have been
# updated.
$(BUILD_SPECS_DIR): $(STATUS_FLAGS_DIR)/build_specs.flag
	@touch $@
	@echo "Finished updating $@." | tee -a $(srpm_expand_log)

# For each SRPM, if it is newer than the spec extract a new copy of the .spec file
$(STATUS_FLAGS_DIR)/build_specs.flag: $(srpms) $(BUILD_SRPMS_DIR)
	@echo "Extracting new or updated SRPMs from \"$(BUILD_SRPMS_DIR)\"." | tee $(srpm_expand_log) && \
	for srpm in $(srpms); do \
		spec_destination=$(BUILD_SPECS_DIR)/$$(rpm -qp $$srpm --define='with_check 1' --queryformat %{NAME}-%{VERSION}-%{RELEASE}/%{NAME}.spec) && \
		spec_dir=$$(dirname $$spec_destination) && \
		if [ ! -f $@ -o $$srpm -nt $@ ]; then \
			srpm_filename=$$(basename $$srpm) && \
			echo "Extracting \"$$srpm_filename\" to \"$$spec_dir\"." | tee -a $(srpm_expand_log) && \
			mkdir -p $$spec_dir && \
			cd $$spec_dir && \
			rpm2cpio $$srpm | cpio -idvu 2>>$(srpm_expand_log) && \
			echo "Extracted \"$$srpm_filename\"." >> $(srpm_expand_log) || $(call print_error,Failed to expand "$$srpm".); \
		fi \
	done || $(call print_error,Checking for spec updates failed. See above errors and "$(srpm_expand_log)" for more details.); \
	touch $@
