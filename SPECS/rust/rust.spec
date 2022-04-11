# Prevent librustc_driver from inadvertently being listed as a requirement
%global __requires_exclude ^librustc_driver-

# Release date and version of stage 0 compiler can be found in "src/stage0.txt" inside the extracted "Source0".
# Look for "date:" and "rustc:".
%define release_date 2022-01-13
%define stage0_version 1.58.0

Summary:        Rust Programming Language
Name:           rust
Version:        1.59.0
Release:        1%{?dist}
License:        ASL 2.0 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.rust-lang.org/
Source0:        https://static.rust-lang.org/dist/rustc-%{version}-src.tar.xz
# Note: the rust-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache run:
#   [repo_root]/toolkit/scripts/build_cargo_cache.sh rustc-%%{version}-src.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
Source2:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{stage0_version}-x86_64-unknown-linux-gnu.tar.gz
Source3:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{stage0_version}-x86_64-unknown-linux-gnu.tar.gz
Source4:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{stage0_version}-x86_64-unknown-linux-gnu.tar.gz
Source5:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{stage0_version}-aarch64-unknown-linux-gnu.tar.gz
Source6:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{stage0_version}-aarch64-unknown-linux-gnu.tar.gz
Source7:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{stage0_version}-aarch64-unknown-linux-gnu.tar.gz

BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  git
BuildRequires:  glibc
BuildRequires:  ninja-build
BuildRequires:  python3

%if %{with_check}
BuildRequires:  python3-xml
%endif

Provides:       cargo = %{version}-%{release}

%description
Rust Programming Language

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar -xf %{SOURCE1} --no-same-owner
popd
%autosetup -p1 -n rustc-%{version}-src

# Rust doesn't recognize our .tar.gz bootstrap files when XZ support is enabled
# This causes stage 0 bootstrap to look online for sources
# So, we remove XZ support detection in the bootstrap program
sed -i "s/tarball_suffix = '.tar.xz' if support_xz() else '.tar.gz'/tarball_suffix = '.tar.gz'/g" src/bootstrap/bootstrap.py

# Setup build/cache directory
BUILD_CACHE_DIR="build/cache/%{release_date}"
mkdir -pv "$BUILD_CACHE_DIR"
%ifarch x86_64
mv %{SOURCE2} "$BUILD_CACHE_DIR"
mv %{SOURCE3} "$BUILD_CACHE_DIR"
mv %{SOURCE4} "$BUILD_CACHE_DIR"
%endif
%ifarch aarch64
mv %{SOURCE5} "$BUILD_CACHE_DIR"
mv %{SOURCE6} "$BUILD_CACHE_DIR"
mv %{SOURCE7} "$BUILD_CACHE_DIR"
%endif

%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

sh ./configure --prefix=%{_prefix} --enable-extended --tools="cargo,rustfmt"
# SUDO_USER=root bypasses a check in the python bootstrap that
# makes rust refuse to pull sources from the internet
USER=root SUDO_USER=root %make_build

%check
ln -s %{_prefix}/src/mariner/BUILD/rustc-%{version}-src/build/x86_64-unknown-linux-gnu/stage2-tools-bin/rustfmt %{_prefix}/src/mariner/BUILD/rustc-%{version}-src/build/x86_64-unknown-linux-gnu/stage0/bin/
%make_build check

%install
USER=root SUDO_USER=root %make_install
rm %{buildroot}%{_docdir}/%{name}/html/.lock
rm %{buildroot}%{_docdir}/%{name}/*.old

%ldconfig_scriptlets

%files
%license LICENSE-MIT
%doc CONTRIBUTING.md README.md RELEASES.md
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-lldb
%{_mandir}/man1/*
%{_libdir}/lib*.so
%{_libdir}/rustlib/*
%{_libexecdir}/cargo-credential-1password
%{_bindir}/rust-gdb
%{_bindir}/rust-gdbgui
%doc %{_docdir}/%{name}/html/*
%{_docdir}/%{name}/html/.stamp
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/COPYRIGHT
%doc %{_docdir}/%{name}/LICENSE-APACHE
%doc %{_docdir}/%{name}/LICENSE-MIT
%doc src/tools/rustfmt/{README,CHANGELOG,Configurations}.md
%doc src/tools/clippy/{README.md,CHANGELOG.md}
%{_bindir}/cargo
%{_bindir}/cargo-fmt
%{_bindir}/rustfmt
%{_datadir}/zsh/*
%doc %{_docdir}/%{name}/LICENSE-THIRD-PARTY
%{_sysconfdir}/bash_completion.d/cargo

%changelog
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
