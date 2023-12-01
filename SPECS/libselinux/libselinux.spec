Summary:        SELinux library and simple utilities
Name:           libselinux
Version:        3.5
Release:        1%{?dist}
License:        Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libsepol-devel
BuildRequires:  pcre-devel
BuildRequires:  swig
Requires:       pcre-libs
Requires:       libsepol

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

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package        utils
Summary:        SELinux libselinux utilies
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    utils
The libselinux-utils package contains the utilities

%package        devel
Summary:        Header files and libraries used to build SELinux
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pcre-devel
Requires:       libsepol-devel >= %{version}

%description    devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications.

%package        python3
Summary:        SELinux python3 bindings for libselinux
Group:          Development/Libraries
Provides:       python3-%{name} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description    python3
The libselinux-python package contains the python3 bindings for developing
SELinux applications.

%prep
%autosetup

%build
sed '/unistd.h/a#include <sys/uio.h>' -i src/setrans_client.c
%make_build clean
%make_build swigify CFLAGS="%{build_cflags} -Wno-error=strict-overflow -fno-semantic-interposition"
%make_build LIBDIR="%{_libdir}" PYTHON=%{python3} pywrap

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" PYTHON=/usr/bin/python3 install install-pywrap

mkdir -p %{buildroot}%{_libdir}/tmpfiles.d
mkdir -p %{buildroot}%{_localstatedir}/run/setrans
echo "d %{_localstatedir}/run/setrans 0755 root root" > %{buildroot}/%{_libdir}/tmpfiles.d/libselinux.conf

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%license LICENSE
%ghost %{_localstatedir}/run/setrans
%{_libdir}/libselinux.so.1
%{_libdir}/tmpfiles.d/libselinux.conf

%files utils
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/ru/man5/*
%{_mandir}/ru/man8/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libselinux.so
%{_libdir}/libselinux.a
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files python3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.5-1
- Auto-upgrade to 3.5 - Azure Linux 3.0 - package upgrades

* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream 
- License verified
- Remove manual pkgconfig provides
- Update source URL to new format
- Lint spec

* Mon May 19 2021 Nick Samson <nisamson@microsoft.com> - 2.9-6
- Removed python2 module support

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.9-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.9-4
- Provide python3-libselinux for -python3 subpackage

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.9-3
- Added %%license line automatically

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.9-2
- Add -Wno-error=strict-overflow to resolve build break with gcc9

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.9-1
- Update to 2.9. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.8-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.8-2
- Added BuildRequires python2-devel

* Fri Aug 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 2.8-1
- Update to version 2.8 to get it to build with gcc 7.3

* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.6-4
- Fix compilation issue for glibc-2.26

* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.6-3
- Include pytho3 packages.

* Mon May 22 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.6-2
- Include python subpackage.

* Wed May 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.6-1
- Upgraded to version 2.6

* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> - 2.5-3
- Remove pcre requires and add requires on pcre-libs

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.5-2
- GA - Bump release of all rpms

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.5-1
- Updated to version 2.5

* Wed Feb 25 2015 Divya Thaluru <dthaluru@vmware.com> - 2.4-1
- Initial build.  First version
