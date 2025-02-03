# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Misc. Makefile Defines
#	- Misc. Makefile Functions
#	- Variable prerequisite tracking

######## MISC. MAKEFILE DEFINES ########

# Check if we have pigz available to speed up archive commands
ARCHIVE_TOOL ?= $(shell if command -v pigz 1>/dev/null 2>&1 ; then echo pigz ; else echo gzip ; fi )
# Host and target architecture
build_arch := $(shell uname -m)

no_repo_acl = $(STATUS_FLAGS_DIR)/no_repo_acl.flag

######## MISC. MAKEFILE Functions ########

ifeq (n,$(findstring n,$(firstword $(MAKEFLAGS))))
# Dryrun, noop
create_folder =
else # ifeq (n,$(findstring...
# Creates a folder if it doesn't exist. Also sets the timestamp to 0 if it is
# created. It will recursively call for each parent folder.
# If the folder already exists, it will do nothing.
# If the folder is not created, it will print an error and exit.
#
# Need to do some extra steps here so the user will get meaningful debug output from the shell script, generally a
# call to $(shell ...) will not generate any output to the console.
#
# $1 - Folder path
define create_folder
$(eval create_dir_temp_output = $(shell $(SCRIPTS_DIR)/makedirs.sh $1 $(MARINER_BUILDER_USER))) \
$(if $(create_dir_temp_output),$(warning $(create_dir_temp_output)),) \
$(if $(wildcard $1),,$(error create_folder: $1 not created))
endef
endif # ifeq (n,$(findstring...

# Runs a shell commannd only if we are actually doing a build rather than parsing the makefile for tab-completion etc
# Make will automatically create the MAKEFLAGS variable which contains each of the flags, non-build commmands will include -n
# which is the short form of --dry-run.
#
# $1 - The full command to run, if we are not doing --dry-run
ifeq (n,$(findstring n,$(firstword $(MAKEFLAGS))))
shell_real_build_only =
else # ifeq (n,$(findstring...
shell_real_build_only = $(shell $1)
endif # ifeq (n,$(findstring...

# Echos a message to console, then calls "exit 1"
# Of the form: { echo "MSG" ; exit 1 ; }
#
# $1 - Error message to print
define print_error
{ echo "$1" ; exit 1 ; }
endef

# Echos a message to console, then, if STOP_ON_WARNING is set to "y" calls "exit 1"
# Of the form: { echo "MSG" ; < exit 1 ;> }
#
# $1 - Warning message to print
define print_warning
{ echo "$1" ; $(if $(filter y,$(STOP_ON_WARNING)),exit 1 ;) }
endef

######## VARIABLE DEPENDENCY TRACKING ########

# List of variables to watch for changes.
watch_vars=PACKAGE_BUILD_LIST PACKAGE_REBUILD_LIST PACKAGE_IGNORE_LIST REPO_LIST CONFIG_FILE STOP_ON_PKG_FAIL TOOLCHAIN_ARCHIVE REBUILD_TOOLCHAIN SRPM_PACK_LIST SPECS_DIR MAX_CASCADING_REBUILDS RUN_CHECK TEST_RUN_LIST TEST_RERUN_LIST TEST_IGNORE_LIST EXTRA_BUILD_LAYERS
# Current list: $(depend_PACKAGE_BUILD_LIST) $(depend_PACKAGE_REBUILD_LIST) $(depend_PACKAGE_IGNORE_LIST) $(depend_REPO_LIST) $(depend_CONFIG_FILE) $(depend_STOP_ON_PKG_FAIL)
#					$(depend_TOOLCHAIN_ARCHIVE) $(depend_REBUILD_TOOLCHAIN) $(depend_SRPM_PACK_LIST) $(depend_SPECS_DIR) $(depend_EXTRA_BUILD_LAYERS) $(depend_MAX_CASCADING_REBUILDS) $(depend_RUN_CHECK) $(depend_TEST_RUN_LIST)
#					$(depend_TEST_RERUN_LIST) $(depend_TEST_IGNORE_LIST)

.PHONY: variable_depends_on_phony clean-variable_depends_on_phony setfacl_always_run_phony
clean: clean-variable_depends_on_phony

$(call create_folder,$(STATUS_FLAGS_DIR))
clean-variable_depends_on_phony:
	rm -rf $(STATUS_FLAGS_DIR)

# Watch for the variables by depending on '$(depend_<VAR_NAME>)'.
# Each variable will be tracked as a file $(STATUS_FLAGS_DIR)/<VAR_NAME>_tracking_flag.
# By having each generated target depend on the .PHONY target: variable_depends_on_phony,
# they will alway run. Each rule will check the currently stored value in the file and only
# update it if needed.

# Generate a target which watches a variable for changes so rebuilds can be
# triggered if needed. Uses one file per variable. If the value of the variable
# is not the same as recorded in the file, update the file to match. This will
# force a rebuild of any dependent targets.
#
# $1 - name of the variable to watch for changes
define depend_on_var
depend_$1=$(STATUS_FLAGS_DIR)/$1_tracking_flag
$(STATUS_FLAGS_DIR)/$1_tracking_flag: variable_depends_on_phony
	@if [ ! -f $$@ ]; then \
		echo $($1) > $$@ ; \
	elif [ "$($1)" != "$$$$(cat $$@)" ]; then \
		echo "Updated value of $1 ($$$$(cat $$@) -> $($1))" ; \
		echo $($1) > $$@ ; \
	fi
endef

# Invoke the above rule for each tracked variable
$(foreach var,$(watch_vars),$(eval $(call depend_on_var,$(var))))

# Host's ACLs influence the default permissions of the
# files inside the built RPMs. Disabling them for the repository.
#
# NOTE: we depend on a phony target and create the flag only once becase we want
#       to always run the "setfacl" command but not trigger a re-run of the targets
#       depending on this target.
$(no_repo_acl): setfacl_always_run_phony
	@setfacl -bnR $(PROJECT_ROOT) &>/dev/null && \
	if [ ! -f $@ ]; then \
		touch $@; \
	fi
