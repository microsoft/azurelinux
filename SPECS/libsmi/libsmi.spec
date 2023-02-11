Summary:        A library to access SMI MIB information
Name:           libsmi
Version:        0.4.8
Release:        28%{?dist}
License:        TCL AND BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.ibr.cs.tu-bs.de/projects/libsmi/index.html
#Upstream Source0 url is dead
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
Source1:        smi.conf
Source2:        IETF-MIB-LICENSE.txt
Patch0:         libsmi-0.4.8-wget111.patch
Patch1:         CVE-2010-2891.patch
Patch2:         libsmi-0.4.8-symbols-clash.patch
Patch3:         libsmi-0.4.8-format-security-fix.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool
Requires:       gawk
Requires:       wget

%description
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains tools to check, dump, and convert MIB
definitions and a steadily maintained and revised archive
of all IETF and IANA maintained standard MIB modules.

%package devel
Summary:        Development environment for libsmi library
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains development files needed to develop
libsmi-based applications.

%prep
%setup -q
%patch0 -p1 -b .wget111
%patch1 -p1 -b .CVE-2010-2891
%patch2 -p1 -b .clash
%patch3 -p1 -b .format-security
cp %{SOURCE2} .

%build
%configure \
    --enable-smi \
    --enable-sming \
    --enable-shared \
    --disable-static
%make_build LIBTOOL=%{_bindir}/libtool

iconv -f latin1 -t utf-8 <COPYING >COPYING.utf8
mv COPYING.utf8 COPYING

%install

%make_install

install -d -m 755 %{buildroot}%{_sysconfdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/smi.conf

rm -f %{buildroot}%{_libdir}/*.a
find %{buildroot} -type f -name "*.la" -delete -print

%check
# fails a couple of tests (2 in {0.4.4, 0.4.5})
make check ||:

%ldconfig_scriptlets


%files
%license COPYING IETF-MIB-LICENSE.txt
%doc ANNOUNCE ChangeLog README THANKS TODO
%doc doc/draft-irtf-nmrg-sming-02.txt smi.conf-example
%config(noreplace) %{_sysconfdir}/smi.conf
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/mibs/
%{_datadir}/pibs/
%{_mandir}/man1/*.1*

%files devel
%{_datadir}/aclocal/libsmi.m4
%{_libdir}/pkgconfig/libsmi.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Feb 03 2023 Riken Maharjan <rmaharjan@microsoft.com> - 0.4.8-28
- Move from extended to core.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.8-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
