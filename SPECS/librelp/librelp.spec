Summary:        RELP Library
Name:           librelp
Version:        1.10.0
Release:        2%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/rsyslog/librelp
Source0:        https://download.rsyslog.com/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  autogen
BuildRequires:  automake
BuildRequires:  gnutls-devel
BuildRequires:  libtool
Requires:       gnutls
%if %{with_check}
BuildRequires:  glibc-debuginfo
BuildRequires:  valgrind
%endif

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package        devel
Summary:        Development libraries and header files for librelp
Requires:       %{name} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%autosetup
autoreconf -fiv

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/relp.pc

%changelog
* Wed Sep 06 2023 Osama Esmail <osamaesmail@microsoft.com> - 1.10.0-2
- Adding `glibc-debuginfo` to fix the tests

* Mon Nov 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.10.0-1
- Upgrade to latest version
- Remove upstreamed flaky test disabling
- Change to upstream-hosted source URL
- Remove static libraries
- Lint spec
- License verified

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.17-9
- Remove libtool archive files from final packaging

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.17-8
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 1.2.17-7: Fix check tests.

* Mon Sep 05 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.2.17-7
- Remove the Valgrind workaround in the check section.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.17-6
- Added %%license line automatically

* Wed Mar 11 2020 Christopher Co <chrco@microsoft.com> - 1.2.17-5
- Updated Source location

* Mon Mar 09 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.2.17-4
- Fixed URL. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.17-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 20 2018 Ashwin H <ashwinh@vmware.com> - 1.2.17-2
- Fix librelp %check

* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> - 1.2.17-1
- Updated to version 1.2.17

* Tue Apr 11 2017 Harish Udaiy Kumar <hudaiyakumar@vmware.com> - 1.2.13-1
- Updated to version 1.2.13

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.9-2
- GA - Bump release of all rpms

* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
- Upgrade to 1.2.9

* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> - 1.2.7-1
- Initial build. First version
