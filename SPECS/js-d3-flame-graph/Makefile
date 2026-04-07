VERSION := $(shell rpm --specfile *.spec --qf '%{VERSION}\n' | head -1)
RELEASE := $(shell rpm --specfile *.spec --qf '%{RELEASE}\n' | head -1 | cut -d. -f1)

NAME       := d3-flame-graph
RPM_NAME   := js-$(NAME)
SOURCE_DIR := $(NAME)-$(VERSION)
SOURCE_TAR := $(NAME)-$(VERSION).tar.gz
VENDOR_TAR := $(RPM_NAME)-vendor-$(VERSION)-$(RELEASE).tar.xz

ALL_PATCHES     := $(sort $(wildcard *.patch))
VENDOR_PATCHES  := $(sort $(wildcard *.vendor.patch))
COND_PATCHES    := $(sort $(wildcard *.cond.patch))
REGULAR_PATCHES := $(filter-out $(VENDOR_PATCHES) $(COND_PATCHES),$(ALL_PATCHES))

all: $(SOURCE_TAR) $(VENDOR_TAR)

$(SOURCE_TAR):
	spectool -g $(RPM_NAME).spec

$(VENDOR_TAR): $(SOURCE_TAR)
	rm -rf $(SOURCE_DIR)
	tar xf $(SOURCE_TAR)

	# Patches to apply before vendoring
	for patch in $(REGULAR_PATCHES); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Node.js
	cd $(SOURCE_DIR) && yarn import && yarn install --pure-lockfile
	./list_bundled_nodejs_packages.py $(SOURCE_DIR) >> $@.manifest

	# Patches to apply after vendoring
	for patch in $(VENDOR_PATCHES); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Create tarball
	XZ_OPT=-9 time -p tar cJf $@ \
		$(SOURCE_DIR)/node_modules

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm $(NAME)-*/
