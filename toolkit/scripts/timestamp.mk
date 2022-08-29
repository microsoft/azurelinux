# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Timestamp Set Ups

######## Timestamp Set Ups ########

# At the beginning of the build, create an empty directory
# at build/timestamp, and create an "init" file. 

$(call create_folder,$(TIMESTAMP_DIR)) 
$(shell rm -rf $(TIMESTAMP_DIR)/*)
$(shell touch $(TIMESTAMP_DIR)/init)
