# Package build hangs during debug info extraction.
%global debug_package   %{nil}

%define ltp_prefix /opt/%{name}

# Don't generate requires on Korn shell.
# Mariner doesn't have it, so we can skip/fail its tests.
%global __requires_exclude_from %{ltp_prefix}/testcases/data/file01/in.ksh

Summary:        Linux Test Project
Name:           ltp
Version:        20220930
Release:        1%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/cbl-mariner
Source0:        https://github.com/linux-test-project/ltp/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}_submodules-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  kernel-headers
BuildRequires:  libacl-devel
BuildRequires:  libaio-devel
BuildRequires:  libcap-devel
BuildRequires:  libmnl-devel
BuildRequires:  libnuma-devel
BuildRequires:  libtirpc-devel
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  pkgconfig

Requires:  expect
Requires:  libacl
Requires:  libaio
Requires:  libcap
Requires:  libmnl
Requires:  libnuma
Requires:  libtirpc
Requires:  glibc
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
%autosetup -a 1

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
# Disabling cloning of git submodules - already provided in Source1
sed -i "s/git submodule.*/@echo 'Skipping submodule init - already provided.'/" tools/sparse/Makefile
make check

%files
%license COPYING
%{ltp_prefix}

%files doc
%{_mandir}/*

%changelog
* Wed Nov 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20220930-1
- Original version for CBL-Mariner.
- License verified.
