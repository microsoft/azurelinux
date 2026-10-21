## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/uv.azl.macros}

%bcond check 1
# Should we run tests that require specific Python interpreter versions
# (major.minor, not major.minor.patch)? This adds a few dozen tests, but adds
# BuildRequires on more Python interpreters (which aren’t available in EPEL).
%bcond other_python_versions %{undefined epel}

Name:           uv
Version:        0.12.19
# The uv package has a permanent exception to the Updates Policy in Fedora, so
# it can be updated in stable releases across SemVer boundaries (subject to
# good judgement and actual compatibility of any reverse dependencies). See
# https://docs.fedoraproject.org/en-US/fesco/Updates_Policy/#_other_packages,
# https://pagure.io/fesco/issue/3262. It also has a corresponding exception in
# EPEL, but only in leading branches and only until version 1.0; see
# https://pagure.io/epel/issue/317.
Release:        %autorelease
Summary:        An extremely fast Python package installer and resolver, written in Rust

# The license of the uv project is (MIT OR Apache-2.0), except:
#
# Apache-2.0:
#   - crates/uv-python/src/libc.rs contains code derived from
#     crate(glibc_version)
#   - crates/uv-requirements-txt/src/shquote.rs contains code derived from
#     crate(r-shquote); the original code was (Apache-2.0 OR
#     LGPL-2.1-or-later), but the vendored copy cites only the Apache-2.0
#     option.
#   - crates/uv-build-frontend/src/pipreqs/mappings is a data file taken from
#     https://pypi.org/project/pipreqs, https://github.com/bndr/pipreqs
#
# Apache-2.0 OR BSD-2-Clause:
#   - crates/uv-pep440/ is vendored and forked from crate(pep440_rs)
#   - crates/uv-pep508/ is vendored and forked from crate(pep508_rs)
#   - crates/uv-python/packaging/ is vendored and forked from
#     python3dist(packaging)
#
# (Apache-2.0 OR MIT) AND BSD-3-Clause:
#   - The function wheel_metadata_from_remote_zip in
#     crates/uv-client/src/remote_metadata.rs is vendored and forked from the
#     function lazy_read_wheel_metadata in src/index/lazy_metadata.rs in
#     crate(rattler_installs_packages) and is BSD-3-Clause AND (Apache-2.0 OR
#     MIT): the original routine is BSD-3-Clause, and subsequent modifications
#     are explicitly (Apache-2.0 OR MIT).
#
# MIT
#   - crates/uv-virtualenv/src/activator/ is vendored and forked from
#     python3dist(virtualenv)
#   - crates/uv-netrc/ is vendored from crate(rust-netrc)
#
# Additionally, the following are bundled/forked but happen to be under the
# same (Apache-2.0 OR MIT) terms as uv itself:
#   - crates/uv-extract/src/vendor/cloneable_seekable_reader.rs is vendored and
#     forked from crate(ripunzip)
#
# The following are present in the source but believed not to contribute to the
# licenses of the binary RPMs. Note that test/ecosystem/ contains only
# pyproject.toml files used for testing, not complete bundled projects.
#
# Apache-2.0:
#   - test/ecosystem/airflow/
#   - test/ecosystem/home-assistant-core/
#   - test/ecosystem/transformers/
#   - test/ecosystem/warehouse/
# Apache-2.0 OR MIT:
#   - test/ecosystem/packse/
# BSD-2-Clause-Patent:
#   - test/ecosystem/github-wikidata-bot/
# BSD-3-Clause:
#   - test/ecosystem/jupyterlab/
#   - test/ecosystem/pandas/
#   - test/ecosystem/saleor/
# MIT:
#   - crates/uv-python/fetch-download-metadata.py is derived from
#     https://github.com/mitsuhiko/rye/tree/f9822267a7f00332d15be8551f89a212e7bc9017
#     which was MIT.
#   - test/ecosystem/black/
#   - test/ecosystem/poetry/
#   - test/ecosystem/semantic-kernel/
#
# Rust crates compiled into the executable contribute additional license terms.
# To obtain the following list of licenses, build the package and note the
# output of %%{cargo_license_summary}.
#
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Apache-2.0 AND CC0-1.0
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 AND ISC AND (MIT OR Apache-2.0)
# Apache-2.0 OR Apache-2.0 WITH LLVM-exception
# Apache-2.0 OR BSD-2-Clause
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR ISC OR MIT
# Apache-2.0 OR MIT
# Apache-2.0 OR MIT OR Zlib
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSD-3-Clause
# CDLA-Permissive-2.0
# ISC
# LGPL-3.0-or-later OR MPL-2.0
# MIT
# MIT AND (MIT OR Apache-2.0)
# MIT OR Apache-2.0
# MIT OR LGPL-3.0-or-later
# MIT OR Zlib OR Apache-2.0
# MIT-0
# MIT-0 OR Apache-2.0
# MPL-2.0
# Unicode-3.0
# Unlicense OR MIT
# Zlib
License:        %{shrink:
    0BSD AND
    (0BSD OR Apache-2.0 OR MIT) AND
    Apache-2.0 AND
    (Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT) AND
    (Apache-2.0 OR Apache-2.0 WITH LLVM-exception) AND
    (Apache-2.0 OR BSD-2-Clause) AND
    (Apache-2.0 OR BSD-2-Clause OR MIT) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR ISC OR MIT) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 OR MIT OR Zlib) AND
    (Apache-2.0 OR MIT-0) AND
    (Apache-2.0 WITH LLVM-exception) AND
    BSD-3-Clause AND
    CC0-1.0 AND
    CDLA-Permissive-2.0 AND
    ISC AND
    (LGPL-3.0-or-later OR MIT) AND
    (LGPL-3.0-or-later OR MPL-2.0) AND
    MIT AND
    MIT-0 AND
    (MIT OR Unlicense) AND
    MPL-2.0 AND
    Unicode-3.0 AND
    Unicode-DFS-2016 AND
    Zlib
    }
# LICENSE.dependencies contains a full license breakdown
URL:            https://github.com/astral-sh/uv
Source0:        %{url}/archive/%{version}/uv-%{version}.tar.gz
# Default system-wide configuration file
# https://docs.astral.sh/uv/configuration/files
Source1:        uv.toml
Source9999: uv.azl.macros

# Downstream: Always find the system-wide uv executable
# See discussion in “Should uv.find_uv_bin() be able to find /usr/bin/uv?”
# https://github.com/astral-sh/uv/issues/4451
Patch:          0001-Downstream-Always-find-the-system-wide-uv-executable.patch
# Downstream: Revert source-code changes for pre-release blake2
# Revert source changes from “Upgrade BLAKE2 to unify hashing digest versions”,
# https://github.com/astral-sh/uv/pull/20834. We do not wish to upgrade
# rust-blake2 to a pre-release.
Patch:          0002-Downstream-Revert-source-code-changes-for-pre-releas.patch
# Downstream: Avoid embed-manifest dependency in uv crate build script
# The embed-manifest dependency only does something useful when (cross-?)
# compiling for Windows.
Patch:          0003-Downstream-Avoid-embed-manifest-dependency-in-uv-cra.patch

# Add license texts for new contents of test/ecosystem/ from PR#20068
# https://github.com/astral-sh/uv/pull/20174
Patch:          %{url}/pull/20174.patch

BuildSystem:    pyproject
BuildOption(install): --assert-license uv

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# On some releases and architectures, Koji builders sometimes or always run out
# of memory in the final linking step. This cannot be fixed by adding
# "-C link-args=-Wl,--no-keep-memory" to the RUSTFLAGS (as that seems to have
# no significant effect on memory requirements), nor can it be fixed by
# reducing parallelism (although we do need this as well), since nothing else
# is happening at that point in the build. See:
# https://doc.rust-lang.org/rustc/codegen-options/index.html#debuginfo
%global rustflags_debuginfo 1

