# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Timestamp Set Ups

######## Timestamp Set Ups ########

# Need to short circuit the automatic entry from the tools.mk file for our go tool so it can be used anywhere
timestamper_tool = $(TOOL_BINS_DIR)/bldtracker

# At the beginning of the build, create an empty directory at build/timestamp
$(call create_folder,$(TIMESTAMP_DIR))
