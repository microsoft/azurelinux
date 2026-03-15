Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        The Ogg bitstream file format library
Name:           libogg
Version:        1.3.5
Release:        1%{?dist}
License:        BSD-3-Clause
URL:            http://www.xiph.org/

Source:         https://downloads.xiph.org/releases/ogg/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
Libogg is a library for manipulating Ogg bitstream file formats.
Libogg supports both making Ogg bitstreams and getting packets from
Ogg bitstreams.


%package devel
Summary:        Files needed for development using libogg
Requires:       libogg = %{version}-%{release}
Requires:       pkgconfig
Requires:       automake


%description devel
Libogg is a library used for manipulating Ogg bitstreams. The
libogg-devel package contains the header files and documentation
needed for development using libogg.


%package devel-docs
Summary:        Documentation for developing Ogg applications
BuildArch:      noarch


%description devel-docs
Documentation for developing applications with libogg


%prep
%setup -q


%build
%configure --disable-static
%make_build


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mv $RPM_BUILD_ROOT%{_docdir}/%{name} __installed_docs


%ldconfig_scriptlets


%files
%doc AUTHORS CHANGES COPYING README.md
%{_libdir}/libogg.so.0*


%files devel
%dir %{_includedir}/ogg
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.so
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4


%files devel-docs
%doc __installed_docs/*


%changelog
* Wed Nov 20 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.3.5-1
-License Verified
- Upgrade to version 1.3.5

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.3.4-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:1.3.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 02 2019 Miroslav Lichvar <mlichvar@redhat.com> 2:1.3.4-1
- update to 1.3.4
- include soname in file list

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Miroslav Lichvar <mlichvar@redhat.com> 2:1.3.3-1
- update to 1.3.3
- add gcc to build requirements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:1.3.2-9
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2:1.3.2-4
- Use '|' instead of '/' as pattern delimiter in sed expressions (Fix FTBFS).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Jaromir Capik <jcapik@redhat.com> - 2:1.3.2-1
- Upgrading to 1.3.2
- Cleaning the spec
- Fixing bogus dates in the changelog

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 09 2013 Jaromir Capik <jcapik@redhat.com> - 2:1.3.0-5
- fixing multilib conflict (#831414)

* Tue Mar 26 2013 Jaromir Capik <jcapik@redhat.com> - 2:1.3.0-4
- aarch64 support (#925834)
- minor spec cleaning

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Gregory Maxwell <greg@xiph.org> 1.3.0-1
- libogg 1.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Adam Jackson <ajax@redhat.com> 1.2.2-2
- Fix epoch.

* Tue Dec 07 2010 Adam Jackson <ajax@redhat.com> 1.2.2-1
- libogg 1.2.2

* Mon Apr 26 2010 Adam Jackson <ajax@redhat.com> 1.2.0-1
- libogg 1.2.0

* Tue Nov 10 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 2:1.1.4-3
- fixed libogg-devel-docs (BZ #510608) (By Edward Sheldrake)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.1.4-1
- libogg 1.1.4

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 1.1.4-0.1.rc1
- libogg 1.1.4rc1
- split devel docs to noarch subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2:1.1.3-10
- Rebuild for pkgconfig provides

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.1.3-9
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-8
- Some more small specfile cleanups for merge review (bz 226035)

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-7
- Some small specfile cleanups
- Add smpflags to make invocation (bz 226035)

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2:1.1.3-6
- Don't install Makefile's as %%doc, avoiding a multilib conflict (bz 342281)

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2:1.1.3-5
- Rebuild for PPC toolchain bug

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-4
- Require automake in the -devel package

* Thu Feb  8 2007 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-3
- Package review cleanups
- Don't ship a static library

* Thu Aug 17 2006 Matthias Clasen <mclasen@redhat.com> - 2:1.1.3-2.fc6
- Fix 202280

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:1.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> 2:1.1.3-1
- Update to 1.1.3
- doc/ogg changed to doc/libogg

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 2:1.1.2-2
- rebuild for gcc 4.0

* Wed Sep 29 2004 Colin Walters <walters@redhat.com> 2:1.1.2-1
- Update to 1.1.2
- Delete upstreamed libogg-1.1-64bit.patch
- Delete upstreamed libogg-underquoted.patch

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 2:1.1-4
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 2:1.1-1
- update to 1.1

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 2:1.0-5.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Bill Nottingham <notting@redhat.com> 2:1.0-3
- fix ogg.m4

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2:1.0-2
- remove unpackaged files from the buildroot

* Thu Jul 18 2002 Bill Nottingham <notting@redhat.com> 1.0-1
- one-dot-oh

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.0rc3

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc2

* Fri Jul  6 2001 Bill Nottingham <notting@redhat.com>
- own %%{_includedir}/ogg

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc1

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- beta4

* Tue Feb  6 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Wed Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Mon Dec 11 2000 Bill Nottingham <notting@redhat.com>
- fix bogus group

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- clean up specfile slightly

* Sat Sep 02 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