# As a separate limitation, memory exhaustion (OOM) can occur during parallel
# portions of the build.
# - Because very many workspace crates can be built in parallel, builders with
#   a very large number of CPUs may OOM. Typical workspace crates peak out at
#   roughly 2–4 GB per rustc process.
# - The uv crate needs much more memory to compile and link, at least 8 GB, and
#   when building the tests we may be building bin and lib versions at the same
#   time, along with the it (integration test) crate, which is also rather
#   large. This is a problem for “low memory” builders (<20 GB or so).
# Unfortunately, this means that we need to scale the memory per task based on
# the memory requirements of the top-level uv crate in order to avoid OOM on
# all kinds of builders.
%global _smp_tasksize_proc 10240

# Compilation may fail on builders with very many cores (e.g. 192 cores) due to
# “too many open files.” Try to keep the files/core ratio from getting too low.
%global _smp_ncpus_max 48

BuildRequires:  cargo-rpm-macros
BuildRequires:  rust2rpm-helper
BuildRequires:  tomcli
%if %{with check} && %{with other_python_versions}
# See trove classifiers in pyproject.toml for supported Pythons.
BuildRequires:  /usr/bin/python3.9
BuildRequires:  /usr/bin/python3.10
BuildRequires:  /usr/bin/python3.11
BuildRequires:  /usr/bin/python3.12
BuildRequires:  /usr/bin/python3.13
BuildRequires:  /usr/bin/python3.13t
BuildRequires:  /usr/bin/python3.14
BuildRequires:  /usr/bin/python3.14t
BuildRequires:  /usr/bin/python3.15
BuildRequires:  /usr/bin/python3.15t
%endif

# In https://github.com/astral-sh/uv/issues/5588#issuecomment-2257823242,
# upstream writes “These have diverged significantly and the upstream versions
# are only passively maintained, uv requires these custom versions and can't
# use a system copy.”
#
# crates/uv-pep440/
# Version number from crates/uv-pep440/CHANGELOG.md; it was also in
# crates/uv-pep440/Cargo.toml until uv 0.9.11, when internal crates started
# being versioned and published on crates.io.
Provides:       bundled(crate(pep440_rs)) = 0.7.0
# crates/uv-pep508/
# Version number from crates/uv-pep508/Changelog.md; it was also in
# crates/uv-pep508/Cargo.toml until uv 0.9.11, when internal crates started
# being versioned and published on crates.io, but the version in Cargo.toml was
# 0.6.0. The source reflects upstream changes in 0.7.0.
Provides:       bundled(crate(pep508_rs)) = 0.7.0
# crates/uv-virtualenv/
# As a whole, this crate is derived from https://github.com/konstin/gourgeist
# 0.0.4, which was published as https://crates.io/crates/gourgeist. It looks
# like the project was subsumed into `uv`, and the link to `uv` at
# https://konstin.github.io/gourgeist/ (“See
# https://github.com/astral-sh/uv/tree/main/crates/uv-virtualenv for the up to
# date version”) supports this. We therefore consider this not to be a real
# case of bundling, since the source in uv is now the canonical one, and we do
# not add:
#   Provides:       bundled(crate(gourgeist)) = 0.0.4

# crates/uv-extract/src/vendor/cloneable_seekable_reader.rs
# Version number is an educated guess based on comparison of file contents,
# cross-checked with timing: the file was first introduced to uv as
# crates/puffin-installer/src/vendor/cloneable_seekable_reader.rs in
# https://github.com/astral-sh/uv/commit/2a846e76b7725633776fd08e04ce8b827bb0580f
# on 2023-10-08, and 0.4.0 was the current release of ripunzip at that time.
Provides:       bundled(crate(ripunzip)) = 0.4.0
# wheel_metadata_from_remote_zip only, in
# crates/uv-client/src/remote_metadata.rs
# Version number is, at the time of this writing, the only release of
# https://github.com/prefix-dev/rip containing the corresponding function
# lazy_read_wheel_metadata in
# (crates/rattler_installs_packages/)src/index/lazy_metadata.rs.
Provides:       bundled(crate(rattler_installs_packages)) = 0.9.0

# crates/uv-python/src/libc.rs
# This is at least partially derived (with changes) from the glibc_version
# crate, https://github.com/delta-incubator/glibc-version-rs. The last commit
# that we can match up with the file in uv is
# 5e1002dc7a3c39c0d72631cc488bef2fc5fea0fb, although it would be equally
# correct to reference any of several slightly later commits.
Provides:       bundled(crate(glibc_version)) = 0.1.2^20221117git5e1002d

# crates/uv-requirements-txt/src/shquote.rs
# The unquote implementation is vendored from the r-shquote crate because it is
# unmaintained upstream, https://github.com/astral-sh/uv/issues/11780.
Provides:       bundled(crate(r-shquote)) = 0.1.1

# crates/uv-keyring
# From crates/uv-keyring/README.md, “This is vendored from [keyring-rs
# crate](https://github.com/open-source-cooperative/keyring-rs)
# commit 9635a2f53a19eb7f188cdc4e38982dcb19caee00.” The commit message of the
# referenced upstream commit indicates it corresponds to 4.0.0-rc2.
#
# The text of https://github.com/astral-sh/uv/pull/14725 explains the differing
# design goals and tradeoffs that lead uv to fork keyring-rs rather than using
# the upstream https://crates.io/crates/keyring crate or trying to get the
# necessary changes merged upstream. Based on this explanation, there does not
# appear to be any prospect of unbundling.
Provides:       bundled(crate(keyring)) = 4.0.0~rc2

# crates/uv-netrc
# From crates/uv-netrc/README.md, “This crate vendors the rust-netrc parser for
# use by uv. The source was vendored from gribouille/netrc, as published in
# rust-netrc 0.1.2[…]”
#
# Upstream justifies the bundling in
# https://github.com/astral-sh/uv/pull/19409: they want unreleased bug fixes,
# including those pertaining to https://github.com/astral-sh/uv/issues/16083,
# and to avoid a dependency on thiserror v1. In response to the mandatory
# query, they report they are open to de-vendoring if a new rust-netrc release
# with the desired changes appears.
Provides:       bundled(crate(rust-netrc)) = 0.1.2

# The contents of crates/uv-virtualenv/src/activator/ are a bundled and
# slightly forked copy of a subset of https://pypi.org/project/virtualenv; see
# https://github.com/pypa/virtualenv/tree/main/src/virtualenv/activation.
#
# The same justification for not attempting to unbundle downstream applies as
# for the bundling from python3dist(packaging), below; additionally, some of
# the scripts have been forked. See also:
#   https://github.com/astral-sh/uv/issues/5588#issuecomment-2257474140
#
# The scripts were last updated from virtualenv upstream in
# https://github.com/astral-sh/uv/pull/15272 on 2025-09-05. The PR was opened
# on 2025-08-14 and last revised on 2025-08-30; the latest virtualenv release
# throughout that time interval was 20.34.0.
Provides:       bundled(python3dist(virtualenv)) = 20.34

