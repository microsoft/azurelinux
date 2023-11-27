Summary:        Library for accessing X.509 and CMS data structure.
Name:           libksba
Version:        1.6.4
Release:        1%{?dist}
# See AUTHORS file for licensing details
License:        (LGPLv3+ or GPLv2+) and GPLv3+ 
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Security/Libraries.
URL:            https://www.gnupg.org/(fr)/download/index.html#libksba
Source0:        https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  libgpg-error-devel >= 1.8
Requires:       libgpg-error >= 1.8

%description
Libksba is a library to make the tasks of working with X.509 certificates,
CMS data and related objects more easy. It provides a highlevel interface
to the implemented protocols and presents the data in a consistent way.

%package        devel
Summary:        Development libraries and header files for libksba
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel >= 1.8

%description    devel
The package contains libraries and header files for
developing applications that use libksba.

%prep
%autosetup

%build
%configure \
    --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_infodir}

%check
%make_build -k check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license AUTHORS COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv3
%{_bindir}/ksba-config
%{_libdir}/%{name}.so.8*

%files devel
%{_libdir}/%{name}.so
%{_datadir}/aclocal/ksba.m4
%{_includedir}/ksba.h
%{_libdir}/pkgconfig/ksba.pc

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.4-1
- Auto-upgrade to 1.6.4 - Azure Linux 3.0 - package upgrades

* Wed Jan 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.6.3-1
- Auto-upgrade to 1.6.3 - to fix CVE-2022-47629

* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 1.6.0-1
- Upgrade to latest upstream version
- Split out development files into a devel subpackage
- Lint spec
- License verified

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.3.5-4
- Provide libksba-devel for base package

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.3.5-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue    Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-1
- Udpated to version 1.3.5

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- BuildRequired libgpg-error-devel.

* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 1.3.4-1
- Initial Build.
