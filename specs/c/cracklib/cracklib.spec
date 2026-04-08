# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Reflects the values hard-coded in various Makefile.am's in the source tree.
%define dictdir %{_datadir}/cracklib
%define dictpath %{dictdir}/pw_dict

Summary: A password-checking library
Name: cracklib
Version: 2.9.11
Release: 8%{?dist}
URL: https://github.com/cracklib/cracklib
License: LGPL-2.1-or-later

Source0: https://github.com/cracklib/cracklib/releases/download/v%{version}/cracklib-%{version}.tar.gz
Source1: https://github.com/cracklib/cracklib/releases/download/v%{version}/cracklib-words-%{version}.gz
# From attachment to https://bugzilla.redhat.com/show_bug.cgi?id=627449
Source2: cracklib.default.zh_CN.po
# No upstream source for this, just words missing from the current cracklib-words
Source3: missing-words.gz

Patch: cracklib-2.9.11-packlib-reentrant.patch
Patch: cracklib-2.9.11-simplistic.patch

BuildRequires: gcc
BuildRequires: words, gettext
BuildRequires: gettext-autopoint
BuildRequires: zlib-devel
Conflicts: cracklib-dicts < 2.8
# The cracklib-format script calls gzip, but without a specific path.
Requires: gzip

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics, with the purpose of stopping users
from choosing passwords that are easy to guess. CrackLib performs
several tests on passwords: it tries to generate words from a username
and gecos entry and checks those words against the password; it checks
for simplistic patterns in passwords; and it checks for the password
in a dictionary.

CrackLib is actually a library containing a particular C function
which is used to check the password, as well as other C
functions. CrackLib is not a replacement for a passwd program; it must
be used in conjunction with an existing passwd program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you install
CrackLib, you will also want to install the cracklib-dicts package.

%package devel
Summary: Development files needed for building applications which use cracklib
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The cracklib-devel package contains the header files and libraries needed
for compiling applications which use cracklib.

%package dicts
Summary: The standard CrackLib dictionaries
BuildRequires: words >= 2-13
BuildRequires: make
Requires: cracklib = %{version}-%{release}

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words. Cracklib-dicts also
contains the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%prep
%autosetup -p 1 

# Replace zn_CN.po with one that wasn't mis-transcoded at some point.
install -p -m 644 %{SOURCE2} po/zh_CN.po

mkdir cracklib-dicts
for dict in %{SOURCE3} %{SOURCE1}
do
        cp -fv ${dict} cracklib-dicts/
done
chmod +x util/cracklib-format

%build
# Use the dictionary from the build to test
sed -i 's,util/cracklib-check <,util/cracklib-check $(DESTDIR)/$(DEFAULT_CRACKLIB_DICT) <,' Makefile.in
%configure --with-pic \
 --without-python \
 --with-default-dict=%{dictpath} --disable-static
make -C po update-gmo
make

%install
%make_install 'pythondir=${pyexecdir}'
./util/cracklib-format cracklib-dicts/* | \
./util/cracklib-packer %{buildroot}%{dictpath}
./util/cracklib-format %{buildroot}%{dictdir}/cracklib-small | \
./util/cracklib-packer %{buildroot}%{dictdir}/cracklib-small
rm -f %{buildroot}%{dictdir}/cracklib-small
sed s,/usr/lib/cracklib_dict,%{dictpath},g lib/crack.h > %{buildroot}%{_includedir}/crack.h
ln -s cracklib-format %{buildroot}%{_sbindir}/mkdict
# packer link removed as it clashes with hashicorp's packer binary.
#ln -s cracklib-packer %{buildroot}/%{_sbindir}/packer
touch %{buildroot}/top

toprelpath=..
touch %{buildroot}/top
while ! test -f %{buildroot}%{_libdir}/$toprelpath/top ; do
	toprelpath=../$toprelpath
done
rm -f %{buildroot}/top
if test %{dictpath} != %{_libdir}/cracklib_dict ; then
ln -s $toprelpath%{dictpath}.hwm %{buildroot}%{_libdir}/cracklib_dict.hwm
ln -s $toprelpath%{dictpath}.pwd %{buildroot}%{_libdir}/cracklib_dict.pwd
ln -s $toprelpath%{dictpath}.pwi %{buildroot}%{_libdir}/cracklib_dict.pwi
fi
rm -f %{buildroot}%{_libdir}/python*/site-packages/_cracklib*.*a
rm -f %{buildroot}%{_libdir}/libcrack.la

