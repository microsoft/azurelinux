Summary:         A library for handling different graphics file formats
Name:            netpbm
Version:         10.90.00
Release:         5%{?dist}
# See copyright_summary for details
License:         BSD and GPLv2 and IJG and MIT and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://svn.code.sf.net/p/netpbm/code/advanced netpbm-%%{version}
# svn checkout https://svn.code.sf.net/p/netpbm/code/userguide netpbm-%%{version}/userguide
# svn checkout https://svn.code.sf.net/p/netpbm/code/trunk/test netpbm-%%{version}/test
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
Source0:         %{_mariner_sources_url}/%{name}-%{version}.tar.xz
Patch0:          netpbm-security-scripts.patch
Patch1:          netpbm-security-code.patch
Patch2:          netpbm-ppmfadeusage.patch
Patch3:          netpbm-CVE-2017-2587.patch
Patch4:          netpbm-python3.patch
Patch5:          netpbm-time.patch
Patch6:          netpbm-gcc4.patch
Patch7:          netpbm-bmptopnm.patch
Patch8:          netpbm-CAN-2005-2471.patch
Patch9:          netpbm-xwdfix.patch
Patch10:         netpbm-multilib.patch
Patch11:         netpbm-glibc.patch
Patch12:         netpbm-docfix.patch
Patch13:         netpbm-fiasco-overflow.patch
Patch14:         netpbm-cmuwtopbm.patch
Patch15:         netpbm-pamtojpeg2k.patch
Patch16:         netpbm-manfix.patch
Patch17:         netpbm-manual-pages.patch
Patch18:         netpbm-jasper.patch
Patch19:	 netpbm-userguide.patch
Patch20:	 netpbm-libdir-so.patch
Patch21:         disable-pamx-build.patch

BuildRequires:   libjpeg-devel, libpng-devel, libtiff-devel, flex, gcc, jbigkit-devel
BuildRequires:   perl-generators, python3, jasper-devel, libxml2-devel
BuildRequires:   perl(Config), perl(Cwd), perl(English), perl(Fcntl), perl(File::Basename)
BuildRequires:   perl(strict)

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package devel
Summary:         Development tools for programs which will use the netpbm libraries
Requires:        netpbm = %{version}-%{release}

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.  You'll also need
to have the netpbm package installed.

%package progs
Summary:         Tools for manipulating graphics files in netpbm supported formats
Requires:        netpbm = %{version}-%{release}

%description progs
The netpbm-progs package contains a group of scripts for manipulating the
graphics files in formats which are supported by the netpbm libraries.  For
example, netpbm-progs includes the rasttopnm script, which will convert a
Sun rasterfile into a portable anymap.  Netpbm-progs contains many other
scripts for converting from one graphics file format to another.

If you need to use these conversion scripts, you should install
netpbm-progs.  You'll also need to install the netpbm package.

%package doc
Summary:         Documentation for tools manipulating graphics files in netpbm supported formats
Requires:        netpbm-progs = %{version}-%{release}

%description doc
The netpbm-doc package contains a documentation in HTML format for utilities
present in netpbm-progs package.

If you need to look into the HTML documentation, you should install
netpbm-doc.  You'll also need to install the netpbm-progs package.

%prep
%autosetup -p1
rm -rf converter/other/jpeg2000/libjasper/
rm -rf converter/other/jbig/libjbig/

%build
./configure <<EOF



















EOF

TOP=`pwd`

make \
	CC="%{__cc}" \
	LDFLAGS="$RPM_LD_FLAGS -L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
	CFLAGS="$RPM_OPT_FLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing" \
	CFLAGS_CONFIG="$RPM_OPT_FLAGS" \
	LADD="-lm" \
	JPEGINC_DIR=%{_includedir} \
	PNGINC_DIR=%{_includedir} \
	TIFFINC_DIR=%{_includedir} \
	JPEGLIB_DIR=%{_libdir} \
	JBIGLIB=%{_libdir}/libjbig.so.2.1 \
	PNGLIB_DIR=%{_libdir} \
	TIFFLIB_DIR=%{_libdir} \
	LINUXSVGALIB="NONE" \
	XML2LIBS="NONE"

# prepare man files
cd userguide
# BZ 948531
rm -f *.manual-pages
rm -f *.manfix
for i in *.html ; do
  ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
  mkdir -p man/man${i}
  mv *.${i} man/man${i}
done


%install
make package pkgdir=%{buildroot}/usr LINUXSVGALIB="NONE" XML2LIBS="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
mkdir -p %{buildroot}%{_libdir}
if [ "%{_libdir}" != "/usr/lib" ]; then
  mv %{buildroot}/usr/lib/lib* %{buildroot}%{_libdir}
fi

mkdir -p %{buildroot}%{_datadir}
mv userguide/man %{buildroot}%{_mandir}

# Get rid of the useless non-ascii character in pgmminkowski.1
sed -i 's/\xa0//' %{buildroot}%{_mandir}/man1/pgmminkowski.1

# Don't ship man pages for non-existent binaries and bogus ones
for i in hpcdtoppm \
	 ppmsvgalib vidtoppm picttoppm \
	 directory error extendedopacity \
	 pam pbm pgm pnm ppm index libnetpbm_dir \
	 liberror ppmtotga; do
	rm -f %{buildroot}%{_mandir}/man1/${i}.1
done
rm -f %{buildroot}%{_mandir}/man5/extendedopacity.5

