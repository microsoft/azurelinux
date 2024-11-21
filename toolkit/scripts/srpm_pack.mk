# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- SRPM Packing


######## SRPM PACKING ########

# Options for SRPM_FILE_SIGNATURE_HANDLING:
# enforce - Source signatures must match those specified in a signatures file
# skip    - Do not check signatures
# update  - Check signatures and updating any mismatches in the signatures file
SRPM_FILE_SIGNATURE_HANDLING ?= enforce

SRPM_BUILD_CHROOT_DIR = $(BUILD_DIR)/SRPM_packaging
SRPM_BUILD_LOGS_DIR = $(LOGS_DIR)/pkggen/srpms

toolchain_spec_list = $(toolchain_build_dir)/toolchain_specs.txt
srpm_pack_list_file = $(BUILD_SRPMS_DIR)/pack_list.txt

# Configure the list of packages we want to process into SRPMs
# Strip any whitespace from user input and reasign using override so we can compare it with the empty string
override SRPM_PACK_LIST := $(strip $(SRPM_PACK_LIST))

ifneq ($(SRPM_PACK_LIST),) # Pack list has user entries in it, only build selected .spec files
local_specs = $(wildcard $(addprefix $(SPECS_DIR)/*/,$(addsuffix .spec,$(SRPM_PACK_LIST))))
$(srpm_pack_list_file): $(depend_SRPM_PACK_LIST)
	@echo $(SRPM_PACK_LIST) | tr " " "\n" > $(srpm_pack_list_file)
else # Empty pack list, build all under $(SPECS_DIR)
local_specs = $(call shell_real_build_only, find $(SPECS_DIR)/ -type f -name '*.spec')
$(srpm_pack_list_file): $(depend_SRPM_PACK_LIST)
	@truncate -s 0 $@
endif
local_spec_dirs = $(foreach spec,$(local_specs),$(dir $(spec)))
local_spec_sources = $(call shell_real_build_only, find $(local_spec_dirs) -type f -name '*')

$(call create_folder,$(BUILD_DIR))
$(call create_folder,$(BUILD_SRPMS_DIR))
$(call create_folder,$(SRPM_BUILD_CHROOT_DIR))

# General targets
##help:target:input-srpms=Scan the local `*.spec` files, locate sources, and create `*.src.rpm` files. Limit via SRPM_PACK_LIST.
.PHONY: toolchain-input-srpms input-srpms clean-input-srpms
input-srpms: $(BUILD_SRPMS_DIR)
toolchain-input-srpms: $(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag

clean: clean-input-srpms
clean-input-srpms:
	rm -rf $(BUILD_SRPMS_DIR)
	rm -rf $(STATUS_FLAGS_DIR)/build_srpms.flag
	rm -rf $(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag
	@echo Verifying no mountpoints present in $(SRPM_BUILD_CHROOT_DIR)
	$(SCRIPTS_DIR)/safeunmount.sh "$(SRPM_BUILD_CHROOT_DIR)" && \
	rm -rf $(SRPM_BUILD_CHROOT_DIR)

# The directory freshness is tracked with a status flag. The status flag is only updated when all SRPMs have been
# updated.
$(BUILD_SRPMS_DIR): $(STATUS_FLAGS_DIR)/build_srpms.flag
	@touch $@
	@echo Finished updating $@

ifeq ($(DOWNLOAD_SRPMS),y)
$(STATUS_FLAGS_DIR)/build_srpms.flag: $(local_specs) $(local_spec_dirs) $(local_spec_sources) $(SPECS_DIR) $(go-downloader)
	for spec in $(local_specs); do \
		spec_file=$${spec} && \
		srpm_file=$$(rpmspec -q $${spec_file} --srpm --define='with_check 1' --define='dist $(DIST_TAG)' --queryformat %{NAME}-%{VERSION}-%{RELEASE}.src.rpm) && \
		for url in $(SRPM_URL_LIST); do \
			$(go-downloader) $${url}/$${srpm_file} \
				-O $(BUILD_SRPMS_DIR)/$${srpm_file} \
				--no-verbose \
				$(if $(TLS_CERT),--certificate=$(TLS_CERT)) \
				$(if $(TLS_KEY),--private-key=$(TLS_KEY)) \
				&& \
			touch $(BUILD_SRPMS_DIR)/$${srpm_file} && \
			break; \
		done || $(call print_error,Loop in $@ failed) ; \
		{ [ -f $(BUILD_SRPMS_DIR)/$${srpm_file} ] || \
			$(call print_error,Failed to download $${srpm_file});  } \
	done || $(call print_error,Loop in $@ failed) ; \
	touch $@

# Since all the SRPMs are being downloaded by the "input-srpms" target there is no need to differentiate toolchain srpms.
$(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag: $(STATUS_FLAGS_DIR)/build_srpms.flag
	@touch $@
else
$(STATUS_FLAGS_DIR)/build_srpms.flag: $(chroot_worker) $(local_specs) $(local_spec_dirs) $(SPECS_DIR) $(go-srpmpacker) $(srpm_pack_list_file) $(local_spec_sources)
	GODEBUG=netdns=go $(go-srpmpacker) \
		--dir=$(SPECS_DIR) \
		--output-dir=$(BUILD_SRPMS_DIR) \
		--source-url=$(SOURCE_URL) \
		--dist-tag=$(DIST_TAG) \
		--ca-cert=$(CA_CERT) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		--build-dir=$(SRPM_BUILD_CHROOT_DIR) \
		--signature-handling=$(SRPM_FILE_SIGNATURE_HANDLING) \
		--worker-tar=$(chroot_worker) \
		$(if $(filter y,$(RUN_CHECK)),--run-check) \
		$(if $(SRPM_PACK_LIST),--pack-list=$(srpm_pack_list_file)) \
		--log-file=$(SRPM_BUILD_LOGS_DIR)/srpmpacker.log \
		--log-level=$(LOG_LEVEL) \
		--log-color=$(LOG_COLOR) \
		--cpu-prof-file=$(PROFILE_DIR)/srpm_packer.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/srpm_packer.mem.pprof \
		--trace-file=$(PROFILE_DIR)/srpm_packer.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/srpm_packer.jsonl && \
	touch $@

$(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag: $(toolchain_spec_list) $(go-srpmpacker)
	GODEBUG=netdns=go $(go-srpmpacker) \
		--dir=$(SPECS_DIR) \
		--output-dir=$(BUILD_SRPMS_DIR) \
		--source-url=$(SOURCE_URL) \
		--dist-tag=$(DIST_TAG) \
		--ca-cert=$(CA_CERT) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		--build-dir=$(SRPM_BUILD_CHROOT_DIR) \
		--signature-handling=$(SRPM_FILE_SIGNATURE_HANDLING) \
		--pack-list=$(toolchain_spec_list) \
		$(if $(filter y,$(RUN_CHECK)),--run-check) \
		--log-file=$(LOGS_DIR)/toolchain/srpms/toolchain_srpmpacker.log \
		--log-level=$(LOG_LEVEL) \
		--log-color=$(LOG_COLOR) \
		--cpu-prof-file=$(PROFILE_DIR)/srpm_toolchain_packer.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/srpm_toolchain_packer.mem.pprof \
		--trace-file=$(PROFILE_DIR)/srpm_toolchain_packer.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/srpm_toolchain_packer.jsonl && \
	touch $@
endif
