Summary:        Enhanced seccomp library
Name:           libseccomp
Version:        2.5.4
Release:        1%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/seccomp/libseccomp/wiki
Source0:        https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gperf
%if %{with_check}
BuildRequires:  which
%endif

%description
The libseccomp library provides an easy to use, platform independent, interface
to the Linux Kernel syscall filtering mechanism: seccomp. The libseccomp API
is designed to abstract away the underlying BPF based syscall filter language
and present a more conventional function-call based filtering interface that
should be familiar to, and easily adopted by application developers.

%package        devel
Summary:        Development files used to build applications with libseccomp support
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%ldconfig_scriptlets

%files
%license LICENSE
%doc CREDITS README.md
%{_libdir}/libseccomp.so.2*

%files devel
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/libseccomp.so
%{_libdir}/libseccomp.a
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.5.4-1
- Auto-upgrade to 2.5.4 - Azure Linux 3.0 - package upgrades

* Thu Jan 13 2022 Henry Li <lihl@microsoft.com> - 2.5.3-1
- Upgrade to version 2.5.3
- Add gperf as BR
- Add /usr/include/seccomp-syscalls.h to libseccomp-devel package

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 2.4.1-4
- Remove pkgconfig provides (no longer necessary)
- Require base package from devel subpackage
- Include libseccomp soname version in %%file section

* Tue Jun 29 2021 Thomas Crain <thcrain@microsoft.com> - 2.4.1-3
- Provide libseccomp-static from devel subpackage
- Version the pkgconfig provides
- Modernize spec with macros
- Remove libtool archive files

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.4.1-1
- Update to 2.4.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.3.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jan 9 2019 Michelle Wang <michellew@vmware.com> - 2.3.3-2
- Fix make check for libseccomp.

* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> - 2.3.3-1
- Updated to version 2.3.3.

* Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> - 2.3.2-1
- Updated to version 2.3.2.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.2.3-2
- GA - Bump release of all rpms.

* Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
- First release of the package.