mkdir -p %{buildroot}%{_datadir}/netpbm
mv %{buildroot}/usr/misc/*.map %{buildroot}%{_datadir}/netpbm/
mv %{buildroot}/usr/misc/rgb.txt %{buildroot}%{_datadir}/netpbm/
rm -rf %{buildroot}/usr/README
rm -rf %{buildroot}/usr/VERSION
rm -rf %{buildroot}/usr/link
rm -rf %{buildroot}/usr/misc
rm -rf %{buildroot}/usr/man
rm -rf %{buildroot}/usr/pkginfo
rm -rf %{buildroot}/usr/config_template
rm -rf %{buildroot}/usr/pkgconfig_template

# Don't ship the static library
rm -f %{buildroot}%{_libdir}/lib*.a

# remove/symlink/substitute obsolete utilities
pushd %{buildroot}%{_bindir}
rm -f pgmtopbm pnmcomp
ln -s pamcomp pnmcomp
echo -e '#!/bin/sh\npamditherbw $@ | pamtopnm\n' > pgmtopbm
chmod 0755 pgmtopbm
popd

%ldconfig_scriptlets

%check
pushd test
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
export PBM_TESTPREFIX=%{buildroot}%{_bindir}
export PBM_BINPREFIX=%{buildroot}%{_bindir}
./Execute-Tests && exit 0
popd

%files
%doc doc/HISTORY README
%license doc/copyright_summary doc/COPYRIGHT.PATENT doc/GPL_LICENSE.txt
%{_libdir}/lib*.so.*

%files devel
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{_mandir}/man3/*
%{_libdir}/lib*.so

%files progs
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/netpbm/

%files doc
%doc userguide/*

%changelog
* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.90.00-5
- Bumping release to re-build with newer 'libtiff' libraries.

* Fri Apr 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.90.00-4
- Updating source URL.

* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.90.00-3
- Removing dependency on 'ghostscript'.
- License verified.

* Wed Mar 31 2021 Henry Li <lihl@microsoft.com> - 10.90.00-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libX11-devel from build requirement
- Apply patch to disable building and installing pamx 

* Thu Mar 26 2020 Josef Ridky <jridky@redhat.com> - 10.90.00-1
- New upstream release 10.90.00 (#1817279)

* Wed Mar 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 10.89.00-3
- Add perl dependencies for build

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.89.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Josef Ridky <jridky@redhat.com> - 10.89.00-1
- New upstream release 10.89.00 (#1787801)

* Mon Dec 09 2019 Josef Ridky <jridky@redhat.com> - 10.88.00-1
- New upstream release (#1756647)

* Wed Aug 21 2019 Josef Ridky <jridky@redhat.com> - 10.87.00-1
- New upstream release (#1725280)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.86.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Josef Ridky <jridky@redhat.com> - 10.86.00-2
- Enable MPEG and MPEG-2 support (#1700164)

* Mon Apr 01 2019 Josef Ridky <jridky@redhat.com> - 10.86.00-1
- New upstream release (#1694351)

* Tue Feb 12 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 10.84.03-3
- Package %%{_libdir}/*.so (RHBZ#1676370).

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.84.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Josef Ridky <jridky@redhat.com> - 10.84.03-1
- New upstream release (#1634256)

* Wed Nov 21 2018 Josef Ridky <jridky@redhat.com> - 10.83.01-2
- Use system version of jasper and jbigkit library (#1651965)

* Mon Jul 23 2018 Josef Ridky <jridky@redhat.com> - 10.83.01-1
- New upstream release 10.83.01 (#1596970)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.82.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Josef Ridky <jridky@redhat.com> - 10.82.00-3
- Backport unimplemented fixes from 10.79.00 (#1585695)

* Wed Apr 11 2018 Rafael Santos <rdossant@redhat.com> - 10.82.00-2
- Use standard Fedora build and linker flags (bug #1543858)

* Tue Mar 27 2018 Josef Ridky <jridky@redhat.com> - 10.82.00-1
- New upstream release 10.82.00 (#1560330)

* Mon Feb 26 2018 Josef Ridky <jridky@redhat.com> - 10.81.00-4
- spec clean up
- build against Python3

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.81.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Josef Ridky <jridky@redhat.com> - 10.81.00-2
- change ghostscript requirement

* Wed Jan 03 2018 Josef Ridky <jridky@redhat.com> - 10.81.00-1
- New upstream release 10.81.00 (#1529904)
- update spec file

* Thu Oct 19 2017 Josef Ridky <jridky@redhat.com> - 10.80.00-2
- Rebuilt for python package

* Mon Oct 02 2017 Josef Ridky <jridky@redhat.com> - 10.80.00-1
- New upstream release 10.80.00 (#1496797)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.79.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.79.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Josef Ridky <jridky@redhat.com> - 10.79.00-1
- New upstream release 10.79.00 (#1466772)

* Wed Mar 29 2017 Josef Ridky <jridky@redhat.com> - 10.78.00-1
- New upstream release 10.78.00

* Wed Feb 08 2017 Josef Ridky <jridky@redhat.com> - 10.77.00-3
- fix CVE-2017-2586, CVE-2017-2587 (#1419545)
- fix CVE-2017-5849 (#1419650)

* Mon Jan 23 2017 Josef Ridky <jridky@redhat.com> - 10.77.00-2
- fix #1404757 - add copyright_summary to doc section

* Mon Jan 23 2017 Josef Ridky <jridky@redhat.com> - 10.77.00-1
- New upstream release 10.77.00 (#1408611)

* Mon Dec  5 2016 Josef Ridky <jridky@redhat.com> - 10.76.00-2
- set Provides: bundled for jasper and jbigkit library (#1395716)

* Thu Nov 10 2016 Josef Ridky <jridky@redhat.com> - 10.76.00-1
- Update to the latest upstream release 10.76.00 (#1393713)

* Thu Jul 28 2016 Josef Ridky <jridky@redhat.com> - 10.75.99-1
- Update to the latest upstream release 10.75.99 (#1361103)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10.71.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 10 2015 Petr Hracek <phracek@redhat.com> - 10.71.02-1
- Update to the latest upstream release (#1252352)

* Thu Aug 06 2015 Petr Hracek <phracek@redhat.com> - 10.66.02-7
- remove doc/copyright_summary (#1219743)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.66.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Petr Hracek <phracek@redhat.com> - 10.66.02-5
- Moving libnetpbm.so from netpbm-devel to netpbm (#1180811)

* Tue Jan 20 2015 Petr Hracek <phracek@redhat.com> - 10.66.02-4
- Add missing pnmtops to netpbm-progs (#1171903)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.66.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.66.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Petr Hracek <phracek@redhat.com> - 10.66.02-1
- Update new sources (#1063264)

* Mon Apr 14 2014 Jaromir Capik <jcapik@redhat.com> - 10.61.02-9
- Fixing format-security flaws (#1037217)

* Wed Nov 13 2013 Petr Hracek <phracek@redhat.com> - 10.61.02-8
- pnmtops hangs in case of more then 10 files (#1029512)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.61.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 10.61.02-6
- Perl 5.18 rebuild

* Mon Jun 17 2013 Petr Hracek <phracek@redhat.com> - 10.61.02-5
- Manual page corrections (#948531)

* Wed Jun 05 2013 Petr Hracek <phracek@redhat.com> - 10.61.02-4
- pnmpsnr: compare the same images failed (#969479)

* Tue May 28 2013 Petr Hracek <phracek@redhat.com> - 10.61.02-3
- pnmtops: Multi-page PAM files correction (#833546)

* Mon May 27 2013 Petr Hracek <phracek@redhat.com> 10.61.02-2
- Man page corrections (#948531)

* Wed Feb 20 2013 Jindrich Novy <jnovy@redhat.com> 10.61.02-1
- update to 10.61.02

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.61.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 10.61.01-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 03 2013 Jindrich Novy <jnovy@redhat.com> 10.61.01-1
- update to 10.61.01
- sync patches

* Fri Dec 14 2012 Jindrich Novy <jnovy@redhat.com> 10.60.05-1
- update to 10.60.05
- fixes pngtopam and ppmpat

* Wed Dec 05 2012 Jindrich Novy <jnovy@redhat.com> 10.60.04-1
- update to 10.60.04
- fixes pamtotiff, pnmmontage, pnmpsnr, pbmpscale, pgmhist,
  pampick, pamtompfont
- fix dates in changelog

* Tue Nov 27 2012 Jindrich Novy <jnovy@redhat.com> 10.60.03-2
- add upstream test suite

* Wed Nov 21 2012 Jindrich Novy <jnovy@redhat.com> 10.60.03-1
- update to 10.60.3
- fixes xbmptopbm, pamtojpeg2k

* Mon Oct 08 2012 Jindrich Novy <jnovy@redhat.com> 10.60.01-1
- update to 10.60.01
- fixes pamgauss, sunicontopnm

* Tue Oct 02 2012 Jindrich Novy <jnovy@redhat.com> 10.60.00-1
- update to 10.60.00
- speeds up xpmtoppm

* Tue Sep 25 2012 Jindrich Novy <jnovy@redhat.com> 10.59.03-1
- update to 10.59.03
- fixes xpmtoppm

* Fri Jul 20 2012 Jindrich Novy <jnovy@redhat.com> 10.59.02-1
- update to 10.59.02
- fixes getline() glibc function conflict

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.59.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Jindrich Novy <jnovy@redhat.com> 10.59.01-1
- update to 10.59.01

* Fri Jun 22 2012 Jindrich Novy <jnovy@redhat.com> 10.58.03-1
- update to 10.58.03
- pnmtops is back

* Wed Jun 13 2012 Jindrich Novy <jnovy@redhat.com> 10.58.01-3
- fix ppmtopict buffer underflow
- fix memory corruption in pnmtopclxl

* Sun May 06 2012 Jindrich Novy <jnovy@redhat.com> 10.58.01-2
- rebuild against new libtiff

* Mon Apr 09 2012 Jindrich Novy <jnovy@redhat.com> 10.58.01-1
- update to 10.58.01

* Mon Mar 12 2012 Jindrich Novy <jnovy@redhat.com> 10.57.04-1
- update to 10.57.04
- fixes ppmquantall

* Fri Mar 02 2012 Jindrich Novy <jnovy@redhat.com> 10.57.03-1
- update to 10.57.03

* Mon Feb 13 2012 Jindrich Novy <jnovy@redhat.com> 10.57.02-1
- update to 10.57.02

* Tue Jan 17 2012 Jindrich Novy <jnovy@redhat.com> 10.57.01-1
- update to 10.57.01

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.56.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Jindrich Novy <jnovy@redhat.com> 10.56.05-1
- update to 10.56.05
- fixes pamscale

* Fri Nov 25 2011 Jindrich Novy <jnovy@redhat.com> 10.56.04-1
- update to 10.56.04
- fixes pngtopam
- use more robust way to create library symlinks

* Wed Nov 16 2011 Jindrich Novy <jnovy@redhat.com> 10.56.03-2
- fix library symlink to point to the new soname

* Fri Nov 11 2011 Jindrich Novy <jnovy@redhat.com> 10.56.03-1
- update to 10.56.03
- fixes compilation against new libpng

* Tue Sep 27 2011 Jindrich Novy <jnovy@redhat.com> 10.47.31-1
- update to 10.47.31
- fixes bmptopnm

* Wed Aug 24 2011 Jindrich Novy <jnovy@redhat.com> 10.47.30-1
- update to 10.47.30
- fixes opacity in pnmtopng
- fixes pnmquant perl compatibility

* Tue Jul 26 2011 Jindrich Novy <jnovy@redhat.com> 10.47.29-1
- update to 10.47.29

* Tue Jun 28 2011 Jindrich Novy <jnovy@redhat.com> 10.47.28-1
- update to 10.47.28

* Mon Mar 28 2011 Jindrich Novy <jnovy@redhat.com> 10.47.27-1
- update to 10.47.27
- fixes error message in g3topbm + documentation fixes

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.47.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jindrich Novy <jnovy@redhat.com> 10.47.26-1
- update to 10.47.26
- drop upstreamed asciitopgm patch

* Mon Jan 17 2011 Jindrich Novy <jnovy@redhat.com> 10.47.25-1
- update to 10.47.25
- fix asciitopgm (#670082), thanks to Jonathan Kamens

* Sat Jan  1 2011 Jindrich Novy <jnovy@redhat.com> 10.47.24-1
- update to 10.47.24

* Tue Dec 14 2010 Jindrich Novy <jnovy@redhat.com> 10.47.23-1
- update to 10.47.23

* Tue Oct 19 2010 Jindrich Novy <jnovy@redhat.com> 10.47.21-2
- fix HTML pages from which man pages are now generated correctly (#644248)

* Mon Oct 18 2010 Jindrich Novy <jnovy@redhat.com> 10.47.21-1
- update to 10.47.21

* Fri Oct  1 2010 Jindrich Novy <jnovy@redhat.com> 10.47.20-1
- update to 10.47.20

* Mon Aug 30 2010 Jindrich Novy <jnovy@redhat.com> 10.47.19-1
- update to 10.47.19

* Sat Aug 14 2010 Jindrich Novy <jnovy@redhat.com> 10.47.18-1
- update to 10.47.18

* Mon Jul 12 2010 Jindrich Novy <jnovy@redhat.com> 10.47.17-1
- update to 10.47.17

* Fri Jun 18 2010 Jindrich Novy <jnovy@redhat.com> 10.47.16-1
- update to 10.47.16
- fixes pbmtext

* Mon Jun  7 2010 Jindrich Novy <jnovy@redhat.com> 10.47.15-1
- update to 10.47.15

* Tue Jun  1 2010 Jindrich Novy <jnovy@redhat.com> 10.47.14-2
- add -fno-strict-aliasing to CFLAGS

* Fri May 21 2010 Jindrich Novy <jnovy@redhat.com> 10.47.14-1
- update to 10.47.14
- fixes memory leak in pamarith

* Tue May  4 2010 Jindrich Novy <jnovy@redhat.com> 10.47.13-1
- update to 10.47.13
- fixes pnmtops

* Mon May  3 2010 Jindrich Novy <jnovy@redhat.com> 10.47.12-3
- fix cmuwtopbm so that magic bytes test actually works
- fix pamtojpeg2k (don't close stdout twice)
- fix documentation for pamperspective and pbmtoepson

* Wed Apr 28 2010 Jindrich Novy <jnovy@redhat.com> 10.47.12-2
- fix CVE-2007-2721 (#501451)
- add missing man pages

* Tue Apr 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> 10.47.12-1
- update to 10.47.12
- remove ppmtompeg, due to legal issues

* Thu Mar 18 2010 Jindrich Novy <jnovy@redhat.com> 10.47.10-3
- package docs in separate netpbm-doc package (#492437)
- don't package patch backups in documentation
- netpbm-progs package requires ghostscript

* Wed Mar 17 2010 Jindrich Novy <jnovy@redhat.com> 10.47.10-2
- pgmtopbm should generate PBM, not PAM file
- forwardport pnmmontage from 10.35 to make it work
- fix pamstretch-gen

* Wed Feb 24 2010 Jindrich Novy <jnovy@redhat.com> 10.47.10-1
- update to 10.47.10
- fixes crash in pnmhistmap

* Wed Feb 17 2010 Jindrich Novy <jnovy@redhat.com> 10.47.09-3
- remove obsolete pgmtopbm and pnmcomp, symlink them to the new
  compatible variants
- fix ppmfade -h, --help options
- add missing man pages
- link against -lz (#564649)

* Wed Jan 27 2010 Jindrich Novy <jnovy@redhat.com> 10.47.09-2
- fix buffer overflow in pnmtofiasco

* Mon Jan 25 2010 Jindrich Novy <jnovy@redhat.com> 10.47.09-1
- update to 10.47.09, fixes occassional crash in pamtosvg
- fix documentation
- fix ppmfade exit status

* Wed Jan 13 2010 Jindrich Novy <jnovy@redhat.com> 10.47.08-1
- update to 10.47.08

* Wed Dec 30 2009 Jindrich Novy <jnovy@redhat.com> 10.47.07-1
- update to 10.47.07

* Mon Dec 14 2009 Jindrich Novy <jnovy@redhat.com> 10.47.06-1
- update to 10.47.06 - fixes the dumb pamtosvg mistake in 10.47.05
- pnmmargin won't create leftovers in /tmp (#547888)

* Thu Dec 10 2009 Jindrich Novy <jnovy@redhat.com> 10.47.05-1
- update to 10.47.05
- fixes pnmtofiasco, fiascotopnm, pamtosvg, pamtouil and ppmrainbow
- upstream fix to pamtosvg caused netpbm not to be rebuildable on
  any arch because of missing semicolon, the fix is now fixed :-/

* Mon Dec  7 2009 Jindrich Novy <jnovy@redhat.com> 10.47.04-3
- fix segfault in pnmsmooth (#545089)

* Fri Nov 27 2009 Jindrich Novy <jnovy@redhat.com> 10.47.04-2
- fix ppmpat segfault when using -camo option (#541568)

* Wed Oct 21 2009 Jindrich Novy <jnovy@redhat.com> 10.47.04-1
- update to 10.47.04 (it is now stable) (#529525)

* Fri Oct  9 2009 Jindrich Novy <jnovy@redhat.com> 10.35.68-1
- update to 10.35.68

* Fri Sep  4 2009 Jindrich Novy <jnovy@redhat.com> 10.35.67-1
- update to 10.35.67
- fix configuration

* Wed Jul 29 2009 Jindrich Novy <jnovy@redhat.com> 10.35.66-1
- update to 10.35.66
- sync svgatopam patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.35.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Jindrich Novy <jnovy@redhat.com> 10.35.65-1
- update to 10.35.65

* Sun May 17 2009 Jindrich Novy <jnovy@redhat.com> 10.35.64-1
- update to 10.35.64
- fixes pnmremap, giftopnm, ppmpat, ppmdraw

* Tue Apr 28 2009 Jindrich Novy <jnovy@redhat.com> 10.35.63-1
- update to 10.35.63
- basically new release with some of our patches applied upstream

* Tue Apr 14 2009 Jindrich Novy <jnovy@redhat.com> 10.35.62-1
- update to 10.35.62
- upstream fixes pamstereogram
- fix options in pamperspective, pbmtoepson, ppmpat, pamaddnoise
  so that they match their man pages (#483011, #483070, #483243, #483245)
- avoid clashes with getline() from glibc

* Tue Mar 31 2009 Jindrich Novy <jnovy@redhat.com> 10.35.61-2
- remove two hunks from security patch breaking pbmclean and pbmlife (#493015)
- fix ppmdfont and svgtopnm, thanks to Jiri Moskovcak

* Mon Mar 23 2009 Jindrich Novy <jnovy@redhat.com> 10.35.61-1
- update to 10.35.61
- upstream fixes array bound violation in pbmtog3
- drop .pbmtog3segfault patch, we fixed this some time ago already
  and it is in upstream now
- use saner exit status in ppmfade

* Thu Feb 26 2009 Jindrich Novy <jnovy@redhat.com> 10.35.60-3
- fix broken perl syntax in ppmfade
- fix exit status and error reporting in ppmrainbow

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.35.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Jindrich Novy <jnovy@redhat.com> 10.35.60-1
- update to 10.35.60
- update .security patch, minor cleanup
- fixes xwdtopnm for at least some direct color 24/32 images
- fixes memory leak and out of memory crash in libpammap

* Thu Jan 29 2009 Jindrich Novy <jnovy@redhat.com> 10.35.59-1
- update to 10.35.59
- fixes array bound violation in ilbmtoppm
- fixes garbage output when input in fitstopnm is little endian
  floating point FITS

* Wed Jan 28 2009 Jindrich Novy <jnovy@redhat.com> 10.35.58-4
- fix segfault in ximtoppm (#482891), the utility lacked the
  command line parsing initialization code

* Thu Jan 22 2009 Jindrich Novy <jnovy@redhat.com> 10.35.58-3
- fix cmuwmtopbm and other utilities by making endianess
  functions work correctly on 64bit systems (#476863)

* Wed Jan 21 2009 Jindrich Novy <jnovy@redhat.com> 10.35.58-2
- fix pnmtofiasco to accept image from stdin (#476989, #227283)

* Mon Jan 19 2009 Jindrich Novy <jnovy@redhat.com> 10.35.58-1
- update to 10.35.38
- fixes crashes in picttoppm, pbmtomrf, mrftopbm
- fixes bugs in leaftoppm, ilbmtoppm

* Tue Dec 23 2008 Jindrich Novy <jnovy@redhat.com> 10.35.57-3
- unbreak ppmshadow and ppmrainbow (#476989)
- pnmmontage won't crash because of uninitialized memory usage

* Fri Dec 19 2008 Jindrich Novy <jnovy@redhat.com> 10.35.57-2
- fix segfault in pamtosvg caused by not reverting "sentinel value" (#476989)

* Mon Dec 15 2008 Jindrich Novy <jnovy@redhat.com> 10.35.57-1
- update to 10.35.57

* Thu Nov  6 2008 Jindrich Novy <jnovy@redhat.com> 10.35.55-1
- update to 10.35.55

* Mon Oct 27 2008 Jindrich Novy <jnovy@rehdat.com> 10.35.54-1
- update to 10.35.54
- adds better randomization for ppmforge, pgmnoise, pgmcrater
- fixes array bounds violation in pnm_createBlackTuple() with PBM, PGM
- fixes crash in pnmtoddif with any PGM input

* Tue Oct 14 2008 Jindrich Novy <jnovy@redhat.com> 10.35.53-1
- update to 10.35.53
- fixes pamditherbw (-value parameter other than .5 with -fs)

* Sat Sep 27 2008 Jindrich Novy <jnovy@redhat.com> 10.35.52-1
- update to 10.35.52
- fixes crash of libppmd/ppmdraw when line is completely out of frame

* Thu Sep 18 2008 Jindrich Novy <jnovy@redhat.com> 10.35.51-1
- update to netpbm-10.35.51
- make it actually compilable by removing duplicated function
  in pamcomp.c

* Wed Aug 27 2008 Jindrich Novy <jnovy@redhat.com> 10.35.49-2
- link against system jasper instead of embedded one (#460300)

* Thu Aug 14 2008 Jindrich Novy <jnovy@rehdat.com> 10.35.49-1
- update to 10.35.49
- fixes crash in pamcut when cutting a region entirely to the
  left or right of the input image, with -pad

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.35.48-2
- fix license tag

* Mon Aug  4 2008 Jindrich Novy <jnovy@redhat.com> 10.35.48-1
- update to 10.35.48
- fixes buffer overrun in pamperspective and pngtopnm output format
- update .security2 patch so that it applies with fuzz==0

* Tue Jun 24 2008 Jindrich Novy <jnovy@rehdat.com> 10.35.46-1
- update to 10.35.46
- fixes pbmtext, pamtotga, pamtouil and pnmtopclxl

* Mon Jun  9 2008 Jindrich Novy <jnovy@redhat.com> 10.35.45-1
- update to 10.35.45
- fixes anytopnm, pamtohtmltbl, xvminitoppm, pbmtogo, tgatoppm

* Mon May 26 2008 Jindrich Novy <jnovy@redhat.com> 10.35.44-1
- update to 10.35.44
- fixes pamscale PBM input with -nomix, pamtilt crash

* Mon May 12 2008 Jindrich Novy <jnovy@redhat.com> 10.35.43-1
- update to 10.35.43
- fixes pbmtext and documentation of pamthreshold

* Mon Apr 14 2008 Jindrich Novy <jnovy@redhat.com> 10.35.42-1
- update to 10.35.42
- fixes pnmnorm, resolution of conflicting -wpercent and -wvalue

* Mon Mar 31 2008 Jindrich Novy <jnovy@redhat.com> 10.35.41-1
- update to 10.35.41 (fixes pnmnorm and gcc-4.3 build)

* Fri Mar 14 2008 Jindrich Novy <jnovy@redhat.com> 10.35.40-2
- package rgb.txt for pnmtopng (#313301)
- drop useless xorg-x11-server-utils BR

* Sun Mar  9 2008 Jindrich Novy <jnovy@redhat.com> 10.35.40-1
- update to 10.35.40 (fixes pgmdeshadow, pgmmedian, pgmbentley and pamtosvg)

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 10.35.39-1
- update to 10.35.39 (fixes crash in pamtosvg)

* Thu Feb 14 2008 Jindrich Novy <jnovy@redhat.com> 10.35.38-1
- update to 10.35.38 (fixes to pbmtext and ppmtoarbtxt)
- fix to let it built with gcc 4.3

* Thu Jan 17 2008 Jindrich Novy <jnovy@redhat.com> 10.35.37-1
- update to 10.35.37

* Mon Dec 31 2007 Jindrich Novy <jnovy@redhat.com> 10.35.36-1
- update to 10.35.36

* Thu Dec 13 2007 Jindrich Novy <jnovy@redhat.com> 10.35.35-1
- update to 10.35.35

* Mon Nov 26 2007 Jindrich Novy <jnovy@redhat.com> 10.35.34-1
- update to 10.35.34
- sync security patch and fix typos

* Wed Nov 14 2007 Jindrich Novy <jnovy@redhat.com> 10.35.33-1
- update to 10.35.33

* Fri Nov  2 2007 Jindrich Novy <jnovy@redhat.com> 10.35.32-2
- remove man pages that lacks corresponding binaries (#220739)

* Thu Oct 18 2007 Jindrich Novy <jnovy@redhat.com> 10.35.32-1
- remove .svn directories from tarball to reduce its size
- update fixes rhbz#337181 and likely others

* Thu Oct 18 2007 MATSUURA Takanori <t.matsuu at gmail.com> 10.35.32-0
- update to 10.35.32 from svn tree
- create man pages from userguide HTML files

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 10.35-17
- add xorg-x11-server-utils BR (#313301)

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 10.35-16
- rebuild for ppc32
- fix open() calls so that netpbm builds with new glibc

* Mon Aug 20 2007 Jindrich Novy <jnovy@redhat.com> 10.35-15
- fix .ppmquantall patch (#207799)
- merge cmapsize with bmptopnm patch (#224554)

* Mon Jul 16 2007 Jindrich Novy <jnovy@redhat.com> 10.35-14
- /usr/share/netpbm is no more unowned (#248300)

* Wed Jun 20 2007 Jindrich Novy <jnovy@redhat.com> 10.35-13
- package map files needed by pnmtopalm (#244983)

* Thu Mar 29 2007 Jindrich Novy <jnovy@redhat.com> 10.35-12
- merge review fixes (#226191), thanks to Jason Tibbitts

* Fri Feb  2 2007 Jindrich Novy <jnovy@redhat.com> 10.35-11
- fix pbmtomacp buffer overflow (#226969)

* Mon Jan 29 2007 Jindrich Novy <jnovy@redhat.com> 10.35-10
- bmptopnm won't crash with "BMPlencolormap: internal error!" (#224554)

* Thu Dec 28 2006 Jindrich Novy <jnovy@redhat.com> 10.35-9
- pbmtog3 won't segfault on 64bit arches (#220739)

* Tue Dec 19 2006 Jindrich Novy <jnovy@redhat.com> 10.35-8
- remove bogus man pages (#220112, #220113)
- overflow2() no more conflicts with libgd.so (#216116)
- fix BuildRoot

* Thu Oct 12 2006 Jindrich Novy <jnovy@redhat.com> 10.35-7
- remove  note about OSL 1 licensing from COPYRIGHT.PATENT file

* Mon Oct  2 2006 Jesse Keating <jkeating@redhat.com> 10.35-6
- rebuild for new libpng, again.

* Mon Oct  2 2006 Jesse Keating <jkeating@redhat.com> 10.35-5
- rebuild for new libpng

* Mon Oct  2 2006 Jindrich Novy <jnovy@redhat.com> 10.35-4
- rebuild (#208866)

* Fri Sep 29 2006 Jindrich Novy <jnovy@redhat.com> 10.35-3
- remove OSL 1.1 from security patch (#208587)

* Sun Sep 24 2006 Jindrich Novy <jnovy@redhat.com> 10.35-2
- fix ppmquantall (#207799), thanks to Steve Grubb

* Mon Sep 18 2006 Jindrich Novy <jnovy@redhat.com> 10.35-1
- update to 10.35
- drop .pnmtopng, .rgbtxt patches, fixed upstream
- sync .xwidfix, .ppmtompeg patches
- regenerate man pages

* Thu Sep 14 2006 Jindrich Novy <jnovy@redhat.com> 10.34-8
- readd pbmtols, author claims it's LGPL (#202519)
- add .l1 suffixes to tarball names to reflect legal fixes
  in the upstream release with the same NVR

* Wed Sep 13 2006 Jindrich Novy <jnovy@redhat.com> 10.34-7
- rebuild

* Thu Sep  7 2006 Jindrich Novy <jnovy@redhat.com> 10.34-6.fc6
- regenerate man pages so that makewhatis isn't confused (#204991)
  (upstream makeman script was broken -> now fixed)

* Mon Sep  4 2006 Jindrich Novy <jnovy@redhat.com> 10.34-5.fc6
- readd spottopgm, author claims it's GPL (#202519)

* Tue Aug 15 2006 Jindrich Novy <jnovy@redhat.com> 10.34-4.fc6
- legal fixes (#202519):
- remove pbmtols, spottopgm, jbig and hpcd stuff from source
  and doc tarballs

* Sat Aug 12 2006 Jindrich Novy <jnovy@redhat.com> 10.34-3.fc6
- pamscale won't waste all system resources by usage of uninitialized
  variables for output image resolution (#199871)
- use %%{?dist}

* Wed Jul 19 2006 Jindrich Novy <jnovy@redhat.com> 10.34-2
- fix double free corruption in ppmtompeg (#199409),
  thanks to Milan Zazrivec

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 10.34-1.1
- rebuild

* Thu Jun 22 2006 Jindrich Novy <jnovy@redhat.com> 10.34-1
- update to 10.34
- drop .ppmtogif, .nstring patches
- remove some overflow checks from .security patch, it's
  now resolved in the new upstream version
- don't use svgalib by default (don't compile/ship ppmsvgalib)
- don't compile svgtopam because of the libxml dependency
- add BuildRequires libX11-devel
- fix build on x86_64 and ppc64

* Mon Jun  5 2006 Jindrich Novy <jnovy@redhat.com> 10.33-3
- fix multilib conflict (#192735)
- remove jbigtopnm man page

* Fri Apr 14 2006 Jindrich Novy <jnovy@redhat.com> 10.33-2
- fix image corruption in ppmtogif, thanks to Gilles Detillieux (#188597)
- fix nsting.h to let pnmtopng and other utilities using seekable opening
  mode work on x86_64 (#188594)

* Wed Apr  5 2006 Jindrich Novy <jnovy@redhat.com> 10.33-1
- update to 10.33
- drop upstreamed .ppmdepth patch
- fix segfault in ppmtompeg when encoding jpeg images (#185970)

* Mon Apr  3 2006 Jindrich Novy <jnovy@redhat.com> 10.32-2
- fix broken symlink in upstream: pnmsdepth -> pamdepth (#187667)

* Tue Feb 28 2006 Jindrich Novy <jnovy@redhat.com> 10.32-1
- update to 10.32
- drop .msbmp patch, applied upstream
- sync the rest of the patches
- regenerate man pages

* Mon Feb 20 2006 Jindrich Novy <jnovy@redhat.com> 10.31-5
- add missing flex BuildRequires
- fix anytopnm to recognize ms-bmp files (#182060)

* Tue Feb 14 2006 Jindrich Novy <jnovy@redhat.com> 10.31-4
- make xwdtopnm work on x86_64 (#181001)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 10.31-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jindrich Novy <jnovy@redhat.com> 10.31-3
- fix segfault caused by usage of uninitialized variables while
  parsing cmdline arguments in pnmtopng (#179645)
- add validity check for date/time in pnmtopng
- fix unchecked sscanf reads

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 10.31-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Jindrich Novy <jnovy@redhat.com> 10.31-2
- rebuild to have greater version than in FC4 (#177698)

* Fri Dec 30 2005 Jindrich Novy <jnovy@redhat.com> 10.31-1
- update to 10.31
- update security patch
- regenerate man pages

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Jindrich Novy <jnovy@redhat.com> 10.30-2
- fix path to rgb.txt to fit modular X (#174128)

* Fri Oct 21 2005 Jindrich Novy <jnovy@redhat.com> 10.30-1
- update to 10.30
- update manpath, gcc4 patches
- update security patch - fixed length problem in rle_addhist
- update partly upstreamed bmptopnm, pnmtopng patches
- drop manpath patch
- regenerate man pages

* Thu Oct 06 2005 Jindrich Novy <jnovy@redhat.com> 10.29-2
- fix segfault in pnmtopng caused by referencing a NULL pointer (#169532)

* Tue Aug 16 2005 Jindrich Novy <jnovy@redhat.com> 10.29-1
- update to 10.29
- drop upstreamed .libpm, .pnmtojpeg, .pbmtolj patches
- update .CAN-2005-2471 patch

* Mon Aug 15 2005 Jindrich Novy <jnovy@redhat.com> 10.28-6
- link libnetpbm.so against -lm (#165980)

* Tue Aug 09 2005 Jindrich Novy <jnovy@redhat.com> 10.28-5
- fix CAN-2005-2471, unsafe gs calls from pstopnm (#165355)

* Thu Jul 21 2005 Jindrich Novy <jnovy@redhat.com> 10.28-4
- fix buffer overflow in pbmtolj (#163596)

* Mon Jun 27 2005 Jindrich Novy <jnovy@redhat.com> 10.28-3
- create symlink pnmtopnm -> pamtopnm, this works now in
  netpbm-10.28 (#161436)

* Tue Jun 21 2005 Jindrich Novy <jnovy@redhat.com> 10.28-2
- fix segfault in pbmtolj caused by unchecked assertions
  caused by definition of NDEBUG (#160429)
- drop hunk from .security patch causing dual inclusion
  of string.h in pbmtolj.c

* Fri Jun 10 2005 Jindrich Novy <jnovy@redhat.com> 10.28-1
- update to 10.28
- regenerated man pages
- sync .security, .security2, .badlink, .libpm, .gcc4 patches
- drop upstreamed .pngtopnm, .pnmcolormap patches

* Tue May 31 2005 Jindrich Novy <jnovy@redhat.com> 10.27-4
- fix segfault in pnmcolormap what makes latex2html/ppmquant
  unusable (#158665, #139111)

* Mon May 16 2005 Jindrich Novy <jnovy@redhat.com> 10.27-3
- fix ppmdither leak caused by bug in security patch (#157757)
- drop gcc34 patch

* Mon May 09 2005 Jindrich Novy <jnovy@redhat.com> 10.27-2
- fix invalid strcmp condition in bmptopnm, typo in pnmtojpeg
  (David Constanzo, #157106, #157118)
- proper read longs and shorts in libpm.c (David Constanzo, #157110)
- fix segfault in bmptopnm caused by freeing an uninitialized pointer

* Tue Mar 29 2005 Jindrich Novy <jnovy@redhat.com> 10.27-1
- update to the new 10.27 release
- update .security2, .security patch
- regenerate man pages
- remove jbig, hpcd
- remove config_template from /usr
- don't create symlink to pamtopnm

* Mon Mar 14 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-3
- fix overflow checking of integers with incompatible endianess
  causing problems using xwdtopnm (#147790)

* Wed Mar 09 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-2
- add .gcc4 patch to fix some missing declarations of headers,
  some pointer signedness mismatches, remove xmalloc2
- rebuilt with gcc4

* Thu Mar 03 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-1
- update to netpbm-10.26.4, remove jbig, hpcd
- this version fixes #149924
- regenerate man pages (don't include man pages without binaries - #146863)

* Wed Jan 05 2005 Jindrich Novy <jnovy@redhat.com> 10.26-1
- update to netpbm-10.26-1, remove jbig, hpcd
- regenerate man pages, remove man pages for non existent binaries
- update security patch, additional fixes
- drop upstreamed misc patch, merge malloc patch with security patch

* Mon Oct 25 2004 Jindrich Novy <jnovy@redhat.com> 10.25-3
- include man pages in troff format, thanks to Michal Jaegerman (#136959)
- drop bmpbpp patch, fixed upstream
- remove pcdovtoppm, ppmsvgalib, vidtoppm man pages because binaries
  for them are not present (#136471)

* Mon Oct 18 2004 Jindrich Novy <jnovy@redhat.com> 10.25-2
- avoid compile crash when "-msse" is in CFLAGS

* Mon Oct 18 2004 Jindrich Novy <jnovy@redhat.com> 10.25-1
- update to latest upstream 10.25
- drop initvar patch
- update security, misc patch
- add bmpbpp patch to use only appropriate bit depths for BMP (#135675)

* Thu Sep 23 2004 Jindrich Novy <jnovy@redhat.com> 10.24-3
- added patch to suppress installation of doc.url to /usr/bin #133346

* Wed Aug 18 2004 Jindrich Novy <jnovy@redhat.com> 10.24-2
- added patch to fix compile crash for 64bit machines
- various hacks related to .security patch

* Mon Aug 16 2004 Jindrich Novy <jnovy@redhat.com> 10.24-1
- updated to 10.24
- updated docs

* Thu Aug 05 2004 Jindrich Novy <jnovy@redhat.com> 10.23-2
- added pngtopnm patch
- added malloc patch

* Tue Aug 03 2004 Jindrich Novy <jnovy@redhat.com> 10.23-1
- updated to netpbm-10.23 upsteam (and removed jbig, hpcd)
- $TMPDIR patch removed, obsolete
- updated gcc34 patch
- removed nestedfunc patch, already applied in upstream version
- updated security patch to conform to 10.23 (mostly in ppmtompeg/frame.c)

* Fri Jul 02 2004 Phil Knirsch <pknirsch@redhat.com> 10.22-2
- Fixed Zero byte allocation error in bmptopnm (#123169)
- Honour the $TMPDIR in ppmfade (#117247)
- Fixed nested function bug (#117377)
- Fixed several uninitialized variables (#117377)

* Mon Jun 28 2004 Phil Knirsch <pknirsch@redhat.com> 10.22-1
- Update to latest upstream version 10.22 (also for docs).
- Removed jbig and hdcp code from tarball.

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- merged fix for pnmrotate crash freeing wrong number of rows

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 10.19-7
- fixed compilation with gcc34

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-6
- Fixed problem in pnmquant with GetOptions() and args/ARGV (#115788).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 10.19-5
- rebuilt

* Tue Feb 10 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-4
- Fixed several tmp vulnerabilities in scripts and apps. Based on Debian
  security fix for netpbm-9.24.

* Mon Feb 09 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-3
- Included doc tarball with manpages (#114755).
- Fixed small manpage incorrectness (#84922).
- Fixed message from giftopnm (#114756).

* Fri Jan 30 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-2
- No need anymore to fix ppmfade and ppmshade.

* Thu Jan 29 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-1
- Major update to latest upstream version 10.19.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 28 2003 Phil Knirsch <pknirsch@redhat.com> 9.24-11
- Updated Alan's patch.

* Wed Feb 19 2003 Phil Knirsch <pknirsch@redhat.com> 9.24-10
- Added big security patch by Alan Cox.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 9.24-9
- rebuilt

* Thu Dec 19 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-8
- Removed print filters again as they are too dangerous.

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 9.24-7
- Merge in hammer changes, rebuild

* Sun Sep 08 2002 Arjan van de Ven <arjanv@redhat.com>
- fix for x86-64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-5
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 09 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-3
- Fixed a possible gcc compiler problem for inline struct parameters (#62181).
- Added missing .map files to progs files selection (#61625).

* Tue Apr 02 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-2
- Fixed stupid dangling symlink problem (#62478)

* Tue Mar 12 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-1
- Updated to netpbm version 9.24
- Hacked around a couple of library problems.

* Tue Nov 06 2001 Phil Knirsch <phil@redhat.de>
- Updated to netpbm version 9.20

* Fri Jun 22 2001 Philipp Knirsch <pknirsch@redhat.de>
- Updated to netpbm version 9.14
- Removed pnmtotiff resize patch as it is now part of the original package
- Removed pstopnm csh fix as it is now part of the original package
- Removed asciitopgm memcpy fix as it is now part of the original package
- Removed manpages patch as it is now part of the original package

* Mon Feb 12 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #26767 where the new glibc time and sys/time fixes needed
  to be done.

* Fri Feb  9 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switched filters to printconf filters

* Wed Jan 24 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #21644 where few manpages had a small error.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #19487 where asciitopgm dumped core on Alpha. Actually
  dumped core everywhere

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- update to 9.9
- Due to patent infringement problems removed the jbig support from the tarball
  (pnm/jbig + Makefile changes) and created a new tarball

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- include shared libraries missing from previous build

* Tue Oct 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.8
- make sure shhopt.h is included in the -devel package (#19672)
- rename shhopt.h to pbmshhopt.h because it's not the same as the normal
  shhopt.h that other things (like util-linux) expect

* Wed Aug  9 2000 Crutcher Dunnavant <crutcher@redhat.com>
- added a png-to-pnm.fpi filter

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move netpbm-progs to the Applications/Multimedia group
- reintroduce patches from the old libgr package

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.5

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.4

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch back to the netpbm tree, which is maintained again

* Mon Feb 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure all man pages are included (#9328)
- fix pstopnm bomb when xres == yres (#9329)
- add libjpeg and libz because libtiff now needs them

* Wed Feb 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- added/updated TIFF compression patch from jik@kamens.brookline.ma.us (#8826)

* Mon Dec 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- added TIFF resolution patch from jik@kamens.brookline.ma.us (#7589)

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- added section 5 man pages

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- fix tiff-to-pnm.fpi (#4267)

* Thu Jul 29 1999 Bill Nottingham <notting@redhat.com>
- add a pile of foo-to-bar.fpi filters (#4251)

* Tue Mar 23 1999 Michael Johnson <johnsonm@redhat.com>
- removed old png.h header file that was causing png utils to die
- build png in build instead of install section...

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- patch for 24-bit .BMP files (from sam@campbellsci.co.uk)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 15)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- clean up the spec file
- build for glibc 2.1
- patch to fix pktopbm

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- glibc2 defines random in <stdlib.h> (pbm/pbmplus.h problem #693)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- cleaned up the spec file a little bit
- validated mike's changes :-)

* Wed May 6 1998 Michael Maher <mike@redhat.com>
- added pnm-to-ps.fpi that was missing from previous packages

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- altered install so that the package installs now even if a previous
  version was not installed on the system 

* Thu Apr 16 1998 Erik Troan <ewt@redhat.com>
- built against libpng 1.0

* Thu Nov 06 1997 Donnie Barnes <djb@redhat.com>
- changed copyright from "distributable" to "freeware"
- added some missing scripts that existed in netpbm
- added some binaries that weren't getting built
- added patch to build tiff manipulation progs (requires libtiff)

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- obsoletes netpbm now

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>
- mucked config.guess and Make.Rules to build on Alpha/Linux

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- updated to 2.0.13
- dropped libjpeg and libtiff (those should come from home sources)
- removed glibc patch (new version appears to have it!)
- added i686 as a valid arch type to config.guess

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