mkdir -p %{buildroot}%{_mandir}/man{3,8}
install -p -m644 doc/*.3 %{buildroot}%{_mandir}/man3/
install -p -m644 doc/*.8 %{buildroot}%{_mandir}/man8/
if ! test -s %{buildroot}%{_mandir}/man8/cracklib-packer.8 ; then
    echo .so man8/cracklib-format.8 > %{buildroot}%{_mandir}/man8/cracklib-packer.8
fi
if ! test -s %{buildroot}%{_mandir}/man8/cracklib-unpacker.8 ; then
    echo .so man8/cracklib-format.8 > %{buildroot}%{_mandir}/man8/cracklib-unpacker.8
fi

%find_lang %{name}

%check
make test DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc README README-WORDS NEWS README-LICENSE AUTHORS
%license COPYING.LIB
%{_libdir}/libcrack.so.*
%dir %{_datadir}/cracklib
%{_datadir}/cracklib/cracklib.magic
%{_sbindir}/*cracklib*
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_libdir}/libcrack.so
%{_mandir}/man3/*

%files dicts
%{_datadir}/cracklib/pw_dict.*
%{_datadir}/cracklib/cracklib-small.*
%{_libdir}/cracklib_dict.*
%{_sbindir}/mkdict

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 2.9.11-3
- migrated to SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Paul Wouters <paul.wouters@aiven.io - 2.9.11-1
- Resolves: rhbz#2123955 cracklib-2.9.11 is available
- Remove old patches, port remaining patches to 2.9.11
- Use man pages from doc/ instead of pulling them from debian

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 30 2022 Parag Nemade <pnemade AT redhat DOT com> - 2.9.7-30
- As -dicts subpackage installs files under %%{_libdir} path it should not be noarch
- this fixes FTBFS on F37+

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 30 2021 Paul Wouters <paul.wouters@aiven.io> - 2.9.6-27
- Resolves: rhbz#1994196 Remove /usr/bin/packer symbolic link

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.9.6-23
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug  9 2019 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-21
- Drop Python 2 bindings completely

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 26 2018 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-18
- Fix regression in dictionary creation and lookup

* Wed Oct 10 2018 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-17
- Fix minor bug found in the Coverity scan

* Tue Oct  9 2018 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-16
- Updated translations

* Fri Jul 13 2018 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-15
- The test must use the dictionary from the build

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-13
- Drop Python 2 support in RHEL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.6-11
- Switch to %%ldconfig_scriptlets

* Wed Jan 03 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.9.6-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.9.6-9
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.9.6-8
- Python 2 binary package renamed to python2-cracklib
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  8 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.6-4
- fix CVE-2016-6318 - avoid overflows in GECOS handling and mangling password (#1364944)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.6-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 23 2015 Tomáš Mráz <tmraz@redhat.com> - 2.9.6-1
- new upstream release
- cleanup of the word lists

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.9.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb  5 2014 Tomáš Mráz <tmraz@redhat.com> - 2.9.1-2
- move python files to libdir

* Mon Dec  9 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.1-1
- new upstream release

* Mon Dec  2 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-9
- update only .gmo files to avoid multilib conflicts (#1036305)

* Thu Nov 28 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-8
- updated translations

* Thu Oct 31 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-7
- do not remove any printable characters in cracklib-format

* Thu Oct 31 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-6
- fix the broken zh_CN translation

* Tue Sep  3 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-5
- make the simplistic check and the purging of special characters much
  less aggressive (#1003624, #985378)

* Wed Aug 28 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-4
- revert compression of the dictionaries as the performance penalty is too big

* Wed Aug 21 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-3
- fix the python module to work with compressed dictionaries (#972542)
- fix various dictionary lookup errors (#986400, #986401)
- make the library reentrant and fix compilation warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun  3 2013 Nalin Dahyabhai <nalin@redhat.com> - 2.9.0-1
- update to 2.9.0 (#970065)
  - adds FascistCheckUser()
- go ahead and compress the main dictionary, since we're linking with zlib
  anyway

* Tue Jan 29 2013 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-3
- point cracklib-packer and cracklib-unpacker man pages to cracklib-format
  (internal tooling)

* Wed Dec 19 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-2
- add missing buildrequires: on zlib-devel (#888876)

* Mon Dec 17 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-1
- update to 2.8.22 (#887461), which now returns an error instead of exiting
  when there's a failure opening the dictionary in FascistCheck()

* Thu Dec 13 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.21-1
- update to 2.8.21

* Mon Dec 10 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.20-1
- update to 2.8.20 (#885439)

* Tue Nov 20 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.19-3
- update the copy of the debian source package to one that can currently be
  retrieved using the URL we list for it

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.19-1
- update to 2.8.19

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Nalin Dahyabhai <nalin@redhat.com> - 2.8.18-1
- update to 2.8.18
- add man pages from Debian (#583932)
- replace zh_CN translation (related to #627449)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.8.16-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul  3 2010 Dan Horák <dan[at]danny.cz> - 2.8.16-3
- added gettext-autopoint as BR:

* Thu May 20 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.16-2
- pull in changes to the Hindi translation (#589188)

* Tue Apr 20 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.16-1
- update to 2.8.16

* Fri Jan 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-3
- add passwords derived from rockyou breach data to the dictionaries (Matthew
  Miller, #557592)

* Thu Jan 21 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-2
- update license: tag
- include license file

* Tue Dec  1 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-1
- update to 2.8.15
- update cracklib-words to the current version (2008-05-07)
- fixup URLs for various dictionary sources that we use
- fix freeing-an-uninitialized-pointer in the python module (SF#2907102)
- add a disttag

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-5
- add explicit dependency on gzip for the sake of cracklib-format (Daniel
  Mach, #501278)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-3
- drop trailing "." from the package description for the dicts
  subpackage (#225659)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.13-2
- Rebuild for Python 2.6

* Tue Oct 28 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-1
- update to 2.8.13, which overhauls the python bindings and revises
  FascistCheck()'s behavior:
  2.8.12 success: returns None, fail: returns error text, other: exceptions
  2.8.13 success: returns candidate, fail: throws ValueError, other: exceptions

* Tue Oct 28 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.12-3
- fix errors rebuilding with libtool that's newer than the one upstream
  has (#467364)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.12-2
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.12-1
- update to 2.8.12, which was relicensed to GPLv2
- package the now-bundled cracklib-small dictionary in cracklib-dicts

* Tue Aug 21 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-3
- rebuild

* Mon Jul 23 2007 Nalin Dahyabhai <nalin@redhat.com>
- add a %%check script to catch things like #249210

* Mon Jul 23 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-2
- work around non-executable util/cracklib-format giving us empty/garbage
  dictionaries (#249210)

* Thu Jul 19 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-1
- update to 2.8.10

* Wed Jun 20 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-11
- improve reports of out-of-memory exceptions so that they don't include a
  bogus filename
- improve reports of file-missing exceptions from the python module so that
  they give the right filename (#225858)

* Mon Mar 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-10
- explicitly include required headers from <packer.h> (#228698)
- attempt to provide doc strings in the python module

* Mon Feb 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-9
- drop final "." from summaries (Jef Spaleta, #225659)
- drop static library from -devel subpackage (Jef Spaleta, #225659)
- note that the most recently-added wordlist came from bugzilla (#225659)
- remove explicit dependency on gzip, as it's implicit (Jef Spaleta, #225659)
- convert %%triggerpostun to not use a shell as an interpreter (#225659)

* Wed Jan 31 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-8
- add word list from attachment #126053 (#185314)

* Thu Jan 25 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-7
- fix check for the existence of dictionaries when the caller specifies a
  location (#224347, upstream #1644628)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.8.9-6
- rebuild against python 2.5

* Sun Oct 29 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-5
- split out cracklib-python (#203327)

* Sun Oct 29 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-4
- split out cracklib-devel (#203569)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.9-3.1
- rebuild

* Mon Jun 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.9-3
- Add missing br, automake, libtool (#194738)

* Tue Apr 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-2
- update to 2.8.9
- only create compat symlinks for the dictionaries if we aren't installing
  them into the old locations

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.6-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.6-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.6-1
- update to 2.8.6
- remove .la file (#172632)

* Wed Sep 28 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.5-2
- update to 2.8.5

* Tue Sep 27 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.4-1
- update to 2.8.4
- build python module

* Fri May 13 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.3-1
- update to 2.8.3

* Thu Mar 17 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.2-1
- update to 2.8.2

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.1-1
- update to 2.8.1
  - moves dictionary to new default location under %%{_datadir} -- the
    dictionary format is the same across all architectures
  - renames "packer" to "cracklib-packer"
- conflict with cracklib-dicts < 2.8, where the on-disk format was not
  compatible on 64-bit arches due to now-fixed cleanliness bugs
- move binaries for manipulating and checking words against dictionaries
  from -dicts into the main package

* Mon Jan  3 2005 Nalin Dahyabhai <nalin@redhat.com> 2.7-30
- rebuild

* Mon Jan  3 2005 Nalin Dahyabhai <nalin@redhat.com> 2.7-29
- correctly build on 64-bit systems (part of #143417)
- patch so that 32- and 64-bit libcrack can read dictionaries which were
  incorrectly generated on 64-bit systems of the same endianness (more #143417)
- include a sample cracklib magic file
- stop using /usr/dict/* when building the dictionary
- list words as a build requirement, which it is, instead of a run-time
  requirement
- provide a virtual arch-specific dep in cracklib-dicts, require it in
  cracklib (part of #143417)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.7-26
- update URL (previous page moved) (#114894)

* Fri Jan 30 2004 Nalin Dahyabhai <nalin@redhat.com> 2.7-25
- fix ldconfig invocation in trigger for older versions which included the
  soname symlink (#114620)

* Mon Dec  1 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-24
- include packer.h for reading dictionaries directly, since we already include
  packer in the -dicts subpackage (#68339)
- don't include the soname symlink in the package, let ldconfig do its job

* Wed Jun 18 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-23
- rebuild

* Mon Jun 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-22
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update URL

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared libs

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Sep 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-19
- fix for builds on multilib systems (set DICTPATH properly)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-16
- rebuild in new environment

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-15
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct  2 2001 Nalin Dahyabhai <nalin@redhat.com> 2.7-13
- use getpwuid_r instead of getpwuid

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 2.7-12
- remove cruft that ldconfig already knows how to manage
- don't explicitly strip anything -- the brp setup decides that
- tweak the header so that it can be used in C++ (#46685)
- buildprereq the words package

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add link from library major version number

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS fixes
- fix undeclared function warnings from the new compiler
- fix URL

* Fri Apr 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- switched to use /usr/share/dict/words

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.7
- build shared libraries

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added -fPIC

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- basic spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
