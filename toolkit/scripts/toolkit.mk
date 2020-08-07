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

# Outputs
toolkit_archive   = $(OUT_DIR)/toolkit-$(RELEASE_VERSION).tar.gz
toolkit_remove_archive = $(OUT_DIR)/toolkit-*.tar.gz
toolkit_build_dir = $(BUILD_DIR)/toolkit
toolkit_tools_dir = $(toolkit_build_dir)/tools/toolkit_bins

.PHONY: package-toolkit clean-package-toolkit

clean: clean-package-toolkit
clean-package-toolkit:
	rm -f $(toolkit_remove_archive)
	rm -rf $(toolkit_build_dir)

package-toolkit: go-tools
	rm -rf $(toolkit_build_dir) && \
	mkdir -p $(toolkit_build_dir) && \
	mkdir -p $(toolkit_tools_dir) && \
	cp -r $(toolkit_root)/* $(toolkit_build_dir) && \
	cp $(toolkit_component_extra_files) $(toolkit_build_dir) && \
	cp $(go_tool_targets) $(toolkit_tools_dir) && \
	rm -rf $(toolkit_build_dir)/out && \
	tar -I $(ARCHIVE_TOOL) -cvp -f $(toolkit_archive) -C $(toolkit_build_dir)/.. $(notdir $(toolkit_build_dir))
