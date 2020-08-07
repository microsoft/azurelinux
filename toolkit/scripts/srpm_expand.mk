# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- SRPM Expanding

$(call create_folder,$(BUILD_SPECS_DIR))

######## SRPM EXPANDING ########

srpms = $(shell find $(BUILD_SRPMS_DIR)/ -type f -name '*.src.rpm')

.PHONY: expand-specs clean-expand-specs
expand-specs: $(BUILD_SPECS_DIR)

clean: clean-expand-specs
clean-expand-specs:
	rm -rf $(BUILD_SPECS_DIR)
	rm -rf $(STATUS_FLAGS_DIR)/build_specs.flag

# The directory freshness is tracked with a status flag. The status flag is only updated when all SPECS have been
# updated.
$(BUILD_SPECS_DIR): $(STATUS_FLAGS_DIR)/build_specs.flag
	@touch $@
	@echo Finished updating $@

$(STATUS_FLAGS_DIR)/build_specs.flag: $(srpms) $(BUILD_SRPMS_DIR)
	# For each SRPM, if it is newer than the spec extract a new copy of the .spec file
	for srpm in $(srpms); do \
		srpm_file=$${srpm} && \
		spec_destination=$(BUILD_SPECS_DIR)/$$(rpm -qp $${srpm_file} --define='with_check 1' --queryformat %{NAME}-%{VERSION}-%{RELEASE}/%{NAME}.spec) && \
		spec_dir=$$(dirname $${spec_destination}) && \
		if [ $${srpm_file} -nt $@ -o ! -f $@ ]; then \
			mkdir -p $${spec_dir} && \
			echo extracting $${spec_destination} && \
			cd $${spec_dir} && rpm2cpio $${srpm_file} | cpio -idvu || $(call print_error,Failed to expand $${srpm_file}) ; \
		fi || $(call print_error,If in $@ failed) ; \
	done || $(call print_error,Loop in $@ failed) ; \
	touch $@



