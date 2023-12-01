Summary:        SELinux binary policy manipulation library
Name:           libsepol
Version:        3.5
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/archive/refs/tags/%{version}.tar.gz#/selinux-%{version}.tar.gz

%if %{with_check}
BuildRequires:  bison
BuildRequires:  CUnit-devel
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  gcc
%endif

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

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package        devel
Summary:        Header files and libraries used to build policy manipulation tools
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%autosetup -n selinux-%{version}/%{name}
sed  -i 's/int rc;/int rc = SEPOL_OK;/' ./cil/src/cil_binary.c

%build
%make_build clean
%make_build CFLAGS="%{build_cflags} -fno-semantic-interposition"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8

%make_install LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}"

rm -f %{buildroot}%{_bindir}/genpolbools
rm -f %{buildroot}%{_bindir}/genpolusers
rm -f %{buildroot}%{_bindir}/chkcon
rm -rf %{buildroot}%{_mandir}/man8
rm -rf %{buildroot}%{_mandir}/ru/man8

%check
# Tests require the "checkpolicy" project to be built as well. That in turn requires "libsepol-devel".
%make_install DESTDIR=/ LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}"
pushd ../checkpolicy
%make_build CFLAGS="%{build_cflags} -fno-semantic-interposition"
popd

%make_build test

%post
/sbin/ldconfig
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libsepol.so.2
%{_bindir}/sepol_check_access
%{_bindir}/sepol_compute_av
%{_bindir}/sepol_compute_member
%{_bindir}/sepol_compute_relabel
%{_bindir}/sepol_validate_transition

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/libsepol.a
%{_libdir}/pkgconfig/libsepol.pc
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%{_includedir}/sepol/*.h
%{_includedir}/sepol/cil/*.h
%{_mandir}/man3/*.3.gz

%changelog
* Fri Nov 24 2023 Andrew Phelps <anphel@microsoft.com> - 3.5-1
- Upgrade to version 3.5

* Thu Nov 04 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 3.2-2
- Fixing BR on "CUnit-devel".
- Switching to source tarball for full SELinux project to include test dependencies.

* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream and update source URL format
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Remove cunit source, switch to check-time build requirement on cunit
- Bump libsepol sover to 2
- Lint spec
- License verified

* Tue Feb 23 2021 Henry Li <lihl@microsoft.com> - 3.1-1
- Upgrade libsepol to version 3.1

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.9-7
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.9-6
- Add explicit provide for libsepol-static

* Tue Jun 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.9-5
- Remove unused "systemd-bootstrap" from requires.

* Fri May 29 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.9-4
- Use "systemd-bootstrap" to break circular dependencies.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.9-3
- Added %%license line automatically

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.9-2
- Add cflags to make to fix gcc9 compatibility.

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.9-1
- Update to 2.9. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.8-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Aug 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 2.8-1
- Update to version 2.8 to get it to build with gcc 7.3

* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> - 2.6-1
- Updating version to 2.6

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.5-2
- GA - Bump release of all rpms

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.5-1
- Updated to version 2.5

* Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> - 2.4-1
- Initial build. First version
