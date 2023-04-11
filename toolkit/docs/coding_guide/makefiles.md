Start with a heading listing the contents of the makefile.
```make
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Group 1
#	- Group 2
```
Call `create_folder` on any folders which must be created before the build runs. `create_folder` will create the folder if it does not exist, then set the timestamp to zero (epoch) so that Make will calculate timestamps correctly versus any external files it isn't directly responsible for.

Add any variables which apply to the entire makefile here. User-overwritable variables should be `$(UPPER_CASE_VAR) ?= default`, while local or derived variables which apply to the whole group should be `$(lower_case_var) = $(shell foo)`
```make
# Describe the variables in a block above if they are related.
MY_OUT_FOLDER    ?= $(OUTPUT_FOLDER)/my_out
my_other_folder  = $(MY_OUT_FOLDER)/my_local

$(call create_folder,$(MY_OUT_FOLDER))
$(call create_folder,$(my_other_folder))
```
Add a heading for each group of targets and recipes.

Define targets or variables which apply to this group.
```make
######## GROUP 1 ########

# Any lists, derived targets, or other group specific variables
a_list_of_targets = t1 t2 t3
a_found_list_of_targets := $(shell find -name '*.my_files')

# A group local variable
group_name = group1
```
Where applicable, each group should define its own high-level `.PHONY` targets to build all and clean all.
```make
.PHONY: group-1 clean-group-1 misc-phony-target
group-1: $(a_found_list_of_targets)

clean: clean-group-1
clean-go-tools:
	rm -rf $(MY_OUT_FOLDER)
	rm -rf $(MY_OTHER_OUT_FOLDER)
```
Fill the remainder of the makefile here, grouping local variables with their related targets and recipes where it makes sense. Variables listed in the `$(watch_vars)` list in `scripts/utils.mk` can be 'depended' on by other targets. Any change to the value of this variable will cause a rebuild of all depending targets.
```make
# Describe what defined functions do
#
# $1 - Message to echo
define echo
{ echo "$1" ; }
endef

# Variables added to the $(watch_vars) list in scripts/utils.mk can be 'depended' on.
my_out_folder.txt:  $(depend_MY_OUT_FOLDER)
        @echo $(MY_OUT_FOLDER) changed value! > $@
```
When using `$(shell ...)` consider how long the shell command will run for. When tab completing Make will run with `-n|--dry-run` which will parse the makefiles, and generate a list of possible targets. If the shell command is very slow it will freeze the tab completion until complete. Instead we have an alternate function `$(call shell_real_build_only, ...)` which will only run the command during an actual build.

Consider this especially for complex calls to `find` etc.
```make
# Consider replacing this:
local_specs = $(shell find $(SPECS_DIR)/ -type f -name '*.spec')
# With this:
local_specs = $(call shell_real_build_only, find $(SPECS_DIR)/ -type f -name '*.spec')
```