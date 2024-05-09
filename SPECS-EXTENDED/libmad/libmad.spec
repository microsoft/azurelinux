Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libmad
Version:	0.15.1b
Release:	30%{?dist}
Summary:	MPEG audio decoder library

License:	GPLv2+
URL:		https://www.underbit.com/products/mad/
Source0:	https://download.sourceforge.net/mad/%{name}-%{version}.tar.gz
#Create the same header on multilibs arches
Patch0:		libmad-0.15.1b-multiarch.patch
Patch1:		libmad-0.15.1b-ppc.patch
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/534287
Patch2:		Provide-Thumb-2-alternative-code-for-MAD_F_MLN.diff
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/513734
Patch3:		libmad.thumb.diff
Patch4:		https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/libmad/files/libmad-0.15.1b-cflags.patch
Patch5:		https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/libmad/files/libmad-0.15.1b-cflags-O2.patch
#Patches taken from debian - Kurt Roeckx <kurt@roeckx.be>
Patch6:         length-check.patch
Patch7:         md_size.diff

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool


%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

%package        devel
Summary:	MPEG audio decoder library development files
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?el5}
Requires:	pkgconfig
%endif

%description	devel
%{summary}.


%prep
%setup -q
#Only relevant on multilibs arches
%ifarch %{ix86} x86_64 ppc ppc64
%patch 0 -p1 -b .multiarch
%endif
%patch 1 -p1 -b .ppc
%patch 2 -p1 -b .alt_t2
%patch 3 -p1 -b .thumb
%patch 4 -p1 -b .cflags
%patch 5 -p1 -b .02
%patch 6 -p1 -b .lc
%patch 7 -p1 -b .md_size

touch -r aclocal.m4 configure.ac NEWS AUTHORS ChangeLog

# Create an additional pkgconfig file
%{__cat} << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF



%build
autoreconf -sfiv
%configure \
%if 0%{?__isa_bits} == 64
	--enable-fpm=64bit \
%endif
%ifarch %{arm}
	--enable-fpm=arm \
%endif
	--disable-dependency-tracking \
	--enable-accuracy \
	--disable-static    

%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
install -D -p -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc
touch -r mad.h.sed %{buildroot}/%{_includedir}/mad.h


%ldconfig_scriptlets


%files
%doc CHANGES CREDITS README TODO
%license COPYING COPYRIGHT
%{_libdir}/libmad.so.*

%files devel
%{_libdir}/libmad.so
%{_libdir}/pkgconfig/mad.pc
%{_includedir}/mad.h


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.15.1b-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-26
- Add patches from debian

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1b-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-20
- Update Thumb-2 patch - rhbz#1414486

* Wed Nov 23 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-19
- Add patches from gentoo
- Allow debuginfo generation

* Fri Nov 18 2016 Nicolas Chauvet <kwizart@gmail.com> -0.15.1b-18
- Spec file clean-up and review

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.15.1b-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-16
- Mass rebuilt for Fedora 19 Features

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-15
- Don't use multiarch patch when the result is not hardcoded
- Update FPM
- Add patches from lp#534287 and lp#534287

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1b-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 19 2009 David Juran <david@juran.se> - 0.15.1b-13
- ppc asm patch from David Woodhouse (Bz 730)
- rpmlint warnings

* Wed Jul  1 2009 David Juran <david@juran.se> - 0.15.1b-12
- fix typo in multiarch patch
- fix ppc64 version (Bz 691)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.15.1b-11
- rebuild for new F11 features

* Wed Jan 28 2009 David Juran <david@juran.se> - 0.15.1b-10
- fix timestamps (Bz 264)

* Sun Jan 25 2009 David Juran <david@juran.se> - 0.15.1b-9
- fix multiarch (Bz 264)

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.15.1b-8
- rebuild for buildsys cflags issue

* Thu Jul 24 2008 David Juran <david@juran.se> - 0.15.1b-7
- Bump release for RpmFusion

* Tue Feb 19 2008 David Juran <david@juran.se> - 0.15.1b-6
- use $RPM_OPT_FLAGS - Bz 1873

* Sun Sep 30 2007 David Juran <david@juran.se> - 0.15.1b-5
- Grab mad.pc from freshrpms.
- merge configure-optioins with freshrpms
- Adjusted Licence tag (GPLv2)
- Drop static archive

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.15.1b-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.1b-3
- Use 64bit fixed point math on x86_64.
- Filter deprecated gcc flags, build with dependency tracking disabled.
- Move "b" to version field.

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.15.1-2.b
- Drop Epoch in devel dep, too

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Feb 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.15.1-0.lvn.1.b
- Update to 0.15.1b.

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.15.0-0.fdr.1.b.0.94
- Remove comment after scriptlets

* Mon Jun 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.15.0-0.fdr.1.b
- Update to 0.15.0b.
- Split separate from the old mad package to follow upstream.
- -devel requires pkgconfig.

* Thu Apr 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.3.b
- Fix missing "main" package dependencies in *-devel.
- Include patch from Debian, possibly fixes #187 comment 7, and adds
  pkgconfig files for libraries.

* Sun Apr 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.2.b
- Split into mad, libmad, -devel, libid3tag and -devel packages (#187).
- Provide mp3-cmdline virtual package and alternative.
- Build shared library.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.1.b
- Update to current Fedora guidelines.
- Exclude %%{_libdir}/*.la.

* Thu Feb 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.14.2b-1.fedora.1
- First Fedora release, based on Matthias Saou's work.

* Fri Sep 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuild for Red Hat Linux 8.0 (missing because of license issues).
- Spec file cleanup.

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 0.14.2b-3
- ship libid3tag too

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- split libmad off into a separate package
