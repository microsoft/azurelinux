Summary:        The Vorbis General Audio Compression Codec tools
Name:           vorbis-tools
Version:        1.4.2
Release:        6%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.xiph.org/
Source:         https://ftp.osuosl.org/pub/xiph/releases/vorbis/%{name}-%{version}.tar.gz
# https://lists.xiph.org/pipermail/vorbis-dev/2021-January/020538.html
# https://lists.xiph.org/pipermail/vorbis-dev/2013-May/020336.html
Patch0:         vorbis-tools-1.4.2-man-page.patch
BuildRequires:  flac-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libao-devel
BuildRequires:  libcurl-devel
BuildRequires:  libvorbis-devel
BuildRequires:  make
BuildRequires:  speex-devel
Provides:       vorbis = %{version}-%{release}
# source code of vorbis-tools contains a copy of vasnprintf.c from gnulib
Provides:       bundled(gnulib)

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

The vorbis package contains an encoder, a decoder, a playback tool, and a
comment editor.

%prep
%autosetup -p1

%build
# fix FTBFS if "-Werror=format-security" flag is used (#1025257)
export CFLAGS="%{optflags} -Wno-error=format-security"
%configure
%make_build

%install
%make_install
rm -rf %{buildroot}/%{_docdir}/%{name}*
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ogg123/ogg123rc-example
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Jan 03 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.4.2-6
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Remove epoch
- License verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Kamil Dudka <kdudka@redhat.com> - 1:1.4.1-2
- new upstream release

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1:1.4.0-34
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 06 2018 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-30
- add virtual provides for bundled(gnulib)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-28
- add explicit BR for the gcc compiler

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-22
- oggenc: fix large alloca on bad AIFF input (CVE-2015-6749)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:1.4.0-20
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-19
- validate count of channels in the header (CVE-2014-9638 and CVE-2014-9639)

* Mon Jan 26 2015 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-18
- do not use stack variable out of its scope of validity (#1185558)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-16
- translate the newly added .po files into .gmo files during build (#1116650)

* Mon Jul 07 2014 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-15
- update po files from translationproject.org (#1116650)

* Tue Jun 10 2014 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-14
- fix FTBFS if "-Werror=format-security" flag is used (#1025257)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 03 2013 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-12
- fix an off-by-one error in the vcut utility (#1003607)

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-11
- fix various man page issues

* Mon Aug 05 2013 Hans de Goede <hdegoede@redhat.com> - 1:1.4.0-10
- Fix FTBFS caused by unversioned docdir change (#992862)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-7
- fix URL to format documentation in vorbiscomment.1 man page (#887540)

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-6
- fix specfile issues reported by the fedora-review script

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 02 2010 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-2
- rebuilt against libao-1.0.0 (#618171)

* Fri Mar 26 2010 Kamil Dudka <kdudka@redhat.com> - 1:1.4.0-1
- new upstream release

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> - 1:1.2.0-7
- fix source URL

* Tue Oct 06 2009 Kamil Dudka <kdudka@redhat.com> - 1:1.2.0-6
- upstream patch fixing crash of oggenc --resample (#526653)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1:1.2.0-3
- fixed seting flags for stderr (#467064)

* Sat May 31 2008 Hans de Goede <j.w.r.degoede@hhs.n> - 1:1.2.0-2
- Stop calling autoconf, this was no longer necessarry and in current
  rawhide breaks us from building (because aclocal.m4 does not match
  the new autoconf version)
- Drop our last 2 patches, they were modifying configure, but since we called
  autoconf after that in effect they were not doing anything, review has
  confirmed that they indeed are no longer needed)
- Drop using system libtool hack, this is dangerous when the libtool used
  to generate ./configure and the one used differ
- Remove various antique checks (for example check if RPM_BUILD_ROOT == /) 
- Drop unnecessary explicit library Requires
- Cleanup BuildRequires

* Tue Mar 11 2008 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-1
- update to 1.2.0
- remove libcurl and oggdec patches, applied upstream
- drop unneeded autoconf BR
- fix BuildRoot

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.1.1.svn20070412-6
- Autorebuild for GCC 4.3

* Thu Nov 15 2007 Hans de Goede <j.w.r.degoede@hhs.n> - 1:1.1.1.svn20070412-5
- Minor specfile cleanups for merge review (bz 226532)

* Thu Oct 04 2007 Todd Zullinger <tmz@pobox.com> - 1:1.1.1.svn20070412-4
- Upstream patch to fix oggdec writing silent wav files (#244757)

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.1.1.svn20070412-3
- Rebuild for build ID

* Wed May 16 2007 Christopher Aillon <caillon@redhat.com> 1:1.1.1.svn20070412-2.fc7
- Bring back support for http URLs which was broken with the previous update
  See https://bugzilla.redhat.com/240351

* Thu Apr 12 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.1.svn20070412-1.fc7
- Upgrade to a current SVN snapshot of vorbis-tools to get our FLAC support
  back, after the recent libFLAC upgrade (#229124)
- Remove obsolete UTF8 and Curl mute patches

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 1.1.1-5
- rebuild with libFLAC.so.8, link with libogg instead of libOggFLAC

* Wed Nov  1 2006 Matthias Clasen <mclasen@redhat.com> - 1:1.1.1-4 
- Rebuild against new curl
- Don't use CURLOPT_MUTE

* Sun Oct 29 2006 Matthias Clasen <mclasen@redhat.com> - 1:1.1.1-3
- Fix charset conversion (#98816)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-2
- rebuild
- Add missing br libtool

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.1-1
- Update to version 1.1.1

* Tue Mar 29 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.0.1-6
- rebuild for flac 1.1.2

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.0.1-5
- rebuild with gcc 4.0

* Wed Jul 28 2004 Colin Walters <walters@redhat.com>
- rebuild

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 1:1.0.1-1
- update to 1.0.1

* Tue Oct 21 2003 Bill Nottingham <notting@redhat.com> 1.0-7
- rebuild (#107673)

* Fri Sep  5 2003 Bill Nottingham <notting@redhat.com> 1.0-6
- fix curl detection so ogg123 gets built (#103831)

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 1.0-5
- Fix link errors

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1:1.0-2
- rebuild on all arches

* Thu Jul 18 2002 Bill Nottingham <notting@redhat.com>
- one-dot-oh

* Tue Jul 16 2002 Elliot Lee <sopwith@redhat.com>
- Add builddep on curl-devel

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0rc3-3
- s/Copyright/License/
- Add curl-devel as a build dependency

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.0rc3

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.0rc2

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- split libao, libvorbis out

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- own %%{_libdir}/ao
- I love libtool

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add links from library major version numbers in rpms

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to rc1

* Fri May  4 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- fixed perl line in spec file to set optims correctly

* Tue Mar 20 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64, again
- use optflags, not -O20 -ffast-math (especially on alpha...)

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- beta4

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64

* Thu Feb  8 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Wed Feb 07 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25391. ogg123 now usses the OSS driver by default if
  none was specified.

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- update CVS, grab aRts backend for libao

* Wed Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- hack up specfile some, merge some packages

* Sat Oct 21 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
