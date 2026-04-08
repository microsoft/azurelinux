# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#%%global debugtrace 1

# Set to 0 when upgrading to a new ICU release that contains up-to-date timezone data.
# (or update the timezone data update..).
%global use_tzdata_update 0

%define version_dash %{gsub %{version} %. -}
%define version_underscore %{gsub %{version} %. _}

Name:      icu
Version:   77.1
Release:   1%{?dist}
Summary:   International Components for Unicode

License:   Unicode-DFS-2016 AND BSD-2-Clause AND BSD-3-Clause AND NAIST-2003 AND LicenseRef-Fedora-Public-Domain
URL:       http://site.icu-project.org/
Source0:   https://github.com/unicode-org/icu/releases/download/release-%{version_dash}/icu4c-%{version_underscore}-src.tgz
%if 0%{?use_tzdata_update}
Source1:   https://github.com/unicode-org/icu/releases/download/release-%{version_dash}/icu4c-%{version_underscore}-data.zip
Source2:   https://raw.githubusercontent.com/unicode-org/icu-data/main/tzdata/icunew/2022b/44/metaZones.txt
Source3:   https://raw.githubusercontent.com/unicode-org/icu-data/main/tzdata/icunew/2022b/44/timezoneTypes.txt
Source4:   https://raw.githubusercontent.com/unicode-org/icu-data/main/tzdata/icunew/2022b/44/windowsZones.txt
Source5:   https://raw.githubusercontent.com/unicode-org/icu-data/main/tzdata/icunew/2022b/44/zoneinfo64.txt
%endif
Source10:   icu-config.sh

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: doxygen, autoconf, python3
BuildRequires: make
Requires: lib%{name}%{?_isa} = %{version}-%{release}

Patch4: gennorm2-man.patch
Patch5: icuinfo-man.patch
# https://github.com/unicode-org/icu/pull/3496
Patch6: 3496.patch

%description
Tools and utilities for developing with icu.

%package -n lib%{name}
Summary: International Components for Unicode - libraries

%description -n lib%{name}
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.

%package  -n lib%{name}-devel
Summary:  Development files for International Components for Unicode
Requires: lib%{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n lib%{name}-devel
Includes and definitions for developing with icu.

%package -n lib%{name}-doc
Summary: Documentation for International Components for Unicode
BuildArch: noarch

%description -n lib%{name}-doc
%{summary}.

%{!?endian: %global endian %(%{__python3} -c "import sys;print (0 if sys.byteorder=='big' else 1)")}
# " this line just fixes syntax highlighting for vim that is confused by the above and continues literal


%prep
%autosetup -p1 -n icu
%if 0%{?use_tzdata_update}
pushd source
unzip -o %{SOURCE1}
rm -f data/in/icudt*l.dat
cp -v -f %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} data/misc
popd
%endif

%build
pushd source
autoconf
CFLAGS='%optflags -fno-strict-aliasing'
CXXFLAGS='%optflags -fno-strict-aliasing'
# Endian: BE=0 LE=1
%if ! 0%{?endian}
CPPFLAGS='-DU_IS_BIG_ENDIAN=1'
%endif

#rhbz856594 do not use --disable-renaming or cope with the mess
OPTIONS='--with-data-packaging=library --disable-samples'
%if 0%{?debugtrace}
OPTIONS=$OPTIONS' --enable-debug --enable-tracing'
%endif
%configure $OPTIONS

#rhbz#225896
sed -i 's|-nodefaultlibs -nostdlib||' config/mh-linux
#rhbz#813484
sed -i 's| \$(docfilesdir)/installdox||' Makefile
# There is no source/doc/html/search/ directory
sed -i '/^\s\+\$(INSTALL_DATA) \$(docsrchfiles) \$(DESTDIR)\$(docdir)\/\$(docsubsrchdir)\s*$/d' Makefile
# rhbz#856594 The configure --disable-renaming and possibly other options
# result in icu/source/uconfig.h.prepend being created, include that content in
# icu/source/common/unicode/uconfig.h to propagate to consumer packages.
test -f uconfig.h.prepend && sed -e '/^#define __UCONFIG_H__/ r uconfig.h.prepend' -i common/unicode/uconfig.h

