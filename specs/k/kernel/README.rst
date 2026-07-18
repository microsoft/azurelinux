============================
Azure Linux Kernel Component
============================

This directory contains the maintained local RPM spec and supporting sources
for the Azure Linux kernel component. The component builds the general-purpose
kernel for x86_64 and aarch64, kernel tools and selftests, and the NVIDIA open
GPU kernel module subpackages.

Source and configuration
========================

The kernel source comes from the Azure Linux ``rolling-lts/azl4`` branch of the
`CBL-Mariner-Linux-Kernel repository`_. ``kernel.comp.toml`` pins the source
archive and its hash. The architecture-specific Azure Linux configurations are
``6.18-x86_64-azl.config`` and ``6.18-aarch64-azl.config``.

``kernel.spec`` is the source of truth for packaging. Edit it directly rather
than editing the generated copy under ``specs/k/kernel/``. Supporting files in
this directory provide module signing, package inspection, gating, and the
NVIDIA open kernel module integration.

Release management
==================

The component uses manual release calculation. For a change that affects the
source RPM or binary RPMs:

* increment ``azl_pkgrelease`` in ``kernel.spec``;
* add a matching entry to the inline ``%changelog``;
* refresh ``locks/kernel.lock`` and ``specs/k/kernel/``.

Build and test
==============

Run all commands from the root of the `Azure Linux repository`_::

	azldev comp list -p kernel -q -O json
	azldev comp update -p kernel -q
	azldev comp render -p kernel -q
	azldev comp build -p kernel --preserve-buildenv on-failure -q

Inspect the rendered files before building. Test resulting RPMs in an Azure
Linux mock chroot; do not install them on the development host. See the
repository ``AGENTS.md`` and ``.github/skills/skill-mock/SKILL.md`` for the
required inspection and smoke-test workflow.

Keep packaging changes focused on Azure Linux requirements and avoid restoring
unused architecture or variant machinery inherited from other distributions.

.. _CBL-Mariner-Linux-Kernel repository: https://github.com/microsoft/CBL-Mariner-Linux-Kernel/tree/rolling-lts/azl4
.. _Azure Linux repository: https://github.com/microsoft/azurelinux
