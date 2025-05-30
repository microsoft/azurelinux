# Package build hangs during debug info extraction.
%global debug_package   %{nil}

%define ltp_prefix /opt/%{name}

# Don't generate requires on Korn shell.
# Mariner doesn't have it, so we can skip/fail its tests.
%global __requires_exclude_from %{ltp_prefix}/testcases/data/file01/in.ksh

Summary:        Linux Test Project
Name:           ltp
Version:        20240129
Release:        1%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://github.com/linux-test-project/ltp
Source0:        https://github.com/linux-test-project/ltp/releases/download/%{version}/ltp-full-%{version}.tar.xz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  libacl-devel
BuildRequires:  libaio-devel
BuildRequires:  libcap-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnuma-devel
BuildRequires:  libtirpc-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  pkg-config

Requires:  diffutils
Requires:  ethtool
Requires:  expect
Requires:  gawk
Requires:  glibc
Requires:  libacl
Requires:  libaio
Requires:  libcap
Requires:  libmnl
Requires:  libnuma
Requires:  libtirpc
Requires:  psmisc
Requires:  tcsh

%description
Linux Test Project is a set of tests to validate the reliability, robustness, and stability of the Linux kernel.

%package doc
Summary:        LTP documentation
BuildArch:      noarch

%description doc
LTP documentation and manuals.

%prep
%autosetup -n ltp-full-%{version}

%build
make autotools
%configure \
    --bindir=%{ltp_prefix}/bin \
    --exec_prefix=%{ltp_prefix} \
    --prefix=%{ltp_prefix}
%make_build

%install
%make_install

%check
make check

%preun
# Removing files with names not known until the tests are run.
rm -rf %{ltp_prefix}/{output,results,testcases/bin/[0-9]*}

%files
%license COPYING
%{ltp_prefix}

%files doc
%{_mandir}/*

%changelog
* Tue Feb 06 2024 Amrita Kohli <amritakohli@microsoft.com> - 20240129-1
- Upgrade to 20240129 for Mariner 3.0 release

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 20230127-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 08 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 20230127-1
- Updating to version 20230127.
- Fixed project URL.

* Tue Jan 17 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 20220930-3
- Adding missing dependency on 'ethtool' and 'diffutils'.

* Tue Dec 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20220930-2
- Fool-proofing LTP dependencies.
- Cleaning up directories created during tests.

* Wed Nov 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20220930-1
- Original version for CBL-Mariner.
- License verified.