# The contents of crates/uv-python/python/packaging/ are a bundled copy of a
# subset of https://pypi.org/project/packaging.
#
# This was added in
# https://github.com/astral-sh/uv/commit/7964bfbb2bed50a5c7b0650a7b6799a66503a33a,
# the commit message of which helps explain the rationale. In part:
#
#   The architecture of uv does not necessarily match that of the python
#   interpreter. In cross compiling/testing scenarios the operating system can
#   also mismatch. To solve this, we move arch and os detection to python,
#   vendoring the relevant pypa/packaging code, preventing mismatches between
#   what the python interpreter was compiled for and what uv was compiled for.
#
# We cannot use the system package directly because these Python sources are
# compiled into the uv executable, and the binary package does not even depend
# on the system Python interpreter. Patching uv to read the sources from the
# system package at runtime would be much too extreme for a downstream change.
# Copying sources from the system package into the build tree is feasible, but
# – especially considering that the sources are not necessarily executed with
# the system Python interpreter – the risks of deviating from upstream’s tested
# sources would seem to greatly outweigh any possible benefits of such
# “build-time unbundling.” We therefore consider this instance of bundling
# technically necessary. See also:
#   https://github.com/astral-sh/uv/issues/5588#issuecomment-2257474140
#
# README.md has the bundled commit hash, __init__.py has the version number,
# and https://github.com/pypa/packaging/tree/${commit} is the source of the
# snapshot date.
Provides:       bundled(python3dist(packaging)) = 24.1~dev0^20240310gitcc938f9

# The contents of crates/uv-build-frontend/src/pipreqs/mapping are copied from
# https://pypi.org/project/pipreqs. Since this is just a data file, since uv
# does not take Python dependencies, and since pipreqs is not currently
# actively maintained anyway, there is no reasonable prospect of unbundling.
# The version number is just that of the latest pipreqs release at the time the
# data file was vendored.
Provides:       bundled(python3dist(pipreqs)) = 0.5.0

%global common_description %{expand:
An extremely fast Python package and project manager, written in Rust.

Highlights:

  • A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine,
    virtualenv, and more.
  • 10-100x faster than pip.
  • Provides comprehensive project management, with a universal lockfile.
  • Runs scripts, with support for inline dependency metadata.
  • Installs and manages Python versions.
  • Runs and installs tools published as Python packages.
  • Includes a pip-compatible interface for a performance boost with a familiar
    CLI.
  • Supports Cargo-style workspaces for scalable projects.
  • Disk-space efficient, with a global cache for dependency deduplication.}

BuildRequires: /usr/bin/python3.12
%description %{common_description}


%package -n python3-uv
Summary:        Importable Python module for uv

BuildArch:      noarch

Requires:       uv = %{version}-%{release}

%description -n python3-uv %{common_description}

This package provides an importable Python module for uv.


%prep -a
# Collect license files of vendored dependencies
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/packaging \
    crates/uv-python/python/packaging/LICENSE.*
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/pep440_rs crates/uv-pep440/License-*
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/pep508_rs crates/uv-pep508/License-*
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/pipreqs \
    crates/uv-build-frontend/src/pipreqs/LICENSE
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/ripunzip crates/uv-extract/src/vendor/LICENSE
install -D --preserve-timestamps --mode=0644 \
    --target=LICENSE.bundled/rust-netrc crates/uv-netrc/LICENSE
# The original license text from rattler_installs_packages is present in a
# comment, but we want it in a separate file so we can ensure it is present in
# the binary RPM.
install --directory LICENSE.bundled/rattler_installs_packages
awk '$2 == "BSD" { out=1 }; $2 == "```" { out=0 }; out' \
    crates/uv-client/src/remote_metadata.rs |
  sed --regexp-extended 's@^///( |$)@@' |
  tee LICENSE.bundled/rattler_installs_packages/LICENSE
# Similarly for virtualenv. All files in
# crates/uv-virtualenv/src/activator/activate/ have the same license text.
install --directory LICENSE.bundled/virtualenv
awk '$1 == "#" { out=1 }; $1 != "#" { out=0; exit }; out' \
    crates/uv-virtualenv/src/activator/activate |
  sed --regexp-extended 's@^#( |$)@@' |
  tee LICENSE.bundled/virtualenv/LICENSE

# Patch out foreign (e.g. Windows-only) dependencies. Follow symbolic links so
# that we also patch the bundled crates we just finished setting up.
find -L . -type f -name Cargo.toml -print \
    -execdir rust2rpm-helper strip-foreign -o '{}' '{}' ';'

