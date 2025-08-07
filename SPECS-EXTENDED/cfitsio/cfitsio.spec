Summary:        Library for manipulating FITS data files
Name:           cfitsio
Version:        4.5.0
Release:        1%{?dist}
License:        CFITSIO
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://heasarc.gsfc.nasa.gov/fitsio/
Source0:        https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{name}-%{version}.tar.gz
Patch:          cfitsio-noversioncheck.patch
 
BuildRequires: gcc-gfortran
BuildRequires: make
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: curl-devel
 
%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing 
data files in FITS (Flexible Image Transport System) data format. CFITSIO 
simplifies the task of writing software that deals with FITS files by 
providing an easy to use set of high-level routines that insulate the 
programmer from the internal complexities of the FITS file format. At the 
same time, CFITSIO provides many advanced features that have made it the 
most widely used FITS file programming interface in the astronomical 
community.
 
%package devel
Summary: Headers required when building programs against cfitsio
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
 
%description devel
Headers required when building a program against the cfitsio library.
 
%package static
Summary: Static cfitsio library
 
%description static
Static cfitsio library; avoid use if possible.
 
%package docs
Summary: Documentation for cfitsio
BuildArch:  noarch
 
%description docs
Stand-alone documentation for cfitsio.
 
%package utils
Summary: CFITSIO based utilities
Requires: %{name} = %{version}-%{release}
Provides: fpack{?_isa} = %{version}-%{release}
Obsoletes: fpack <= 4.5.0-1  
Provides: fitsverify{?_isa} = 4.22-5
Obsoletes: fitsverify <= 4.22-4
 
%description utils
This package contains utility programas provided by CFITSIO
 
%prep
%autosetup -p1
 
%build
%configure --enable-reentrant -with-bzip2 --includedir=%{_includedir}/%{name}
make %{?_smp_mflags}
 
%check
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std
 
%install
make DESTDIR=%{buildroot} install
#
rm %{buildroot}/%{_bindir}/cookbook
rm %{buildroot}/%{_bindir}/smem
rm %{buildroot}/%{_bindir}/speed
 
%ldconfig_scriptlets
%files
%doc README.md ChangeLog
%license licenses/License.txt
%{_libdir}/libcfitsio.so.10*
 %{_libdir}/libcfitsio.la
 
%files devel
%doc utilities/cookbook.*
%{_includedir}/%{name}
%{_libdir}/libcfitsio.so
%{_libdir}/pkgconfig/cfitsio.pc
 
%files static
%license licenses/License.txt
%{_libdir}/libcfitsio.a
 
%files docs
%doc docs/fitsio.pdf docs/cfitsio.pdf
%license licenses/License.txt
 
%files utils
%doc docs/fpackguide.pdf
%license licenses/License.txt
%{_bindir}/fitsverify
%{_bindir}/fitscopy
%{_bindir}/fpack
%{_bindir}/funpack
%{_bindir}/imcopy

%changelog
* Thu Nov 28 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 4.5.0-1
- Upgrade to version 4.5.0

* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 4.0.0-5
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified

* Thu Jan 05 2023 Kalev Lember <klember@redhat.com> - 4.0.0-4
- Use make_install macro

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 4.0.0-1
- New upstream version 4.0.0

