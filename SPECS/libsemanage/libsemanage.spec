%define libsepolver 2.9-1
%define libselinuxver 2.9-1

%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary: SELinux binary policy manipulation library
Name: libsemanage
Version: 2.9
Release: 3%{?dist}
License: LGPLv2+
Source0: https://github.com/SELinuxProject/selinux/releases/download/20190315/libsemanage-2.9.tar.gz
# fedora-selinux/selinux: git format-patch -N 20190315 -- libsemanage
# i=1; for j in 00*patch; do printf "Patch%04d: %s\n" $i $j; i=$((i+1));done
Patch0001: 0001-libsemanage-Fix-RESOURCE_LEAK-and-USE_AFTER_FREE-cov.patch
URL: https://github.com/SELinuxProject/selinux/wiki
Source1: semanage.conf

BuildRequires: gcc
BuildRequires: libselinux-devel >= %{libselinuxver} swig
BuildRequires: libsepol-devel >= %{libsepolver}
BuildRequires: audit-devel
BuildRequires: bison flex bzip2

BuildRequires: python3
BuildRequires: python3-devel

Requires: bzip2-libs audit-libs
Requires: libselinux%{?_isa} >= %{libselinuxver}

Provides: libsemanage.so.1

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

libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The semanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package python3
Summary: semanage python 3 bindings for libsemanage
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libselinux-python3

%description python3
The libsemanage-python3 package contains the python 3 bindings for developing
SELinux management applications.

%prep
%autosetup -n libsemanage-%{version} -p 2


%build
make clean
make %{?_smp_mflags} swigify CFLAGS="%{build_cflags} -Wno-error=strict-overflow"
make LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all
make LIBDIR="%{_libdir}" %{?_smp_mflags} PYTHON=/usr/bin/python3 pywrap

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_sharedstatedir}/selinux
mkdir -p ${RPM_BUILD_ROOT}%{_sharedstatedir}/selinux/tmp
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=/usr/bin/python3 install install-pywrap

cp %{SOURCE1} ${RPM_BUILD_ROOT}/etc/selinux/semanage.conf
ln -sf  %{_libdir}/libsemanage.so.1 ${RPM_BUILD_ROOT}/%{_libdir}/libsemanage.so

sed -i '1s%\(#! */usr/bin/python\)\([^3].*\|\)$%\13\2%' %{buildroot}%{_libexecdir}/selinux/semanage_migrate_store

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_sysconfdir}/selinux
%config(noreplace) %{_sysconfdir}/selinux/semanage.conf
%{_libdir}/libsemanage.so.1
%{_mandir}/man5/*
%{_mandir}/ru/man5/*
%dir %{_libexecdir}/selinux
%dir %{_sharedstatedir}/selinux
%dir %{_sharedstatedir}/selinux/tmp

%files devel
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%dir %{_includedir}/semanage
%{_includedir}/semanage/*.h
%{_libdir}/libsemanage.a
%{_mandir}/man3/*

%files python3
%{python3_sitelib}/*.so
%{python3_sitelib}/semanage.py*
%{_libexecdir}/selinux/semanage_migrate_store

%changelog
* Tue Aug 25 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-1
- Initial import from Fedora 31
