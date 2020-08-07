Summary:        Tools for zstd compression and decompression
Name:           zstd
Version:        1.4.4
Release:        1%{?dist}
URL:            https://facebook.github.io/zstd/
License:        BSD and GPLv2
Group:          Applications/File
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/facebook/zstd/releases/download/v%{version}/%{name}-%{version}.tar.gz

Requires:       zstd-libs = %{version}-%{release}

%description
The zstd package contains programs for compressing and decompressing files

%package devel
Summary:        Header and development files for zstd
Requires:       %{name} = %{version}-%{release}
%description    devel
Header and development files for zstd compression

%package libs
Summary:        Libraries for zstd
Group:          System Environment/Libraries
%description libs
This package contains minimal set of shared zstd libraries.

%package doc
Summary:        Documentation files for zstd
Requires:       %{name} = %{version}-%{release}
%description doc
Documentation files for zstd

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix}
rm %{buildroot}%{_libdir}/libzstd.a

%check
make check %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE COPYING
%{_bindir}/zstd
%{_bindir}/zstdless
%{_bindir}/zstdmt
%{_bindir}/unzstd
%{_bindir}/zstdgrep
%{_bindir}/zstdcat

%files devel
%exclude %{_includedir}/zbuff.h
%{_includedir}/*.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so


%files libs
%license LICENSE COPYING
%{_libdir}/libzstd.so.*

%files doc
%{_mandir}/man1/*

%changelog
*   Sat May 2 2020 Henry Beberman <henry.beberman@microsoft.com> 1.4.4-1
-   Original version for CBL-Mariner.
