# See https://docs.pagure.org/copr.copr/user_documentation.html#make-srpm

.DEFAULT_GOAL=srpm

# Directory of this very Makefile
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Provide defaults for variables overwritten by make-srpm in copr
outdir?=$(ROOT_DIR)/..
spec?=python-nanobind.spec

.PHONY: srpm
srpm:
	rpmbuild \
		--define "_srcrpmdir $(outdir)" \
		--define "_sourcedir $(shell pwd)" \
		--define "_disable_source_fetch 0" \
		-bs $(spec)
