# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Upstream was putting changes silently into svn over a number of years
# When they moved to gitlab, this became visible
# It does not seem that they've ever done a proper release since 0.4.8
# Leaving the version as is and using the gitlab source from the latest commit (2021)
%global commit c5830721

# One of the bison-generated parsers uses an int as a List *.  This
# seems to be an actual bug.  However, the parser cannot be
# regenerated with current bison in Fedora.
# <https://bugzilla.redhat.com/show_bug.cgi?id=2256912>
%global build_type_safety_c 1

Name:		libsmi
Version:	0.4.8
Release:	44%{?dist}
Summary:	A library to access SMI MIB information
# lib/parser-smi.c is GPL-2.0-or-later, but with the Bison exception that says it can be used under any terms
# as part of the larger libsmi work, so we are choosing to use it under the core libsmi licenses instead.
License:	TCL AND BSD-3-Clause
URL:		http://www.ibr.cs.tu-bs.de/projects/libsmi/index.html
Source0:	https://gitlab.ibr.cs.tu-bs.de/nm/libsmi/-/archive/%{commit}/libsmi-%{commit}.tar.gz
Source1:	smi.conf
Source2:	IETF-MIB-LICENSE.txt
Patch0:		libsmi-0.4.8-wget111.patch
Patch2:		libsmi-c5830721-symbols-clash.patch
Patch4:		libsmi-c5830721-configure-c99.patch
Patch5:		libsmi-c99.patch
Patch6:		libsmi-c5830721-fix-missing-declaration.patch
Patch7:		libsmi-c5830721-switch-fixes.patch
Patch8:		libsmi-c5830721-include-fix.patch
Patch9:		libsmi-c5830721-missing-semicolon.patch
Patch10:	libsmi-c5830721-cleanups.patch
Patch11:	libsmi-c5830721-test-fix-typo.patch
BuildRequires:	libtool
BuildRequires:	flex, bison
BuildRequires:	make
Requires:	gawk, wget

%description
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains tools to check, dump, and convert MIB
definitions and a steadily maintained and revised archive
of all IETF and IANA maintained standard MIB modules.


%package devel
Summary:	Development environment for libsmi library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains development files needed to develop
libsmi-based applications.

%prep
%setup -q -n %{name}-%{commit}
%patch -P 0 -p1 -b .wget111
%patch -P 2 -p1 -b .clash
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1 -b .fix-missing-declaration
%patch -P 7 -p1 -b .switch-fixes
%patch -P 8 -p1 -b .include-fix
%patch -P 9 -p1 -b .missing-semicolon
%patch -P 10 -p1 -b .cleanups
%patch -P 11 -p1 -b .fix-test-typo

# We need to prime the pump here.
pushd lib
bison -v -t -d -psming parser-sming.y
bison -v -t -d -pyang parser-yang.y
popd
cp %{SOURCE2} .

%build
%set_build_flags
export CFLAGS="$CFLAGS -std=gnu99"
autoreconf -iv
%configure \
    --enable-smi \
    --enable-sming \
    --enable-shared \
    --with-yangdir=%{_datadir}/libsmi-yang/ \
    --disable-static
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

iconv -f latin1 -t utf-8 <COPYING >COPYING.utf8
mv COPYING.utf8 COPYING

%install
rm -rf $RPM_BUILD_ROOT
%{make_install}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/smi.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
# fails a couple of tests (2 in {0.4.4, 0.4.5}, 3 as of 2024-01-03)
# BUT... it shouldn't segfault or crash.
make check ||:

%ldconfig_scriptlets


%files
%doc ANNOUNCE ChangeLog COPYING README THANKS TODO
%doc doc/draft-irtf-nmrg-sming-02.txt smi.conf-example
%doc IETF-MIB-LICENSE.txt
%config(noreplace) %{_sysconfdir}/smi.conf
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/mibs/
%{_datadir}/pibs/
%{_datadir}/libsmi-yang/
%{_mandir}/man1/*.1*

%files devel
%{_datadir}/aclocal/libsmi.m4
%{_libdir}/pkgconfig/libsmi.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*.3*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 14 2024 Tom Callaway <spot@fedoraproject.org> - 0.4.8-40
- update license tag to reflect reality (thanks to mhlavink)

* Thu Feb 15 2024 Tom Callaway <spot@fedoraproject.org> - 0.4.8-39
- move yang files to avoid conflict with frr

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Florian Weimer <fweimer@redhat.com> - 0.4.8-37
- C type-safety level downgrade due to pointer/int conversion bugs (#2256912)

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan  5 2024 Tom Callaway <spot@fedoraproject.org> - 0.4.8-35
- update to the latest available source tree, cleanup as much as we can

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 14 2023 Florian Weimer <fweimer@redhat.com> - 0.4.8-33
- Port to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar  5 2018 Tom Callaway <spot@fedoraproject.org> - 0.4.8-22
- rebuild to get more LDFLAGS through libtool (bz1548707)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec  3 2013 Tom Callaway <spot@fedoraproject.org> - 0.4.8-13
- fix format-security issues

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Tom Callaway <spot@fedoraproject.org> - 0.4.8-11
- add IETF MIB license text to resolve legal issue

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Tom Callaway <spot@fedoraproject.org> - 0.4.8-9
- mark symbols which conflict with RPM as "internal", resolves bz 864324
  Thanks to Michele Baldessari

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.8-5
- fix CVE-2010-2891

* Thu Feb 25 2010 Radek Vokal <rvokal@redhat.com> - 0.4.8-4
- fix lincese field, based on the tarball project is now GPL+

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.4.8-1
- update to 0.4.8
- patch fix for bz 441944

* Tue Feb 12 2008 Adam Jackson <ajax@redhat.com> 0.4.5-4
- Add %%defattr. (#430298)

* Thu Jan 10 2008 Stepan Kasal <skasal@redhat.com> - 0.4.5-3
- libsmi-devel should not require automake
- convert COPYING to utf-8

* Fri Oct  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.5-2
- Handle rpath problems in 64-bit systems (#209522).

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.5-1
- Update to 0.4.5.

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.4-1
- Update to 0.4.4.

* Fri Apr  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.3-1
- First build.

# vim:set ai ts=4 sw=4 sts=4 et:
