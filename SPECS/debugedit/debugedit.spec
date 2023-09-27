Summary:      Debugedit - obtain debug information from binaries.
Name:         debugedit
Version:      5.0
Release:      3%{?dist}
License:      GPLv3+
URL:          https://sourceware.org/debugedit/
Vendor:       Microsoft Corporation
Distribution: Mariner
Source0:      https://sourceware.org/ftp/%{name}/%{version}/%{name}-%{version}.tar.xz
Patch0:       BUG-28161.patch
BuildRequires: automake
BuildRequires: binutils

%description
%{summary}

%prep
%autosetup -p1

%build
autoreconf
automake --add-missing
./configure && make

%install
make install

%check
make check
cat tests/testsuite.log

%files
%defattr(-,root,root)
%license COPYING3
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Sep 21 2023 Osama Esmail <osamaesmail@microsoft.com> - 5.0-3
- Replace make_build_check with make build_check

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Oct 08 2021 Mateusz Malisz <mamalisz@microsoft.com> 5.0-1
- Original version for CBL-Mariner
- License verified
