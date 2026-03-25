# Makefile for vm-base kiwi image builds
#
# Used by Koji's --make-prep option to configure the build environment
# inside the mock chroot before kiwi-ng runs.
#
# For gen1 (BIOS) builds, the default /etc/kiwi.yml uses partx for
# partition mapping, which does not work with MBR/BIOS disk layouts.
# This target patches kiwi.yml to use kpartx instead.
#
# Usage:
#   koji kiwi-build --make-prep --kiwi-profile=gen1 <target> <scm> vm-base.kiwi

KIWI_CONF := /etc/kiwi.yml

prep:
	@echo "==> Patching $(KIWI_CONF) to use kpartx for partition mapping..."
	@if [ -f "$(KIWI_CONF)" ]; then \
		sed -i '/^#mapper:/s/^#//' "$(KIWI_CONF)"; \
		sed -i '/^#  - part_mapper:/s/^#//' "$(KIWI_CONF)"; \
		sed -i 's/^\(  - part_mapper:\).*/\1 kpartx/' "$(KIWI_CONF)"; \
		echo "==> $(KIWI_CONF) updated:"; \
		grep -A2 '^mapper:' "$(KIWI_CONF)" || true; \
	else \
		echo "==> $(KIWI_CONF) not found, creating minimal config..."; \
		printf 'mapper:\n  - part_mapper: kpartx\n' > "$(KIWI_CONF)"; \
	fi
	@echo "==> Done"
