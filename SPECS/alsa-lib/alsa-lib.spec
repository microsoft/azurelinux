Summary:        ALSA library
Name:           alsa-lib
Version:        1.2.6.1
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Internet
URL:            https://alsa-project.org
Source0:        https://www.alsa-project.org/files/pub/lib/%{name}-%{version}.tar.bz2
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3

%description
The ALSA Library package contains the ALSA library used by programs
(including ALSA Utilities) requiring access to the ALSA sound interface.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.2.6.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jan 4 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.2.6.1-1
- Update to version 1.2.6.1

* Wed May 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.2-2
- Replace python2 dependencies with python3
- License verified

* Thu May 28 2020 Andrew Phelps <anphel@microsoft.com> - 1.2.2-1
- Update to version 1.2.2 to fix CVE-2009-0035

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.9-2
- Added %%license line automatically

* Mon Mar 16 2020 Andrew Phelps <anphel@microsoft.com> - 1.1.9-1
- Update to version 1.1.9. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.1.7-1
- initial version, moved from Vivace
