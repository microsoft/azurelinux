Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global rcver %{nil}

Name:		libgadu
Version:	1.12.2
Release:	11%{?dist}
Summary:	A Gadu-gadu protocol compatible communications library
License:	LGPLv2
Source0:	https://github.com/wojtekka/libgadu/releases/download/%{version}%{?rcver}/libgadu-%{version}%{?rcver}.tar.gz
Patch0:	libgadu-1.12.2-gcc10.patch
URL:		https://libgadu.net/
BuildRequires:  gcc
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	gnutls-devel
BuildRequires:	gsm-devel
BuildRequires:	libxml2-devel
# protobuf-c-1.0.0 is an incompatible update from 0.15
BuildRequires:	protobuf-c-devel >= 1.0.0
BuildRequires:	speex-devel
BuildRequires:	zlib-devel

%description
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -l pl
libgadu umożliwia łatwe dodanie do różnych aplikacji komunikacji
bazującej na protokole Gadu-Gadu.

%package devel
Summary:	Libgadu development library
Summary(es):	Biblioteca de desarrollo de libgadu
Summary(pl):	Część biblioteki libgadu dla programistów
Requires:	libgadu = %{version}-%{release}
Requires:	pkgconfig

%description devel
The libgadu-devel package contains the header files necessary
to develop applications with libgadu.

%description devel -l pl
Pakiet libgadu-devel zawiera pliki nagłówkowe potrzebne
do kompilowania aplikacji korzystających z libgadu.

%package doc
Summary:	Libgadu library developer documentation
Summary(pl):	Dokumentacja biblioteki libgadu dla programistów
Requires:	libgadu = %{version}-%{release}
BuildArch:	noarch

%description doc
The libgadu-doc package contains the documentation for the
libgadu library.

%description doc -l pl
Pakiet libgadu-doc zawiera dokumentację biblioteki libgadu.

%prep
%setup -q -n %{name}-%{version}%{?rcver}
%patch 0 -p1 -b .gcc10

# bug 1126750: touch to force rebuild with protobuf-c-1.0.0 (incompatible with 0.15)
touch packets.proto

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--without-openssl \
	--with-pthread

make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check

%ldconfig_scriptlets

%files
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/libgadu.so.*

%files devel
%{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_libdir}/pkgconfig/*

%files doc
%doc docs/protocol.html docs/html

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.2-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 24 2020 Than Ngo <than@redhat.com> - 1.12.2-10
- Fixed FTBFS

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.12.2-1
- update to 1.12.2 release
- add missing BRs for the remaining tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.12.1-1
- update to 1.12.1 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-3
- fix build with new protobuf-c (bug 1126750)

* Wed Aug  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.0-2
- Rebuild (protobuf-c)

* Wed Jul 23 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-1
- update to 1.12.0 release
- drop obsolete patches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-0.6.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.5.rc3
- fix crash in resolver test on i686

* Thu May 22 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.4.rc3
- update to 1.12.0-rc3 (fixes CVE-2014-3775)
- fix hash testcase compilation

* Tue Feb 11 2014 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.3.rc2
- update to 1.12.0-rc2 (fixes CVE-2013-6487)

* Wed Dec 11 2013 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.2.rc1
- update to 1.12.0-rc1
- drop attr from file list

* Wed Nov 06 2013 Dominik Mierzejewski <rpm@greysector.net> - 1.12.0-0.1.20131101git3f1b8ce
- update to 1.12.0 prerelease from git (fixes CVE-2013-4488)
- update Source and URL to new location
- clean up spec file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Dominik Mierzejewski <rpm@greysector.net> 1.11.2-1
- updated to 1.11.2 (bug 782047)
- dropped obsolete patch
- fix build (Dan Winship, bug 851676)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Dominik Mierzejewski <rpm@greysector.net> 1.11.0-2
- fixed TLS usage via gnutls (rhbz #718619)

* Sat Jun 04 2011 Dominik Mierzejewski <rpm@greysector.net> 1.11.0-1
- updated to 1.11.0
- enabled gsm/speex to support voice connections
- enabled zlib to support GG10 contact list import/export

* Mon Mar 14 2011 Dominik Mierzejewski <rpm@greysector.net> 1.10.1-1
- updated to 1.10.1

* Sun Feb 27 2011 Dominik Mierzejewski <rpm@greysector.net> 1.10.0-1
- updated to 1.10.0 final
- enabled SSL support via gnutls
- added API docs to -doc
- updated summaries and descriptions for -devel

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.1-1
- updated to 1.9.1

* Wed May 19 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-1
- updated to 1.9.0 final

* Sun Mar 14 2010 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.4.rc3
- updated to 1.9.0-rc3
- adds basic support for new GG protocol (UTF-8 and new status messages)
- full upstream changelog (Polish only) https://toxygen.net/libgadu/releases/1.9.0-rc3.html
- drop Requires: openssl-devel from -devel subpackage

* Sun Dec 06 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.3.rc2
- disabled OpenSSL support (not used in practice),
  fixes license trouble for GPL apps

* Sun Dec 06 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.2.rc2
- updated to 1.9.0-rc2

* Sun Sep 13 2009 Dominik Mierzejewski <rpm@greysector.net> 1.9.0-0.1.rc1
- updated to 1.9.0-rc1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.2-5
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.8.2-2
- rebuild with new openssl

* Sun Oct 26 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.2-1
- updated to 1.8.2 (security update)
- preserve timestamps during make install
- put defattr at the top of files section (fixes rpmlint error)

* Wed Jun 18 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.1-1
- updated to 1.8.1

* Sun Feb 24 2008 Dominik Mierzejewski <rpm@greysector.net> 1.8.0-1
- updated to 1.8.0

* Sat Feb 16 2008 Dominik Mierzejewski <rpm@greysector.net> 1.7.2-1
- updated to 1.7.2

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.7.1-3
 - Rebuild for deps

* Sun Aug 26 2007 Dominik Mierzejewski <rpm@greysector.net> 1.7.1-2
- rebuild for BuildID
- update license tag

* Wed Apr 25 2007 Dominik Mierzejewski <rpm@greysector.net> 1.7.1-1
- updated to 1.7.1 (security fixes)

* Sun Sep 17 2006 Dominik Mierzejewski <rpm@greysector.net> 1.7.0-1
- initial build
