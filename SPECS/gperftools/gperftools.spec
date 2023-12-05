Summary:        A fast malloc tool for threads
Name:           gperftools
Version:        2.12
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/gperftools/gperftools
Source0:        %{url}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

# Using an empty patch to ignoring this CVE because it's considered a false positive.
# For more details see: https://github.com/gperftools/gperftools/issues/1013.
Patch:          CVE-2018-13420.nopatch

%description
gperftools is a collection of a high-performance multi-threaded malloc() implementation, plus some pretty nifty performance analysis tools.

%package devel
Summary:        gperftools devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for gperftools.

%package docs
Summary:        gperftools docs
Group:          Development/Tools
%description docs
The contains gperftools package doc files.

%prep
%setup -q

%build
./configure \
   --prefix=%{_prefix} \
   --docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
TCMALLOC_SAMPLE_PARAMETER=128 && make check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/pprof
%{_bindir}/pprof-symbolize
%{_libdir}/libprofiler*.so.*
%{_libdir}/libtcmalloc*.so.*

%files devel
%{_includedir}/google/*
%{_includedir}/gperftools/*
%{_libdir}/libprofiler*.a
%{_libdir}/libprofiler*.so
%{_libdir}/libtcmalloc*.a
%{_libdir}/libtcmalloc*.so
%{_libdir}/pkgconfig/lib*

%files docs
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.12-1
- Auto-upgrade to 2.12 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.9.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 16 2022 Cameron Baird <cameronbaird@microsoft.com> 2.9.1-1
- Update source to v2.9.1

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.7-4
- Added %%license line automatically

* Mon May 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.7-3
- Marking CVE-2018-13420 as false positive.
- Updated 'Source0` tag.
- License verified.
- Converted tabs to spaces.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 2.7-1
- Update version to 2.7

* Mon Jul 31 2017 Vinay Chang Lee <changlee@vmware.com> 2.5-2
- Fix %check

* Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5-1
- Initial version of gperftools package.
