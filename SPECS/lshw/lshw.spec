Summary:        Hardware lister
Name:           lshw
Version:        B.02.19.2
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://ezix.org/src/pkg/lshw/tags
Source0:        https://www.ezix.org/software/files/%{name}-%{version}.tar.gz

%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory configuration,
firmware version, mainboard configuration, CPU version and speed, cache
configuration, bus speed, etc. Information can be displayed in plain text,
XML or HTML.

%package docs
Summary:        lshw docs
Group:          Applications/System

%description docs
The package contains lshw doc files.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/lshw

%files docs
%defattr(-,root,root)
%{_datadir}/*

%changelog
* Wed Nov 22 2023 Aditya Dubey <adityadubey@microsoft.com> - B.02.19.2-1
- Upgrade to B.02.19.2
- Updated Source0

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - B.02.19-1
- Upgrade to B.02.19
- Fix Source0

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - B.02.18-4
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - B.02.18-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> B.02.18-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
- Initial version of lshw package for Photon.
