# Prevent librustc_driver from inadvertently being listed as a requirement
%global __requires_exclude ^librustc_driver-

# Release date and version of stage 0 compiler can be found in "src/stage0.json" inside the extracted "Source0".
# Look for "date:" and "rustc:".
%define release_date 2023-07-13
%define stage0_version 1.71.0

Summary:        Rust Programming Language
Name:           rust
Version:        1.72.0
Release:        5%{?dist}
License:        (ASL 2.0 OR MIT) AND BSD AND CC-BY-3.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.rust-lang.org/
# Notes:
#  - rust source official repo is https://github.com/rust-lang/rust
#  - cargo source official repo is https://github.com/rust-lang/cargo
#  - crates.io source official repo is https://github.com/rust-lang/crates.io
Source0:        https://static.rust-lang.org/dist/rustc-%{version}-src.tar.xz
# Note: the rust-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache, leverage the: generate_source_tarball.sh
#
# An example run for rust 1.68.2:
# - Download Rust Source (1.68.2):
#   wget https://static.rust-lang.org/dist/rustc-1.68.2-src.tar.xz
# - Create a directory to store the output from the script:
#   mkdir rustOutputDir
# - Get prereqs for the script (for a mariner container):
#   tdnf -y install rust wget jq tar ca-certificates
# - Run the script:
#   ./generate_source_tarball --srcTarball path/to/rustc-1.68.2-src.tar.xz --outFolder path/to/rustOutputDir --pkgVersion 1.68.2
#

Source1:        rustc-%{version}-src-cargo.tar.gz
Source2:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{stage0_version}-x86_64-unknown-linux-gnu.tar.xz
Source3:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{stage0_version}-x86_64-unknown-linux-gnu.tar.xz
Source4:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{stage0_version}-x86_64-unknown-linux-gnu.tar.xz
Source5:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{stage0_version}-aarch64-unknown-linux-gnu.tar.xz
Source6:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{stage0_version}-aarch64-unknown-linux-gnu.tar.xz
Source7:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{stage0_version}-aarch64-unknown-linux-gnu.tar.xz
BuildRequires:  binutils
BuildRequires:  cmake
# make sure rust relies on curl from CBL-Mariner (instead of using its vendored flavor)
BuildRequires:  curl-devel
BuildRequires:  git
BuildRequires:  glibc
# make sure rust relies on libgit2 from CBL-Mariner (instead of using its vendored flavor)
BuildRequires:  libgit2-devel
# make sure rust relies on nghttp2 from CBL-Mariner (instead of using its vendored flavor)
BuildRequires:  nghttp2-devel
BuildRequires:  ninja-build
# make sure rust relies on openssl from CBL-Mariner (instead of using its vendored flavor)
BuildRequires:  openssl-devel
BuildRequires:  python3
%if %{with_check}
BuildRequires:  glibc-static >= 2.35-6%{?dist}
%endif
# rustc uses a C compiler to invoke the linker, and links to glibc in most cases
Requires:       binutils
Requires:       curl
Requires:       gcc
Requires:       glibc-devel
Requires:       libgit2
Requires:       nghttp2
Requires:       openssl
Provides:       cargo = %{version}-%{release}

%description
Rust Programming Language

%package doc
Summary:        Rust documentation.
BuildArch:      noarch

%description doc
Documentation package for Rust.

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar -xf %{SOURCE1} --no-same-owner
popd
%autosetup -p1 -n rustc-%{version}-src

# Setup build/cache directory
BUILD_CACHE_DIR="build/cache/%{release_date}"
mkdir -pv "$BUILD_CACHE_DIR"
%ifarch x86_64
cp %{SOURCE2} "$BUILD_CACHE_DIR"
cp %{SOURCE3} "$BUILD_CACHE_DIR"
cp %{SOURCE4} "$BUILD_CACHE_DIR"
%endif
%ifarch aarch64
cp %{SOURCE5} "$BUILD_CACHE_DIR"
cp %{SOURCE6} "$BUILD_CACHE_DIR"
cp %{SOURCE7} "$BUILD_CACHE_DIR"
%endif

%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

sh ./configure \
    --prefix=%{_prefix} \
    --enable-extended \
    --tools="cargo,clippy,rustfmt,rust-analyzer-proc-macro-srv" \
    --release-channel="stable" \
    --release-description="CBL-Mariner %{version}-%{release}"

# SUDO_USER=root bypasses a check in the python bootstrap that
# makes rust refuse to pull sources from the internet
USER=root SUDO_USER=root %make_build

%check
# We expect to generate dynamic CI contents in this folder, but it will fail since the .github folder is not included
# with the published sources.
mkdir -p .github/workflows
./x.py run src/tools/expand-yaml-anchors

ln -s %{_prefix}/src/mariner/BUILD/rustc-%{version}-src/build/x86_64-unknown-linux-gnu/stage2-tools-bin/rustfmt %{_prefix}/src/mariner/BUILD/rustc-%{version}-src/build/x86_64-unknown-linux-gnu/stage0/bin/
ln -s %{_prefix}/src/mariner/BUILD/rustc-%{version}-src/vendor/ /root/vendor
# remove rustdoc ui flaky test issue-98690.rs (which is tagged with 'unstable-options')
rm -v ./tests/rustdoc-ui/issue-98690.*
%make_build check

