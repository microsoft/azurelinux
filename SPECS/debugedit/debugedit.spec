Summary: Debugedit - obtain debug information from binaries.
Name:    debugedit
Version: 5.0
Release: 1%{?dist}
License: GPLv3+
URL:     https://sourceware.org/debugedit/
Vendor:  Microsoft Corporation
Distribution: Mariner
Source0: https://sourceware.org/ftp/%{name}/%{version}/%{name}-%{version}.tar.xz

%description
%{summary}

%prep
%setup -q

%build
%configure
%make_build

%install
%make_install

%check
make check

%files
%defattr(-,root,root)
%license COPYING3
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Oct 08 2021 Mateusz Malisz <mamalisz@microsoft.com> 5.0-1
- Initial CBL-Mariner creation.
