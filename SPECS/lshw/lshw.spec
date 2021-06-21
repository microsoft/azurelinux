Summary:        Hardware lister
Name:           lshw
Version:        B.02.18
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/lyonel/lshw/releases
Source0:        http://www.ezix.org/software/files/%{name}-%{version}.tar.gz
%define sha1 lshw=c0240f5e53cf40769d52e316719e8010ea6bdea3
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner

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
/usr/share/*

%changelog
* Sat May 09 00:21:24 PST 2020 Nick Samson <nisamson@microsoft.com> - B.02.18-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> B.02.18-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*    Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> B.02.18-1
-    Initial version of lshw package for Photon.
