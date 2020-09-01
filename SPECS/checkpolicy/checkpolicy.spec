%define libselinuxver 2.9-1
%define libsepolver 2.9-1

Summary: SELinux policy compiler
Name: checkpolicy
Version: 2.9
Release: 1%{?dist}
License: GPLv2
Source0: https://github.com/SELinuxProject/selinux/releases/download/20190315/checkpolicy-2.9.tar.gz
Conflicts: selinux-policy-base < 3.13.1-138
BuildRequires: gcc
BuildRequires: bison flex flex-devel libsepol-devel >= %{libsepolver} libselinux-devel  >= %{libselinuxver}

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

This package contains checkpolicy, the SELinux policy compiler.
Only required for building policies.

%prep
%autosetup -p 1 -n checkpolicy-%{version}

%build

%set_build_flags

make clean
make LIBDIR="%{_libdir}"
cd test
make LIBDIR="%{_libdir}"

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
make LIBDIR="%{_libdir}" DESTDIR="${RPM_BUILD_ROOT}" install
install test/dismod ${RPM_BUILD_ROOT}%{_bindir}/sedismod
install test/dispol ${RPM_BUILD_ROOT}%{_bindir}/sedispol

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/checkpolicy
%{_bindir}/checkmodule
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz
%{_mandir}/ru/man8/checkpolicy.8.gz
%{_mandir}/ru/man8/checkmodule.8.gz
%{_bindir}/sedismod
%{_bindir}/sedispol

%changelog
* Wed Aug 19 2020 Daniel Burgener <Daniel.Burgener@microsoft.com> 2.9-1
-   Initial import from Fedora 31 (license: MIT)