%install
USER=root SUDO_USER=root %make_install
mv %{buildroot}%{_docdir}/%{name}/LICENSE-THIRD-PARTY .
rm %{buildroot}%{_docdir}/%{name}/{COPYRIGHT,LICENSE-APACHE,LICENSE-MIT}
rm %{buildroot}%{_docdir}/%{name}/html/.lock
rm %{buildroot}%{_docdir}/%{name}/*.old
rm %{buildroot}%{_bindir}/*.old

%ldconfig_scriptlets

%files
%license LICENSE-APACHE LICENSE-MIT LICENSE-THIRD-PARTY COPYRIGHT
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-lldb
%{_libdir}/lib*.so
%{_libdir}/rustlib/*
%{_libexecdir}/cargo-credential-1password
%{_libexecdir}/rust-analyzer-proc-macro-srv
%{_bindir}/rust-gdb
%{_bindir}/rust-gdbgui
%{_bindir}/cargo
%{_bindir}/cargo-clippy
%{_bindir}/cargo-fmt
%{_bindir}/clippy-driver
%{_bindir}/rustfmt
%{_datadir}/zsh/*
%{_sysconfdir}/bash_completion.d/cargo

%files doc
%license LICENSE-APACHE LICENSE-MIT LICENSE-THIRD-PARTY COPYRIGHT
%doc %{_docdir}/%{name}/html/*
%doc %{_docdir}/%{name}/README.md
%doc CONTRIBUTING.md README.md RELEASES.md
%doc src/tools/clippy/CHANGELOG.md
%doc src/tools/rustfmt/Configurations.md
%{_mandir}/man1/*

%changelog
* Mon Oct 30 2023 Rohit Rawat <rohitrawat@microsoft.com> - 1.72.0-5
- Test comment, no changes made.

* Tue Oct 10 2023 Daniel McIlvaney <damcilva@microsoft.com> - 1.72.2-4
- Explicitly call './x.py' instead of 'x.py'

* Wed Oct 04 2023 Minghe Ren <mingheren@microsoft.com> - 1.72.2-3
- Bump release to rebuild against glibc 2.35-6

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.72.2-2
- Bump release to rebuild against glibc 2.35-5

* Wed Sep 06 2023 Daniel McIlvaney <damcilva@microsoft.com> - 1.72.2-1
- Bump to version 1.72.2 to address CVE-2023-38497, CVE-2023-40030

* Tue Aug 22 2023 Rachel Menge <rachelmenge@microsoft.com> - 1.68.2-5
- Bump release to rebuild against openssl 1.1.1k-26

* Wed Jul 05 2023 Andrew Phelps <anphel@microsoft.com> - 1.68.2-4
- Bump release to rebuild against glibc 2.35-4

* Wed Jun 21 2023 Jonathan Behrens <jbehrens@microsoft.com> - 1.68.2-3
- Include "cargo-clippy" tool in the package.

* Wed May 17 2023 Tobias Brick <tobiasb@microsoft.com> - 1.68.2-2
- Fix CVE-2023-27477 by patching cranelift vulnerability that is exposed in rust

* Tue Mar 28 2023 Muhammad Falak <mwani@microsoft.com> - 1.68.2-1
- Bump version to 1.68.2 to revoke leaked github keys

* Mon Mar 13 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.68.0-1
- Updating to version 1.68.0

* Thu Nov 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.62.1-4
- Split out separate 'doc' subpackage to reduce default package size.
- Updated license information.

* Tue Nov 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.62.1-3
- Adding missing test dependency on "glibc-static".

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.62.1-2
- Breaking change: Configure as a stable release, which disables unstable features
- Add runtime requirements on gcc, binutils, glibc-devel
- Package ASL 2.0 license, additional copyright information
- Fix licensing info- dual-licensed, not multiply-licensed
- License verified

* Thu Aug 18 2022 Chris Co <chrco@microsoft.com> - 1.62.1-1
- Updating to version 1.62.1

* Mon Mar 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.59.0-1
- Updating to version 1.59.0 to fix CVE-2022-21658.
- Updating build instructions to fix tests.

* Thu Mar 03 2022 Bala <balakumaran.kannan@microsoft.com> - 1.56.1-2
- Build rustfmt tool as it is required to run PTest
- Create softlink for rustfmt in stage0

* Wed Nov 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.56.1-1
- Updating to version 1.56.1.
- Switching to building with Python 3.

* Mon May 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.47.0-5
- Add provides for 'cargo' from the base package

* Tue May 04 2021 Thomas Crain <thcrain@microsoft.com> - 1.47.0-4
- Remove XZ support detection in bootstrap

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.47.0-3
- Patch CVE-2020-36317, CVE-2021-28875, CVE-2021-28876, CVE-2021-28877, CVE-2021-28878
- Redo patch for CVE-2021-28879 with regards to patches listed above

* Mon Apr 19 2021 Thomas Crain <thcrain@microsoft.com> - 1.47.0-2
- Patch CVE-2021-28879

* Wed Feb 24 2021 Andrew Phelps <anphel@microsoft.com> - 1.47.0-1
- Update version to 1.47.0

* Wed Jan 06 2021 Thomas Crain <thcrain@microsoft.com> - 1.39.0-8
- Add python-xml BR for package test
- Add ignore-linker-output-non-utf8-test patch to skip faulty test

* Wed Aug 12 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.39.0-7
- Add patch for the build to not fail on file not found error.

* Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.39.0-6
- Temporarily disable generation of debug symbols.

* Thu May 28 2020 Chris Co <chrco@microsoft.com> - 1.39.0-5
- Update source checkout and prep steps

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.39.0-4
- Added %%license line automatically

* Mon May 4 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.39.0-3
- Fix build issue when building from Docker

* Tue Apr 21 2020 Andrew Phelps <anphel@microsoft.com> - 1.39.0-2
- Support building offline.

* Thu Mar 19 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.39.0-1
- Update to 1.39.0. Fix URL. Fix Source0 URL. License verified.

* Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> - 1.34.2-3
- Set SUDO_USER and USER to allow rust to hydrate as root

* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 1.34.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> - 1.34.2-1
- Initial build. First version
