========================
Azure Linux kernel package
========================

Azure Linux maintains this component as a local spec.  Edit ``kernel.spec`` and
the source files in this directory; do not edit the rendered files under
``specs/k/kernel/``.  Azure Linux-specific changes in the spec are marked with
``AZL:`` comments.

The local spec is a maintained fork of the Fedora 43 kernel dist-git spec at
commit ``5271a1b047ef402ddee40242e02eda23fc273044``.  Azure Linux originally
applied its changes as overlays to that snapshot, then vendored the rendered
result as a local spec in July 2026.  It does not automatically receive later
Fedora spec changes; review and port relevant Fedora changes deliberately.

The kernel source comes from the ``rolling-lts/azl4`` branch of the
`Azure Linux kernel repository`_.  ``kernel.comp.toml`` pins the source archive,
its SHA-512 checksum, the NVIDIA open kernel module archive, and the kABI
reference archives used while assembling the source package.  Because the
component uses ``replace-upstream = true``, ``base/comps/kernel/sources`` is
the matching upstream manifest and must list the same kernel archive filename
and checksum.

A kernel source version update must update the separate ``kernel-headers``
component at the same time; it builds headers from the same Azure Linux kernel
archive.  A same-version rebuild of the kernel (config, patch, or
``azl_pkgrelease`` bump) does not require touching ``kernel-headers`` unless
that change also affects its output.  The ``kernel-headers`` inputs live under
``base/comps/kernel-headers/``.

Version and release
===================

The package version is split across macros near the top of ``kernel.spec``:

* ``specrpmversion`` is the first three components, for example ``6.18.31``.
* ``kextraversion`` is the fourth component, for example ``1``.
* ``azl_pkgrelease`` is the Azure Linux rebuild counter.

Together these produce a release such as ``6.18.31-1.16.azl4``.  For a new
kernel source version, update ``specrpmversion`` and ``kextraversion`` and reset
``azl_pkgrelease`` to ``1``.  For a same-version packaging or configuration
change, increment only ``azl_pkgrelease``.  Add a matching entry at the top of
the hand-maintained ``%changelog``.

``kabiversion`` is independent of the kernel source version.  kABI checking is
currently disabled, but the spec still declares the two kABI archives.  Do not
bump it unless matching archives and checksums are available.  The NVIDIA open
module version is also an independent pin and does not need to change with every
kernel update.

Kernel configurations
=====================

The build uses the complete Azure Linux configurations:

* ``6.18-x86_64-azl.config``
* ``6.18-aarch64-azl.config``

During ``%prep``, the spec replaces the Fedora-generated configurations with
these files and runs ``process_configs.sh -w -n -c``.  This checks for changed,
invalid, and newly introduced options using Kconfig's ``olddefconfig`` and
``listnewconfig`` targets.  Resolve new options explicitly rather than silently
accepting defaults.  Keep the required-config policy under
``scripts/ci/kernel/kernel-config-checker/`` in sync when an intentional change
affects a protected option.

Update workflow
===============

The ``kernel-update`` agent skill (``.agents/skills/kernel-update/SKILL.md``)
is the authoritative checklist for source bumps, config-only rebuilds, lock
refreshes, and build/test validation.  Follow it end-to-end; the notes below
only summarize the component-specific pieces a maintainer should be aware of
before reading it.

Editable inputs live in this directory and in ``base/comps/kernel-headers/``:

* ``kernel.comp.toml`` — source pin (filename, URL, SHA-512), NVIDIA open and
  kABI archives, build defines.
* ``sources`` — local-spec upstream manifest; must list the same kernel
  archive as ``kernel.comp.toml`` because the component sets
  ``replace-upstream = true``.
* ``kernel.spec`` — version macros (``specrpmversion``, ``kextraversion``,
  ``azl_pkgrelease``), hand-maintained ``%changelog``.
* ``6.18-x86_64-azl.config`` and ``6.18-aarch64-azl.config`` — complete Azure
  Linux configurations validated with ``process_configs.sh -w -n -c``.
* ``base/comps/kernel-headers/kernel-headers.comp.toml`` and its overlays —
  coordinated with source version bumps only.

Generated outputs under ``specs/k/kernel/``, ``specs/k/kernel-headers/``,
``locks/kernel.lock``, and ``locks/kernel-headers.lock`` are produced by
``azldev comp render`` and ``azldev comp update`` — never edit them directly.

Mock chroots share the host kernel, so ``uname`` and ``modprobe`` inside mock
do not exercise the built kernel.  Boot an image or VM with the new RPMs for
functional kernel and driver testing.  The required-config policy under
``scripts/ci/kernel/kernel-config-checker/`` must stay in sync when an
intentional change affects a protected option.

.. _Azure Linux kernel repository: https://github.com/microsoft/CBL-Mariner-Linux-Kernel