# The uv-trampoline crate (a fork of posy trampolines, from
# https://github.com/njsmith/posy) uses a set of trampoline Windows executables
# for launching Python scripts. These precompiled executables are funished by
# the uv-trampoline-builder crate. We must remove them to prove they are not
# used in the build. Since they are used only on Windows, nothing is lost by
# doing so.
rm --verbose crates/uv-trampoline-builder/trampolines/*.exe
# Per Cargo.toml, uv-trampoline is excluded from the workspace and not compiled
# because it still requires a nightly compiler. For now, we remove it entirely
# to show that we do not need to document bundling from posy. Note that we
# *cannot* cleanly remove uv-trampoline-builder, only the precompiled
# trampolines themselves.
rm --recursive --verbose crates/uv-trampoline

# Remove the dependency on embed-manifest, which applies only when (cross-?)
# compiling for Windows. This requires an accompanying source-code patch for
# the uv crate’s build script.
tomcli set Cargo.toml del workspace.dependencies.embed-manifest
tomcli set crates/uv/Cargo.toml del build-dependencies.embed-manifest
# The embed-manifest depenency is also used in uv-trampoline, which we removed.

# Do not strip the compiled executable; we need useful debuginfo. Upstream set
# this intentionally, so this change makes sense to keep downstream-only.
tomcli set pyproject.toml false tool.maturin.strip
tomcli set Cargo.toml false profile.release.strip

# Exclude the bench crate from the workspace. We don’t need to build and run
# benchmarks, and it brings in unwanted additional dev dependencies.
tomcli set Cargo.toml append workspace.exclude crates/uv-bench
# The uv-dev crate provides “development utilities for uv,” which should not be
# needed here. It also brings extra dependencies that we would prefer to avoid.
tomcli set Cargo.toml append workspace.exclude crates/uv-dev

# Disable several default features that control which tests are compiled and
# executed, and which are not usable in offline builds:
#
# - test-crates-io: Introduces a testing dependency on crates.io.
# - test-git: Introduces a testing dependency on Git. This sounds innocuous –
#   we have git! – but in fact, it controls tests of git dependencies, which
#   implies accessing remote repositories, e.g. on GitHub.
# - test-git-lfs: as for git, but also require Git Large File Storage; again,
#   this implies accessing remote repositories
# - test-pypi: Introduces a testing dependency on PyPI.
# - test-python-managed: Introduces a testing dependency on managed Python
#   installations. (These are pre-compiled Pythons downloaded from the
#   Internet.)
# - test-r2: Introduces a testing dependency on R2.
#
# These are OK:
# - test-python: Introduces a testing dependency on a local Python installation.
# - test-slow: Include "slow" test cases.
# - test-ecosystem: Includes test cases that require ecosystem packages
#
# Note that the python-patch feature, which ”introduces a dependency on a local
# Python installation with specific patch versions,” is already not among the
# default features.
tomcli set crates/uv/Cargo.toml lists delitem features.test-defaults \
    'test-(crates-io|git(-lfs)?|pypi|python-managed|r2)'
# - -test-osv: Introduces a testing dependency on osv.dev.
tomcli set crates/uv-audit/Cargo.toml lists delitem features.default \
    'test-(osv)'

%if %{without other_python_versions}
# Many of these tests require specific Python versions (major.minor, not
# major.minor.patch, unless the python-patch feature is enabled). Manually
# selecting the tests in these modules that would succeed with just the system
# Python would be far too tedious.
omit_modules() {
  set -o nounset
  set -o errexit
  main_module="${1}"
  commented_modules=''
  comment='Downstream-only: skip, needs specific Python interpreter versions'
  shift
  while [ "${#}" != 0 ]
  do
    commented_modules="${commented_modules-}${commented_modules+|}${1}"
    shift
  done
  sed --regexp-extended --in-place \
      "s@mod (${commented_modules});@// ${comment}\n#[cfg(any())]\n&@" \
      "${main_module}"
}
# -p uv --test build
omit_modules crates/uv/tests/build/main.rs build_backend
# -p uv --test it:
omit_modules crates/uv/tests/it/main.rs \
    auth branching_urls network upgrade version
# -p uv --test python:
omit_modules crates/uv/tests/python/main.rs \
    'python_(dir|find|install|list|pin)' venv
# -p uv --test workspace:
omit_modules crates/uv/tests/workspace/main.rs \
    workspace 'workspace_(dir|list|metadata)'
# -p uv --test pip:
omit_modules crates/uv/tests/pip/main.rs \
    'pip_(debug|list|show|tree|uninstall)'
%endif

# For unclear reasons, maturin checks for the presence of optional crate
# dependencies that correspond to features we have not enabled. We need to
# patch out those that are not packaged, an unfortunate but straightforward
# hack. See further commentary in %%generate_buildrequires.
tomcli set crates/uv/Cargo.toml del dependencies.axoupdater
tomcli set crates/uv/Cargo.toml del features.self-update
tomcli set crates/uv/Cargo.toml del features.tracing-durations-export
tomcli set crates/uv/Cargo.toml del dependencies.tracing-durations-export

# Reproduce the patch we carry in the rust-rustls package:
# - default to the ring crypto backend
# - drop support for the aws-lc-rs crypto backend
tomcli set Cargo.toml lists delitem workspace.dependencies.rustls.features \
    '(aws_lc_rs|prefer-post-quantum)'
tomcli set Cargo.toml append workspace.dependencies.rustls.features ring

# We retain the following example even when there are currently no dependencies
# that need to be adjusted.
#
# # foocrate
# #   wanted: 0.2.0
# #   currently packaged: 0.1.2
# #   https://bugzilla.redhat.com/show_bug.cgi?id=1234567
# tomcli set Cargo.toml str workspace.dependencies.foocrate.version 0.1.2

# tikv-jemallocator
#   wanted: 0.6.0
#   currently packaged: 0.7.0
#   https://github.com/astral-sh/uv/pull/19735
# We use sed instead of tomcli because the target.cfg(…) expression is a
# *mess*, and we don’t want to have to write it out here.
sed --regexp-extended --in-place \
    's/^(tikv-jemallocator\b.*version = ")0\.6\.0"/\1>=0.6.0, <0.8.0"/' \
    crates/uv-performance-memory-allocator/Cargo.toml

# blake2
#   wanted: 0.11.0-rc.6
#   currently packaged: 0.10.6
# Downstream-only: revert “Upgrade BLAKE2 to unify hashing digest versions”,
# https://github.com/astral-sh/uv/pull/20834. We do not wish to upgrade
# rust-blake2 to a pre-release. There is an anccompanying source-code patch.
tomcli set Cargo.toml str workspace.dependencies.blake2.version 0.10.6

%cargo_prep


%generate_buildrequires -p
# For unclear reasons, maturin checks for all crate dependencies when it is
# invoked as part of %%pyproject_buildrequires – including those corresponding
# to optional features.
#
# Furthermore, if we do not supply -a to %%cargo_generate_buildrequires, then
# maturin will fail looking for crates like pyo3 (and will still look for
# optional crate dependencies).
#
# Since maturin always checks for dev-dependencies, we need -t so that they are
# generated even when the “check” bcond is disabled.
%cargo_generate_buildrequires -a -t


%build -a
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies


%install -a
if [ '%{python3_sitearch}' != '%{python3_sitelib}' ]
then
  # Maturin is really designed to build compiled Python extensions, but (when
  # the uv executable is not bundled in the Python package) the uv Python
  # library is actually pure-Python, and the python3-uv subpackage can be
  # noarch. We can’t tell maturin to install to the appropriate site-packages
  # directory, but we can fix the installation path manually.
  install --directory %{buildroot}%{python3_sitelib}
  mv %{buildroot}%{python3_sitearch}/uv* %{buildroot}%{python3_sitelib}
  sed --regexp-extended --in-place \
      's@%{python3_sitearch}@%{python3_sitelib}@' %{pyproject_files}
fi

# generate and install shell completions
for cmd in uv uvx
do
  target/rpm/${cmd} --generate-shell-completion bash > ${cmd}.bash
  target/rpm/${cmd} --generate-shell-completion fish > ${cmd}.fish
  target/rpm/${cmd} --generate-shell-completion zsh > _${cmd}

  install -Dpm 0644 ${cmd}.bash -t %{buildroot}/%{bash_completions_dir}
  install -Dpm 0644 ${cmd}.fish -t %{buildroot}/%{fish_completions_dir}
  install -Dpm 0644 _${cmd} -t %{buildroot}/%{zsh_completions_dir}
done

# Install a default system-wide configuration file
install -D --preserve-timestamps --mode=0644 \
    --target='%{buildroot}%{_sysconfdir}/uv' '%{SOURCE1}'


%check -a
%if %{with check}
# These tests rely on debug assertions, and fail when tests are compiled in
# release mode:
#
# cargo test -p uv-auth --lib:
skip="${skip-} --skip keyring::tests::fetch_url_no_host"
skip="${skip-} --skip keyring::tests::fetch_url_with_empty_username"
skip="${skip-} --skip keyring::tests::fetch_url_with_no_username"
skip="${skip-} --skip keyring::tests::fetch_url_with_password"

%if %{without other_python_versions}
# These tests require specific Python interpreter versions, which upstream
# normally downloads, precompiled, into the build area.
skip="${skip-} --skip version::self_version"
skip="${skip-} --skip version::self_version_json"
skip="${skip-} --skip version::self_version_short"
%endif

%ifnarch %{x86_64} %{arm64}
# On other architectures, the list of available downloads differs, e.g. pypy
# and graalpy downloads may be missing.
skip="${skip-} --skip python_list::python_list_downloads"
# Similarly, version numbers may not match exactly.
skip="${skip-} --skip python_list::python_list_with_mirrors"
%endif
%ifarch %{power64}
# The error message lacks the expected hint:
#   hint: A managed Python download is available for PyPy, but Python downloads
#   are set to 'never'
# This might be worth reporting upstream, but is not a serious issue.
skip="${skip-} --skip python_pin::python_pin_resolve"
%endif
%ifarch riscv64
# These expect managed interpreters of the form
# cpython-3.##-linux-riscv64gc-any, but crates/uv-python/download-metadata.json
# only has them for cpython-3.##-linux-riscv64-gnu. It’s not weird to find
# holes in the managed interpreter support matrix for less common
# architectures.
skip="${skip-} --skip python_find::python_find"
skip="${skip-} --skip python_list::python_list"
skip="${skip-} --skip python_pin::python_pin_resolve"
%endif

# It’s not clear what causes the trivial discrepancy, but we find that this
# fails when building in qemu-user-static emulated chroots.
#    4       │-  Caused by: Failed to query Python interpreter at `[TEMP_DIR]/bar`
#    5       │-  Caused by: [PERMISSION DENIED]
#          4 │+  Caused by: Querying Python at `[TEMP_DIR]/bar` failed with
#                exit status exit status: 127
skip="${skip-} --skip python_find::python_find_path"

# Test registry_client::tests::test_redirect_to_server_with_credentials is
# flaky
# https://github.com/astral-sh/uv/issues/16447
skip="${skip-} --skip registry_client::tests::test_redirect_to_server_with_credentials"

# This requires specific Python interpreter versions (so it would be grouped
# with the conditionalized integration tests above), but it also requires
# network access to PyPI, so it must be skipped either way until it can be
# appropriately conditionalized upstream; see
# https://github.com/astral-sh/uv/pull/13699#issuecomment-2916115588.
skip="${skip-} --skip remote_metadata::remote_metadata_with_and_without_cache"

# Upstream is trying to ensure platform-independent byte-for-byte deterministic
# wheels. This isn’t quite working out. It would be nice to understand this,
# but this kind of reproducibility can be brittle, and there are many possible
# innocuous reasons behind it.
# ---- tests::built_by_uv_building stdout ----
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Snapshot Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Snapshot: built_by_uv_building-4
# Source: crates/uv-build-backend/src/lib.rs:652
# ────────────────────────────────────────────────────────────────────────────────
# Expression: format!("{:x}", sha2::Sha256::digest(fs_err::read(&wheel_path).unwrap()))
# ────────────────────────────────────────────────────────────────────────────────
# -old snapshot
# +new results
# ────────────┬───────────────────────────────────────────────────────────────────
#     1       │-319afb04e87caf894b1362b508ec745253c6d241423ea59021694d2015e821da
#           1 │+007327b23085c5debf31fb44df7a2294b5882aefdba960bdd68fab665db12c5a
# ────────────┴───────────────────────────────────────────────────────────────────
skip="${skip-} --skip tests::built_by_uv_building"

# The list of HTTP status codes contains 103, but the expected list from the
# snapshot doesn’t. This seems like a trivial discrepancy, probably due to a
# dependency version differing from Cargo.lock.
skip="${skip-} --skip base_client::tests::retried_status_codes"

# Harmless and trivial discrepancies in error messages:
#     8       │-  Caused by: error decoding response body for url (http://[LOCALHOST]/tqdm/)
#           8 │+  Caused by: error decoding response body
skip="${skip-} --skip network::retry_read_timeout_index"
#     9       │-  Caused by: error decoding response body for url (http://[LOCALHOST]/)
#           9 │+  Caused by: error decoding response body
skip="${skip-} --skip network::retry_read_timeout_python_downloads_json"

# These fail flakily: most frequently on ppc64le, but this seems to be just a
# matter of luck, since we suspect a race condition. We have also seen failures
# on aarch64. This is probably a race involving the SSL_CERT_FILE environment
# variable, which process-isolated testing in “cargo nextest” (used by
# upstream) should avoid. That suggests there is nothing to report upstream.
# When this fails, the error looks something like:
#   Error: failed to build HTTP client
#   Caused by:
#       0: certificate in `/tmp/uv/tests/certs/.tmpFF0lkk/ca.pem` (from
#          `SSL_CERT_FILE`) could not be used as a trust anchor on certificate
#          `CN=uv-test-ca, O=Astral Software Inc.`
#       1: ExtensionValueInvalid
skip="${skip-} --skip user_agent_version::test_user_agent_has_linehaul"
skip="${skip-} --skip user_agent_version::test_user_agent_has_subcommand"
skip="${skip-} --skip user_agent_version::test_user_agent_has_version"
# Similarly, with an error like:
#   Client::new(): reqwest::Error {
#     kind: Builder,
#     source: General("No CA certificates were loaded from the system")
#   }
# There are probably more of these.
skip="${skip-} --skip base_client::tests::test_redirect_no_referer_if_disabled"
skip="${skip-} --skip base_client::tests::test_redirect_preserves_authorization_header_on_same_origin"
skip="${skip-} --skip base_client::tests::test_redirect_removes_authorization_header_on_cross_origin"
skip="${skip-} --skip retry::tests::retried_status_codes"
skip="${skip-} --skip retry::tests::retry_logs_redact_signed_urls"
# This has been seen to fail in koji, so far only on x86_64, but so far not in
# a local mock build. It’s very possible that this is another testing race
# condition that would be avoided by process isolation in “cargo nextest.” It
# seems unlikely that it is a real and serious problem, although a proper
# diagnosis would be welcome.
skip="${skip-} --skip interpreter::tests::test_cache_eviction_with_unchanged_executable"

%cargo_test -- -- --exact ${skip-}
%endif


%files
%license LICENSE-APACHE LICENSE-MIT LICENSE.dependencies LICENSE.bundled/
%doc CHANGELOG.md
%doc README.md

%{_bindir}/uv
# Equivalent to “uv tool run”:
%{_bindir}/uvx

%{bash_completions_dir}/{uv,uvx}.bash
%{fish_completions_dir}/{uv,uvx}.fish
%{zsh_completions_dir}/_{uv,uvx}

%dir %{_sysconfdir}/uv
%config(noreplace) %{_sysconfdir}/uv/uv.toml


%files -n python3-uv -f %{pyproject_files}


%changelog
## START: Generated by rpmautospec
* Wed Oct 21 2026 Dan Streetman <ddstreet@ieee.org> - 0.12.19-2
- build(uv): update after rust prerequisites

* Fri Sep 25 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.19-1
- Update to 0.12.9 (close RHBZ#2540893)

* Wed Sep 23 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.18-1
- Update to 0.12.18 (close RHBZ#2539073)

* Mon Sep 21 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.17-2
- Preserve `PROFILE` env. var. handling in `uv` crate build script

* Mon Sep 21 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.17-1
- Update to 0.12.17 (close RHBZ#2536872)

* Wed Sep 16 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.15-2
- Skip two more flaky/racy tests

* Tue Sep 15 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.15-1
- Update to 0.12.15 (close RHBZ#2533726)

* Tue Sep 15 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.14-1
- Update to 0.12.14 (close RHBZ#2533575)

* Sat Sep 12 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.13-3
- Make Python 3.15 system interpreters available for testing

* Fri Sep 11 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.13-2
- Skip yet another test that flakes due to CA cert env. var. races

* Thu Sep 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.13-1
- Update to 0.12.13

* Wed Sep 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.12-1
- Update to 0.12.12 (close RHBZ#2530499)

* Sat Sep 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.10-1
- Update to 0.12.0 (close RHBZ#2528984)

* Fri Sep 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.9-2
- Skip another test that’s flaky due test envvar races

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.9-1
- Update to 0.12.9 (close RHBZ#2515847)

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.8-1
- Update to 0.12.8

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.7-3
- Skip a test observed to fail in koji on x86_64

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.7-2
- Improved patch for dirhash tests

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.7-1
- Update to 0.12.7

* Thu Sep 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.6-1
- Update to 0.12.6

* Wed Sep 02 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.5-1
- Update to 0.12.5

* Wed Sep 02 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.4-1
- Update to 0.12.4

* Sat Aug 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.3-1
- Update to 0.12.3 (close RHBZ#2512634)

* Thu Aug 06 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.2-1
- Update to 0.12.2 (close RHBZ#2511719)

* Wed Aug 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-5
- Skip another test that flakes due to racy env-vars

* Wed Aug 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-4
- Ship the license file for the vendored rust-netrc

* Wed Aug 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-3
- More spec-file comment improvements

* Tue Aug 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-2
- Document bundling of rust-netrc crate

* Sun Aug 02 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.1-1
- Update to 0.12.1 (close RHBZ#2509887)

* Fri Jul 31 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-1
- Update to 0.12.0

* Fri Jul 31 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.33-1
- Update to 0.11.33

* Mon Jul 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.32-2
- Skip a test that fails in emulated chroots

* Fri Jul 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.32-1
- Update to 0.11.32 (close RHBZ#2506667)

* Fri Jul 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.31-6
- Skip some tests related to managed interpreters on riscv64

* Wed Jul 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.31-5
- Use the provisional pyproject declarative buildsystem

* Wed Jul 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.31-4
- Assert that the .dist-info directory contains license files

* Wed Jul 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.31-3
- Use pyproject long options

* Wed Jul 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.31-1
- Update to 0.11.31 (close RHBZ#2501168)

* Sat Jul 18 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.28-4
- Avoid OOM on builders with relatively little total memory

* Fri Jul 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Wed Jul 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.28-1
- Update to 0.11.28 (close RHBZ#2497922)

* Tue Jul 07 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.27-1
- Update to 0.11.27 (close RHBZ#2497560)

* Thu Jul 02 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.26-1
- Update to 0.11.26 (close RHBZ#2495097)

* Sat Jun 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.25-1
- Update to 0.11.25

* Wed Jun 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.24-1
- Update to 0.11.24 (close RHBZ#2492025)

* Sun Jun 21 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.23-1
- Update to 0.11.23 (close RHBZ#2490666)

* Sun Jun 21 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.22-1
- Update to 0.11.22

* Thu Jun 18 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.21-4
- Rebuilt with `reflink-copy` 0.1.30

* Thu Jun 18 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.21-3
- Fix skipping tests that require alternative versions of Python

* Wed Jun 17 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.21-2
- Rebuilt with webpki-root-certs 1.0.8

* Fri Jun 12 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.21-1
- Update to 0.11.21 (close RHBZ#2487856)

* Thu Jun 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.19-2
- Allow tikv-jemallocator 0.7

* Thu Jun 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.19-1
- Update to 0.11.19 (close RHBZ#2484591)

* Wed Jun 03 2026 Python Maint <python-maint@redhat.com> - 0.11.18-3
- Rebuilt for Python 3.15

* Wed Jun 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.18-2
- Backport upstream fix for skipping uv check tests when offline

* Wed Jun 03 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.18-1
- Update to 0.11.18 (close RHBZ#2483122)

* Sun May 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.16-2
- Use various long options

* Fri May 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.16-1
- Update to 0.11.16 (close RHBZ#2480652)

* Tue May 19 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.15-1
- Update to 0.11.15 (close RHBZ#2479704)

* Wed May 13 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.14-1
- Update to 0.11.14 (close RHBZ#2468985)

* Sat May 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.12-1
- Update to 0.11.12 (close RHBZ#2466908)

* Fri May 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.11-1
- Update to 0.11.11 (close RHBZ#2466908)

* Wed May 06 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.10-1
- Update to 0.11.10 (close RHBZ#2466908)

* Tue May 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.9-1
- Update to 0.11.9 (close RHBZ#2466654)

* Thu Apr 16 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.7-1
- Update to 0.11.7 (close RHBZ#2458860)

* Thu Apr 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.6-2
- Skip user_agent_version:: tests on all architectures

* Thu Apr 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.6-1
- Update to 0.11.6 (close RHBZ#2454177)

* Thu Apr 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.5-2
- Skip three tests that fail only on ppc64le

* Thu Apr 09 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.5-1
- Update to 0.11.5 (close RHBZ#2454177)

* Wed Apr 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.4-1
- Update to 0.11.4 (close RHBZ#2454177)

* Fri Mar 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.11.2-1
- Update to 0.11.2 (close RHBZ#2450582)

* Wed Aug 19 2026 reuben olinsky <reubeno@users.noreply.github.com> - 0.10.12-4
- build: mass rebuild auto-bumpable components

* Wed Aug 19 2026 reuben olinsky <reubeno@users.noreply.github.com> - 0.10.12-3
- build: mass rebuild auto-bumpable components

* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 0.10.12-2
- feat: introduce deterministic commit resolution via Azure Linux lock file

* Fri Mar 20 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.12-1
- Update to 0.10.12 (close RHBZ#2449243)

* Tue Mar 17 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.11-1
- Update to 0.10.11 (close RHBZ#2448300)

* Sun Mar 15 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.10-1
- Update to 0.10.10 (close RHBZ#2447540)

* Sun Mar 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.9-1
- Update to 0.10.9 (close RHBZ#2445402)

* Wed Mar 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.8-1
- Update to 0.10.8 (close RHBZ#2444235)

* Fri Feb 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.7-1
- Update to 0.10.7 (close RHBZ#2443313)

* Wed Feb 25 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.6-1
- Update to 0.10.6 (close RHBZ#2442225)

* Wed Feb 25 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.5-1
- Update to 0.10.5

* Wed Feb 18 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.4-1
- Update to 0.10.4 (close RHBZ#2440513)

* Mon Feb 16 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.3-1
- Update to 0.10.3 (close RHBZ#2440201)

* Tue Feb 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.2-1
- Update to 0.10.2

* Tue Feb 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.1-1
- Update to 0.10.1 (close RHBZ#2437188)

* Sun Feb 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.10.0-1
- Update to 0.10.0 (close RHBZ#2437188)

* Sun Feb 08 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.30-2
- Rebuilt with jsonwebtoken patched for CVE-2026-25537
- Fixes RHBZ#2437472; fixes RHBZ#2437467; fixes RHBZ#2437461

* Thu Feb 05 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.30-1
- Update to 0.9.30 (close RHBZ#2437002)

* Wed Feb 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.29-1
- Update to 0.9.29 (close RHBZ#2436550)

* Thu Jan 29 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.28-1
- Update to 0.9.28 (close RHBZ#2433149)

* Thu Jan 29 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.27-1
- Update to 0.9.27

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.26-1
- Update to 0.9.26 (close RHBZ#2428381)
- Update package description from upstream

* Tue Jan 06 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.22-1
- Update to 0.9.22 (close RHBZ#2427393)

* Sun Jan 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.21-6
- Remove some EPEL10-specific test skips that are no longer required

* Sun Jan 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.21-5
- Backport gating several tests on python-managed feature

* Wed Dec 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.21-4
- Update virtual Provides version for bundled virtualenv scripts

* Wed Dec 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.21-2
- Skip python_list::python_list_with_mirrors, not python_list_mirrors

* Tue Dec 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.21-1
- Update to 0.9.21 (close RHBZ#2425941)

* Tue Dec 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.20-3
- Allow procfs 0.18

* Tue Dec 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.20-2
- Skip python_list::python_list_mirrors on less-common architectures

* Tue Dec 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.20-1
- Update to 0.9.20 (close RHBZ#2425941)

* Tue Dec 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.18-1
- Update to 0.9.18 (close RHBZ#2422900)

* Sun Dec 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.17-2
- Update spdx to 0.13

* Wed Dec 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.17-1
- Update to 0.9.17

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.16-1
- Update to 0.9.16

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.15-1
- Update to 0.9.15

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.14-1
- Update to 0.9.14

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.13-1
- Update to 0.9.13

* Tue Dec 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.12-1
- Update to 0.9.12

* Mon Dec 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.11-1
- Update to 0.9.11

* Fri Dec 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.10-1
- Update to 0.9.10

* Fri Dec 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.9-4
- No longer allow etcetera version 0.10

* Wed Dec 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.9-2
- Skip flaky test_redirect_to_server_with_credentials on *all* arches

* Wed Dec 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.9-1
- Update to 0.9.9

* Fri Nov 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.8-1
- Update to 0.9.8 (close RHBZ#2413462)

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.7-4
- Drop conditionals for F41, soon to be EOL

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.7-3
- Lower maximum CPUs a bit more

* Sun Nov 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.7-2
- Allow spdx 0.12

* Fri Oct 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.7-1
- Update to 0.9.7 (close RHBZ#2408776)

* Thu Oct 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.6-1
- Update to 0.9.6 (close RHBZ#2407283)

* Sat Oct 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.5-6
- Remove a few more now-unnecessary test skips

* Sat Oct 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.5-5
- Consolidate ppc64le/s390x skips for the same test

* Sat Oct 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.5-4
- Remove python_list::python_list* test skips that no longer fail

* Sat Oct 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.5-3
- Skip a test that is flaky on ppc64le

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.5-1
- Update to 0.9.5 (close RHBZ#2402923)

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.4-1
- Update to 0.9.4

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.3-1
- Update to 0.9.3

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.2-1
- Update to 0.9.2

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.1-1
- Update to 0.9.1

* Fri Oct 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.9.0-1
- Update to 0.9.0

* Thu Oct 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.24-4
- Try to work around “too many open files” on 192-core builders

* Thu Oct 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.24-3
- Revert "Allow hashbrown 0.15 (for EPEL10.1)"

* Thu Oct 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.24-2
- Allow hashbrown 0.15 (for EPEL10.1)

* Wed Oct 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.24-1
- Update to 0.8.24

* Wed Oct 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.23-1
- Update to 0.8.23

* Wed Oct 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.22-1
- Update to 0.8.22

* Wed Oct 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.21-1
- Update to 0.8.21

* Thu Oct 16 2025 Gordon Messmer <gordon.messmer@gmail.com> - 0.8.20-2
- Use rpm's native resource tunable to limit parallelism.

* Mon Sep 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.20-1
- Update to 0.8.20 (close RHBZ#2389326)

* Mon Sep 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.19-1
- Update to 0.8.19

* Mon Sep 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.18-1
- Update to 0.8.18

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.17-1
- Update to 0.8.17

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.16-1
- Update to 0.8.16

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.15-1
- Update to 0.8.15

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.14-1
- Update to 0.8.14

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.13-1
- Update to 0.8.13

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.12-1
- Update to 0.8.12

* Sun Sep 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.11-5
- Use the bundled reqwest-middleware, too

* Wed Sep 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.11-4
- Rebuilt with astral-tokio-tar version 0.5.5
- Security fix for path traversal CVE-2025-59825 / GHSA-3wgq-wrwc-vqmv

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.11-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.11-2
- Rebuilt with rust-tracing-subscriber-0.3.20
- Fixes CVE-2025-58160: fixes RHBZ#2392055, fixes RHBZ#2392012, fixes
  RHBZ#2391975

* Sat Aug 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.11-1
- Update to 0.8.11 (close RHBZ#2388413)

* Sat Aug 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.10-1
- Update to 0.8.10

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.9-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.9-1
- Update to 0.8.9 (close RHBZ#2387762)

* Sat Aug 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.8-1
- Update to 0.8.8 (close RHBZ#2387194)

* Sat Aug 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.6-1
- Update to 0.8.6

* Wed Aug 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.5-1
- Update to 0.8.5 (close RHBZ#2386647)

* Thu Jul 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.4-1
- Update to 0.8.4 (close RHBZ#2381845)

* Thu Jul 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.3-1
- Update to 0.8.3

* Tue Jul 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.2-2
- No longer allow indicatif 0.17

* Tue Jul 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.2-1
- Update to 0.8.2

* Tue Jul 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.1-1
- Update to 0.8.1

* Tue Jul 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.0-2
- Update console to 0.16

* Tue Jul 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.0-1
- Update to 0.8.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.22-1
- Update to 0.7.22

* Wed Jul 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.21-1
- Update to 0.7.21 (close RHBZ#2379944)

* Thu Jul 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.20-1
- Update to 0.7.20 (close RHBZ#2379147)

* Tue Jul 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.19-3
- Skip one test on s390x for now

* Tue Jul 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.19-2
- Follow upstream in using the jemalloc allocator

* Mon Jul 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.19-1
- Update to 0.7.19 (close RHBZ#2375472)

* Mon Jul 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.18-1
- Update to 0.7.18

* Mon Jul 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.17-1
- Update to 0.7.17

* Sat Jun 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.16-2
- No longer allow which 7

* Sat Jun 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.16-1
- Update to 0.7.16 (close RHBZ#2374471)

* Sat Jun 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.15-1
- Update to 0.7.15

* Thu Jun 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.14-3
- Skip a known issue with reqwest>0.12.5 for now

* Thu Jun 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.14-2
- Bundle ONLY reqwest-retry, not reqwest-middleware

* Thu Jun 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.14-1
- Update to 0.7.14

* Wed Jun 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.13-4
- Allow which 8

* Fri Jun 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.13-3
- No longer allow nix 0.29

* Wed Jun 18 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.13-2
- No longer allow goblin 0.9

* Fri Jun 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.13-1
- Update to 0.7.13 (close RHBZ#2372605)

* Tue Jun 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.12-2
- Unpin reqwest since we will coordinate updates to avoid regressions

* Mon Jun 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.12-1
- Update to 0.7.12 (close RHBZ#2370087)

* Mon Jun 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.11-1
- Update to 0.7.11

* Mon Jun 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.10-1
- Update to 0.7.10
- Loosen goblin and nix dependencies until they can be updated

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.7.9-2
- Rebuilt for Python 3.14

* Sat May 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.9-1
- Update to 0.7.9 (close RHBZ#2369514)

* Thu May 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.8-4
- Skip python_list::python_list_downloads on less-common architectures

* Wed May 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.8-3
- No longer need to skip several `help::*` tests

* Wed May 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.8-2
- Enable integration tests in Fedora

* Sun May 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.8-1
- Update to 0.7.8 (close RHBZ#2368123)

* Tue May 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.6-1
- Update to 0.7.6 (close RHBZ#2367417)

* Sat May 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.5-1
- Update to 0.7.5 (close RHBZ#2362372)

* Sat May 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.4-1
- Update to 0.7.4

* Fri May 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.3-1
- Update to 0.7.3

* Tue May 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.2-1
- Update to 0.7.2

* Tue May 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.1-1
- Update to 0.7.1

* Tue May 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.7.0-1
- Update to 0.7.0

* Tue May 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.17-2
- No longer patch out tests requiring wiremock

* Mon May 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.17-1
- Update to 0.6.17

* Fri Apr 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.16-2
- Update ron to 0.10

* Tue Apr 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.16-1
- Update to 0.6.16 (close RHBZ#2361555)

* Mon Apr 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.14-5
- Stop allowing etcetera 0.8

* Mon Apr 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.14-4
- Remove a test skip that was a workaround for url 2.5.2

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.14-3
- Patch bundled pubgrub/version-ranges fork for ron 0.9.0 final

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.14-2
- Rebuilt with rust-idna 1.x

* Thu Apr 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.14-1
- Update to 0.6.14 (close RHBZ#2358763)

* Tue Apr 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.13-1
- Update to 0.6.13 (close RHBZ#2358064)

* Fri Apr 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.12-2
- Update License expression

* Fri Apr 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.12-1
- Update to 0.6.12 (close RHBZ#2354987)

* Fri Apr 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.11-1
- Update to 0.6.11

* Thu Apr 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.10-1
- Update to 0.6.10

* Sat Mar 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.9-2
- Stop patching the forked async-zip for zip 0.6; use zip 2

* Fri Mar 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.9-1
- Update to 0.6.9 (close RHBZ#2353965)

* Wed Mar 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.8-1
- Update to 0.6.8 (close RHBZ#2353281)

* Tue Mar 18 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.7-1
- Update to 0.6.7 (close RHBZ#2353121)

* Wed Mar 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.6-1
- Update to 0.6.6 (close RHBZ#2351456)

* Mon Mar 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.5-2
- Drop patch that allowed mailparse 0.15.x (we now have 0.16.x)

* Mon Mar 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.5-1
- Update to 0.6.5 (close RHBZ#2350517)

* Tue Mar 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.4-1
- Update to 0.6.4 (close RHBZ#2349718)

* Sun Mar 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.3-4
- Make the CI test for disabling Python auto-installation more robust

* Fri Feb 28 2025 Lumir Balhar <lbalhar@redhat.com> - 0.6.3-3
- [test] Add some basic smoke tests

* Thu Feb 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.3-2
- Backport vendoring of r-shquote unquote implementation

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.3-1
- Update to 0.6.3 (close RHBZ#2347458)

* Thu Feb 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.2-1
- Update to 0.6.2 (close RHBZ#2345851)

* Thu Feb 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.1-1
- Update to 0.6.1

* Tue Feb 18 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.6.0-1
- Update to 0.6.0

* Thu Feb 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.31-1
- Update to 0.5.31 (close RHBZ#2345448)

* Wed Feb 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.30-2
- Skip tests with insignificant snapshot differences on some branches

* Wed Feb 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.30-1
- Update to 0.5.30 (close RHBZ#2344596)

* Wed Feb 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.29-4
- Update sanitize-filename requirement from 0.5 to 0.6 in async_zip

* Sun Feb 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.29-3
- Rebuilt with rust-astral-tokio-tar 0.5.1

* Fri Feb 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.29-1
- Update to 0.5.29 (close RHBZ#2344126)

* Wed Feb 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.28-1
- Update to 0.5.28 (close RHBZ#2343881)

* Tue Feb 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.27-1
- Update to 0.1.27 (close RHBZ#2343669)

* Fri Jan 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.26-1
- Update to 0.5.26 (close RHBZ#2343108)

* Wed Jan 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.25-1
- Update to 0.5.25 (close RHBZ#2342713)

* Fri Jan 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.24-1
- Update to 0.5.24 (close RHBZ#2341672)

* Fri Jan 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.23-1
- Update to 0.5.23

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.22-1
- Update to 0.5.22 (close RHBZ#2337040)

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.21-2
- Stop allowing itertools 0.13, now that 0.14 is packaged

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.21-1
- Update to 0.5.21

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.20-1
- Update to 0.5.20

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.19-1
- Update to 0.5.19

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.18-1
- Update to 0.5.18

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.17-1
- Update to 0.5.17

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.16-1
- Update to 0.5.16 (close RHBZ#2336058)

* Wed Jan 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.15-1
- Update to 0.5.15

* Thu Jan 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.14-1
- Update to 0.5.14 (close RHBZ#2335339)

* Sun Dec 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.13-1
- Update to 0.5.13 (close RHBZ#2334581)

* Fri Dec 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.12-1
- Update to 0.5.12 (close RHBZ#2334267)

* Mon Dec 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.11-1
- Update to 0.5.11 (close RHBZ#2331735)

* Mon Dec 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.10-1
- Update to 0.5.10

* Mon Dec 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.9-1
- Update to 0.5.9

* Mon Dec 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.8-1
- Update to 0.5.8

* Fri Dec 20 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.7-4
- Stop allowing older versions of the procfs and which crates

* Wed Dec 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.7-3
- Make the backoff crate dependency Windows-only

* Mon Dec 09 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.7-2
- Follow upstream in using zlib-rs instead of zlib-ng

* Sun Dec 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.7-1
- Update to 0.5.7 (close RHBZ#2330950)

* Wed Dec 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.6-1
- Update to 0.5.6 (close RHBZ#2330247)

* Sun Dec 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.5-3
- No longer patch to allow thiserror 1.x

* Thu Nov 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.5-2
- Revert "Backport a path-escaping fix for the batch activation script"

* Wed Nov 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.5-1
- Update to 0.5.5 (close RHBZ#2329188)

* Wed Nov 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.4-2
- Backport a path-escaping fix for the batch activation script

* Thu Nov 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.4-1
- Update to 0.5.4 (close RHBZ#2327512)

* Thu Nov 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.3-1
- Update to 0.5.3

* Tue Nov 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.2-2
- Stop loosening the mailparse dependency version bound

* Mon Nov 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.2-1
- Update to 0.5.2 (close RHBZ#2323792)

* Sat Nov 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.1-1
- Update to 0.5.1

* Sat Nov 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5.0-1
- Update to 0.5.0

* Thu Nov 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.30-4
- Also configure python-preference = "system"

* Thu Nov 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.30-3
- Install a default system-wide uv.toml
- Configure python-downloads = "manual"

* Tue Nov 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.30-2
- Backport commit to unbundle reqwest-middleware/reqwest-retry

* Mon Nov 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.30-1
- Update to 0.4.30

* Sun Nov 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.29-4
- Stop allowing goblin 0.8 (since goblin 0.9 is packaged)

* Sun Nov 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.29-3
- Add a bcond that would re-enable integration tests

* Sun Nov 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.29-2
- Remove python-managed and git from the default features
- Both of these imply network access during testing.

* Thu Oct 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.29-1
- Update to 0.4.29

* Tue Oct 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.28-1
- Update to 0.4.28

* Mon Oct 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.27-1
- Update to 0.4.27

* Fri Oct 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.26-1
- Update to 0.4.26 (close RHBZ#2321691)

* Mon Oct 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.25-1
- Update to 0.4.25

* Fri Oct 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.24-1
- Update to 0.4.24 (close RHBZ#2319248)

* Fri Oct 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.23-1
- Update to 0.4.23

* Thu Oct 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.22-1
- Update to 0.4.22

* Thu Oct 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.21-1
- Update to 0.4.21

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.20-1
- Update to 0.4.20 (close RHBZ#2314073)

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.19-1
- Update to 0.4.19

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.18-1
- Update to 0.4.18

* Thu Oct 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.17-1
- Update to 0.4.17
- Stop patching the tracing-tree dependency, since 0.4 is now packaged
- Generate separate completion scripts for uvx; this has been possible
  since release 0.4.14 due to https://github.com/astral-sh/uv/pull/7511

* Wed Sep 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.16-1
- Update to 0.4.16

* Sun Sep 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.15-1
- Update to 0.4.15 (close RHBZ#2314073)

* Fri Sep 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.10-1
- Update to 0.4.10

* Wed Sep 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.9-1
- Update to 0.4.9 (close RHBZ#2311362)

* Wed Sep 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.8-1
- Update to 0.4.8

* Sun Sep 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.7-1
- Update to 0.4.7

* Fri Sep 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.6-1
- Update to 0.4.6 (close RHBZ#2310414)

* Thu Sep 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.5-1
- Update to 0.4.5

* Wed Sep 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.4-1
- Update to 0.4.4 (close RHBZ#2309685)

* Sun Sep 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.2-1
- Update to 0.4.2

* Sat Aug 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.1-1
- Update to 0.4.1

* Thu Aug 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-1
- Update to 0.4.0

* Wed Aug 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.5-1
- Update to 0.3.5

* Tue Aug 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.4-3
- Increase per-process memory allowance when building

* Tue Aug 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.4-1
- Update to 0.3.4

* Mon Aug 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.3-3
- Use %%constrain_build to prevent memory exhaustion on many-core builders

* Mon Aug 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.3-2
- Reduce debuginfo level to “limited”
- Fixes failures due to memory exhaustion on builders, particularly in F41

* Sat Aug 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.3-1
- Update to 0.3.3 (close RHBZ#2307495)

* Sat Aug 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.2-1
- Update to 0.3.2

* Thu Aug 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-1
- Update to 0.3.0

* Wed Aug 21 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.37-1
- Update to 0.2.37

* Sun Aug 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.35-1
- Update to 0.2.35

* Thu Aug 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.34-1
- Update to 0.2.34

* Thu Aug 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.33-3
- For now, remove the entire uv-trampoline crate before building

* Thu Aug 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.33-2
- Remove (unused) pre-compiled Windows executables before building

* Fri Aug 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.33-1
- Update to 0.2.33

* Thu Aug 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.32-1
- Initial package (close RHBZ#2299712)
## END: Generated by rpmautospec
