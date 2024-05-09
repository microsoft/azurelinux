Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Database Independent Abstraction Layer for C
Name: libdbi
Version: 0.9.0
Release: 16%{?dist}
License: LGPLv2+
URL: https://libdbi.sourceforge.net/

Source: https://prdownloads.sourceforge.net/libdbi/%{name}-%{version}.tar.gz

# add support for aarch64 to the shipped old automake files
# -> fixed in upstream (see https://sourceforge.net/p/libdbi/mailman/message/31868578/)
#    but upstream haven't realeased new version yet
Patch1: libdbi-aarch64.patch

BuildRequires: openjade docbook-style-dsssl
BuildRequires: gcc
Conflicts: libdbi-dbd-mysql < 0.8
Conflicts: libdbi-dbd-pgsql < 0.8

%description
libdbi implements a database-independent abstraction layer in C, similar to the
DBI/DBD layer in Perl. Writing one generic set of code, programmers can
leverage the power of multiple databases and multiple simultaneous database
connections by using this framework.

The libdbi package contains just the libdbi framework.  To make use of
libdbi you will also need one or more plugins from libdbi-drivers, which
contains the plugins needed to interface to specific database servers.

%package devel
Summary: Development files for libdbi (Database Independent Abstraction Layer for C)
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The libdbi-devel package contains the header files and documentation
needed to develop applications with libdbi.

%package doc
Summary: Documentation for libdbi (Database Independent Abstraction Layer for C)
BuildArch: noarch

%description doc
The libdbi-doc package contains guides for development of applications with libdbi.



%prep
%setup -q -n %{name}-%{version}

%patch 1 -p1

%build
%configure

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdbi.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdbi.la

# we will include generated documentation in -devel subpackage,
# so we need to remove it from builddir, since it would be included
# automatically otherwise
rm -rf ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}

%ldconfig_scriptlets

%files
%doc AUTHORS
%doc ChangeLog
%doc README
%doc NEWS
%license COPYING
%{_libdir}/libdbi.so.*

%files devel
%doc TODO
%{_includedir}/dbi/
%{_libdir}/libdbi.so
%{_libdir}/pkgconfig/dbi.pc

%files doc
%license COPYING
%doc doc/programmers-guide.pdf
%doc doc/programmers-guide/
%doc doc/driver-guide.pdf
%doc doc/driver-guide/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 0.9.0-11
- Add missing BuildRequires: gcc/gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Marek Skalicky <mskalick@redhat.com> - 0.9.0-4
- Add doc subpackage
- Change license handling

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Jan Pacner <jpacner@redhat.com> - 0.9.0-1
- new version: 0.9.0

* Mon Jul 29 2013 Honza Horak <hhorak@redhat.com> - 0.8.4-4
- Spec file clean-up
- Add aarch64 support
- Remove generated doc to not be included automatically

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Tom Lane <tgl@redhat.com> 0.8.4-2
- Prevent undesirable change in library soname version number

* Sun Jul 22 2012 Tom Lane <tgl@redhat.com> 0.8.4-1
- Update to version 0.8.4 (seems to contain only configure-support updates,
  but might as well adopt it)
- Fix memory leak due to incorrect test in _is_row_fetched()
Related: #733413

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  3 2010 Tom Lane <tgl@redhat.com> 0.8.3-4
- Do not use -ffast-math; it breaks things and seems quite unlikely to offer
  any useful performance benefit for this type of package, anyway
Resolves: #629964

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 0.8.3-1
- Update to version 0.8.3.

* Tue Oct 30 2007 Tom Lane <tgl@redhat.com> 0.8.2-3
- Fix package's selection of CFLAGS to include RPM_OPT_FLAGS
Resolves: #330681

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-2
- Fix typo in Release field.

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-1
- Update to version 0.8.2.
- Update License tag to match code.
- Remove static library and .la file, per packaging guidelines.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-2.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.8.1-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 0.8.1-1
- Update to version 0.8.1.

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 0.7.2-2
- Packaging improvements per discussion with sopwith.

* Thu Mar 10 2005 Tom Lane <tgl@redhat.com> 0.7.2-1
- Import new libdbi version, splitting libdbi-drivers into a separate SRPM
  so we can track new upstream packaging.

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 0.6.5-11
- Rebuild with gcc4.

* Mon Nov 08 2004 Tom Lane <tgl@redhat.com> 0.6.5-10
- build against mysqlclient10, not mysql, for license reasons

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jul 03 2003 Patrick Macdonald <patrickm@redhat.com> 0.6.5-7
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 24 2003 Tom Lane <tgl@redhat.com>
- /usr/include/dbi should be owned

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 01 2002 Elliot Lee <sopwith@redhat.com> 0.6.5-3
- multilibify

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.6.5-1
- 0.6.5

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.6.4-2
- 0.6.4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Sep 20 2001 Trond Eivind Glomsrd <teg@redhat.com> 0.6.2-1
- Sanitize, prepare for distribution

* Sat Aug 4 2001 David Parker <david@neongoat.com>
- initial spec file created
