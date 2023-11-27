Summary:        Provides IPC between GnuPG Components
Name:           libassuan
Version:        2.5.6
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://gnupg.org/software/libassuan/index.html
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  libgpg-error-devel >= 1.21
Requires:       libgpg-error >= 1.21

%description
The libassuan package contains an inter process communication library
used by some of the other GnuPG related packages. libassuan's primary use
is to allow a client to interact with a non-persistent server.
libassuan is not, however, limited to use with GnuPG servers and clients.
It was designed to be flexible enough to meet the demands
of many transaction based environments with non-persistent servers.

%package        devel
Summary:        Development files for libassuan
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel >= 1.21

%description    devel
This package contains development files for libassuan

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}/%{_infodir}

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license AUTHORS COPYING
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so.0*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/assuan.h
%{_datadir}/aclocal/*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.5.6-1
- Auto-upgrade to 2.5.6 - Azure Linux 3.0 - package upgrades

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 2.5.5-2
- Remove manual pkgconfig(*) provides in toolchain specs

* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 2.5.5-1
- Upgrade to latest upstream version
- Split out development files into devel subpackage
- Lint spec
- License verified

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 2.5.1-5
- Provide pkgconfig(libassuan).

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.5.1-4
- Provide libassuan-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.5.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.5.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> - 2.5.1-1
- Update to version 2.5.1

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> - 2.4.3-1
- Upgrade version to 2.4.3

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.4.2-3
- BuildRequired libgpg-error-devel.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.4.2-2
- GA - Bump release of all rpms

* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.4.2-1
- Updated to version 2.4.2

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> - 2.2.0-2
- Updated group.

* Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> - 2.2.0-1
- Initial version
