# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           zchunk
Version:        1.5.1
Release:        3%{?dist}
Summary:        Compressed file format that allows easy deltas
License:        BSD-2-Clause AND MIT
URL:            https://github.com/zchunk/zchunk
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  meson
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Provides:       bundled(buzhash-urlblock) = 0.1

%description
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

%package libs
Summary: Zchunk library

%description libs
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the zchunk library, libzck.

%package devel
Summary: Headers for building against zchunk
Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description devel
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the headers necessary for building against the zchunk
library, libzck.

%prep
%autosetup
# Remove bundled sha libraries
rm -rf src/lib/hash/sha*

%build
%meson -Dwith-openssl=enabled -Dwith-zstd=enabled
%meson_build

%install
%meson_install
mkdir -p %{buildroot}%{_libexecdir}
install contrib/gen_xml_dictionary %{buildroot}%{_libexecdir}/zck_gen_xml_dictionary

%check
%meson_test

%ldconfig_scriptlets libs

%files
%doc README.md contrib
%{_bindir}/zck*
%{_bindir}/unzck
%{_libexecdir}/zck_gen_xml_dictionary
%{_mandir}/man1/*.gz

%files libs
%license LICENSE
%doc README.md
%{_libdir}/libzck.so.*

%files devel
%doc zchunk_format.txt
%{_libdir}/libzck.so
%{_libdir}/pkgconfig/zck.pc
%{_includedir}/zck.h

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Jonathan Dieter <jonathan@dieter.ie> - 1.5.1-1
- Fix memory leak
- Ensure version is set properly inside zchunk

* Wed Jul 17 2024 Jonathan Dieter <jonathan@dieter.ie> - 1.5.0-1
- Fix bug when managing different contexts in different threads

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Jonathan Dieter <jdieter@gmail.com> - 1.4.0-1
- Add native OpenSSL 3 compatibility
- Add new function for getting zchunk context from chunk
- Fix bug when assembling from multiple sources

* Thu Oct  5 2023 Jonathan Dieter <jdieter@gmail.com> - 1.3.2-1
- Fix a couple of unsigned integer overflow bugs

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr  4 2023 Jonathan Dieter <jdieter@gmail.com> - 1.3.1-1
- Fix a few low severity security bugs including
  - An off-by-one overflow when reading compressed integers from a
    malicious zchunk file
  - Error handling being skipped when the number of bytes read doesn't
    match what's expected
  - Not freeing memory when attempting to reallocate to size 0

* Sat Feb 25 2023 Jonathan Dieter <jdieter@gmail.com> - 1.3.0-1
- Add option to generate a zchunk header from an uncompressed file without
  actually creating a zchunk file

* Sat Feb 18 2023 Jonathan Dieter <jdieter@gmail.com> - 1.2.4-1
- Fix test compatibility with zstd-1.5.4

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 16 2022 Jonathan Dieter <jdieter@gmail.com> - 1.2.3-1
- Fixed some small formatting issues

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 18 2022 Jonathan Dieter <jdieter@gmail.com> - 1.2.2-1
- Fixed a number of small issues highlighted by Coverity

* Sat Mar 12 2022 Jonathan Dieter <jdieter@gmail.com> - 1.2.1-1
- Fixed bug that limited size of file that could be compressed using zchunk to 2GB
- Fixed memory leak

* Sun Feb 20 2022 Jonathan Dieter <jdieter@gmail.com> - 1.2.0-1
- Add `--uncompressed` option to zck, allowing for embedding of uncompressed
  digests in the header
- Various small bug fixes

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.1.15-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Jonathan Dieter <jdieter@gmail.com> - 1.1.15-1
- Fix major bug when creating a zchunk file that contains a dictionary

* Thu May 20 2021 Jonathan Dieter <jdieter@gmail.com> - 1.1.14-1
- Fix tests on all arches when built against zstd-1.5.0

* Sat May  1 2021 Jonathan Dieter <jdieter@gmail.com> - 1.1.11-1
- Fix multipart download failures on rare web servers

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Jonathan Dieter <jdieter@gmail.com> - 1.1.9-1
- Fixes for test failures with zstd-1.4.7+
- Add man pages

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Jonathan Dieter <jdieter@gmail.com> - 1.1.5-1
- Fix small bug in corner case when handling write failures

* Wed Nov 13 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.4-1
- Fix download failure when web server doesn't include content-type with each
  range

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 19 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.2-2
- Fix multipart range handling to work with quotes, fixes #1706627
- Fix file creation permissions so they respect umask
- Actually push new sources

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.1.1-3
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.1-2
- Fix compilation on GCC 4.4.7 so it builds on EL6
- Add missing sources
- Also, zchunk will now automatically do all your taxes

* Sat Mar 23 2019 Jonathan Dieter <jdieter@gmail.com> - 1.1.0-1
- Optimize chunk matching while downloading, significantly reducing CPU usage

* Sat Mar 16 2019 Jonathan Dieter <jdieter@gmail.com> - 1.0.4-1
- Fix multipart boundary bug when dealing with lighttpd servers

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jonathan Dieter <jdieter@gmail.com> - 1.0.3-1
- Fix several memory leaks and use-after-frees

* Fri Dec 28 2018 Jonathan Dieter <jdieter@gmail.com> - 1.0.2-1
- Use hash table for finding identical chunks, speeding up process considerably
- Add test case to verify that identical chunk checking is working

* Sat Dec 22 2018 Jonathan Dieter <jdieter@gmail.com> - 1.0.0-1
- 1.0 release.  API/ABI stability is now guaranteed

* Sun Dec 09 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.17-1
- Turn off some tests for big-endian architectures since zstd isn't
  deterministic on them

* Sat Dec 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.16-1
- Add zck_gen_zdict binary to generate optimal zdict for a zchunk file
- Add functions to API to simplify extracting a single chunk
- Change default zstd compression to 9 for a 6x speed increase in compression
  speed for a 5% increase in compression size

* Tue Nov 13 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.15-1
- Switch from optional flags to more robust optional elements

* Thu Nov 01 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.14-1
- Sanity check hex hashes passed in as an option

* Mon Oct 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.13-1
- Add read support for zchunk files with optional flags
- Fix tests for zstd-1.3.6

* Fri Sep 28 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.11-1
- Fix small bug where creating a zck_dl context fails when zck context is NULL

* Tue Sep 18 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.10-1
- Update to 0.9.10
- Fixes security bugs found by Coverity

* Fri Aug 10 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.7-2
- Add contrib scripts to docs
- Fix test failures for zstd <= 1.3.4
- Add gen_xml_dictionary to libexecdir with zck_ prefix

* Wed Aug 01 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.5-1
- Update to 0.9.4
- Fix failing tests on ppc64, ppc64le, arm7, and s390x
- Fix intermittent parallel test failures

* Tue Jul 31 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.3-1
- Update to 0.9.3
- Fix intermittent bug where auto-chunking wasn't deterministic

* Mon Jul 30 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.2-1
- Update to 0.9.2
- Set minimum and maximum chunk sizes for both automatic and
  manual chunking
- New tests
- ABI (but not API change) - Use bool from stdbool.h
- Allow specification of output file in zck

* Wed Jul 25 2018 Jonathan Dieter <jdieter@gmail.com> - 0.9.1-1
- Update to 0.9.1
- New error handling functions
- File format changes
- API changes
- Proposed permanent stable ABI
- Fix Rawhide build error

* Thu Jul 12 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.6-1
- Update to 0.7.6
- SHA-512 and SHA-512/128 support
- New default chunk checksum type SHA-512/128
- Automatic chunking moved into libzck and is now default
- New option to disable automatic chunking
- Bugfixes

* Wed Jul 04 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.5-4
- Fix ldconfig scriptlets to run on libs package
- Rename zchunk-libs-devel to zchunk-devel
- Add BR: gcc
- Explicitly enable zstd and openssl support
- Simplify file globs

* Tue Jul 03 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.5-1
- Split libs into separate package
- Fix license
- Provide bundled buzhash
- Fix punctuation
- Simplify source0 using url macro
- Remove bundled sha library and add dependency on OpenSSL

* Mon Jul 02 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.4-2
- Add zchunk format definition to -devel documentation

* Fri Jun 22 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.4-1
- Add --stdout argument to unzck
- Use meson native versioning rather than manual header and fix
  pkgconfig output

* Tue Jun 12 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.2-1
- Rename zck_get_dl_range to zck_get_missing_range because it
  was too similar to the unrelated zck_dl_get_range function

* Mon Jun 11 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.1-1
- New functions in the library

* Fri Jun 08 2018 Jonathan Dieter <jdieter@gmail.com> - 0.7.0-1
- Massive API rework in preparation for ABI stability guarantee

* Wed Jun 06 2018 Jonathan Dieter <jdieter@gmail.com> - 0.6.2-1
- Header and API cleanup
- Fix warnings

* Tue Jun 05 2018 Jonathan Dieter <jdieter@gmail.com> - 0.6.0-1
- Massive rework of zckdl utility
- Main library no longer depends on curl, only zckdl utility
- Rework API
- Support for servers that have different maximum ranges in a request

* Thu May 10 2018 Jonathan Dieter <jdieter@gmail.com> - 0.5.2-1
- Add new zck_get_range() function
- Add tests
- Range functions are no longer prefixed with "Range: bytes="

* Wed May 09 2018 Jonathan Dieter <jdieter@gmail.com> - 0.5.0-1
- Command line utilities now provide help and usage examples and take
  proper flags
- Reading a zchunk header no longer automatically reads the dictionary

* Sun Apr 29 2018 Jonathan Dieter <jdieter@gmail.com> - 0.4.0-1
- Next release with incompatible file format changes
- File format has been reworked to allow checking of the header checksum
  without reading full header into memory at once
- Terminology changes for the header

* Fri Apr 20 2018 Jonathan Dieter <jdieter@gmail.com> - 0.3.0-1
- Next release with incompatible file format changes
- File format now supports streams and signatures

* Tue Apr 17 2018 Jonathan Dieter <jdieter@gmail.com> - 0.2.2-1
- First release
- Fix build on EL7
