Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A library for interfacing IEEE 1284-compatible devices
Name: libieee1284
Version: 0.2.11
Release: 33%{?dist}
License: GPLv2+
URL: https://cyberelk.net/tim/libieee1284/
Source0: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch1: libieee1284-strict-aliasing.patch
Patch2: libieee1284-aarch64.patch
BuildRequires:  gcc
BuildRequires: xmlto

%description
The libieee1284 library is for communicating with parallel port devices.

%package devel
Summary: Files for developing applications that use libieee1284
Requires: %{name} = %{version}-%{release}

%description devel
The header files, static library, libtool library and man pages for
developing applications that use libieee1284.

%prep
%setup -q
# Fixed strict aliasing warnings (bug #605170).
%patch 1 -p1 -b .strict-aliasing

# Add support for building on aarch64 (bug #925774).
%patch 2 -p1 -b .aarch64

%build
touch doc/interface.xml
%configure --without-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/python*/*/*a
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%files
%doc README COPYING TODO AUTHORS NEWS
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%{_includedir}/ieee1284.h
%{_libdir}/*.so
%{_mandir}/*/*

%ldconfig_scriptlets

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.11-33
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.11-29
- Subpackage python2-libieee1284 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.11-26
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.11-25
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.11-24
- Python 2 binary package renamed to python2-libieee1284
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-20
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 30 2013 Tim Waugh <twaugh@redhat.com> 0.2.11-14
- Add support for building on aarch64 (bug #925774).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 23 2010 Tim Waugh <twaugh@redhat.com> 0.2.11-9
- The python sub-package now requires the exactly-matching main
  package (bug #605169).
- Fixed strict aliasing warnings (bug #605170).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Tim Waugh <twaugh@redhat.com> 0.2.11-7
- Package review fix: removed trailing dot in python package summary
  (bug #226031).

* Thu May 14 2009 Tim Waugh <twaugh@redhat.com> 0.2.11-6
- Package review fixes (bug #226031):
  - Drop prereq on ldconfig.
  - Removed trailing dot in devel package summary.
  - Fixed devel package requirement on main package.
  - Use SMP make flags.
  - Removed static libraries and la files.
  - Fixed source URL.
  - Make sure timestamps are preserved on install.
  - Ship AUTHORS and NEWS.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.2.11-4
- Rebuild for Python 2.6

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 0.2.11-3
- Don't build PDF documentation as this creates multilib conflicts.

* Wed Jan  9 2008 Tim Waugh <twaugh@redhat.com> 0.2.11-2
- Rebuilt.

* Tue Sep 18 2007 Tim Waugh <twaugh@redhat.com> 0.2.11-1
- 0.2.11 (bug #246406).

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 0.2.9-5
- Added dist tag.
- Fixed summary.
- Better buildroot tag.
- More specific license tag.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.2.9-4
- rebuild against python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.9-3.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.9-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.9-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Tim Waugh <twaugh@redhat.com> 0.2.9-3
- Rebuild man pages.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.2.9-2
- Rebuild for new GCC.

* Thu Jan 20 2005 Tim Waugh <twaugh@redhat.com> 0.2.9-1
- 0.2.9.
- Build requires python-devel.
- Ship Python extension module.

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 0.2.8-4 
- add Prereq: /sbin/ldconfig

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  9 2003 Tim Waugh <twaugh@redhat.com> 0.2.8-1
- Initial Red Hat Linux package.

* Wed Feb 26 2003 Tim Waugh <twaugh@redhat.com>
- Use the Makefile rule to build the PDF.

* Sat Aug 24 2002 Tim Waugh <twaugh@redhat.com>
- Ship test program.

* Sat Aug  3 2002 Tim Waugh <twaugh@redhat.com>
- The archive is now distributed in .tar.bz2 format.

* Fri Apr 26 2002 Tim Waugh <twaugh@redhat.com>
- No need to create man page symlinks any more.
- Build requires xmlto now, not docbook-utils.

* Wed Apr 24 2002 Tim Waugh <twaugh@redhat.com>
- The tarball builds its own man pages now; just adjust the symlinks.
- Run ldconfig.

* Mon Jan  7 2002 Tim Waugh <twaugh@redhat.com>
- Ship the PDF file with the devel package.

* Thu Nov 15 2001 Tim Waugh <twaugh@redhat.com>
- Initial specfile.
