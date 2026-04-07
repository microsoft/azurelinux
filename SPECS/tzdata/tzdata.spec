# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Timezone data
Name: tzdata
Version: 2025c
%define tzdata_version 2025c
%define tzcode_version 2025c
Release: 1%{?dist}
License: LicenseRef-Fedora-Public-Domain AND (GPL-2.0-only WITH ClassPath-exception-2.0)
URL: https://www.iana.org/time-zones
Source0: ftp://ftp.iana.org/tz/releases/tzdata%{tzdata_version}.tar.gz
Source1: ftp://ftp.iana.org/tz/releases/tzcode%{tzcode_version}.tar.gz

Patch002: 0002-Fix-have-snprintf-error.patch
Patch003: 0003-continue-to-ship-posixrules.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: gawk, glibc, perl-interpreter
BuildRequires: java-25-devel
BuildRequires: glibc-common >= 2.5.90-7
Conflicts: glibc-common <= 2.3.2-63
BuildArchitectures: noarch
ExcludeArch: i686

# Using '--with vanguard' will change the data format to the new vanguard form.
%bcond_with vanguard

%description
This package contains data files with rules for various timezones around
the world.

%package java
Summary: Timezone data for Java
Source3: javazic-1.8-37392f2f5d59.tar.xz
Source4: ZoneTest.java
Patch100: 8051641.patch
Patch101: javazic-harden-links.patch

%description java
This package contains timezone information for use by Java runtimes.

%prep
%setup -q -c -a 1

%patch -p1 -P 2
%if 0%{?rhel}
%patch -p1 -P 3
%endif

# zic now defaults to "-b slim" to control data bloat.
# This can cause build issues for some packages.
# For now, build with ZFLAGS="-b fat" for backward compatibitliy.

# tzdata-2018g introduced 25:00 transition times.  This breaks OpenJDK.
# Use rearguard for java
mkdir rearguard
make VERSION=%{version} ZFLAGS="-b fat" tzdata%{version}-rearguard.tar.gz.t
mv tzdata%{version}-rearguard.tar.gz rearguard
pushd rearguard
tar zxf tzdata%{version}-rearguard.tar.gz
popd

%if 0%{?rhel}
# Use rearguard for rhel (overwrite default dataform)
tar zxf rearguard/tzdata%{version}-rearguard.tar.gz
%endif

tar xf %{SOURCE3}
%patch -P 100
%patch -p1 -P 101

echo "%{name}%{tzdata_version}" >> VERSION

%build
# Run make to create the tzdata.zi file
rm tzdata.zi
%if %{with vanguard}
make VERSION=%{version} ZFLAGS="-b fat" DATAFORM=vanguard tzdata.zi
%elif 0%{?rhel}
make VERSION=%{version} ZFLAGS="-b fat" DATAFORM=rearguard tzdata.zi
%else
make tzdata.zi
%endif

FILES="africa antarctica asia australasia europe northamerica southamerica
       etcetera backward factory"

mkdir zoneinfo/{,posix,right}
zic -b fat -y ./yearistype -d zoneinfo -L /dev/null -p America/New_York $FILES
zic -b fat -y ./yearistype -d zoneinfo/posix -L /dev/null $FILES
zic -b fat -y ./yearistype -d zoneinfo/right -L leapseconds $FILES

# grep -v tz-art.htm tz-link.htm > tz-link.html

# tzdata-2018g introduced 25:00 which breaks java - use the rearguard files for java
JAVA_FILES="rearguard/africa rearguard/antarctica rearguard/asia \
      rearguard/australasia rearguard/europe rearguard/northamerica \
      rearguard/southamerica rearguard/etcetera \
      rearguard/backward"

# Java 8 tzdata
pushd javazic-1.8
javac -source 1.8 -target 1.8 -classpath . `find . -name \*.java`
popd

java -classpath javazic-1.8 build.tools.tzdb.TzdbZoneRulesCompiler \
    -srcdir . -dstfile tzdb.dat \
    -verbose \
    $JAVA_FILES javazic-1.8/tzdata_jdk/gmt javazic-1.8/tzdata_jdk/jdk11_backward

%install
rm -fr $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}
cp -prd zoneinfo $RPM_BUILD_ROOT%{_datadir}
install -p -m 644 zone.tab zone1970.tab iso3166.tab leap-seconds.list leapseconds tzdata.zi $RPM_BUILD_ROOT%{_datadir}/zoneinfo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/javazi-1.8
install -p -m 644 tzdb.dat $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/

%check
echo ============TESTING===============
/usr/bin/env LANG=C make -k VALIDATE=':' check && true

