.DEFAULT_GOAL=help

# See ~/.config/mock/<CONFIG>.cfg or /etc/mock/<CONFIG>.cfg
# Tweak this to centos-stream-9-x86_64 to build for CentOS
MOCK_CHROOT?=fedora-41-x86_64
MOCK_OPTS?=
MOCK_OPTS_DEFAULT?=--no-clean --no-cleanup-after $(MOCK_OPTS)
YYYYMMDD=$(shell date +%Y%m%d)
SOURCEDIR=$(shell pwd)
SPEC=python-nanobind.spec
# When nothing is given, this will be automatically determined
SRPM_PATH?=

######### Get sources

.PHONY: get-sources
## Downloads all sources we need for a build.
get-sources:
	fedpkg sources

######### Build SRPM

.PHONY: srpm
## Builds an SRPM that can be used for a build.
srpm:
	fedpkg srpm

######### Scrub mock chroot and cache

.PHONY: scrub-chroot
## Completely remove the fedora chroot and cache.
scrub-chroot:
	mock -r $(MOCK_CHROOT) --scrub all

######### Do a mock build

.PHONY: mockbuild
## Start a mock build of the SRPM.
mockbuild: srpm get-srpm
	mock -r $(MOCK_CHROOT) $(MOCK_OPTS_DEFAULT) $(srpm_path)

######### Edit-last-failing-script

.PHONY: get-last-run-script
## Get the file that was last modified in /var/tmp/ within the chroot.
get-last-run-script:
	$(eval last_run_script:=/var/tmp/$(shell ls -t1 /var/lib/mock/$(MOCK_CHROOT)/root/var/tmp | head -n1))
	$(info last_run_script=$(last_run_script))
	@echo > /dev/null

.PHONY: edit-last-failing-script
## Opens the last failing or running script from mock in your editor
## of choice for you to edit it and later re-run it in mock with:
## "make mockbuild-rerun-last-script".
edit-last-failing-script: get-last-run-script
	$$EDITOR /var/lib/mock/$(MOCK_CHROOT)/root$(last_run_script)

######### Re-run the last failing script from mock

.PHONY: mockbuild-rerun-last-script
## Re-runs the last failing or running script of your mock mockbuild.
mockbuild-rerun-last-script: get-last-run-script
	mock --root=$(MOCK_CHROOT) --shell 'sh -e $(last_run_script)'

.PHONY: help
# Based on https://gist.github.com/rcmachado/af3db315e31383502660
## Display this help text.
help:/
	$(info Available targets)
	$(info -----------------)
	@awk '/^[a-zA-Z\-0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		helpCommand = substr($$1, 0, index($$1, ":")-1); \
		if (helpMessage) { \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			gsub(/##/, "\n                                       ", helpMessage); \
		} else { \
			helpMessage = "(No documentation)"; \
		} \
		printf "%-37s - %s\n", helpCommand, helpMessage; \
		lastLine = "" \
	} \
	{ hasComment = match(lastLine, /^## (.*)/); \
          if(hasComment) { \
            lastLine=lastLine$$0; \
	  } \
          else { \
	    lastLine = $$0 \
          } \
        }' $(MAKEFILE_LIST)

######### Version/Release helper targets to build name of SRPM

.PHONY: get-version
## Determines the nanobind version given in the python-nanobind.spec file.
get-version:
	$(eval version:=$(shell grep -ioP '^Version:\s*\K[^\s]+' $(SPEC)))
	$(info Version: $(version))
	@echo > /dev/null

.PHONY: get-release
## Parses the spec file for the Release: tag
get-release:
	$(eval release:=$(shell rpmautospec calculate-release $(SPEC) | cut -d ':' -f2 | tr -d -c [:digit:]))
	$(info Release: $(release))
	@echo > /dev/null

.PHONY: get-srpm
## Determines the name of the SRPM used for release builds
## Can be overriden by giving "make ... SRPM_PATH=foo.src.rpm".
get-srpm: get-version get-release
	$(eval srpm_path:=python-nanobind-${version}-${release}*.src.rpm)
	$(info SRPM Release: $(srpm_path))
	@echo > /dev/null