* Sun Aug 01 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 3.490-4
- Remove rpath in utilities

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.490-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.490-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 3.490-1
- Update to 3.490

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.470-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.470-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 01 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 3.470-1
- Update to 3.470
- Patch to revert bogus soname increase
- Patch to fix fprintf format errors

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.450-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 3.450-1
- Update to 3.450 (fixes bz #1570484)
- Patch to use LDFLAGS (fixes bz #1547590)

* Mon Mar 12 2018 Christian Dersch <lupinix@fedoraproject.org> - 3.430-1
- new version

* Fri Feb 23 2018 Christian Dersch <lupinix@mailbox.org> - 3.420-1
- new version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.370-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 02 2017 Christian Dersch <lupinix@mailbox.org> - 3.370-10
- Fix hcompress

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.370-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.370-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.370-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.370-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.370-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 3.370-4
- Remove glibc-headers from devel requires (fixes bz #1230471)

* Thu Sep 18 2014 Orion Poplawski <orion@cora.nwra.com> - 3.370-3
- Ship cookbook example in -devel docs

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.370-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 3.370-1
- New upstream (3.370)
- Patches for ppc64le and aarch64 added upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.360-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 3.360-3
- Add ppc64le support (bz #1097248).

* Tue Apr 15 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.360-2
- Add AArch64 support.

* Mon Dec 09 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.360-1
- New upstream (3.360)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.350-1
- New upstream source (3.350)
- Upstream provides soname
- pkgconfig file rearrangement now a patch instead of using sed

* Thu Mar 21 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.340-1
- New upstream source

* Tue Mar 19 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.330-4
- Using libcfitsio-version.so.0 as soname

* Tue Mar 19 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.330-3
- Fixed permissions of libcfitsio and fpack, funpack

* Sun Mar 17 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.330-2
- Soname contains full package version (upstream doesn't track API changes)

* Sun Mar 10 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 3.330-1
- New upstream version
- Reverted the patch removing run time check

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.310-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.310-2
- Removed check at runtime of the version of the library

* Wed Aug 29 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.310-1
- New upstream version
- Modified cfitsio.patch for new version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.300-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.300-1
- Updated to 3.300
- Reorganized patches (zlib patch was lost somehow)

* Fri Apr 13 2012 Orion Poplawski <orion@cora.nwra.com> - 3.300-0.1.beta
- Update to 3.300 beta
- Drop s390 patch applied upstream
- Rebase makefile and zlib patches

* Mon Jan 16 2012 Orion Poplawski <orion@cora.nwra.com> - 3.290-4
- Drop incluedir mod in package config file (bug #782213)

* Fri Jan 06 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-3
- Adding the libz patch

* Fri Jan 06 2012 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-2
- Using system libz

* Mon Dec 05 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.290-1
- New upstream version
- Reorganizing patches

* Sat Oct 29 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.280-2
- Enable multithreading support

* Thu Jun 09 2011 Sergio Pascual <sergiopr@fedoraproject.org> - 3.280-1
- New upstream version, with improved image compression floating-point FITS

* Mon Apr 11 2011 Matthew Truch <matt at truch.net> - 3.270-1
- Upstream 3.270 release.
-   Several bugfixes.
-   A few new library functions.
-   License change (no longer uses GPL code).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.250-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Matthew Truch <matt at truch.net> - 3.250-5
- Require fully versioned cfitsio for fpack as cfitsio doesn't properly soname itself.

* Mon Jul 26 2010 Matthew Truch <matt at truch.net> - 3.250-4
- Re-fix cfitsio.pc file (BZ 618291)
- Fix typo in date of previous changelog entry.

* Thu Jul 22 2010 Orion Poplawski <orion@cora.nwra.com> - 3.250-3
- Build and ship fpack/funpack in fpack package

* Wed Jul 7 2010 Matthew Truch <matt at truch.net> - 3.250-2
- Include license as %%doc in -static and -docs subpackages.

* Sun Jul 4 2010 Matthew Truch <matt at truch.net> - 3.250-1
- Upstream 2.250 release.

* Wed Jun 30 2010 Karsten Hopp <karsten@redhat.com> 3.240-4
- add s390(x) as bigendian machines

* Sun Feb 21 2010 Matthew Truch <matt at truch.net> - 3.240-3
- Fix pkgconfig file which contains the wrong version number.

* Sat Feb 20 2010 Matthew Truch <matt at truch.net> - 3.240-2
- Bump for rebuild.

* Wed Jan 27 2010 Matthew Truch <matt at truch.net> - 3.240-1
- Update to upstream 3.240 release.

* Mon Nov 2 2009 Matthew Truch <matt at truch.net> - 3.210-2
- Re-introduce library soname patch (accidentally removed it).  

* Tue Oct 20 2009 Matthew Truch <matt at truch.net> - 3.210-1
- Update to upstream 3.210 release.

* Fri Jul 24 2009 Matthew Truch <matt at truch.net> - 3.140-2
- Bump to include proper tarball.

* Tue Jul 21 2009 Matthew Truch <matt at truch.net> - 3.140-1
- Update to upstream 3.140 release.
- Bump for mass rebuild.

* Wed Jun 17 2009 Matthew Truch <matt at truch.net> - 3.130-5
- Separate -docs noarch subpackage as per BZ 492438.
- Explicitly set file attributes correctly.  

* Tue Mar 10 2009 Matthew Truch <matt at truch.net> - 3.130-4
- Set correct version in pkgconfig .pc file.  

* Sun Feb 22 2009 Matthew Truch <matt at truch.net> - 3.130-3
- Re-check testprogram output.
- Build for koji, rpm, gcc upgrade.  

* Thu Feb 5 2009 Matthew Truch <matt at truch.net> - 3.130-2
- Fix source file naming typo.

* Wed Feb 4 2009 Matthew Truch <matt at truch.net> - 3.130-1
- Update to 3.130 upstream.

* Sat Sep 20 2008 Matthew Truch <matt at truch.net> - 3.100-2
- Test library with included test-suite.  

* Fri Sep 19 2008 Matthew Truch <matt at truch.net> - 3.100-1
- Update to 3.100 upstream.
  Includes bugfixes and new compression scheme.

* Fri Mar 7 2008 Matthew Truch <matt at truch.net> - 3.060-3
- Properly indicated include and lib directories in .pc file
  (BZ 436539)
- Fix typo in -static descrition.

* Mon Feb 11 2008 Matthew Truch <matt at truch.net> - 3.060-2
- Bump release for rebuild.

* Fri Nov 9 2007 Matthew Truch <matt at truch.net> - 3.060-1
- Update to 3.060 bugfix release.
- Add static package (BZ 372801)

* Tue Aug 21 2007 Matthew Truch <matt at truch.net> - 3.040-3
- Bump release for rebuild (build-id etc.)

* Thu Aug 2 2007 Matthew Truch <matt at truch.net> - 3.040-2
- Update License tag

* Mon Jul 9 2007 Matthew Truch <matt at truch.net> - 3.040-1
- Upgrade to version 3.040 of cfitsio.

* Fri Feb 16 2007 Matthew Truch <matt at truch.net> - 3.030-2
- Require pkgconfig for -devel.
- export CC=gcc so we don't clobber $RPM_OPT_FLAGS, thereby 
  ruining any -debuginfo packages.  
  See RedHat Bugzilla 229041.

* Fri Jan 5 2007 Matthew Truch <matt at truch.net> - 3.030-1
- Upgrade to version 3.020 of cfitsio.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-3
- Commit correct patch to configure and Makefiles.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-2
- Modify spec file to install to correct directories.
- Package cfitsio.pc file in -devel package.

* Wed Dec 6 2006 Matthew Truch <matt at truch.net> - 3.020-1
- Upgrade to revision 3.020 of cfitsio.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 3.006-6
- Bump release for rebuild in prep. for FC6.

* Thu Mar 30 2006 Matthew Truch <matt at truch.net> - 3.006-5
- Include defattr() for devel package as well - bug 187366

* Sun Mar 19 2006 Matthew Truch <matt at truch.net> - 3.006-4
- Don't use macro {buildroot} in build, only in install as per 
  appended comments to Bugzilla bug 172042

* Fri Mar 10 2006 Matthew Truch <matt at truch.net> - 3.006-3
- Point to f95 instead of g95 as per bugzilla bug 185107

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-2
- Fix spelling typo in name of License.txt file.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-1
- Use new 3.006 fully official stable (non-beta) upstream package.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.005-0.2.beta
- Bump release for FC5 extras rebuild.

* Fri Dec 23 2005 Matthew Truch <matt at truch.net> - 3.005-0.1.beta
- Update to 3.005beta release.

* Mon Nov 14 2005 Matthew Truch <matt at truch.net> - 3.004-0.12.b
- Put in proper URL and Source addresses.
- Sync up spec files.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.11.b
- Clean up unused code in spec file.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.10.b
- Set environment variables correctly.
- Include patch so Makefile will put things where they belong.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.9.b
- Set libdir and includedir correctly for build process.

* Sat Nov 12 2005 Matthew Truch <matt at truch.net> - 3.004-0.8.b
- unset FC once we are done with the build

* Sat Nov 12 2005 Ed Hill <ed@eh3.com> - 3.004-0.7.b
- shared libs and small cleanups

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.6.b
- Own include directory created by the devel package.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.5.b
- Shorten summary.
- Improve specfile post and postun syntax.
- Install headers in cfitsio include subdir.
- Include more documentation provided in tarball.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.4.b
- Require cfitsio for cfitsio-devel

* Sat Nov 05 2005 Matthew Truch <matt at truch.net> - 3.004-0.3.b
- Use proper virgin tarball from upstream.

* Sun Oct 30 2005 Matthew Truch <matt at truch.net> - 3.004-0.2.b
- Include gcc-gfortran build requirment and make sure it gets used.
- Use macros instead of hard coded paths.
- Include home page in description

* Sat Oct 29 2005 Matthew Truch <matt at truch.net> - 3.004-0.1.b
- Initial spec file for Fedora Extras.
