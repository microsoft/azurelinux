#
# This include file contains metadata comments that get extracted at runtime
# to generate the command-line help for this Makefile (exposed via the 'help'
# target).
#
# Syntax:
# -------
# Help metadata comments are expected to be full-line '#' comments that start
# with the string "##help:" (without quotes). Following that prefix is a
# tag indicating the type of help metadata being defined. The format looks
# like this:
# 
#     ##help:TAG:CONTENT
#
# The format of the content differs by tag. Here are the main tags used:
#
#     ---------------------------------------------------------------------
#     target
#     ---------------------------------------------------------------------
#     Describes a Makefile target intended for direct use by consumers of
#     the toolkit. For consistency's sake, it recommended that the description
#     of the target be terminated by a period (.).
#
#     Format:
#         ##help:target:TARGET-NAME=DESCRIPTION-OF-TARGET
#
#     Example:
#         ##help:target:MY_TARGET=My target.
#
#     ---------------------------------------------------------------------
#     var
#     ---------------------------------------------------------------------
#     Describes a well-known variable that influences the Makefile and its
#     targets in a meaningful (and supported) way.
#
#     Format:
#         ##help:var:VAR-NAME:POSSIBLE-VALUES=DESCRIPTION-OF-VAR
#
#     For each variable, we document the possible values that it can take
#     on (if enumerable), or otherwise use a human-readable 'metavar' that
#     describes what the value should be.
#
#     Examples:
#         ##help:var:MY_ENUM:{a,b,c}=My enum var
#         ##help:var:MY_STRING:<path_to_relevant_thing>=Path to relevant thing
#
#     ---------------------------------------------------------------------
#     example
#     ---------------------------------------------------------------------
#     Describes general example usage for the Makefile.
#
#     Format:
#         ##help:example:EXAMPLE-TEXT-LINE-HERE
#
# There are also special metadata for the toplevel description included at
# the start of the help output, as well as items for the headings used before
# each section:
#
#     desc            - toplevel description
#     target-heading  - heading displayed before the list of targets
#     var-heading     - heading displayed before the list of variables
#     example-heading - heading displayed before the list of examples
# 
# The 'help' target in the toplevel Makefile is responsible for extracting these
# metadata comments, sorting them (where required), and rendering them into
# sensible-looking output.
#
# The remainder of this file includes some of the special tags described above.
#

#
# Top-level description.
#

##help:desc:[1mThis Makefile is the primary entry point for the Mariner Toolkit.[0m
##help:desc:
##help:desc:For full details, please consult the documentation under toolkit/docs.

#
# Headings.
#

##help:target-heading:
##help:target-heading:[4;95mTargets:[0m

##help:var-heading:
##help:var-heading:[4;95mVariables:[0m

##help:example-heading:
##help:example-heading:[4;95mExamples:[0m

#
# Examples.
#

##help:example:Build only my-package.spec and its requirements:
##help:example:    [3msudo make -j$(nproc) build-packages SRPM_PACK_LIST="my-package"[0m
##help:example:

##help:example:Force rebuild my-package.spec after having already built it:
##help:example:    [3msudo make -j$(nproc) build-packages SRPM_PACK_LIST="my-package" PACKAGE_REBUILD_LIST="my-package"[0m
##help:example:

##help:example:Build an image using a specific JSON config file:
##help:example:    [3msudo make -j$(nproc) image CONFIG_FILE=./imageconfigs/core-efi.json[0m
##help:example:
