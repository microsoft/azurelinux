%define         underscore_version %(echo %{version} | cut -d. -f1-3 --output-delimiter="_")
# Do not create debuginfo sub-package because there is no binary executable
%global debug_package %{nil}

Summary:        Compiler built-ins
Name:           libecb
Version:        9.30
Release:        2%{?dist}
License:        BSD OR GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://software.schmorp.de/pkg/libecb.html
# Below link points to the correct revision of the sources but doesn't give tarballs with reproducible hashes.
# How to re-build this file for CBL-Mariner in a reproducible way:
#   1. cvs -d :pserver:anonymous@cvs.schmorp.de/schmorpforge export -r rxvt-unicode-rel-%%{underscore_version} %%{name}
#   2. mv %%{name} %%{name}-%%{version}
#   3. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}.tar.gz %%{name}-%%{version}
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source0:        https://cvs.schmorp.de/libecb/?view=tar&pathrev=rxvt-unicode-rel-%{underscore_version}#/%{name}-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  perl-podlators

%description
This project delivers you many GCC built-ins, attributes and a number of
generally useful low-level functions, such as popcount, expect, prefetch,
noinline, assume, unreachable and so on.

This is a dummy package. All the useful files are delivered by %{name}-devel
package.

%package devel
Summary:        Compiler built-ins
# Packaging guidelines require header-only packages:
# to be architecture-specific, to deliver headers in -devel package, to
# provide -static symbol for reverse build-requires.
# Replace libecb package:
Provides:       libecb-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libecb = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libecb < 0.20150218

%description devel
This project delivers you many GCC built-ins, attributes and a number of
generally useful low-level functions, such as popcount, expect, prefetch,
noinline, assume, unreachable and so on.

%prep
%autosetup -p1

%build
pod2man ecb.pod > ecb.3

%install
install -d %{buildroot}%{_includedir}
install -m 0644 -t %{buildroot}%{_includedir} *.h
install -d %{buildroot}%{_mandir}/man3
install -m 0644 -t %{buildroot}%{_mandir}/man3 *.3

%files devel
%license LICENSE
%doc Changes README
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Tue Apr 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.30-2
- Fixing "%%underscore_version" macro definition.

* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.30-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Switching to using CVS revision tag as version.
- License verified.

* Fri Dec 17 2021 Petr Pisar <ppisar@redhat.com> - 0.20211217-1
- CVS snapshot taken on 20211217 (Fedora patches merged)

* Thu Oct 21 2021 Petr Pisar <ppisar@redhat.com> - 0.20211021-1
- CVS snapshot taken on 2021-10-21 (added ECB_64BIT_NATIVE, ecb_i2a,
  ecb_ptrmix)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20200430-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20200430-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20200430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 30 2020 Petr Pisar <ppisar@redhat.com> - 0.20200430-1
- CVS snapshot taken on 2020-04-30 (added ECB_OPTIMIZE_SIZE, unaligned load and
  store, host order conversions, bit rotations)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20190722-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20190722-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Petr Pisar <ppisar@redhat.com> - 0.20190722-1
- CVS snapshot taken on 2019-07-22 (ECB_MEMORXY_FENCE_RELAXED memory fence
  added, use the memory barriers of a C++ compiler)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20181119-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Petr Pisar <ppisar@redhat.com> - 0.20181119-1
- CVS snapshot taken on 2018-11-19 (release memory fence switched to a memory
  barrier on x86 and x86_64 platforms, support for ISO C14 and C17 added)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161208-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161208-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161208-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161208-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161208-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Petr Pisar <ppisar@redhat.com> - 0.20161208-1
- CVS snapshot taken on 2016-12-08 (documentation updated)

* Tue Feb 09 2016 Petr Pisar <ppisar@redhat.com> - 0.20160209-1
- CVS snapshot taken on 2016-02-09 (improved ecb_binary16_to_float,
  ecb_float_to_binary16, ecb_binary16_to_binary32, ecb_binary32_to_binary16
  added, ecb_byteorder_helper changed prototype)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150608-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20150608-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Petr Pisar <ppisar@redhat.com> - 0.20150608-1
- CVS snapshot taken on 2015-06-08 (new macros, more documentation, better
  compatibility with x86_64 compilers)

* Wed Feb 18 2015 Petr Pisar <ppisar@redhat.com> - 0.20150218-1
- CVS snapshot taken on 2015-02-18 (C11 compliance)
- Replace libecb package with libecb-devel, users should build-require
  libecb-static

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 0.20141029-1
- CVS snapshot taken on 2014-10-29
- License changed from (BSD) to (BSD or GPLv2+)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130509-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130509-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Petr Pisar <ppisar@redhat.com> - 0.20130509-1
- CVS snapshot taken on 2013-05-09

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Petr Pisar <ppisar@redhat.com> - 0.20121022-1
- CVS snapshot taken on 2012-10-22

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 0.20121008-1
- CVS snapshot taken on 2012-10-08
- Fix for building on big-endian systems (bug #863991)
