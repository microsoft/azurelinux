Summary:        Tools for zstd compression and decompression
Name:           zstd
Version:        1.5.5
Release:        2%{?dist}
License:        BSD-3-Clause AND GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://facebook.github.io/zstd/
Source0:        https://github.com/facebook/zstd/releases/download/v%{version}/%{name}-%{version}.tar.gz
Requires:       %{name}-libs = %{version}-%{release}

%description
The zstd package contains programs for compressing and decompressing files

%package        devel
Summary:        Header and development files for zstd
Requires:       %{name} = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}

%description    devel
Header and development files for zstd compression

%package        libs
Summary:        Libraries for zstd
Group:          System Environment/Libraries
Provides:       lib%{name} = %{version}-%{release}

%description    libs
This package contains minimal set of shared zstd libraries.

%package        doc
Summary:        Documentation files for zstd
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation files for zstd

%prep
%autosetup

%build
%make_build
%make_build -C contrib/pzstd %{!?with_asm:ZSTD_NO_ASM=1}

%install
%make_install prefix=%{_prefix}
find %{buildroot} -type f -name "*.a" -delete -print
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/unzstd
%{_bindir}/zstd
%{_bindir}/pzstd
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_bindir}/zstdgrep
%{_bindir}/zstdcat

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%files libs
%license LICENSE COPYING
%{_libdir}/libzstd.so.1*

%files doc
%{_mandir}/man1/*

%changelog
* Tue Jan 16 2024 Andrew Phelps <anphel@microsoft.com> - 1.5.5-2
- Add pzstd binary

* Mon Oct 16 2023 Andrew Phelps <anphel@microsoft.com> - 1.5.5-1
- Upgrade to version 1.5.5
- License verified

* Tue Oct 12 2021 Thomas Crain <thcrain@microsoft.com> - 1.5.0-1
- Upgrade to latest upstream version
- Change license tag to properly reflect dual licensing situation
- Remove licenses from main package (pulled in through libs subpackage)
- Lint spec

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.4.4-2
- Provide libzstd and libzstd-devel

* Sat May 2 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.4.4-1
- Original version for CBL-Mariner.