# more verbosity for build.log
sed -i -r 's|(PKGDATA_OPTS = )|\1-v |' data/Makefile

%make_build
%make_build doc


%install
#rm -rf source/doc
%make_install %{?_smp_mflags} -C source
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so.*
(
 cd $RPM_BUILD_ROOT%{_bindir}
 mv icu-config icu-config-%{__isa_bits}
)
install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/icu-config


%check
# test to ensure that -j(X>1) didn't "break" man pages. b.f.u #2357
if grep -q @VERSION@ source/tools/*/*.8 source/tools/*/*.1 source/config/*.1; then
    exit 1
fi
%make_build -C source check

# log available codes
pushd source
LD_LIBRARY_PATH=lib:stubdata:tools/ctestfw:$LD_LIBRARY_PATH bin/uconv -l


%files
%license license.html
%exclude %{_datadir}/%{name}/*/LICENSE
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/gendict
%{_bindir}/genrb
%{_bindir}/icuexportdata
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_sbindir}/escapesrc
%{_sbindir}/genccode
%{_sbindir}/gencmn
%{_sbindir}/gennorm2
%{_sbindir}/gensprep
%{_sbindir}/icupkg
%{_mandir}/man1/derb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/gencfu.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/gendict.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/icuexportdata.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/*.8*

%files -n lib%{name}
%license LICENSE
%doc readme.html
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%license LICENSE
%doc source/samples/
%{_bindir}/%{name}-config*
%{_bindir}/icuinfo
%{_mandir}/man1/%{name}-config.1*
%{_mandir}/man1/icuinfo.1*
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config

%files -n lib%{name}-doc
%license LICENSE
%doc readme.html
%doc source/doc/html/*


%changelog
* Thu Jul 24 2025 Frantisek Zatloukal <fzatlouk@redhat.com> - 77.1-1
- Update to 77.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 76.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 76.1-4
- Adjust file patterns for the sbin merge

* Thu Jan 16 2025 Eike Rathke <erack@redhat.com> - 76.1-3
- Resolves: rhbz#2335638 Add upstream patches instead

* Mon Jan 06 2025 Eike Rathke <erack@redhat.com> - 76.1-2
- Resolves: rhbz#2335638 include <type_traits> in unicode/char16ptr.h

* Fri Nov 22 2024 Pete Walter <pwalter@fedoraproject.org> - 76.1-1
- Update to 76.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 74.2-1
- Update to 74.2

* Mon Jan 29 2024 Pete Walter <pwalter@fedoraproject.org> - 74.1-1
- Update to 74.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 73.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 73.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 73.2-3
- Fix broken TestHebrewCalendarInTemporalLeapYear

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 73.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 73.2-1
- Update to 73.2

* Fri Jan 20 2023 Eike Rathke <erack@redhat.com> - 72.1-3
- migrated to SPDX license IDs

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 72.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 28 2022 Pete Walter <pwalter@fedoraproject.org> - 72.1-1
- Update to 72.1

* Fri Sep 23 2022 Mike FABIAN <mfabian@redhat.com> - 71.1-2
- Update timezone data to 2022b

* Wed Jul 27 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 71.1-1
- Update to 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 69.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 05 2022 Mike FABIAN <mfabian@redhat.com> - 69.1-6
- Update timezone data to 2022a

* Wed Feb 02 2022 Eike Rathke <erack@redhat.com> - 69.1-5
- Introduce use_tzdata_update flag

* Tue Feb 01 2022 Mike FABIAN <mfabian@redhat.com> - 69.1-4
- Update timezone data to 2021a4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 69.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 69.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 69.1-1
- Update to 69.1

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 67.1-6
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 67.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 67.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Eike Rathke <erack@redhat.com> - 67.1-3
- Replace unversioned %%{__python} macro with %%{__python3}

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 67.1-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 67.1-1
- Update to 67.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 65.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 65.1-1
- Update to 65.1
- Add a patch from gentoo to fix the build on s390x
- Drop arm test disabling patches as they are no longer needed

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 63.2-4
- Build with Python 3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 63.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Eike Rathke <erack@redhat.com> - 63.2-2
- Resolves: rhbz#1708935 temporarily roll back to 63.1

* Thu May 09 2019 Eike Rathke <erack@redhat.com> - 63.2-1
- Update to 63.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 63.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 63.1-1
- Update to 63.1

* Tue Nov 06 2018 Eike Rathke <erack@redhat.com> - 62.1-3
- Resolves: rhbz#1646703 CVE-2018-18928

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 62.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 62.1-1
- Update to 62.1

* Mon May 28 2018 Eike Rathke <erack@redhat.com> - 61.1-2
- Resolves: rhbz#1582611 Add riscv64 to icu-config.sh

* Tue Apr 24 2018 Eike Rathke <erack@redhat.com> - 61.1-1
- Update to 61.1

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 60.2-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 60.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Pete Walter <pwalter@fedoraproject.org> - 60.2-1
- Update to 60.2

* Thu Dec 14 2017 Eike Rathke <erack@redhat.com> - 60.1-2
- Resolves: rhbz#1524820 CVE-2017-17484

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 60.1-1
- Update to 60.1

* Wed Nov 08 2017 Eike Rathke <erack@redhat.com> - 57.1-9
- Resolves: rhbz#1510932 CVE-2017-14952

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Eike Rathke <erack@redhat.com> - 57.1-6
- Resolves: rhbz#1444101 CVE-2017-7867 CVE-2017-7868

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Eike Rathke <erack@redhat.com> - 57.1-4
- dist.rpmgrill: "Percent signs in specfile changelog should be escaped"

* Fri Nov 18 2016 Eike Rathke <erack@redhat.com> - 57.1-3
- Resolves: rhbz#1377362 CVE-2016-7415

* Tue Nov 01 2016 Eike Rathke <erack@redhat.com> - 57.1-2
- Resolves: rhbz#1360340 CVE-2016-6293

* Fri Apr 15 2016 Eike Rathke <erack@redhat.com> - 57.1-1
- upgrade to upstream ICU 57.1

* Tue Apr 05 2016 Eike Rathke <erack@redhat.com> - 56.1-7
- make check failure is fatal again

* Tue Apr 05 2016 Eike Rathke <erack@redhat.com> - 56.1-6
- remove icu-56.1-codes-cache-extend.patch

* Sun Feb 28 2016 Raphael Groner <projects.rg@smart.ms> - 56.1-5
- even more verbosity and debug output
- add path to extend ICU's internal cache of codes
- use license macro
- provide samples in devel subpackage
- modernize generally

* Sat Feb 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 56.1-4
- %%build: make VERBOSE=1
- %%check: keep 'make check' non-fatal while investigating rhbz#1307633

* Sat Feb 06 2016 Caolán McNamara <caolanm@redhat.com> - 56.1-3
- Resolves: rhbz#1307633 FTBFS, disable check to get build through for now

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 56.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 27 2015 Eike Rathke <erack@redhat.com> - 56.1-1
- Resolves: rhbz#1271353 upgrade to ICU 56.1

* Fri Sep 18 2015 Eike Rathke <erack@redhat.com> - 54.1-5
- Workaround rhbz#1239574 disabling offending tests on armv7hl

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 54.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Eike Rathke <erack@redhat.com> - 54.1-3
- Resolves: rhbz#1190131 CVE-2014-7923 CVE-2014-7926 CVE-2014-9654
- Resolves: rhbz#1184811 CVE-2014-6585 CVE-2014-6591

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 54.1-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan 26 2015 Eike Rathke <erack@redhat.com> - 54.1-1
- Resolves: rhbz#1185433 upgrade to upstream ICU 54.1

* Tue Aug 26 2014 Eike Rathke <erack@redhat.com> - 53.1-1
- Resolves: rhbz#1130771 upgrade to upstream ICU 53.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 52.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Eike Rathke <erack@redhat.com> - 52.1-3
- Resolves: rhbz#1106793 bad 2-digit year test case

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 52.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Eike Rathke <erack@redhat.com> - 52.1-1
- upgrade to upstream ICU 52.1
- Resolves: rhbz#1049265 icu-52.1 is available
- Resolves: rhbz#1050063 Trivial change to icu-config to support ppc64le
- drop icu-51-layout-fix-10107.tgz source
- drop integrated icu.10318.CVE-2013-2924_changeset_34076.patch
- drop integrated icu.10143.memory.leak.crash.patch

* Wed Oct 09 2013 Eike Rathke <erack@redhat.com> - 50.1.2-10
- Resolves: rhbz#1015594 CVE-2013-2924 use-after-free

* Fri Oct 04 2013 Eike Rathke <erack@redhat.com> - 50.1.2-9
- added %%{?_isa} to Requires for multi-arch systems

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Eike Rathke <erack@redhat.com> - 50.1.2-7
- Resolves: rhbz#986814 install icu-config.sh from source2

* Wed Jul 17 2013 Eike Rathke <erack@redhat.com> - 50.1.2-6
- Resolves: rhbz#966141 various flaws in Layout Engine font processing
- Resolves: rhbz#966077 aarch64 support for icu-config.sh wrapper

* Mon Feb 25 2013 Eike Rathke <erack@redhat.com> - 50.1.2-5
- added manpages for gennorm2 and icuinfo, rhbz#884035 related

* Tue Feb 19 2013 Caolán McNamara <caolanm@redhat.com> - 50.1.2-4
- Resolves: fdo#52519 crash on typing some Malayalam

* Tue Jan 29 2013 Eike Rathke <erack@redhat.com> - 50.1.2-3
- Resolves: rhbz#856594 roll back and build without --disable-renaming again

* Mon Jan 28 2013 Eike Rathke <erack@redhat.com> - 50.1.2-2
- Resolves: rhbz#856594 include content of icu/source/uconfig.h.prepend

* Fri Jan 25 2013 Eike Rathke <erack@redhat.com> - 50.1.2-1
- Update to 50.1.2
- Resolves: rhbz#856594 to-do add --disable-renaming on next soname bump
- removed upstream applied icu.9283.regexcmp.crash.patch

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 49.1.1-7
- Related: rhbz#856594 reenable icu symbol renaming

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 49.1.1-6
- Resolves: rhbz#856594 disable icu symbol renaming

* Fri Aug 31 2012 Tom Callaway <spot@fedoraproject.org> - 49.1.1-5
- apply upstream fix (bug 9283) for regexcmp crash causing Chromium segfaults

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 49.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Caolán McNamara <caolanm@redhat.com> - 49.1.1-3
- probably parallel-build safe by now. Add a check for original breakage

* Fri Jun 15 2012 Caolán McNamara <caolanm@redhat.com> - 49.1.1-2
- Resolves: rhbz#804313 multi-lib pain

* Thu Apr 19 2012 Eike Rathke <erack@redhat.com> - 49.1.1-1
- Update to 49.1.1

* Thu Apr 19 2012 Eike Rathke <erack@redhat.com> - 4.8.1.1-3
- Resolves: rhbz#813484 doxygen 1.8.0 does not provide installdox, omit from install

* Mon Jan 30 2012 Jon Masters <jcm@jonmasters.org> - 4.8.1.1-2
- Correct reference to BZ681941, add temporary fix for ARM FTBFS side effect

* Fri Jan 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> -4.8.1.1-1
- Update to 4.8.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Eike Rathke <erack@redhat.com> - 4.8.1-3
- Resolves: rhbz#766542 CVE-2011-4599 Stack-based buffer overflow
- add icu.8984.CVE-2011-4599.patch

* Mon Oct 24 2011 Caolán McNamara <caolanm@redhat.com> - 4.8.1-2
- Resolves: rhbz#747193 try and enable ccmp for Indic fonts

* Wed Sep 07 2011 Caolán McNamara <caolanm@redhat.com> - 4.8.1-1
- Resolves: rhbz#681941 don't link unneccessary -lm, etc.
- add icu.8800.freeserif.crash.patch

* Tue Mar 08 2011 Caolán McNamara <caolanm@redhat.com> - 4.6-2
- Resolves: rhbz#681941 don't link unneccessary -lm, etc.

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 4.6-1
- latest version
- upgrade includes a .pc now of its own, drop ours
- drop integrated icu.6995.kannada.patch
- drop integrated icu.7971.buildfix.patch
- drop integrated icu.7972.buildfix.patch
- drop integrated icu.7932.doublecompare.patch
- drop integrated icu.8011.buildfix.patch

* Fri Feb 11 2011 Caolán McNamara <caolanm@redhat.com> - 4.4.2-8
- Resolves: rhbz#674328 yet more ways that freeserif crashes libicu

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Caolán McNamara <caolanm@redhat.com> - 4.4.2-6
- Resolves: rhbz#674328 more ways that freeserif crashes libicu

* Wed Feb 02 2011 Caolán McNamara <caolanm@redhat.com> - 4.4.2-5
- Resolves: rhbz#674328 freeserif crashes libicu

* Thu Jan 13 2011 Caolán McNamara <caolanm@redhat.com> - 4.4.2-4
- Resolves: rhbz#669237 strip libicudata

* Mon Nov 29 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.2-3
- Resolves: rhbz#657964 icu-config bindir returns sbindir

* Thu Nov 25 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.2-2
- Resolves: rhbz#654200 revert icu#5431

* Mon Oct 04 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.2-1
- latest version

* Wed Sep 29 2010 jkeating - 4.4.1-6
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.1-5
- upstream patches

* Thu Sep 09 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.1-4
- Resolves: rhbz#631403 doxygen no longer generates gifs

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.1-3
- move licences into libicu, and add them into the -doc subpackage
  as well

* Wed May 26 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.1-2
- Resolves: rhbz#596171 drop icu.icu6284.strictalias.patch and use
  -fno-strict-aliasig as upstream has added a pile more and doesn't look
  interested in proposed patchs

* Thu Apr 29 2010 Caolán McNamara <caolanm@redhat.com> - 4.4.1-1
- latest version
- drop integrated icu.icu7567.libctest.patch

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 4.4-1
- latest version
- drop integrated icu.6969.pkgdata.patch
- drop integrated icu.icu7039.badextract.patch
- drop integrated icu.XXXX.buildfix.patch

* Wed Dec 02 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-8
- Resolves: rhbz#543386 update icu-config

* Thu Nov 19 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-7
- Fix FTBFS with yet another autoconf version that changes
  behaviour

* Mon Aug 31 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-6
- Resolves: rhbz#520468 fix s390x and other secondary archs

* Tue Jul 28 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-5
- icu#7039 fix broken use of extract to get tests working

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-3
- make documentation noarch

* Tue Jul 14 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-2
- rpmlint warnings

* Fri Jul 03 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.1-1
- 4.2.1 release

* Fri Jun 26 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.0.1-3
- Resolves: rhbz#508288 multilib conflict

* Thu Jun 11 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.0.1-2
- Resolves: rhbz#505252 add icu.6995.kannada.patch

* Mon Jun 08 2009 Caolán McNamara <caolanm@redhat.com> - 4.2.0.1-1
- 4.2.0.1 release

* Sat May 09 2009 Caolán McNamara <caolanm@redhat.com> - 4.2-1
- 4.2 release

* Sun May 03 2009 Caolán McNamara <caolanm@redhat.com> - 4.2-0.1.d03
- 4.2 release candidate
- drop resolved icu.icu6008.arm.padding.patch
- drop resolved icu.icu6439.bare.elif.patch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Caolán McNamara <caolanm@redhat.com> - 4.0.1-2
- fix bare elif for gcc-4.4

* Fri Jan 16 2009 Caolán McNamara <caolanm@redhat.com> - 4.0.1-1
- 4.0.1 release

* Mon Dec 29 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-6
- Resolves rhbz#225896 clean up low hanging rpmlint warnings

* Tue Dec 16 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-5
- drop integrated icu.icu5557.safety.patch

* Thu Nov 20 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-4
- annoyingly upstream tarball was repacked apparently to remove
  some unused/cached dirs

* Sat Sep 06 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-3
- Resolves: rhbz#461348 wrong icu-config

* Tue Aug 26 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-2
- Resolves: rhbz#459698 drop Malayalam patches. Note test with Rachana/Meera
  instead of Lohit Malayalam before filing bugs against icu wrt.
  Malayalam rendering

* Sat Jul 05 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-1
- final release

* Mon Jun 30 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-0.3.d03
- 4.0 release candidate

* Wed Jun 04 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-0.2.d02
- drop icu.icu5498.openoffice.org.patch

* Sat May 31 2008 Caolán McNamara <caolanm@redhat.com> - 4.0-0.1.d02
- 4.0 release candidate
- drop integrated icu.regexp.patch

* Mon May 19 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-8
- add icu.icu6284.strictalias.patch and build with
  strict-aliasing

* Tue Mar 18 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-7
- Resolves: rhbz#437761 modify to icu.icu6213.worstcase.patch for
  other worst case expansions

* Mon Mar 17 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-6
- Resolves: rhbz#437761 add icu.icu6213.bengali.worstcase.patch

* Mon Feb 04 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-5
- Resolves: rhbz#431401 split syllables on 1st 0d4d of a 0d4d +
  (>= 0d15 && <= 0d39) + 0d4d + 0d30 sequence

* Thu Jan 31 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-4
- Resolves: rhbz#431029, rhbz#424661 Remove workaround for 0D31 characters

* Fri Jan 25 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-3
- CVE-2007-4770 CVE-2007-4771 add icu.regexp.patch
- Resolves: rhbz#423211 fix malalayam stuff in light of syllable
  changes

* Fri Jan 11 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-2
- remove icu.icu5365.dependantvowels.patch and cleanup
  icu.icu5506.multiplevowels.patch as they patch and unpatch
  eachother (thanks George Rhoten for pointing out that madness)

* Fri Jan 11 2008 Caolán McNamara <caolanm@redhat.com> - 3.8.1-1
- latest version
- drop fixed icu.icu6084.zwnj.notdef.patch

* Thu Dec 13 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-6
- Resolves: rhbz#423211 experimental hack for 0d15+0d4d+0d30

* Tue Dec 11 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-5
- Resolves: rhbz#415541 icu.icu6084.zwnj.notdef.patch

* Wed Nov 28 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-4
- Resolves: ooo#83991 Malayalam "Kartika" font fix

* Tue Nov 13 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-3
- add icu.openoffice.org.patch

* Sat Oct 27 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-2
- add icu.icu6008.arm.padding.patch to fix an arm problem

* Tue Oct 02 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-1
- latest version

* Mon Sep 03 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-0.2.d02
- next release candidate

* Wed Aug 29 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-0.2.d01
- rebuild

* Tue Aug 07 2007 Caolán McNamara <caolanm@redhat.com> - 3.8-0.1.d01
- 3.8 release candidate
- drop integrated icu.icu5433.oriya.patch
- drop integrated icu.icu5488.assamese.patch
- drop integrated icu.icu5500.devicetablecrash.patch
- drop integrated icu.icu5501.sinhala.biggerexpand.patch
- drop integrated icu.icu5594.gujarati.patch
- drop integrated icu.icu5465.telegu.patch

* Wed Jun 13 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-20
- Resolves: rhbz#243984 change the icu group as it is libicu
  which is "System Environment/Libraries" not icu

* Mon Apr 30 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-19
- Resolves: rhbz#220867 Malayalam rendering

* Tue Feb 13 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-18
- Resolves: rhbz#228457 icu.icu5594.gujarati.patch

* Fri Feb 09 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-17
- spec cleanups

* Mon Feb 05 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-16
- Resolves: rhbz#226949 layout telegu like pango

* Fri Jan 19 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-15
- Resolves: rhbz#214948 icu.icu5506.multiplevowels.patch

* Tue Jan 09 2007 Caolán McNamara <caolanm@redhat.com> - 3.6-14
- Related: rhbz#216089 add icu.icu5557.safety.patch

* Thu Dec 21 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-13
- Resolves: rhbz#220433 modify icu.icu5431.malayam.patch

* Fri Nov 10 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-12
- Resolves: rhbz#214948 icu.icu5506.multiplevowels.patch

* Wed Nov 08 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-11
- Resolves: rhbz#214555 icu.icu5501.sinhala.biggerexpand.patch

* Wed Nov 08 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-10
- Resolves: rhbz#214555 icu.icu5500.devicetablecrash.patch

* Wed Oct 18 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-9
- Resolves: rhbz#213648 extend prev/next to handle ZWJ

* Wed Oct 18 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-8
- Resolves: rhbz213375 (icu.icu5488.assamese.patch)

* Wed Oct 18 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-7
- Resolves: rhbz#211258 (icu.icu5465.telegu.patch)

* Thu Oct 05 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-6
- rh#209391# add icu.icuXXXX.virama.prevnext.patch

* Mon Oct 02 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-5
- rh#208705# add pkg-config Require for -devel package
- add icu.icu5431.malayam.patch for rh#208551#/rh#209084#
- add icu.icu5433.oriya.patch for rh#208559#/rh#209083#

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 3.6-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-3
- rh#206615# render malayam like pango

* Wed Sep 06 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-2
- fix rh#205252#/icu#5365 (gnome#121882#/#icu#4026#) to make icu
  like pango for multiple dependant vowels

* Sun Sep 03 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-1
- final release

* Mon Aug 14 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-0.1.d02
- bump

* Tue Aug 08 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-0.2.d01
- c++ code not alias correct

* Mon Jul 31 2006 Caolán McNamara <caolanm@redhat.com> - 3.6-0.1.d01
- rh#200728# update to prelease 3.6d01 to pick up on sinhala fixes
- drop integrated rh190879.patch
- drop integrated icu-3.4-sinhala1.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4-10.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4-10.1
- rebuild

* Sat Jun 10 2006 Caolán McNamara <caolanm@redhat.com> - 3.4-10
- rh#194686# BuildRequires

* Tue May 09 2006 Caolán McNamara <caolanm@redhat.com> - 3.4-9
- rh#190879# backport fix

* Wed May 03 2006 Caolán McNamara <caolanm@redhat.com> - 3.4-8
- add Harshula's icu-3.4-sinhala1.patch for some Sinhala support

* Tue May 02 2006 Caolán McNamara <caolanm@redhat.com> - 3.4-7
- add a pkgconfig.pc, make icu-config use it

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.4-6.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.4-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 03 2006 Caolán McNamara <caolanm@redhat.com> - 3.4-6
- add icu-gcc41.patch

* Tue Oct 11 2005 Caolán McNamara <caolanm@redhat.com> - 3.4-5
- clear execstack requirement for libicudata

* Mon Sep 12 2005 Caolán McNamara <caolanm@redhat.com> - 3.4-4
- import extra icu.spec into fedora core for openoffice.org
- build with gcc 4

* Wed Aug 31 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 3.4-3
- Use dist
- gcc32 does not understand -fstack-protector and
  --param=ssp-buffer-size=4

* Tue Aug  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.4-2
- 3.4.

* Sun Jul 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.4-0.2.d02
- 3.4-d02.
- Don't ship static libraries.

* Wed Apr 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.2-3
- Apply upstream case mapping mutex lock removal patch.
- Build with gcc 3.2 as a temporary workaround for #152495.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.2-2
- rebuilt

* Sat Jan  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.2-1
- Don't use %%{_smp_mflags} (b.f.u #2357).
- Remove unnecessary Epochs.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2-0.fdr.1
- Update to 3.2.

* Sun Jul 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.0-0.fdr.1
- Update to 3.0, datadirs patch no longer needed.
- Package data in shared libs, drop -locales subpackage.
- Rename -docs subpackage to libicu-doc, and generate graphs with graphviz.

* Sat Dec 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6.1-0.fdr.3
- Partial fix for bad datadirs returned by icu-config (works as long as
  data packaging mode is not "common" or "dll").

* Sun Nov 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6.1-0.fdr.2
- First complete version.

* Sun Sep 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6.1-0.fdr.1
- Update to 2.6.1.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.6-0.fdr.1
- First build, based on upstream and SuSE 8.2 packages.