# Create a custom JAVA_HOME, where we can replace tzdb.dat with the
# one just built, for testing.
system_java_home=$(dirname $(readlink -f $(which java)))/..
mkdir -p java_home
cp -Lr $system_java_home/* java_home/.
for tzdb in $(find java_home -name tzdb.dat) ; do
    rm $tzdb
    cp $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/tzdb.dat $tzdb
done
# Compile the smoke test and run it.
cp %{SOURCE4} .
javac ZoneTest.java
java_home/bin/java ZoneTest
echo ============END TESTING===========

%files
%{_datadir}/zoneinfo
%license LICENSE
%doc README
%doc theory.html
%doc tz-link.html
%doc tz-art.html

%files java
%{_datadir}/javazi-1.8

%changelog
* Sun Dec 14 2025 Patsy Griffin <patsy@redhat.com> - 2025c-1
  Update to tzdata-2025c (#2421294)
  - Update the expiration date for the leap seconds files.

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2025b-3
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Patsy Griffin <patsy@redhat.com> - 2025b-1
  Update to tzdata-2025b (#2354293)
  - Chile's Aysén Region moves from -04/-03 to -03 year-round,
    diverging from America/Santiago and creating a new zone
    America/Coyhaique.

* Tue Feb 04 2025 Patsy Griffin <patsy@redhat.com> - 2025a-1
  Update to tzdata-2025a (#2338511)
  - Paraguay is now permanently at -03. This impacts timestamps
    starting on 2025-03-22.
  - Includes improvements to pre-1991 data for the Philippines.
  - Etc/Unknown is now reserved.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 12 2024 Patsy Griffin <patsy@redhat.com> - 2024b-1
- Update to tzdata-2024b (#2310315)
  - Improve historical data for Mexico, Mongolia, and Portugal.
  - System V names are now obsolescent.
  - The main data form now uses %z.
  - The code now conforms to RFC 8536 for early timestamps.
  - Support POSIX.1-2024, which removes asctime_r and ctime_r.
  - Assume POSIX.2-1992 or later for shell scripts.
  - SUPPORT_C89 now defaults to 1.
  - Include two upstream patches for month names as in April vs Apr.
- Harden against links to removed zones

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 28 2024 Patsy Griffin <patsy@redhat.com> - 2024a-8
- zic now defaults to "-b slim" to control data bloat.
  For now, build with ZFLAGS="-b fat" for backward compatibitliy.

* Tue May 14 2024 Miro Hrončok <mhroncok@redhat.com> - 2024a-7
- Rebuilt with glibc-2.39.9000-10 to avoid regressions described in rhbz#2280403

* Fri Apr 26 2024 Jonathan Wakely <jwakely@redhat.com> - 2024a-6
- Add support for --with vanguard

* Thu Apr 04 2024 Patsy Griffin <patsy@redhat.com> - 2024a-5
- Add java patch to fix incorrect calculations for
  Africa/Casablanca starting in 2027. (#2266311)

* Sat Mar 02 2024 Andrew Hughes <gnu.andrew@redhat.com> - 2024a-4
- Remove hardcoded versioned path to javac

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2024a-3
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 06 2024 Patsy Griffin <patsy@redhat.com> - 2024a-2
- Correct the bz# for the tzdata-2024 commit.

* Mon Feb 05 2024 Patsy Griffin <patsy@redhat.com> - 2024a-1
- Rebase to tzdata-2024a
  - Kazakhstan will transition from UTC+6 to UTC+5 on 2024-03-01.
  - Palestine will spring forward a week later than previously
    predicted.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Patsy Griffin <patsy@redhat.com> - 2023d-2
- Migrate License field to SPDX identifiers for
  https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_2

* Wed Jan 03 2024 Patsy Griffin <patsy@redhat.com> - 2023d-1
- Rebase to tzdata-2023d
  - Include time zone changes for Ittoqqortoormiit, Greenland
    and Vostok, Antarctica.
  - Update the expiration date for the leap-seconds.list file.
    No new leap seconds were added.

* Wed Dec 13 2023 Patsy Griffin <patsy@redhat.com> - 2023c-5
- Remove Java 6/7 support for Fedora 40 and RHEL 10 forward.

* Tue  Oct  3 2023 David Cantrell <dcantrell@redhat.com> - 2023c-4
- Use the new syntax for the %%patch macro in the spec file

* Mon Jul 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2023c-3
- Disable Java 6/7 data in RHEL 10 builds

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 29 2023 Patsy Griffin <patsy@redhat.com> - 2023c-1
- Rebase to tzdata-2023c
  - Reinstate Lebanon DST change effective March 25.

* Fri Mar 24 2023 Patsy Griffin <patsy@redhat.com> - 2023b-1
- Rebase to tzdata-2023b
  - Lebanon will transition to DST on April 20/21, not March 25/26.

* Thu Mar 23 2023 Patsy Griffin <patsy@redhat.com> - 2023a-1
- Rebase to tzdata-2023a
 - Egypt reintroduced DST, from April through October.
 - Morocco springs forward April 23, not April 30.
 - Palestine delayed the start of DST this year.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022g-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Patsy Griffin <patsy@redhat.com> - 2022g-1
- Rebase to tzdata-2022g
  - The northern edge of the Mexican state of Chihuahua will
    change time zone to agree with nearby US locations on
    2022-11-30.
  - Added a new Zone America/Ciudad_Juarez that splits from
    America/Ojinaga.

* Mon Oct 31 2022 Patsy Griffin <patsy@redhat.com> - 2022f-1
- Rebase to tzdata-2022f
  - Mexico will stop observing DST except near the US border.
  - Chihuahua moved to -06 year round starting on 2022-10-30.
  - Fiji no longer observes DST.

* Fri Oct 14 2022 Patsy Griffin <patsy@redhat.com> - 2022e-1
- Rebase to tzdata-2022e
  - Jordan and Syria cancelled the DST transition planned
    for 2022-10-28, remaining at +03 permanently.

* Sun Sep 25 2022 Patsy Griffin <patsy@redhat.com> - 2022d-1
- Rebase to tzdata-2022d
  - Palestine DST transition will be on October 29, 2022, 
    not October 28, 2022.
  - Europe/Uzhgorod and Europe/Zaporozhye are moved to 'backzone'.

* Mon Aug 22 2022 Patsy Griffin <patsy@redhat.com> - 2022c-1
- Rebase to tzdata-2022c - supersedes tzdata-2022b
  - Add a work-around for an awk bug in FreeBSD, macOS, etc.
  - Improve tzselect with respect to intercontinental Zones.

* Sun Aug 14 2022 Patsy Griffin <patsy@redhat.com> - 2022b-1
- Rebase to tzdata-2022b
  - Chile transitions to DST on 2022-09-11, not 2022-09-04
  - 'make install' now defaults LOCALTIME to Factory rather than GMT
  - More zones that are the same since 1970 have been moved to backzone.
  - Include patch for awk workaround.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Patsy Griffin <patsy@redhat.com> - 2022a-3
- Java OpenJDK packages are no longer available on i686.
  Exclude i686 builds. (bz #2104108)

* Tue Jun 07 2022 Patsy Griffin <patsy@redhat.com> - 2022a-2
- Include leap-second.list in tzdata install. (#2091390)

* Wed Mar 23 2022 Patsy Griffin <patsy@redhat.com> - 2022a-1
- Rebase to tzdata-2022a
  - Palestine springs forward on 2022-03-27, not 2022-03-26.
  - zdump -v now outputs better failure information.
  - bug fixes for code that reads corrupted TZif data.

* Tue Feb 08 2022 Patsy Griffin <patsy@redhat.com> - 2021e-4
- Clean-up changelog.

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2021e-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Java17

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021e-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Patsy Griffin <patsy@redhat.com> - 2021e-1
- Rebase to tzdata-2021e - supersedes tzdata-2021d
  - Pacific/Fiji suspended DST for the 2021/2022 season.
  - 'zic -r' now marks unspecified timestamps with "-00".
  - Palestine will fall back 2021-10-29 at 01:00, rather
    than the predicted 2021-10-30.

* Thu Oct 07 2021 Patsy Griffin <patsy@redhat.com> - 2021c-1
- Rebase to tzdata-2021c
  - Revert most 2021b changes to the 'backward' file.
  - Fix 'zic -b fat' bug in pre-1970 32-bit data reported in tzdata-2021b.
  - Fix two Link line typos from tzdata-2021b.
  - Distribute the new SECURITY file.

* Sat Sep 25 2021 Patsy Griffin <patsy@redhat.com> - 2021b-1
- Rebase to tzdata-2021b
  - Jordan now starts DST on February's last Thursday.
  - Samoa no longer observes DST.
  - Merge more location-based Zones whose timestamps agree since 1970.
  - Move some backward-compatibility links to 'backward'.
  - Rename Pacific/Enderbury to Pacific/Kanton.
  - Correct many pre-1993 transitions in Malawi, Portugal, etc.
  - zic now creates each output file or link atomically.
  - zic -L no longer omits the POSIX TZ string in its output.
  - zic fixes for truncation and leap second table expiration.
  - zic now follows POSIX for TZ strings using all-year DST.
  - Fix some localtime crashes and bugs in obscure cases.
  - zdump -v now outputs more-useful boundary cases.
  - tzfile.5 better matches a draft successor to RFC 8536.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Patsy Griffin <patsy@redhat.com> - 2021a-1
- Rebase to tzdata-2021a
  - South Sudan will change from +03 to +02 on 2021-02-01.

* Wed Dec 30 2020 Patsy Griffin <patsy@redhat.com> - 2020f-1
- Rebase to tzdata-2020f including changes for tzdata-2020e
  - tzdata-2020f fixes a bug in tzdata-2020e that caused an
    invalid zi file in rearguard format
  - Volgograd changes time zone from UTC+04 to UTC+03 on 2020-12-27.
  - Australia/Currie is identical to Australia/Hobart for all
    timestamps since 1970 and was therefore created by mistake,
    now moved to the "backward" file.

* Wed Dec 16 2020 Patsy Griffin <patsy@redhat.com> - 2020d-3
- Add 0003-continue-to-ship-posixrules.patch to initialize
  POSIXRULES variable.

* Wed Dec 16 2020 Patsy Griffin <patsy@redhat.com> - 2020d-2
- Add conditional support for rhel and eln.

* Fri Oct 23 2020 Patsy Griffin <patsy@redhat.com> - 2020d-1
- Rebase to tzdata-2020d including changes from tzdata-2020c
  - Palestine will end summer time on 2020-10-24 rather than the
    predicted 2020-10-31.
  - Fiji starts DST later than usual, on 2020-12-20.
  - Rearguard now provides an empty file pacificnew to support
    downstream software that expects it.

* Wed Oct 14 2020 Patsy Griffin <patsy@redhat.com> - 2020b-1
- Rebase to tzdata-2020b
  - Yukon timezones represented by America/Whitehorse and
    America/Dawson will change time zone rules from -08/-07 to
    permanent -07 on 2020-11-01, not on 2020-03-08 as 2020a had it.
  - The most recent winter(+08)/summer(+11) transition for Casey Station,
    Antarctica was 2020-10-04 00:01.
  - Remove obsolete files pacificnew, systemv, and yearistype.sh
    from the distribution.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2020a-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 12 2020 Jiri Vanek <jvanek@redhat.com> - 2020a-2
- bumped  source/target to 1.6 for tzdata for jdk6/7
- bumped  source/target to 1.8 for tzdata for jdk8

* Thu Apr 30 2020 Patsy Griffin <patsy@redhat.com> - 2020a-1
- Rebase to tzdata-2020a
  - Morocco will spring forward on 2020-05-31 rather than
    previously predicted 2020-05-24.
  - Canada's Yukon region changed to year round UTC -07
    effective 2020-03-08.
  - America/Godthab was renamed to America/Nuuk.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Patsy Griffin <patsy@redhat.com> - 2019c-2
- Don't build the factory zone for tzdata-java.
  Patch provided by Severin Gehwolf <sgehwolf@redhat.com> (#1789468)

* Mon Sep 23 2019 Patsy Griffin <patsy@redhat.com> - 2019c-1
- Rebase to tzdata-2019c
  - Fiji will observe DST from 2019-11-10 to 2020-01-12.
  - Norfolk Island will begin observing Australian-style DST on 2019-10-06.
- Add Factory back in to be more consistent with upstream.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Patsy Griffin <patsy@redhat.com> - 2019b-1
- Rebase to tzdata-2019b
  - Brazil will no longer observe DST going forward.
  - The 2019 spring transition for Palestine occurred 03-29, not 03-30.

* Fri Mar 29 2019 Patsy Griffin Franklin <patsy@redhat.com> - 2019a-1
- Rebase to tzdata-2019a
  - Palestine will start DST on 2019-03-30, rather than 2019-03-23 as
    previously predicted.
  - Metlakatla rejoined Alaska time on 2019-01-20, ending its observances
    of Pacific standard time.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018i-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Patsy Griffin Franklin <pfrankli@redhat.com> - 2018g-1
- Rebase to tzdata-2018g
  Includes changes for tzdata-2018f.
  - Volgograd will change from UTC+03 to UTC+04 on 2018-10-28 at 02:00.
  - Fiji will end DST on 2019-01-13 instead of the 2019-01-20 as
    previously predicted.
  - Most of Chile will end DST on the first Saturday in April at 24:00
    and restart DST on the first Saturday in September at 24:00.
  - Morocco will change from UTC+00/+01 to permanent +01 effective 2018-10-27.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018e-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 16 2018 Patsy Franklin <pfrankli@redhat.com> - 2018e-1
- Rebase to tzdata-2018e
  - North Korea changed from UTC+8:30 to UTC+9 on May 5, 2018.
  - In this update, the upstream project now defaults to using
    the "vanguard" data implementation which includes negative DST offsets.

* Wed Mar 28 2018 Patsy Franklin <pfrankli@redhat.com> - 2018d-1
- Rebase to tzdata-2018d:
  - DST for Asia/Gaza and Asia/Hebron has changed
    from March 31 to March 24.
  - Antarctica/Casey station changed to UTC+8 on March 11.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Patsy Franklin <pfrankli@redhat.com> - 2018c-1
- Rebase to tzdata-2018c:
  - São Tomé and Príncipe changed from +00 to +01 on January 1, 2018
  - Brazil's DST will start on the first Sunday in November
  - Support for the new zic -t option.
  - Add back pacificnew file omitted in tzdata-2018a

* Thu Oct 26 2017 Patsy Franklin <pfrankli@redhat.com> - 2017c-1
- Rebase to tzdata-2017c.
  - Northern Cyprus will revert to using EQ rules on October 29, 2017.
  - Sudan will switch from +03 to +02 on November 1, 2017.
  - Tonga will not change it's clocks on Novemeber 5, 2017 ending it's
    experiment with DST.
  - Fiji DST will end on January 14, 2018 rather than January 21, 2018.
  - Namibia - starting September 3, 2017 switches from +)1 with DST to
    +02 all year.  This change takes effect April 1, 2018.
  - Turks & Caicos changes from -04 all year to -05 with US DST starting
    on March 11, 2018.  Effective change date is November 4, 2018.
  - tzdata now includes two text versions of the time zone data - tzdata.zi
    and leapseconds.
  - Includes two patches to deal with build issues.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 Patsy Franklin <pfrankli@redhat.com> - 2017b-1
- Rebase to tzdata-2017b
  - Haiti began observing DST on March 12, 2017.

* Sun Mar 12 2017 Patsy Franklin <pfrankli@redhat.com> - 2017a-1
- Rebase to tzdata-2017a
  - Mongolia no longer observes DST
  - Magallanes region of Chile moves from -04/-03 to -03 year round.
    This results in a new zone, America/Punta_Arenas.

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 2016j-3
- Add missing %%license macro

* Wed Jan 18 2017 Patsy Franklin <pfrankli@redhat.com> - 2016j-2
- Add zone1970.tab file.
  Resolves: #1414518

* Thu Dec 01 2016 Patsy Franklin <pfrankli@redhat.com> - 2016j-1
- Rebase to 2016j
  - The Saratov Region of Russia is changing from +03 to +04 on
    2016-12-04, resulting in a new timezone Europe/Saratov.

* Thu Nov 03 2016 Patsy Franklin <pfrankli@redhat.com> - 2016i-1
- Rebase to 2016i
  - Pacific/Tongatapu now begins DST on 2016-11-06 at 02:00 and ends
    on 2017-01-15 at 03:00.
  - Northern Cyprus is changed to +03 year round. This results in a
    split in Cyprus time zones starting 2016-10-30 at 04:00 and
    creates a new zone - Asia/Famagusta.
  - Antarctica/Casey changed from +08 to +11 on 2016-10-22.

* Wed Oct 26 2016 Patsy Franklin <pfrankli@redhat.com> - 2016h-1
- Rebase to 2016h
  - DST ends in Asia/Gaza and Asia/Hebron on 2016-10-29 at 01:00,
    not the predicted date of 2016-10-21 at 00:00.

* Tue Oct 04 2016 Patsy Franklin <pfrankli@redhat.com> - 2016g-1
- Rebase to 2016g
  - Turkey permanently switches from +02 to +03 as of 2016-09-07,
  - Per IERS Bulletin C 52, leap second to be added on 2016-09-31 at 23:59:60.

* Wed Jul 06 2016 Patsy Franklin <pfrankli@redhat.com> - 2016f-1
- Rebase to 2016f
  - Egypt cancelled DST.
  - Asia/Novosibirsk transitions from +06 to +07 on 2016-07-24 at 02:00.

* Fri Jun 17 2016 Patsy Franklin <pfrankli@redhat.com> - 2016e-1
- Rebase to 2016e
  - Africa/Cairo starts DST on July 7 24:00 and ends on October 27
    at 24:00.

* Thu Apr 21 2016 Patsy Franklin <pfrankli@redhat.com> - 2016d-1
- Rebase to 2016d
  - America/Caracas switches from -0430 to -04 on 2016-05-01 at 02:30.
  - Asia/Magadan switchefrom +10 to +11 on 2016-04-24 at 02:00.
  - New zone Asia/Tomsk, split off from Asia/Novosibirsk.  It covers
    Tomsk Oblast, Russia, which switches from +06 to +07 on 2016-05-29
    at 02:00.

* Wed Mar 23 2016 Patsy Franklin <pfrankli@redhat.com> - 2016c-1
- Rebase to 2016c
  - Azerbaijan no longer observes DST.
  - Chile changes from permanent DST to seasonal DST.

* Tue Mar 15 2016 Patsy Franklin <pfrankli@redhat.com> - 2016b-1
- Rebase to 2016b
  - New zones Europe/Astrakhan and Europe/Ulyanovsk for Astrakhan and
    Ulyanovsk Oblasts, Russia, both of which will switch from +03 to +04 on
    2016-03-27 at 02:00 local time.  They need distinct zones since their
    post-1970 histories disagree.  New zone Asia/Barnaul for Altai Krai and
    Altai Republic, Russia, which will switch from +06 to +07 on the same date
    and local time.  The Astrakhan change is already official; the others have
    passed the first reading in the State Duma and are extremely likely.
    Also, Asia/Sakhalin moves from +10 to +11 on 2016-03-27 at 02:00.
  - As a trial of a new system that needs less information to be made up,
    the new zones use numeric time zone abbreviations like "+04"
    instead of invented abbreviations like "ASTT".
  - Haiti will not observe DST in 2016.
  - Palestine's spring-forward transition on 2016-03-26 is at 01:00, not 00:00.
    Guess future transitions will be March's last Saturday at 01:00, not March's
    last Friday at 24:00.

* Tue Feb 02 2016 Patsy Franklin <pfrankli@redhat.com> - 2016a-1
- Rebase to 2016a
  - America/Cayman will not observe daylight saving this year after all.
    Revert our guess that it would.
  - Asia/Chita switches from +0800 to +0900 on 2016-03-27 at 02:00.
  - Asia/Tehran now has DST predictions for the year 2038 and later,
    to be March 21 00:00 to September 21 00:00.  This is likely better
    than predicting no DST, albeit off by a day every now and then.
 
* Mon Oct 05 2015 Patsy Franklin <pfrankli@redhat.com> - 2015g-1
- Rebase to 2015g
  - Turkey's 2015 fall-back transition is scheduled for Nov. 8, not Oct. 25.
  - Norfolk moves from +1130 to +1100 on 2015-10-04 at 02:00 local time.
  - Fiji's 2016 fall-back transition is scheduled for January 17, not 24.
  - Fort Nelson, British Columbia will not fall back on 2015-11-01.  It has
    effectively been on MST (-0700) since it advanced its clocks on 2015-03-08.
    New zone America/Fort_Nelson.

* Wed Aug 12 2015 Patsy Franklin <pfrankli@redhat.com> - 2015f-1
- Rebase to 2015f
  - North Korea switches to +0830 on 2015-08-15.
    The abbreviation remains "KST".
  - Uruguay no longer observes DST.

* Fri Jun 19 2015 Patsy Franklin <pfrankli@redhat.com> - 2015e-1
- Morocco will suspend DST from 2015-06-14 03:00 through 2015-07-19 02:00,
  not 06-13 and 07-18 as we had guessed.
- Assume Cayman Islands will observe DST starting next year, using US rules.
  Although it isn't guaranteed, it is the most likely.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Patsy Franklin <pfrankli@redhat.com> - 2015d-3
- Morocco will suspend DST from 2015-06-14 03:00 through 2015-07-19 02:00,
  not 06-13 and 07-18 as we had guessed.

* Mon Apr 27 2015 Patsy Franklin <pfrankli@redhat.com> - 2015d-1
- Rebase to 2015d
  - Egypt will not observe DST in 2015 and will consider canceling it
    permanently.  For now, assume no DST indefinitely.
  - The abbreviations for Hawaii-Aleutian standard and daylight times
    have been changed from HAST/HADT to HST/HDT, as per US Government
    Printing Office style.  This affects only America/Adak since 1983,
    as America/Honolulu was already using the new style.

* Thu Apr 16 2015 Patsy Franklin <pfrankli@redhat.com> - 2015c-1
- Rebase to 2015c
  - Egypt's spring-forward transition is at 24:00 on April's last Thursday,
    not 00:00 on April's last Friday.  2015's transition will therefore be on
    Thursday, April 30 at 24:00, not Friday, April 24 at 00:00.  Similar fixes
    apply to 2026, 2037, 2043, etc.  (Thanks to Steffen Thorsen.)
- Rebase javazic tool to match latest upstream OpenJDK version

* Wed Mar 25 2015 Patsy Franklin <pfrankli@redhat.com> - 2015b-1
- Rebase to 2015b
  - Mongolia will start observing DST again this year, from the last
    Saturday in March at 02:00 to the last Saturday in September at 00:00.
  - Palestine will start DST on March 28, not March 27.  Also,
    correct the fall 2014 transition from September 26 to October 24.
    Adjust future predictions accordingly.

* Thu Feb 12 2015 Patsy Franklin <pfrankli@redhat.com> - 2015a-1
- Rebase to 2015a
  - New leap second 2015-06-30 23:59:60 UTC as per IERS Bulletin C 49.
  - The Mexican state of Quintana Roo, represented by America/Cancun,
    will shift from Central Time with DST to Eastern Time without DST
    on 2015-02-01 at 02:00.
  - Chile will not change clocks in April or thereafter; its new standard time
    will be its old daylight saving time.  This affects America/Santiago,
    Pacific/Easter, and Antarctica/Palmer.

* Wed Nov 19 2014 Patsy Franklin <pfrankli@redhat.com> - 2014j-1
- Rebase to 2014j
  - Turks & Caicos' switch from US eastern time to UTC-4 year-round
    did not occur on 2014-11-02 at 02:00.  It's currently scheduled
    for 2015-11-01 at 02:00.

* Mon Oct 27 2014 Patsy Franklin <pfrankli@redhat.com> - 2014i-1
- Rebase to 2014i
  - Pacific/Fiji will observe DST from 2014-11-02 02:00 to 2015-01-18 03:00.
  - A new Zone Pacific/Bougainville, for the part of Papua New Guinea
    that plans to switch from UTC+10 to UTC+11 on 2014-12-28 at 02:00

* Mon Oct 06 2014 Patsy Franklin <pfrankli@redhat.com> - 2014h-1
- Rebase to 2014h
  - Changes in past time stamps, code, and documentation.

* Wed Sep 10 2014 Patsy Franklin <pfrankli@redhat.com> - 2014g-1
- Rebase to 2014g
  - Turks & Caicos is switching from US eastern time to UTC-4 year-round,
    modeled as a switch from EST/EDT to AST on 2014-11-02 at 02:00.

* Thu Aug 14 2014 Patsy Franklin <pfrankli@redhat.com> - 2014f-1
- Rebase to 2014f
  - Russian time zone changes effective 2014-10-26
  - Several other time zone abbreviation changes as described in
    the NEWS file.

* Wed Jun 18 2014 Patsy Franklin <pfrankli@redhat.com> - 2014e-4
- Update changelog version to match release version.

* Tue Jun 17 2014 Patsy Franklin <pfrankli@redhat.com> - 2014e-3
- Rebase to 2014e
  - Morrocco suspends DTS for Ramadan
       June 28 at 03:00 and August 2 at 02:00
  - Egypt suspends DTS for Ramadan
       June 26 and July 31 at 24:00
- Additional edit to support OpenJDK8. (#1091029)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Patsy Franklin <pfrankli@redhat.com> 2014c-2
- Add support for new tzdata file format used by OpenJDK8.

* Wed May 14 2014 Patsy Franklin <pfrankli@redhat.com> 2014c-1
- Rebase to 2014c
  -Egypt will re-apply DST on May 15 at 24:00, except that DST
   will not be observed during Ramadan.

* Wed Mar 26 2014 Patsy Franklin <pfrankli@redhat.com> 2014b-1
- Rebase to 2014b
  - Crimea changes to Moscow time on March 30, 2014.

* Wed Mar 12 2014 Patsy Franklin <pfrankli@redhat.com> 2014a-1
- Rebase to 2014a
  - Turkey begins DST on 2014-03-31, not 03-30.

* Tue Jan 21 2014 Patsy Franklin <pfrankli@redhat.com> 2013i-2
- Fiji ends DST on 2014-01-19 at 02:00, not the previously scheduled 03:00.

* Wed Dec 18 2013 Patsy Franklin <pfrankli@redhat.com> 2013i-1
- Rebase with early release of 2013i from Paul Eggert github.
  - Jordan switches back to standard time at 00:00 on December 20,2013.
  - The 2006-2011 transition schedule is planned to resume in 2014.
  - The compile-time flag NOSOLAR has been removed.
  - The files solar87, solar88, and solar89 are no longer distributed.
  - tz-link.htm now mentions Noda Time.

* Wed Oct 30 2013 Patsy Franklin <pfrankli@redhat.com> 2013h-1
- Rebase to 2013h 
  - Lybia switched to using UTC+2 without DST
  - Western Sahara (Africa/ElAaiun) uses Morocco's DST rules
  - Acres and Amazon swithc to UTC-4 and UTC-5 on 2013-11-10
  - Add entries for DST transition in Morocco in the year 2038
 
* Thu Oct  3 2013 Patsy Franklin <pfrankli@redhat.com> 2013g-1
- Morocco moved end of DST from September to October.  Rebase to
  pick up the Morocco DST change.

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 2013d-1
- Rebase to 2013d
  - No fundamental changes
  - Drop four patches introduced in 2013c-2

* Thu Jul  4 2013 Petr Machata <pmachata@redhat.com> - 2013c-2
- Update descriptions in iso3166.tab; make Jerusalem coordinates in
  zone.tab more precise
  (0001-Adjust-commentary-to-try-to-defuse-recent-issues-som.patch)
- Update local mean time for Jerusalem to match more-precise longitude
  (0002-asia-Asia-Jerusalem-Fix-LMT-to-match-more-precise-lo.patch)
- Move Morocco's midsummer 2013 transitions
  (0003-Move-Morocco-s-midsummer-2013-transitions.patch)
- Israel now falls back on the last Sunday of October
  (0004-Israel-now-falls-back-on-the-last-Sunday-of-October.patch)

* Fri May 17 2013 Petr Machata <pmachata@redhat.com> - 2013c-1
- Upstream 2013c
  - Sync past stamps for Palestine and West Bank with timeanddate.com
  - Assume that the recent change to Paraguay's DST rules is permanent
  - Macquarie was uninhabited between 1919 and 1948.  It's also part
    of Australia (update in zone.tab).

* Wed Mar 27 2013 Petr Machata <pmachata@redhat.com> - 2013b-2
- Palestine starts Daylight Saving Time on March 29, 2013
  (tzdata-2013b-gaza.patch)

* Wed Mar 13 2013 Petr Machata <pmachata@redhat.com> - 2013b-1
- Upstream 2013b
  - Paraguay will end DST on March 24 this year
  - Haiti uses US daylight-saving rules this year
  - Morocco does not observe DST during Ramadan
- Upstream 2013a
  - Retire Chile patch, 2013a has the data
  - New Zones Asia/Khandyga, Asia/Ust-Nera, Europe/Busingen
  - Many changes in historical timestamps

* Wed Feb 27 2013 Petr Machata <pmachata@redhat.com> - 2012j-3
- DTS in Chile will end on 2013-04-28
  (0016-Chile-is-changing-its-DST-rules.patch)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012j-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Petr Machata <pmachata@redhat.com> - 2012j-1
- Upstream 2012j
  - Libya moved to CET

* Tue Nov  6 2012 Petr Machata <pmachata@redhat.com> - 2012i-2
- Preserve hardlinks that zic leaves behind, install with cp -d

* Mon Nov  5 2012 Petr Machata <pmachata@redhat.com> - 2012i-1
- Upstream 2012i
  - Cuba switched to DST

* Mon Nov  5 2012 Petr Machata <pmachata@redhat.com> - 2012h-2
- Switch back to using system zic, ignore upstream Makefile at all.
  We do so for java anyway.
- Drop Factory from distribution

* Wed Oct 31 2012 Petr Machata <pmachata@redhat.com> - 2012h-1
- Upstream 2012h
  - Brazilian state Bahia no longer has DST.
  - Brazilian state Tocantins now has DST.
  - Israel has new DST rules next year.
  - Jordan stays on DST this winter.

* Mon Oct 22 2012 Petr Machata <pmachata@redhat.com> - 2012g-1
- Upstream 2012g
  - Adjust the packaging for new Makefile
  - Palestine: Fall transition was Sep 21, not Sep 28
  - Samoa: Daylight Saving Time commences on Sunday 30th September
    2012 and ends on Sunday 7th of April 2013.
- Resolves: #868173

* Mon Sep 17 2012 Petr Machata <pmachata@redhat.com> - 2012f-1
- Fiji will start daylight savings at 2 am on Sunday 21st October 2012
  and end at 3 am on Sunday 20th January 2013.  Guess it will be like
  that in following years as well.
- Resolves: #857231

* Mon Aug 13 2012 Petr Machata <pmachata@redhat.com> - 2012e-1
- Tokelau is in time zone UTC+13, not UTC+14 (and always was)

* Fri Jul 20 2012 Petr Machata <pmachata@redhat.com> - 2012d-1
- Upstream 2012d
  - Morocco will not observe DST during the month of Ramadan.
    DST cessation end date was corrected.

* Fri Jul 13 2012 Petr Machata <pmachata@redhat.com> - 2012c-2
- Morocco will not observe DST during the month of Ramadan
  (tzdata-2012c-morocco.patch)

* Mon Apr  2 2012 Petr Machata <pmachata@redhat.com> - 2012c-1
- Upstream 2012c
  - Haiti observes DST from 2012 on
  - Gaza Strip and Hebron observe DST in 2012
  - Change start of DST in Syria to last Friday in March

* Fri Mar 16 2012 Petr Machata <pmachata@redhat.com> - 2012b-3
- Morocco moved DST entry to last Sunday of April

* Thu Mar 15 2012 Petr Machata <pmachata@redhat.com> - 2012b-2
- Morocco DST starts on the last Sunday of March (March 25, 2012) and
  ends on last Sunday of September, except the month of Ramadan.  It
  is currently unclear what that Ramadan bit means, so this is not
  covered by the patch as of now.

* Tue Mar  6 2012 Petr Machata <pmachata@redhat.com> - 2012b-1
- Rebase to 2012b; changes vs. 2011n-5:
  - Changes to zones for Antarctica stations
  - Armenia abolished DST in 2012 and forward
  - Cuba enters DST on 31st March
  - Falkland Islands will stay on permanent Summer Time
  - New zone for Creston Valley, Canada, which differs from Dawson
    Creek in past stamps.  Changes to historical stamps in Canada.
  - Last year, Tokelau skipped over the date line together with Samoa

* Fri Feb 24 2012 Petr Machata <pmachata@redhat.com> - 2011n-5
- Add a patch for change in Chilean DST
- Update URLs

* Tue Feb 21 2012 Petr Machata <pmachata@redhat.com> - 2011n-4
- Add a patch for the leap second that will occur this summer

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011n-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  3 2011 Petr Machata <pmachata@redhat.com> - 2011n-2
- Fix building of Java zones.  Patch by Deepak Bhole

* Mon Oct 31 2011 Petr Machata <pmachata@redhat.com> - 2011l-1
- Rebase to 2011n
  - Drop all patches, including the Kemerovo patch, which is not in
    upstream
  - Cuba postponed DST by two weeks to Nov 13
  - Fiji will enter DST on Jan 21
- Resolved: #748778

* Wed Oct 19 2011 Petr Machata <pmachata@redhat.com> - 2011l-3
- Ukraine will enter Winter Time after all

* Fri Oct 14 2011 Petr Machata <pmachata@redhat.com> - 2011l-2
- State of Bahia, Brazil, to resume Summer Time on Oct 16
- The project moved, reflect this in URL
- Resolves: #746183

* Tue Oct 11 2011 Petr Machata <pmachata@redhat.com> - 2011l-1
- Upstream 2011l:
  - Fix ancient stamps for America/Sitka
  - Asia/Hebron transitioned to standard time already on Sep 30, not Oct 3
  - Fiji will introduce DST on Oct 22

* Wed Sep 21 2011 Petr Machata <pmachata@redhat.com> - 2011k-0.1.20110921
- Upstream 2011j:
  - Fix the Samoa date line skip
  - Changes in past timestamp typos several Africa zones
- Proposed upstream 2011k:
  - Belarus and Ukraine adopt permanent DST in 2011
  - Palestine suspends DST during Ramadan in 2011
  - Gaza and West Bank split in 2011.  West Bank is tracked in the
    timezone Asia/Hebron.  zone.tab update accordingly.
- Resolves: #737896

* Mon Aug 29 2011 Petr Machata <pmachata@redhat.com> - 2011h-1
- Upstream 2011i:
  - Add Africa/Juba (South Sudan) zone
  - Samoa skips over the date line on 2011-12-30
  - Use KALT as abbreviation for Europe/Kalinigrad
  - Canonical version of the Newfoundland patch
  - Change America/Resolute use of EST to 2006-2007 only
  - Assume Metlakatla abandoned use of daylight saving in 1983
  - Sync iso3166.tab and zone.tab with above
- Resolved: #734063

* Wed Aug 10 2011 Petr Machata <pmachata@redhat.com> - 2011h-2
- Patch for upcoming change in Newfoundland.  The transition time
  changes from 12:01 AM to 2:00 AM.

* Mon Jun 27 2011 Petr Machata <pmachata@redhat.com> - 2011h-1
- Upstream 2011h:
  - Russia abandons DST in 2011.
  - *.tab: change AN (Netherlands Antilles) to CW (Curacao)

* Tue Apr 26 2011 Petr Machata <pmachata@redhat.com> - 2011g-1
- Upstream 2011e:
  - Morocco introduced DST for 2011 from April 2 to July 31.
  - Delay end of DST in Chile in 2011 until May 7.
- Upstream 2011f:
  - The Falkland Islands will not turn back clocks this winter, but
    stay on daylight saving time.
- Upstream 2011g:
  - Egypt abandons DST in 2011 (and forward)
- Dropped tzdata-2011d-chile.patch
- Dropped tzdata-2011d-morocco.patch

* Wed Mar 30 2011 Petr Machata <pmachata@redhat.com> - 2011d-3
- Morocco introduced DST for 2011 from April 2 to July 31. (tzdata-2011d-morocco.patch)

* Tue Mar 29 2011 Petr Machata <pmachata@redhat.com> - 2011d-2
- Delay end of DST in Chile in 2011 until May 7. (tzdata-2011d-chile.patch)

* Tue Mar 15 2011 Petr Machata <pmachata@redhat.com> - 2011d-1
- Upstream 2011d:
  - Change end of DST in Samoa in 2011.
  - Change start of DST in Cuba in 2011.
  - Move start of DST in Turkey by one day in 2011.
- Dropped tzdata-2011b-c.patch

* Fri Mar 04 2011 Petr Machata <pmachata@redhat.com> - 2011b-3
- Kemerovo oblast should use OMST/OMSST abbreviation (tzdata-2011b-kemerovo.patch)

* Thu Mar 03 2011 Petr Machata <pmachata@redhat.com> - 2011b-2
- Update of historical stamps for Juneau, Sitka, and histcurrent stamps
  for Metlakatla.  Sitka and Metlakatla are new zones.
- Delay end of DST in Chile in 2011 until first Sunday in April. (tzdata-2011b-c.patch)

* Wed Feb 09 2011 Petr Machata <pmachata@redhat.com> - 2011b-1
- Upstream 2011b:
  - America/North_Dakota/Beulah: Mercer County, North Dakota, changed
    from the mountain time zone to the central time zone

* Mon Jan 24 2011 Petr Machata <pmachata@redhat.com> - 2011a-1
- Upstream 2011a:
  - Updates of historical stamps for Hawaii

* Tue Nov 09 2010 Petr Machata <pmachata@redhat.com> - 2010o-1
- Upstream 2010o:
  - Fiji will end DST on March 6, 2011, not March 27, 2011

* Wed Oct 27 2010 Petr Machata <pmachata@redhat.com> - 2010n-1
- Upstream 2010m:
  - Hong Kong didn't observe DST in 1977
  - In zone.tab, remove obsolete association of Vostok Station with
    South Magnetic Pole; add association with Lake Vostok
- Upstream 2010n:
  - Change end of DST in Samoa in 2011 from 2011-04-03 0:00 to
    2011-04-03 1:00

* Mon Aug 16 2010 Petr Machata <pmachata@redhat.com> - 2010l-2
- Upstream 2010l:
  - Change Cairo's 2010 reversion to DST from the midnight between
    September 8 and 9 to the midnight between September 9 and 10.
  - Change Gaza's 2010 return to standard time to the midnight between
    August 10 and 11.
  - Bahia de Banderas (Mexican state of Nayarit) changed time zone
    UTC-7 to new time zone UTC-6 on April 4, 2010

* Tue Aug  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2010k-1
- Upstream 2010k:
 - Egypt has announced that DST will be off during Ramadan, but
   DST will resume afterwards (August 10, 2010 - September 9, 2010)

* Tue May 11 2010 Petr Machata <pmachata@redhat.com> - 2010j-1
- Upstream 2010j:
  - Bahia de Banderas (Mexican state of Nayarit) changed time zone
    UTC-7 to new time zone UTC-6 on April 4, 2010

* Mon Apr 19 2010 Petr Machata <pmachata@redhat.com> - 2010i-1
- Upstream 2010i:
  - Morocco will have DST from 2010-05-02 to 2010-08-08
  - San Luis, Argentina will keep permanent DST after April 11, 2010
  - Updates of historical stamps for Taiwan

* Tue Apr 06 2010 Petr Machata <pmachata@redhat.com> - 2010h-2
- Upstream 2010g:
  - No Bangladesh DST in 2010 and forward.
  - Gaza DST starts last Saturday in March at 12:01 a.m. in 2010 and forward
  - Kamchatka and Anadyr change to Moscow+8 on 2010-03-28
  - Samara changes to Moscow+0 on 2010-03-28
  - Related zone.tab updates
- Upstream 2010h:
  - No DST in Tunisia in 2010 and forward
  - No DST in Pakistan in 2010 and forward
- Dropped tzdata-2010g-tunis.patch
- Dropped tzdata-2010f-g.patch
- Dropped tzdata-2010g-karachi.patch

* Mon Mar 29 2010 Petr Machata <pmachata@redhat.com> - 2010f-3
- Tunisia not to observe DST in 2010 (tzdata-2010g-tunis.patch)
- Pakistan not to observe DST in 2010 (tzdata-2010g-karachi.patch)

* Thu Mar 25 2010 Petr Machata <pmachata@redhat.com> - 2010f-2
- Fix the path in tzdata-2010f-g.patch

* Thu Mar 25 2010 Petr Machata <pmachata@redhat.com> - 2010f-1
- Upstream 2010f:
  - Changes to Australian stations in Antarctica
  - Correct 2010 Samoa DST start date
  - New zone Antarctica/Macquarie
  - Change Syria DST start from last Friday in March to first Friday
    in April in 2010 and forward
- Upstream 2010g proposal (tzdata-2010f-g.patch):
  - No Bangladesh DST in 2010 and forward.
  - Gaza DST starts last Saturday in March at 12:01 a.m. in 2010 and forward
  - Kamchatka and Anadyr change to Moscow+8 on 2010-03-28
  - Samara changes to Moscow+0 on 2010-03-28
  - Related zone.tab updates

* Tue Mar 09 2010 Petr Machata <pmachata@redhat.com> - 2010e-1
- Upstream 2010d
  - The DST change in Bangladesh takes place a minute earlier
  - Fiji to end DST on 2010-03-28 at 03:00, about a month earlier
  - Samoa to observe DST this year; they didn't observe DST last year
  - DST in Chile extended to 3 April
- Upstream 2010e:
  - Fix a typo in Bangladesh DST rule

* Mon Mar 01 2010 Petr Machata <pmachata@redhat.com> - 2010c-1
- Upstream 2010a
  - Source code cleanups
  - Historical timestamps for Bangladesh
- Upstream 2010b
  - Northern Mexico's border cities share the DST schedule with the
    United States
- Upstream 2010c
  - Paraguay DST now in effect from 2nd Sunday of April to 1st Sunday
    of October

* Mon Jan 04 2010 Petr Machata <pmachata@redhat.com> - 2009u-1
- Upstream 2009p
  - Argentina does not enter DST on October 18
  - San Luis switched from UTC-4 to UTC-3 on October 11th
- Upstream 2009q
  - Change DST end in Syria from November 1 to last Friday in October
  - Changes to past Hong Kong transitions
  - Kemerovo oblast' in Russia will change current time zone on March 28, 2010.
    Asia/Novokuznetsk is the new time zone name
- Upstream 2009r
  - Changes to local times of three Australian research stations in Antarctica
- Upstream 2009s
  - Fiji plans to re-introduce DST from November 29th 2009 to April 25th 2010
- Upstream 2009u
  - Bangladesh changed their clock back to Standard Time on December 31, 2009
- Dropped tzdata-2009o-argentinas.patch

* Wed Oct 21 2009 Petr Machata <pmachata@redhat.com> - 2009o-2
- San Luis (Argentina) entered DST on October 11 (tzdata-2009o-argentinas.patch)

* Mon Oct 19 2009 Petr Machata <pmachata@redhat.com> - 2009o-1
- Upstream 2009o
  - Bangladesh won't go back to Standard Time from October 1, 2009
  - Pakistan leaves DST on October 1, 2009
- Dropped tzdata-2009m-karachi.patch
- Argentina does not enter DST on October 18 (tzdata-2009o-argentinas.patch)

* Tue Sep 22 2009 Petr Machata <pmachata@redhat.com> - 2009m-2
- Add markers for autoupdate of spec file
- Pakistan leaves the period of DST on October 1 (tzdata-2009m-karachi.patch)

* Wed Sep 16 2009 Petr Machata <pmachata@redhat.com> - 2009m-1
- Upstream 2009m
  - Palestine will will revert back to winter time on Friday, 2009-09-04
  - Samoa passed the DST Bill that fixes DST dates for 2009 and 2010
- Drop Egypt patch

* Thu Aug 13 2009 Petr Machata <pmachata@redhat.com> - 2009k-3
- Egypt starts winter time on August 21.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009k-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Petr Machata <pmachata@redhat.com> - 2009k-1
- Upstream 2009k
  - Mauritius will not continue to observe DST the coming summer
  - Arbitrarily end DST at the end of 2009 so that a POSIX-style time
    zone string can appear in the Dhaka binary file

* Thu Jun 18 2009 Petr Machata <pmachata@redhat.com> - 2009j-1
- Upstream 2009j
  - DST switch for Bangladesh will occur an hour earlier than was
    thought.

* Mon Jun  8 2009 Petr Machata <pmachata@redhat.com> - 2009i-1
- Upstream 2009i
  - Bangladesh introduces DST 2009-06-20

* Tue May 26 2009 Petr Machata <pmachata@redhat.com> - 2009h-2
- Upstream 2009h
  - Convert use of 00:00 stamps to 24:00 of the previous day
  - Clarify that the data is Public Domain
- Drop Cairo patch

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009f-1
- Upstream 2009f
  - Pakistan will observe DST between 2009-04-15 and (probably) 2009-11-01
- Drop Pakistan patch

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009e-3
- Bump up for rebuild

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009e-2
- Pakistan will observe DST between 2009-04-15 and (probably) 2009-11-01

* Mon Apr  6 2009 Petr Machata <pmachata@redhat.com> - 2009e-1
- Upstream 2009e
  - Historical changes for Jordan
  - Palestine will start DST on 2009-03-26 and end 2009-09-27
- Egypt ends DST on 2009-09-24

* Mon Mar 23 2009 Petr Machata <pmachata@redhat.com> - 2009d-1
- Upstream 2009d
  - Morocco will observe DST from 2009-06-01 00:00 to 2009-08-21 00:00
  - Tunisia will not observe DST this year.
  - Syria will start DST on 2009-03-27 00:00 this year
  - Cuba will start DST on midnight between 2009-03-07 and 2009-03-08
  - Province of San Luis, Argentina, went to UTC-04:00 on 2009-03-15

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Petr Machata <pmachata@redhat.com> - 2009a-1
- Upstream 2009a
  - Fix Asia/Kathmandu spelling
  - Historical timestamps for Switzerland and Cuba
  - DST update for America/Resolute

* Thu Oct 30 2008 Petr Machata <pmachata@redhat.com> - 2008i-1
- Upstream 2008i
  - Updates for Argentina: Drop DST in zones America/Argentina/Jujuy,
    La_Rioja, San_Juan, Catamarca, Mendoza, Rio_Gallegos, Ushuaia; new
    zone America/Argentina/Salta (for provinces SA, LP, NQ, RN).

* Mon Oct 13 2008 Petr Machata <pmachata@redhat.com> - 2008h-1
- Upstream 2008h
  - Fix exact DST transition hour for Mauritius
  - Syria will leave the period of DST on Nov 1
  - Fix coordinates of Pacific/Niue

* Tue Oct  7 2008 Petr Machata <pmachata@redhat.com> - 2008g-1
- Upstream 2008g
  - Fixed future DST transitions for Brazil

* Tue Sep 16 2008 Petr Machata <pmachata@redhat.com> - 2008f-1
- Upstream 2008f
  - Changes for Mauritius (extends DST to years to come)
  - Palestine changes clocks for the duration of Ramadan
  - Argentina will start DST on Sunday October 19, 2008
  - Brazil will start DST on 2008-10-19
- Drop Pakistan and Morocco patches

* Thu Aug 28 2008 Petr Machata <pmachata@redhat.com> - 2008e-2
- Pakistan DST is scheduled until Oct/31
- Morocco DST is scheduled until Aug/31

* Tue Aug 12 2008 Petr Machata <pmachata@redhat.com> - 2008e-1
- Upstream 2008e
  - Changes for Mauritius
  - Leap second coverage for 31/Dec 2008
  - Corrections of historical dates

* Tue Jul  8 2008 Petr Machata <pmachata@redhat.com> - 2008d-1
- Upstream 2008d
  - Changes for Brazil and Mauritius

* Fri May 30 2008 Petr Machata <pmachata@redhat.com> - 2008c-1
- Upstream 2008c
  - Mongolia changes zone
  - Pakistan DST is scheduled until Sep/1, instead of Aug/31
- Drop Morocco and Pakistan patches that are superseded by upstream
- Fix a typo in Java subpackage name

* Tue May 27 2008 Petr Machata <pmachata@redhat.com> - 2008b-3
- Morocco introduces DST

* Fri May 23 2008 Petr Machata <pmachata@redhat.com> - 2008b-2
- Pakistan introduces DST

* Wed Mar 26 2008 Petr Machata <pmachata@redhat.com> - 2008b-1
- Upstream 2008b
  - DST changes for Syria, Cuba; Iraq abandons DST
  - Saigon zone renamed Ho_Chi_Minh; backward link provided
  - Add America/Argentina/San_Luis information

* Tue Mar  4 2008 Petr Machata <pmachata@redhat.com> - 2007k-2
- Chile moves DST to 29/Mar
- Related: #435959

* Thu Jan  3 2008 Petr Machata <pmachata@redhat.com> - 2007k-1
- Upstream 2007k
  - Argentina readopted the daylight saving time

* Tue Dec  4 2007 Petr Machata <pmachata@redhat.com> - 2007j-1
- Upstream 2007j
  - New links America/St_Barthelemy and America/Marigot
  - Venezuela is changing their clocks on December 9 at 03:00

* Mon Nov  5 2007 Petr Machata <pmachata@redhat.com> - 2007i-1
- Upstream 2007i
  - Syria DST will take place at Midnight between Thursday and Friday.
  - Cuba will end DST on the last Sunday of October.
- Update tst-timezone.c from glibc CVS

* Mon Oct  1 2007 Petr Machata <pmachata@redhat.com> - 2007h-1
- Upstream 2007h
  - Brazil will observe DST from 2007-10-14 to 2008-02-17
  - Egypt and Gaza switched earlier than we expected
  - Iran will resume DST next year
  - Venezuela is scheduled to change TZ to -4:30 on January 1

* Tue Sep 25 2007 Keith Seitz <keiths@redhat.com> - 2007g-2
- Add support for building java's zoneinfo files in new
  tzdata-java RPM.

* Wed Aug 22 2007 Petr Machata <pmachata@redhat.com> - 2007g-1
- Fix licensing tag.
- Upstream 2007g
  - Egypt switches the September 7, not September 28
  - Daviess, Dubous, Knox, Martin, and Pike Counties, Indiana, switch
    from central to eastern time in November
  - South Australia, Tasmania, Victoria, New South Wales and Lord Howe
    Island are changing their DST rules effective next year
  - Sync several Antarctic station's rules with the New Zealand
  - leapseconds contain changes from the most recent IERS bulletin

* Wed May  9 2007 Petr Machata <pmachata@redhat.com> - 2007f-1
- Upstream 2007f
  - New Zealand is extending DST, starting later this year.
  - Haiti no longer observes DST.
  - The Turks and Caicos switch at 02:00, not at 00:00, and have
    adopted US DST rules.

* Tue Apr  3 2007 Petr Machata <pmachata@redhat.com> - 2007e-1
- Upstream 2007e
  - Syria switched to summer time at Mar/29.
  - Honduras will not enter DST this year.

* Wed Mar 21 2007 Petr Machata <pmachata@redhat.com> - 2007d-1
- Upstream 2007d
  - Mongolia has abolished DST.
  - Turkey will use EU rules this year, changing at 01:00 UTC rather
    than 01:00 standard time.
  - Cuba observed DST starting Sunday.
  - Resolute, Nunavut switched from Central to Eastern time last
    November.

* Mon Feb 26 2007 Petr Machata <pmachata@redhat.com> - 2007c-1
- Upstream 2007c
  - Pulaski County, Indiana, switched back to eastern time.
  - Turkey switches at 01:00 standard time, not at 01:00 UTC.
- Upstream 2007b
  - Changes to the commentary in "leapseconds".

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 2007a-2
- tidy up the specfile per rpmlint comments

* Thu Jan 18 2007 Petr Machata <pmachata@redhat.com> - 2007a-1
- Upstream 2007a
  - Updates to Bahamas, they will be in sync with 2007 US DST change
  - New zone Australia/Eucla
  - Africa/Asmera renamed to Africa/Asmara, link created
  - Atlantic/Faeroe renamed to Atlantic/Faroe, link created
- Packaging
  - Adding BuildRequires: glibc-common >= 2.5.90-7 to build tzdata
    with extended 64-bit format necessary for dates beyond 2037

* Wed Nov 29 2006 Petr Machata <pmachata@redhat.com> - 2006p-1
- Upstream 2006p
  - Official version of Western Australia DST trial changes
  - Latitude/longitude changes for Europe/Jersey and Europe/Podgorica

* Wed Nov 22 2006 Petr Machata <pmachata@redhat.com> - 2006o-2
- Patch for Western Australia DST trial

* Thu Nov  9 2006 Petr Machata <pmachata@redhat.com> - 2006o-1
- Cuba has ended its three years of permanent DST.
- Updates in historical timestamps for Chile.

* Tue Oct 10 2006 Petr Machata <pmachata@redhat.com> - 2006m-2
- Proposed upstream patch (#210058)
  - Jordan will switch to winter time on October 27, not September 29
  - Brazil's DST this year is the first Sunday in November to the last
    Sunday in February.  (Thanks to Frederico A. C. Neves.)
  - ISO 3166 codes for Serbia and Montenegro, zone Europe/Podgorica
  - Commentary and past timestamps changes

* Tue Oct  3 2006 Petr Machata <pmachata@redhat.com> - 2006m-1
- Upstream 2006m:
  - Adjustments for Egypt, Palestine, Uruguay
  - Better description of `until' field in zic (8) manpage

* Thu Sep 21 2006 Petr Machata <pmachata@redhat.com> - 2006l-1
- Upstream 2006k, 2006l:
  - Adjustments for Egypt, Palestine, Cuba, Honduras
  - Documentation changes

* Tue Aug 22 2006 Petr Machata <pmachata@redhat.com> - 2006j-1
- Upstream 2006j
  - Honduras stopped observing DST on Monday at 00:00
  - America/Bermuda will follow the US's lead next year
  - America/Moncton will use US-style rules next year
  - New Zone America/Blanc-Sablon, for Canadians who observe AST all
    year
  - New zone: America/Atikokan instead of America/Coral_Harbour
  - New zones: Europe/Jersey, Europe/Guernsey, Europe/Isle_of_Man
  - Historical changes
  - Commentary updates
- Upstream 2006i
  - localtime.c fixes
- Upstream 2006h
  - zic leapsecond fix

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2006g-1.1
- rebuild

* Thu May 11 2006 Petr Machata <pmachata@redhat.com> - 2006g-1
- Honduras chose to follow Guatemala and will observe DST May/6 to Sep/2
- Nicaragua updates

* Tue May  2 2006 Petr Machata <pmachata@redhat.com> - 2006f-1
- Upstream 2006f
  - America/Guatemala observes DST between Apr/30 and Oct/1
  - Historical changes for Nicaragua
  - Update of America/Indiana/Vincennes in zone table

* Thu Apr 20 2006 Petr Machata <pmachata@redhat.com> - 2006d-1
- Upstream 2006d
  - Haiti observes DST
  - Sri Lanka change actually took effect Apr/15
  - All Canada is now scheduled for 2007 US DST rules
  - Some historical fixes

* Thu Apr  6 2006 Petr Machata <pmachata@redhat.com> - 2006c-1
- Upstream 2006c
  - Time-related changes:
    - dozens of historical and commentary changes
    - Iran stopped observing DST
    - Sri Lanka switches from UTC+6 to UTC+5:30
    - America/Thule and America/Edmonton will adopt new US rules,
      starting 2007
    - Tunisia is adopting regular DST
  - Code:
    - asctime.c: Chages in format strings to silent gcc warnings
    - removing K&R notation from function signatures
    - few fixes across the code

* Thu Mar 16 2006 Petr Machata <pmachata@redhat.com> - 2006b-2
- Patch for Sri Lanka time zone change (#184514)

* Wed Feb 22 2006 Petr Machata <pmachata@redhat.com> 2006b-1
- Upstream 2006b:
  - using tz64code version, as 32 is legacy according to tzdata ML
  - new manual pages for ctime, strftime, tzset
  - some source code reorganizations
  - no timezone/dst rule updates

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 2006a-2
- Small changes in tst-timezone.c

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 2006a-1
- Upstream 2006a:
  - private.h(scheck): changing char* to char const*
  - Rule changes for Palestine, zone changes for Indiana/US, both
    changes for Canada.
  - Many related doc changes.
- Naming scheme in spec file doesn't use %%{name}, but tzdata.

* Thu Jan 12 2006 Petr Machata <pmachata@redhat.com> 2005r-3
- 2005r-3
  - Meta changes.  Renaming tzdata.tar.bz2 file to tzdata$ver-base,
    so that it won't clash across updates.

* Thu Jan  5 2006 Petr Machata <pmachata@redhat.com> 2005r-2
- 2005r
  - Zones EST, MST, HST, EST5EDT, CST6CDT, MST7MDT, PST8PDT moved to
    northamerica to guard against old files with obsolete information
    being left in the time zone binary directory.
  - Changes for countries that are supposed to join 2007 US DST
    change.  This includes most of Canada, however entries already in
    the database (Alberta, British Columbia, Newfoundland, Northwest
    Territories, and Yukon) were left alone for the time being.
  - Fixes in zdump.c (abbrok): conditions are chained, and the string
    is checked for emptiness.

* Sat Dec 17 2005 Jakub Jelinek <jakub@redhat.com> 2005q-2
- 2005q
  - changes for Georgia, Azerbaijan, Jordan, Palestine, Cuba, Nicaragua
  - SystemV timezone changes

* Wed Nov  2 2005 Jakub Jelinek <jakub@redhat.com> 2005n-2
- 2005n
  - changes for Kyrgyzstan and Uruguay
- fix a typo in the Makefile (used TZDATA env var instead of TZDIR during
  make check), update tst-timezone.c from glibc CVS (#172102)

* Tue Sep  6 2005 Jakub Jelinek <jakub@redhat.com> 2005m-2
- 2005m
  - changes for USA (extending DST by 4 weeks since 2007), Tunisia,
    Australia, Kazakhstan
  - historical timezone data changes for Japan, Poland, Northern Ireland and
    Mali
  - timezone name change for East Timor

* Fri Jul 15 2005 Jakub Jelinek <jakub@redhat.com> 2005k-2
- 2005k
  - leap seconds update

* Sat Apr 30 2005 Jakub Jelinek <jakub@redhat.com> 2005i-2
- 2005i
  - updates for Iran, Haiti and Nicaragua

* Mon Apr  4 2005 Jakub Jelinek <jakub@redhat.com> 2005h-2
- 2005h
  - fixes for Kazakhstan

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 2005g-2
- 2005g
  - fixes for Uruguay
- include README and Theory from tzcode tarball in %%{_docdir};
  Theory includes a good summary of how the timezone data files
  are supposed to be named

* Tue Mar  1 2005 Jakub Jelinek <jakub@redhat.com> 2005f-2
- 2005f
  - more updates for Israel, updates for Azerbaijan

* Wed Jan 26 2005 Jakub Jelinek <jakub@redhat.com> 2005c-3
- 2005c
  - updates for Israel and Paraguay

* Mon Nov 29 2004 Jakub Jelinek <jakub@redhat.com> 2004g-1
- 2004g (#141107)
  - updates for Cuba

* Mon Oct 11 2004 Jakub Jelinek <jakub@redhat.com> 2004e-2
- 2004e (#135194)
  - updates for Brazil, Uruguay and Argentina

* Wed Aug  4 2004 Jakub Jelinek <jakub@redhat.com> 2004b-2
- 2004b

* Mon Oct  6 2003 Jakub Jelinek <jakub@redhat.com> 2003d-1
- 2003d

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2003c-1
- 2003c
- updates for Brazil (#104840)

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2003a-2
- rebuilt

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2003a-1
- initial package
