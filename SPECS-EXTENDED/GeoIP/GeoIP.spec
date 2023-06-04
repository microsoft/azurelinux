Vendor:         Microsoft Corporation
Distribution:   Mariner
# Tests require network access so fail in koji; build using --with tests to run them yourself
%bcond_with tests

Name:		GeoIP
Version:	1.6.12
Release:	8%{?dist}
Summary:	Library for country/city/organization to IP address or hostname mapping
License:	LGPLv2+
URL:		http://www.maxmind.com/app/c
Source0:	https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/GeoIP-%{version}.tar.gz
BuildRequires:	coreutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	sed
BuildRequires:	zlib-devel


# Old name of GeoIP library package
Obsoletes:	geoip < %{version}-%{release}
Provides:	geoip = %{version}-%{release}

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from.

It uses file based databases that can optionally be updated on a weekly basis
by installing the geoipupdate-cron (IPv4) and/or geoipupdate-cron6 (IPv6)
packages.

%package devel
Summary:	Development headers and libraries for GeoIP
Requires:	%{name} = %{version}-%{release}
Provides:	geoip-devel = %{version}-%{release}
Obsoletes:	geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications.

%prep
%setup -q

%build
%configure --disable-static --disable-dependency-tracking

# Kill bogus rpaths
sed -i -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}%{_libdir}/*.la

%check
# Tests require network access so fail in koji; build using --with tests to run them yourself
%{?with_tests:LD_LIBRARY_PATH=%{buildroot}%{_libdir} make check}

%ldconfig_scriptlets

%files
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc AUTHORS ChangeLog NEWS.md README.md
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1
%{_libdir}/libGeoIP.so.1.*
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*

%files devel
%{_includedir}/GeoIP.h
%{_includedir}/GeoIPCity.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc

%changelog
* Wed May 17 2023 Andy Zaugg <azaugg@linkedin.com> - 1.6.12-8
- Dropping GeoIP-data package requirement

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.12-7
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- License verified

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.12-2
- Switch to %%ldconfig_scriptlets

* Thu Jan 18 2018 Paul Howarth <paul@city-fan.org> - 1.6.12-1
- Update to 1.6.12
  - Populate metro and area code when performing lookups in IPv6 City
    databases; previously this was only done when using IPv4 City
    databases

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Paul Howarth <paul@city-fan.org> - 1.6.11-1
- Update to 1.6.11
  - Fix use of a NULL pointer when opening a corrupt database with 'GeoIP_open'
    (GH#87)
- Drop EL-5 support
  - Drop redundant BuildRoot: and Group: tags
  - Drop EL5-only dependency on GeoIP-GeoLite-data
  - Drop explicit pkgconfig dependency in devel package
  - Drop buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Mar 30 2017 Paul Howarth <paul@city-fan.org> - 1.6.10-1
- Update to 1.6.10
  - GeoIP_database_info now returns the full version string rather than
    incorrectly truncating it (GH#79)
  - This API is now distributed with a small test copy of GeoIP.dat rather than
    a full copy
  - Fix issue where Visual Studio 2015 was optimizing out initialization code
    (GH#81)
  - Fix test/benchmark on Windows (GH#75)

* Sun Feb 26 2017 Paul Howarth <paul@city-fan.org> - 1.6.9-4
- Fix GeoIP_database_info truncation issue (#1426853, GH#79, GH#80)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Paul Howarth <paul@city-fan.org> - 1.6.9-1
- Update to 1.6.9
  - Allow compilation on older systems by relaxing the autoconf and automake
    minimum versions
  - Avoid potential problems in multi-threaded environments by consistently
    using pread() rather than read()
  - Fix various small issues reported by clang's static analyser
  - Fix a regression introduced in version 1.6.8, which caused
    GeoIP_database_info to erroneously return NULL

* Sun Nov  1 2015 Paul Howarth <paul@city-fan.org> - 1.6.7-1
- Update to 1.6.7
  - Fixed a MSVC parser stack overflow when parsing 'regionName.c' and
    'timeZone.c' (GH#54)
  - Updated region codes and timezones
  - When using 'GEOIP_MEMORY_CACHE' with an invalid database file, the search
    tree traversal could attempt to read memory outside of the memory allocated
    for the memory cache, resulting in a segmentation fault; a check was added
    to ensure that the traversal code does not try to read beyond the end of
    the file, whether in memory, memory mapped, or on disk
  - Previously the return values from file reads were ignored; we now check
    these values to ensure that there were no errors

* Thu Jul 30 2015 Paul Howarth <paul@city-fan.org> - 1.6.6-1
- Update to 1.6.6
  - Replaced usage of deprecated fileno, read, and lseek on Visual Studio 2005+
    with their ISO C++ conformant replacements (GH#55)
  - A warning about using a double as a float was fixed (GH#56)
  - Fixed segfault when doing a lookup on an empty database (GH#62)
  - Fixed a memcheck error from valgrind in the '_check_mtime' function (GH#60)
  - Fixed '_check_mtime' to check the return value of 'gettimeofday' rather
    than just assuming it worked

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Paul Howarth <paul@city-fan.org> - 1.6.5-2
- Work around problems with old GeoIP-data package in CentOS 5 Extras
  repo (http://bugs.centos.org/view.php?id=8488) by requiring
  GeoIP-GeoLite-data rather than the virtual GeoIP-data for EL-5 builds only

* Mon Mar  2 2015 Paul Howarth <paul@city-fan.org> - 1.6.5-1
- Update to 1.6.5
  - Fixed a segmentation fault in geoiplookup when the utility was passed an
    invalid database (#1180874)
  - Additional validation was added for the size used in the creation of the
    index cache (#832913)
  - Changed the code to only look up country codes by using functions that
    ensure that we do not try to look past the end of an array (GitHub #53)

* Fri Feb 20 2015 Paul Howarth <paul@city-fan.org> - 1.6.4-4
- Databases now unbundled to the GeoIP-GeoLite-data package
- Drop long-unused perl helper scripts
- Add explicit pkgconfig dependency for EL-5 build
- Drop timestamp hack for configure, no longer needed

* Tue Feb 10 2015 Paul Howarth <paul@city-fan.org> - 1.6.4-3
- Sub-package the data; going forward, this would be better as a separate
  package, since it has separate upstream releases than the library

* Fri Feb  6 2015 Paul Howarth <paul@city-fan.org> - 1.6.4-2
- Only require geoipupdate prior to F-22, for back-compatibility
- Use %%license where possible
- GeoIP-devel provides geoip-devel as well as obsoleting it
- Update bundled databases

* Thu Jan 29 2015 Philip Prindeville <philipp@fedoraproject.org> - 1.6.4-1
- Require geoipupdate per Paul

* Tue Jan 20 2015 Philip Prindeville <philipp@fedoraproject.org> - 1.6.4-0
- Version bump to 1.6.4 per bz #1158667 (okay, that bug was for 1.6.3)
- Remove geoipupdate as it will be moving into its own package

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Paul Howarth <paul@city-fan.org> - 1.5.1-4
- Add %%check, so we can run tests by building using --with tests
- Update databases from upstream

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Paul Howarth <paul@city-fan.org> - 1.5.1-2
- Properly provide all of the GeoLite databases and their IPv6 equivalents, as
  per the geoip-geolite package that we're obsoleting/providing
- Provide compatibility symlinks for database files that historically had
  different names in GeoIP and geoip-geolite
- Don't distribute unbundled LICENSE files, as per packaging guidelines
- Update license tag to reflect distribution of CC-BY-SA database content
- No longer try to update the databases in %%post
- Maintain timestamps where possible
- Set up GeoIP.dat symlink in package and don't touch it again
- Add update6 package to update the IPv6 databases; have to use wget for this
  rather than geoipupdate as the databases are still in beta

* Wed Jun 12 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.1-1
- Bump to version 1.5.1
- Fix exit codes for various situations (MaxMind support #129155)
- Use versioned obsoletes/provides for geoip-geolite
- Update UTF8 patch
- Change symlink from GeoIP-initial.dat to GeoLiteCountry.dat if we had a
  successful download and now have the latter file.

* Mon Jun 10 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-7
- Annotate conflict with geoip-geolite package (#968074)

* Mon Jun 10 2013 Paul Howarth <paul@city-fan.org> - 1.5.0-6
- Update sub-package requires main package for geoipupdate script

* Sat Jun  8 2013 Paul Howarth <paul@city-fan.org> - 1.5.0-5
- Make GeoIP.dat -> GeoIP-initial.dat symlink in %%install, not %%post,
  and don't %%ghost it
- Run geoipupdate silently in %%post and cron job
- Create empty database files for %%ghost to work with old rpm versions
- Don't try to use noarch subpackages on old rpm versions
- Update %%description to mention database updates
- Drop outdated README.Fedora

* Sat Jun 08 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-4
- Revert ability to replace 3rd-party package

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-3
- Add attributes for %%ghost files

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-2
- Make update subpackage be noarch.

* Fri Jun 07 2013 Philip Prindeville <philipp@fedoraproject.org> - 1.5.0-1
- Version bump to 1.5.0
- Have GeoIP.dat be a symlink to the real data, and install the canned
  GeoIP.dat as GeoIP-initial.dat
- Change config as per Boris' instructions to use 'lite' databases which are
  regularly updated.
- Add pkgconfig (.pc) file into devel subpackage
- Add cron support for refreshing the lite databases and make a separate
  subpackage.

* Sun Mar 24 2013 Paul Howarth <paul@city-fan.org> - 1.4.8-6
- Fix config.guess and config.sub to add aarch64 support (#925403)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Paul Howarth <paul@city-fan.org> - 1.4.8-4
- libGeoIPUpdate and geoipupdate (which is linked against it) are GPL-licensed
  rather than LGPL-licensed (#840896)
- Don't package generic INSTALL file (#661625)
- Kill bogus rpaths on x86_64
- Hardcode library sonames in %%files list to avoid nasty surprises in the
  future
- Drop %%defattr, redundant since rpm 4.4
- Recode docs as UTF-8
- Don't use macros for commands
- Use tabs

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 6 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.4.8-1.1
- Remove -ipv6 patch
- Bump to 1.4.8 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-0.2.20090931cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 31 2009 Matt Domsch <mdomsch@fedoraproject.org> - 1.4.7.0.1.20090931
- apply CVS HEAD 20090931 which includes IPv6 functions

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 08 2009 Michael Fleming <mfleming+rpm@enlartenment.com> - 1.4.6-1
- Add geoiplookup6 man page
- Update to 1.4.6

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.5-2
- Update to 1.4.5
- Fix database URL locations in Perl helper scripts

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-2
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.4-1
- New upstream release.

* Wed Sep 5 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.3-1
- New upstream release.
- Fix GeoIPCity fetcher script
- Update License tag

* Mon Feb 12 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.2-1
- New upstream release.

* Mon Jan 8 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.1-2
- License is actually LGPL now.

* Sun Jan 7 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.1-1
- New upstream release
- Add fetch-geoipdata* scripts to pull free databases automatically if
  desired (bz #198137)
- README.fedora added to briefly explain above.

* Mon Nov 27 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.0-4
- Fix %%install scripts to satisfy newer mock builds

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.4.0-3
- Upstream upgrade
- Added LICENSE.txt file to %%doc, covering GeoIP country/city data license
  (bz #198137)

* Mon May 15 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.17-1
- New upstream release (minor fixes)

* Mon May 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.16-1
- New upstream release
- Add INSTALL document to package.

* Sat Feb 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-3
- Fix Obsoletes/Provides for old "geoip"-convention packages
- Move .so symlinks to -devel where they should be

* Fri Feb 10 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-2
- Remamed to match upstream tarball name
- Removed static libraries
- Added symlinks to packages
- Mark config file noreplace

* Sun Feb 5 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.3.14-1
- Initial review package for Extras
