## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           rpminspect
Version:        2.1
Release:        %autorelease
Summary:        Build deviation analysis and compliance tool

# librpminspect is licensed under the LGPL-3.0-or-later, and:
# * 5 source files in the library are from an Apache-2.0 licensed
#   project
# * Some code in inspect_unicode.c was taken from a blog post about
#   using icu4c and Unicode, it is under the MIT license.
#
# The rpminspect(1) command line tool is licensed under the
# GPL-3.0-or-later.
#
# The rpminspect-data-generic package is licensed under the
# CC-BY-4.0 license.
#
# Not packaged, but in the source:
# * include/uthash.h is BSD-1-Clause
# * include/compat/queue.h is BSD-3-Clause
# * libxdiff/ is LGPL-2.1-or-later
# * libtoml/ is BSD-3-Clause
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND LGPL-2.1-or-later AND Apache-2.0 AND MIT AND BSD-1-Clause AND BSD-2-Clause AND BSD-3-Clause AND CC-BY-4.0
URL:            https://github.com/rpminspect/rpminspect
Source0:        https://github.com/rpminspect/rpminspect/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/rpminspect/rpminspect/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2:        gpgkey-62977BB9C841B965.gpg
Requires:       librpminspect%{?_isa} = %{version}-%{release}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  json-c-devel
BuildRequires:  xmlrpc-c-devel >= 1.32.5
BuildRequires:  libxml2-devel
BuildRequires:  rpm-devel
BuildRequires:  libarchive-devel
BuildRequires:  elfutils-devel
BuildRequires:  kmod-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
BuildRequires:  libyaml-devel
BuildRequires:  file-devel
BuildRequires:  openssl-devel
BuildRequires:  libcap-devel
BuildRequires:  gettext-devel
BuildRequires:  clamav-devel
BuildRequires:  libmandoc-devel >= 1.14.5
BuildRequires:  gnupg2
BuildRequires:  libicu-devel
BuildRequires:  libcdson-devel
%if 1
BuildRequires:  libtoml-devel
%endif


%description
Build deviation and compliance tool.  This program runs a number of tests
against one or two builds of source RPM files.  The built artifacts are
inspected and compared to report changes and validate policy compliance
against the defined parameters.


%package -n librpminspect
Summary:        Library providing RPM test API and functionality

Requires:       desktop-file-utils
Requires:       gettext

%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     annobin-annocheck
%else
Requires:       annobin-annocheck
%endif

# The clamav data is required for the virus inspection.  Either
# install the clamav-data or download the data files directly.
%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     clamav-data
%else
Requires:       clamav-data
%endif

# If these are present, the xml inspection can try DTD validation.
%if 0%{?rhel} >= 8 || 0%{?fedora}
Recommends:     xhtml1-dtds
Recommends:     html401-dtds
%endif

# Necessary to support preprocessing spec files for parsing.  The
# package providing this dependency in turn pulls in other packages
# that define macros.  This is similar to the rpm-build package
# carrying a Requires on the same package.  It ensures the build
# environment has all of the necessary macro definitions that the
# package spec file may use.
%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     system-rpm-config
%else
Requires:       system-rpm-config
%endif

# These programs are only required for the 'shellsyntax' functionality.
# You can use rpminspect without these installed, just disable the
# shellsyntax inspection.
%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     dash
Recommends:     ksh
Recommends:     zsh
Recommends:     tcsh
Recommends:     rc
Recommends:     bash
%else
Requires:       dash
Requires:       ksh
Requires:       zsh
Requires:       tcsh
Requires:       rc
Requires:       bash
%endif

# The abidiff and kmidiff inspections require a external executable by
# the same name, as provided by libabigail.  If it is not present on
# the system, you can disable the relevant inspections.
%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     libabigail >= 2.3
%else
Requires:       libabigail >= 2.3
%endif

# The udevrules inspection requires an external executable (udevadm verify)
# provided by systemd-udev.  If the installed udevadm executable does not
# provide 'verify' command, the udevrules inspection is skipped.
%if 0%{?rhel} >= 8 || 0%{?epel} >= 8 || 0%{?fedora}
Recommends:     systemd-udev
%else
Requires:       systemd-udev
%endif

%description -n librpminspect
The library providing the backend test functionality and API for the
rpminspect frontend program.  This library can also be used by other
programs wanting to incorporate RPM test functionality.


%package -n librpminspect-devel
Summary:        Header files and development libraries for librpminspect

Requires:       librpminspect%{?_isa} = %{version}-%{release}

%description -n librpminspect-devel
The header files and development library links required to build software
using librpminspect.


%package -n rpminspect-data-generic
Summary:        Template data files used to drive rpminspect tests


%description -n rpminspect-data-generic
The rpminspect-data-generic package is meant as a template to build your
product's own data file.  The files in it contain product-specific
information.  The files in this package explain how to construct the
control files.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup


%build
%meson -D tests=false -D with_system_libtoml=true
%meson_build


%install
# Install bundled library docs and licenses
install -D -m 0644 libxdiff/AUTHORS %{buildroot}%{_pkgdocdir}/libxdiff/AUTHORS
install -D -m 0644 libxdiff/README %{buildroot}%{_pkgdocdir}/libxdiff/README
install -D -m 0644 libxdiff/COPYING %{buildroot}%{_defaultlicensedir}/%{name}/libxdiff/COPYING

install -D -m 0644 libtoml/README.md %{buildroot}%{_pkgdocdir}/libtoml/README.md
install -D -m 0644 libtoml/README.rpminspect %{buildroot}%{_pkgdocdir}/libtoml/README.rpminspect
install -D -m 0644 libtoml/LICENSE %{buildroot}%{_defaultlicensedir}/%{name}/libtoml/LICENSE


%meson_install
%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS.md CHANGES.md README.md TODO
%doc %{_pkgdocdir}/libxdiff/AUTHORS
%doc %{_pkgdocdir}/libxdiff/README
%doc %{_pkgdocdir}/libtoml/README.md
%doc %{_pkgdocdir}/libtoml/README.rpminspect
%license COPYING
%license %{_defaultlicensedir}/%{name}/libxdiff/COPYING
%license %{_defaultlicensedir}/%{name}/libtoml/LICENSE
%{_bindir}/rpminspect
%{_mandir}/man1/rpminspect.1*


%files -n librpminspect
%license COPYING.LIB LICENSE-2.0.txt MIT.txt
%{_libdir}/librpminspect.so.*


%files -n librpminspect-devel
%license COPYING.LIB
%{_includedir}/librpminspect
%{_libdir}/librpminspect.so


%files -n rpminspect-data-generic
%license CC-BY-4.0.txt
%{_datadir}/rpminspect


%changelog
* Thu Jan 29 2026 Dave Cantrell <dcantrell@redhat.com> - 2.1-
- Upgrade to rpminspect-2.1

* Thu Aug 14 2025 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.0-5
- Rebuilt for ICU 77.1

* Thu Apr 10 2025 David Cantrell <dcantrell@redhat.com> - 2.0-4
- Fixed the FTBFS erors on rawhide (SWMBZBUGSM-411)

* Mon Dec 09 2024 Pete Walter <pwalter@fedoraproject.org> - 2.0-3
- Rebuild for ICU 76

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 2.0-2
- Rebuild for clamav 1.4.1

* Thu Sep 05 2024 David Cantrell <dcantrell@redhat.com> - 2.0-1
- Upgrade to rpminspect-2.0

* Thu Feb 01 2024 Pete Walter <pwalter@fedoraproject.org> - 1.12.1-2
- Rebuild for ICU 74

* Thu Sep 14 2023 Stephen Gallagher <sgallagh@redhat.com> - 1.11-4
- Use rpm_macro(autorelease) for %%rpmautorelease dependency

* Thu Sep 14 2023 David Cantrell <dcantrell@redhat.com> - 1.11-3
- Use xmlSetGenericErrorFunc() rather than initGenericErrorDefaultFunc()

* Mon May 22 2023 Michal Domonkos <mdomonko@redhat.com> - 1.11-2
- Use RPMTAG_NOT_FOUND macro instead of -1 (for RPM 4.19)

* Fri Mar 03 2023 David Cantrell <dcantrell@redhat.com> - 1.11-1
- Upgrade to rpminspect-1.11

* Sun Jan 22 2023 Orion Poplawski <orion@nwra.com> - 1.10-4
- Rebuild for clamav 1.0.0

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.10-3
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 David Cantrell <dcantrell@redhat.com> - 1.10-1
- Upgrade to rpminspect-1.10

* Wed Mar 02 2022 David Cantrell <dcantrell@redhat.com> - 1.9-1
- Upgrade to rpminspect-1.9

* Wed Feb 09 2022 David Cantrell <dcantrell@redhat.com> - 1.8-4
- Rebuild (related #2046952)

* Tue Feb 08 2022 David Cantrell <dcantrell@redhat.com> - 1.8-3
- Fix invalid free() usage (#2046952)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 David Cantrell <dcantrell@redhat.com> - 1.8-1
- Upgrade to rpminspect-1.8

* Thu Nov 04 2021 David Cantrell <dcantrell@redhat.com> - 1.7-2
- Fix missing %%changelog entries in the package spec file

* Thu Nov 04 2021 David Cantrell <dcantrell@redhat.com> - 1.7-1
- Upgrade to rpminspect-1.7

* Thu Nov 04 2021 David Cantrell <dcantrell@redhat.com> - 1.6-3
- Upgrade to rpminspect-1.6

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.6-3
- Rebuilt with OpenSSL 3.0.0

* Thu Sep 02 2021 David Cantrell <dcantrell@redhat.com> - 1.6-2
- Use %%gpgverify in %%prep

* Thu Sep 02 2021 David Cantrell <dcantrell@redhat.com> - 1.6-1
- Upgrade to rpminspect-1.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org>
- Rebuild for versioned symbols in json-c

* Fri Apr 30 2021 David Cantrell <dcantrell@redhat.com> - 1.5-1
- Begin work on version 1.5
- Use llabs() instead of labs() in the filesize inspection
- Improve has invalid execstack flags reporting
- Use long unsigned int to report size changes in patches
- Fix some errors in the changedfiles inspection
- Update the changedfiles test cases
- Check DT_SONAME in is_elf_shared_library()
- Skip debuginfo and debugsource files in abidiff
- Make sure abidiff test cases add a DT_SONAME to the test lib
- Report INFO level for patches findings by default
- Python black fixes in test/test_abidiff.py
- Update the test/test_patches.py cases for patches changes
- Generate regular changelog in utils/srpm.h
- Skip branches without targets in submit-koji-builds.sh
- Fedora and CentOS systems in ci need diffstat
- opensuse-leap CI job requires diffstat
- Fix the Debian CI jobs in GitHub Actions
- Fix and enable the Ubuntu extra-ci job in GitHub Actions
- Use pip instead of pip3 for the Ubuntu command
- Use apt-get -y install in
- Enable the opensuse-tumbleweed GHA job again
- Make sure the Gentoo GHA job has diffstat
- Get the Arch Linux GHA job working again
- Use ubuntu:latest for the ubuntu GHA image
- Simplify the utils/determine-os.sh script
- Update license table in README.md
- Allow any number of builds specified for fetch only mode
- Handle old or broken versions of libmagic in changedfiles
- Update GitHub Action status badges in README.md
- Fix $(OS) check in the Makefile
- Fix the ubuntu GitHub Actions extra-ci job
- Make sure the centos8 job has git available before cloning
- Change strappend() to work as a variadic function
- Use json_tokener_parse_ex() to get better error reporting
- Fix reading of the javabytecode block in the config file
- Catch missing/losing -fPIC correctly on .a ELF objects (#352)
- Refactor elf_archive_tests() and its helper functions
- Followup fix for find_no_pic, find_pic, and find_all
- Install cpp-coveralls using pacman on Arch Linux
- Install cpp-coveralls using pip on Arch Linux
- Install cpp-coveralls in pre.sh on Arch Linux
- Install required Python modules in pre.sh on Arch Linux
- Do not upgrade pip on Arch Linux, go back to using pip.txt
- Drop DEBUG_PRINT from source generated by pic_bits.sh
- Do not run apt-get update as a second time on Debians systems
- The lost PIC tests need to invoke gcc with -fno-PIC
- Update the OpenSUSE Tumbleweed files, but disable it anyway
- Define inspection_ignores in struct rpminspect
- Clean up the config file section reading code
- Add add_ignore() to init.c
- Fix fetch only mode download directory
- Stub out libcurl download progress callback function
- Perform symbolic owner and group matching in ownership (#364)
- Restrict download_progress() to systems with CURLOPT_XFERINFOFUNCTION
- Read per-inspection ignore lists from the config file.
- Add commented out per-inspection ignore blocks
- Implement per-inspection path ignore support (#351)
- Report annocheck failures correctly in librpminspect.
- Note all regular expression settings use regex(7) syntax
- Allow size_threshold: info in the config file (#261)
- Check ignore list in files for path prefixes to ignore (#360)
- Support a list of expected empty RPMs in the config file (#355)
- Call mparse_reset() before mparse_readfd()
- Do not crash with the -c option specifies a non-existent file
- Update TODO list
- Make sure brp-compress is disabled in test_manpage.py
- Require/Recommend /usr/bin/annocheck
- Note size_threshold can be the keyword info
- Ensure ctxt->lastError.message is not NULL before strdup (#382)
- Handle corrupt compressed files in changedfiles (#382)
- Disable debugging output for the ignore lists in init.c
- Drop debugging output in the xml inspection
- Remove what working directories we can
- Correctly find icons for desktop files in subpackages (#367)
- Followup to the Icon= check in the desktop inspection (#367)
- BuildRequires libmandoc-devel >= 1.14.5
- Manually install mandoc on centos7 for now

* Thu Mar 25 2021 David Cantrell <dcantrell@redhat.com> - 1.4-2
- ExcludeArch %%{ix86} and %%{arm}

* Thu Mar 25 2021 David Cantrell <dcantrell@redhat.com> - 1.4-1
- Start work on the 1.4 release
- Trim git commit summary prefix from changelog lines
- Report the program version number in the results (#309)
- Handle compressed but otherwise empty man pages (#308)
- Flake8 fixes for test_manpage.py
- s/self.rpm/self.after_rpm/ in two test_manpage.py tests
- Disable broken ELF heurisitic and size limit in libclamav
- Modify dump_cfg() to write valid YAML to stdout (#306)
- Migrate more code off hsearch and to uthash
- Replace hsearch() with uthash in the kmod inspection
- Update TEST_METADATA status in TODO and MISSING
- Restrict style checks to specific directories
- Replace hsearch() with uthash in the abidiff inspection
- Change tsearch/twalk use to uthash
- Correct misuse of entry with hentry variables (#321)
- Normalize copyright boilerplates in source files
- Use hentry->key over hentry->value in pathmigration
- Adjust lib/meson.build for Fedora rawhide
- Drop gate.yml and begin non-x86_64 arches in ci.yml
- Add armv7, aarch64, and s390x to the other_arches job
- Change init.c error reporting over to err/warn functions
- Modify file triggers and matrix use in ci.yml
- Split 32-bit osdeps out to post.sh scripts in osdeps/
- Split style.yml in to shellcheck.yml and python.yml
- Rewrite extra-ci.yml to use the matrix strategy method for GHA
- Move the emulated CI jobs to extra-ci.yml
- s/pkg/pki/ for the centos jobs
- Debian and Ubuntu fixes for CI
- Python pip on Debian is called pip
- Try to fix just debian:stable
- Enable debian:testing in extra-ci.yml
- Enable centos8 in extra-ci.yml again
- Enable centos7 in extra-ci.yml again
- Enable opensuse-leap and gentoo in extra-ci.yml again
- Run each test script individually on emulated targets
- Try a different syntax for the emulated matrix jobs
- Install s390 glibc headers on s390x fedora systems
- Detect 32-bit and musl presence in test_elf.py
- Skip lost -fPIC tests if gcc lacks -m32 support
- Add stretch and buster to the emulated targets list
- Drop Debian buster from the emulated targets
- Install gcc-multilib only on Debian x86_64 and s390x systems
- libc-dev:i386 -> libc6-dev:i386
- Disable Debian targets in extra-ci temporarily
- s/AUR/git/g in osdeps/arch/post.sh
- In read_cfgfile(), keep track of block depth correctly (#329)
- A few more yaml parsing fixes for block vs group
- Recommend or Require libabigail >= 1.8.2
- Finish normalizing all the error reporting statements
- Advertise of rpminspect-report in the contrib README.
- Report libclamav version and CVD versions (#258)
- Ensure first argument of warn(3) is a format string.
- Enable werror=true and warning_level=3 in default_options
- Update the translation template file
- Get rid of invalid free() in get_product_release()
- Add inspection_id() to librpminspect
- Update the po/rpminspect.pot template
- Improve mkannounce.sh to handle stable and devel releases

* Thu Mar 25 2021 David Cantrell <dcantrell@redhat.com> - 1.4-1
- Start work on the 1.4 release
- Trim git commit summary prefix from changelog lines
- Report the program version number in the results (#309)
- Handle compressed but otherwise empty man pages (#308)
- Flake8 fixes for test_manpage.py
- s/self.rpm/self.after_rpm/ in two test_manpage.py tests
- Disable broken ELF heurisitic and size limit in libclamav
- Modify dump_cfg() to write valid YAML to stdout (#306)
- Migrate more code off hsearch and to uthash
- Replace hsearch() with uthash in the kmod inspection
- Update TEST_METADATA status in TODO and MISSING
- Restrict style checks to specific directories
- Replace hsearch() with uthash in the abidiff inspection
- Change tsearch/twalk use to uthash
- Correct misuse of entry with hentry variables (#321)
- Normalize copyright boilerplates in source files
- Use hentry->key over hentry->value in pathmigration
- Adjust lib/meson.build for Fedora rawhide
- Drop gate.yml and begin non-x86_64 arches in ci.yml
- Add armv7, aarch64, and s390x to the other_arches job
- Change init.c error reporting over to err/warn functions
- Modify file triggers and matrix use in ci.yml
- Split 32-bit osdeps out to post.sh scripts in osdeps/
- Split style.yml in to shellcheck.yml and python.yml
- Rewrite extra-ci.yml to use the matrix strategy method for GHA
- Move the emulated CI jobs to extra-ci.yml
- s/pkg/pki/ for the centos jobs
- Debian and Ubuntu fixes for CI
- Python pip on Debian is called pip
- Try to fix just debian:stable
- Enable debian:testing in extra-ci.yml
- Enable centos8 in extra-ci.yml again
- Enable centos7 in extra-ci.yml again
- Enable opensuse-leap and gentoo in extra-ci.yml again
- Run each test script individually on emulated targets
- Try a different syntax for the emulated matrix jobs
- Install s390 glibc headers on s390x fedora systems
- Detect 32-bit and musl presence in test_elf.py
- Skip lost -fPIC tests if gcc lacks -m32 support
- Add stretch and buster to the emulated targets list
- Drop Debian buster from the emulated targets
- Install gcc-multilib only on Debian x86_64 and s390x systems
- libc-dev:i386 -> libc6-dev:i386
- Disable Debian targets in extra-ci temporarily
- s/AUR/git/g in osdeps/arch/post.sh
- In read_cfgfile(), keep track of block depth correctly (#329)
- A few more yaml parsing fixes for block vs group
- Recommend or Require libabigail >= 1.8.2
- Finish normalizing all the error reporting statements
- Advertise of rpminspect-report in the contrib README.
- Report libclamav version and CVD versions (#258)
- Ensure first argument of warn(3) is a format string.
- Enable werror=true and warning_level=3 in default_options
- Update the translation template file
- Get rid of invalid free() in get_product_release()
- Add inspection_id() to librpminspect
- Update the po/rpminspect.pot template
- Improve mkannounce.sh to handle stable and devel releases

* Thu Feb 25 2021 David Cantrell <dcantrell@redhat.com> - 1.3.1-1
- Remove duplicate elf_end() call in init_elf_data() (#303)
- Update translation template

* Thu Feb 25 2021 David Cantrell <dcantrell@redhat.com> - 1.3-2
- Small change to the way Koji builds are submitted
- Move the master branch to version 1.3
- Drop DEBUG_PRINT in process_table()
- Add doc/git.md to explain source control conventions
- Change Suggests to Recommends in the spec file
- Add kmidiff and politics to the inspections section of generic.yaml
- Update TODO list
- Use warn() for non-fatal errors in mkdirp()
- Require libabigail >= 1.8 in rpminspect.spec.in
- Enable multiple --headers-dir1 and --headers-dir2 args in abidiff
- Swap out some more fprintf()/fflush() reporting with warn()
- #include <err.h> in peers.c and rmtree.c
- On fedora-rawhide CI jobs, install gcc-c++ and gcc-plugin-devel
- Disable fedora-rawhide GitHub Action for now
- Correctly handle the -w option on rpminspect(1) (#256)
- Drop the relative path handling for the -w option
- Build and install rc from source on opensuse-leap
- Update doc/git.md on how to track upstream
- Add .github/ and osdeps/ directories to extra-ci.yml
- Build and install rc from source on opensuse-tumbleweed
- Adjust curl(1) command line used for rc in opensuse CI jobs
- Trying to figure out why the opensuse jobs produce curl errors
- Another slight change to post.sh for the opensuse-leap CI job
- s/PowerTools/powertools/g in the centos8 PKG_CMD definition
- The output of html2text on opensuse systems is different
- Rename HEADER_MAN to HEADER_MANPAGE (#264)
- Add inspection_header_to_desc() to librpminspect (#264)
- Add xunit output format support (#264)
- Support the new output function call syntax (#264)
- Move init_elf_data() to readelf.c, move data to struct rpminspect
- Update inspect_elf.c unit tests for librpminspect changes
- Remove check_ipv6() from inspect_elf.c
- Create the badfuncs inspection
- Update po/ translation files.
- Add badfuncs test cases
- Forgot to commit test_badfuncs.py.
- Fix flake8 and black errors with test_badfuncs.py
- Skip debug packages in filesize, display changes correctly
- Fix spurious execstack failure
- Fix YAML config file reading for BLOCK_INSPECTIONS
- Expand dump_config() to cover all config file settings
- Minor spelling fixes in strfuncs.c and making code explicit
- Simplify list_to_string() so it handles 1-elements lists right
- Add abspath() to canonicalize path strings
- In the doc inspection, only show diff(1) output for text files (#254)
- Add strxmlescape() to strfuncs.c in librpminspect (#264)
- Output the system-out xunit portion as CDATA (#264)
- Slightly change how strxmlescape() works
- Add the runpath inspection to librpminspect
- Rename test/data/lto.c to test/data/mathlib.c
- Handle the empty string case in abspath()
- Expand dump_cfg() to show runpath settings
- Fix block handling problems in the YAML config reader
- Note single builds cannot be rebases in is_rebase()
- Hook up the driver for the runpath inspection
- Install patchelf for tests on fedora and centos
- Update TODO and README.md files
- Pass -D to rpminspect in the test suite
- Add integration tests for the runpath inspection
- Python flake8 and black fixes in test_runpath.py
- Fixes for GitHub Actions on Debian and Ubuntu
- Disable Rust support in pip modules, more extra-ci fixes
- Update pip and setuptools on debian and ubuntu CI jobs
- Make sure pip is updated on debian, centos7, and centos8
- Fixes for extra-ci on arch, centos7, centos8, and debian
- Adjust docker image names for opensuse and arch
- Add Gentoo Linux to the Extra CI set
- extra-ci.yml typo fix for the gentoo job
- Use gentoo/stage3 as the container for the gentoo CI job
- Disable opensuse-tumbleweed and archlinux CI jobs
- Make sure util/determine-os.sh picks up Gentoo Linux
- In the runpath inspection, fail if DT_RPATH and DT_RUNPATH exist
- Use pip install for PIP_CMD on gentoo
- Set PIP_CMD to pip install -user for gentoo
- Handle a NULL from list_to_string() in abspath()
- Do not match path prefixes in the runpath inspection
- Python black fixes for test_runpath.py
- Stop doing an emerge --sync on the gentoo CI job
- Replace emerge --sync with a manual portage sync
- Use emerge-webrsync to update portage on gentoo
- Add uthash and move the file matching code to it.
- Typo fix in README.md
- Fix some memory leaks found by valgrind
- Create mkannounce.sh to help make release announcements easier
- shellcheck fixes for mkannounce.sh

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 26 2020 David Cantrell <dcantrell@redhat.com> - 1.2-1
- For BUILDTYPE=release, generate the correct type of changelog
- Minor logic error in submit-koji-builds.sh
- Fix reading existing spec file in submit-koji-builds.sh
- Bump development build version to 1.2
- Use is_rebase() in the 'upstream' inspection
- Use rpmtdSetIndex() and rpmtdGetString() in get_header_value()
- Add get_rpmtag_fileflags() to files.c and call from extract_rpm()
- Use correct Version and Release values in download_build()
- #include <rpm/rpmfiles.h> -> #include <rpm/rpmfi.h>
- Add the 'config' inspection to librpminspect
- Rephrase reporting messages in the 'config' inspection
- Add the 'doc' inspection to librpminspect
- Update TODO list
- Minor updates to try and make gate.sh more reliable
- Add config and doc to the inspections list in generic.yaml
- Rename the '%%files' inspection to 'files' (#194)
- Modify baseclass.py to allow 'before' and 'after' NVR tuples
- Use the after tuple to override the NVR in test_abidiff.py
- Use the after tuple to override the NVR in test_upstream.py
- Write rpminspect output to a file in the test suite
- Add 28 test cases for the 'config' inspection
- Fix the errors in the 'config' inspection found by the test suite
- Fix Python problems in the test suite reported by black and flake8
- Add Makefile targets for black and flake8
- One more formatting issue reporting by Python black in test_config.py
- More 'python black' formatting errors reported for test_config.py
- https://mandoc.bsd.lv -> http://mandoc.bsd.lv
- Add a -D/--dump-config option to rpminspect(1)
- Use global reported variable in 'config' inspection
- Fix reporting errors in the 'doc' inspection
- Add test_doc.py with 'doc' inspection test cases
- Ignore flake8 W291 in test_doc.py where we explicitly want whitepsace.
- Add init_rebaseable() to librpminspect
- Check the rebaseable list in is_rebase() in librpminspect
- Update TODO list
- Define a new GitHub Action using utils/gate.sh
- Update the README.md file
- shellcheck fixes for utils/gate.sh
- Use utils/find-ninja.sh to determine what ninja-build command to use
- Install fedora-packager for the gate.yml GitHub Action
- Remove before and after variables from gate.sh; unused
- Remove unnecessary basename() calls in inspect_upstream.c
- Do not assume an or bn contain strings in is_rebase() (#196)
- Adjust what things run during with GitHub Actions
- Add get_rpm_header_string_array() to librpminspect
- Replace init_source() with get_rpm_header_string_array() in
  inspect_upstream.c
- free() allocated output string in inspect_changelog.c on errors
- s/10240/16384/ in archive_read_open_filename() call in unpack.c
- Add the 'patches' inspection to librpminspect
- Add uncompress_file() to librpminspect
- Add filecmp() and use that in place of zcmp/bzcmp/xzcmp
- README.md updates
- Restrict some GitHub Actions to source code and test suite changes.
- Only enable lz4 compression if ARCHIVE_FILTER_LZ4 is defined
- Go ahead and wrap the rest of the libarchive compression filters
- s/class Test/class /g
- Make sure uncompress_file() supports xz compression
- Handle more compressed file MIME types.
- Add test_changedfiles.py to the test suite.
- Add test_patches.py with test cases for the 'patches' inspection
- flake8 fixes in the test suite
- Python format fixes for test_changedfiles.py
- Python format fixes in test_patches.py
- More Python format fixes for test_patches.py
- Remove unnecessary 'a' in DESC_PATCHES
- Better explanation as to why the EmptyLicenseTag tests are skipped.
- Test suite cleanup; add rebase= and same= to TestCompareSRPM
- Black formatting fixes for the test suite.
- Remove unused imports in test_upstream.py
- Revert black fixes for test_config.py
- Fix my email address in test suite source files.
- Support single package URLs for before and after builds (#190)
- Handle invalid/missing RPMs in get_product_release()
- Use warnx(), errx(), and err() in src/rpminspect.c
- Modify submit-koji-builds.sh to pick up all pkg-git branches.
- Update the rpminspect.1 man page to reflect current status.
- Update translation template files in po/
- Support relative directory paths for the -w option (#188)
- Implement the 'virus' inspection and add test cases for it.
- Update po/ template files
- Python formatting fixes for test_virus.py
- Update the osdeps/*/reqs.txt files.
- More osdeps updates for the clamav needs
- Install 'xz' for the 'style' GitHub Action
- Fix a variety of small memory leaks in librpminspect
- Stop the freshclam service for the Ubuntu gate job
- Support slightly older versions of libclamav in inspect_virus.c
- Add the 'politics' inspection to librpminspect.
- In tearDown() in the test suite, call rpmfluff clean() methods
- Add test_politics.py with 'politics' inspection test cases
- Python black format fixes for test_politics.py
- 'it should added' -> 'it should be added'
- Increase the runtime timeout for test_virus.py
- Install the timeout decorator on all OSes in our GitHub Actions
- Install timeout-decorator with pip, not timeout
- Expand librpminspect with support for SHA-224, SHA-384, and SHA-512
- Define DEFAULT_MESSAGE_DIGEST in constants.h and use that.
- Replace some fprintf()/fflush() calls with warn()/warnx() calls
- Rename the 'DT_NEEDED' inspection to 'dsodeps'
- Rename 'LTO' inspection to 'lto'
- Update translation template and fix two incorrect error strings.
- Note all valid message digests in data/politics/GENERIC
- Improve reporting in the patches inspection
- Only fail 'changedfiles' for VERIFY and higher results
- If 'removedfiles' only reports INFO messages, pass the inspection
- If 'addedfiles' only reports INFO results, pass the inspection
- If 'patches' only reports INFO results, pass the inspection
- No need to check value of allowed in permissions_driver()
- Do not let INFO results fail the 'doc' inspection.
- Do not let all INFO results in 'upstream' fail the inspection
- Fix RPMFILE_FLAGS handling for %%config files (#221)
- Still report file changes in the 'config' inspection for rebases
- Correctly check RPMFILE_DOC flags in the 'doc' inspection
- Include rpm/rpmfi.h insted of rpm/rpmfiles.h
- Only check regular files and symlinks in the 'doc' inspection
- Remove unnecessary assert() statements in filecmp()
- Remove incorrect warnx() reportings based on filecmp() return value
- Exclude man pages from the 'doc' inspection
- Honor the -a command line option for downloads as well as runtime
  (#233)
- Allow optional 'commands' block in the config file
- Fix assorted non-critical memory leaks
- Remove unnecessary warn() after a failed stat()
- Additional memory fixes for the abidiff inspection (#244)
- Free ELF symbol names list in find_lto_symbols() before return
- Followup to the memory fixes for read_abi() and free_abi()
- Prevent invalid pointer dereferencing in invalid result in 'patches'
  (#245)
- Avoid reusing the same abi_pkg_entry_t struct in read_abi()
- Allow a set of excluded path prefixes in 'pathmigration'
- Fix the YAML parsing for the pathmigration block
- Document the BRANCHES variable for 'make koji'
- Include the .asc file when submitting new Koji builds (#191)
- Include the .asc file in the spec file

* Mon Oct 26 2020 David Cantrell <dcantrell@redhat.com> - 1.2-1
- For BUILDTYPE=release, generate the correct type of changelog
- Minor logic error in submit-koji-builds.sh
- Fix reading existing spec file in submit-koji-builds.sh
- Bump development build version to 1.2
- Use is_rebase() in the 'upstream' inspection
- Use rpmtdSetIndex() and rpmtdGetString() in get_header_value()
- Add get_rpmtag_fileflags() to files.c and call from extract_rpm()
- Use correct Version and Release values in download_build()
- #include <rpm/rpmfiles.h> -> #include <rpm/rpmfi.h>
- Add the 'config' inspection to librpminspect
- Rephrase reporting messages in the 'config' inspection
- Add the 'doc' inspection to librpminspect
- Update TODO list
- Minor updates to try and make gate.sh more reliable
- Add config and doc to the inspections list in generic.yaml
- Rename the '%%files' inspection to 'files' (#194)
- Modify baseclass.py to allow 'before' and 'after' NVR tuples
- Use the after tuple to override the NVR in test_abidiff.py
- Use the after tuple to override the NVR in test_upstream.py
- Write rpminspect output to a file in the test suite
- Add 28 test cases for the 'config' inspection
- Fix the errors in the 'config' inspection found by the test suite
- Fix Python problems in the test suite reported by black and flake8
- Add Makefile targets for black and flake8
- One more formatting issue reporting by Python black in test_config.py
- More 'python black' formatting errors reported for test_config.py
- https://mandoc.bsd.lv -> http://mandoc.bsd.lv
- Add a -D/--dump-config option to rpminspect(1)
- Use global reported variable in 'config' inspection
- Fix reporting errors in the 'doc' inspection
- Add test_doc.py with 'doc' inspection test cases
- Ignore flake8 W291 in test_doc.py where we explicitly want whitepsace.
- Add init_rebaseable() to librpminspect
- Check the rebaseable list in is_rebase() in librpminspect
- Update TODO list
- Define a new GitHub Action using utils/gate.sh
- Update the README.md file
- shellcheck fixes for utils/gate.sh
- Use utils/find-ninja.sh to determine what ninja-build command to use
- Install fedora-packager for the gate.yml GitHub Action
- Remove before and after variables from gate.sh; unused
- Remove unnecessary basename() calls in inspect_upstream.c
- Do not assume an or bn contain strings in is_rebase() (#196)
- Adjust what things run during with GitHub Actions
- Add get_rpm_header_string_array() to librpminspect
- Replace init_source() with get_rpm_header_string_array() in
  inspect_upstream.c
- free() allocated output string in inspect_changelog.c on errors
- s/10240/16384/ in archive_read_open_filename() call in unpack.c
- Add the 'patches' inspection to librpminspect
- Add uncompress_file() to librpminspect
- Add filecmp() and use that in place of zcmp/bzcmp/xzcmp
- README.md updates
- Restrict some GitHub Actions to source code and test suite changes.
- Only enable lz4 compression if ARCHIVE_FILTER_LZ4 is defined
- Go ahead and wrap the rest of the libarchive compression filters
- s/class Test/class /g
- Make sure uncompress_file() supports xz compression
- Handle more compressed file MIME types.
- Add test_changedfiles.py to the test suite.
- Add test_patches.py with test cases for the 'patches' inspection
- flake8 fixes in the test suite
- Python format fixes for test_changedfiles.py
- Python format fixes in test_patches.py
- More Python format fixes for test_patches.py
- Remove unnecessary 'a' in DESC_PATCHES
- Better explanation as to why the EmptyLicenseTag tests are skipped.
- Test suite cleanup; add rebase= and same= to TestCompareSRPM
- Black formatting fixes for the test suite.
- Remove unused imports in test_upstream.py
- Revert black fixes for test_config.py
- Fix my email address in test suite source files.
- Support single package URLs for before and after builds (#190)
- Handle invalid/missing RPMs in get_product_release()
- Use warnx(), errx(), and err() in src/rpminspect.c
- Modify submit-koji-builds.sh to pick up all pkg-git branches.
- Update the rpminspect.1 man page to reflect current status.
- Update translation template files in po/
- Support relative directory paths for the -w option (#188)
- Implement the 'virus' inspection and add test cases for it.
- Update po/ template files
- Python formatting fixes for test_virus.py
- Update the osdeps/*/reqs.txt files.
- More osdeps updates for the clamav needs
- Install 'xz' for the 'style' GitHub Action
- Fix a variety of small memory leaks in librpminspect
- Stop the freshclam service for the Ubuntu gate job
- Support slightly older versions of libclamav in inspect_virus.c
- Add the 'politics' inspection to librpminspect.
- In tearDown() in the test suite, call rpmfluff clean() methods
- Add test_politics.py with 'politics' inspection test cases
- Python black format fixes for test_politics.py
- 'it should added' -> 'it should be added'
- Increase the runtime timeout for test_virus.py
- Install the timeout decorator on all OSes in our GitHub Actions
- Install timeout-decorator with pip, not timeout
- Expand librpminspect with support for SHA-224, SHA-384, and SHA-512
- Define DEFAULT_MESSAGE_DIGEST in constants.h and use that.
- Replace some fprintf()/fflush() calls with warn()/warnx() calls
- Rename the 'DT_NEEDED' inspection to 'dsodeps'
- Rename 'LTO' inspection to 'lto'
- Update translation template and fix two incorrect error strings.
- Note all valid message digests in data/politics/GENERIC
- Improve reporting in the patches inspection
- Only fail 'changedfiles' for VERIFY and higher results
- If 'removedfiles' only reports INFO messages, pass the inspection
- If 'addedfiles' only reports INFO results, pass the inspection
- If 'patches' only reports INFO results, pass the inspection
- No need to check value of allowed in permissions_driver()
- Do not let INFO results fail the 'doc' inspection.
- Do not let all INFO results in 'upstream' fail the inspection
- Fix RPMFILE_FLAGS handling for %%config files (#221)
- Still report file changes in the 'config' inspection for rebases
- Correctly check RPMFILE_DOC flags in the 'doc' inspection
- Include rpm/rpmfi.h insted of rpm/rpmfiles.h
- Only check regular files and symlinks in the 'doc' inspection
- Remove unnecessary assert() statements in filecmp()
- Remove incorrect warnx() reportings based on filecmp() return value
- Exclude man pages from the 'doc' inspection
- Honor the -a command line option for downloads as well as runtime
  (#233)
- Allow optional 'commands' block in the config file
- Fix assorted non-critical memory leaks
- Remove unnecessary warn() after a failed stat()
- Additional memory fixes for the abidiff inspection (#244)
- Free ELF symbol names list in find_lto_symbols() before return
- Followup to the memory fixes for read_abi() and free_abi()
- Prevent invalid pointer dereferencing in invalid result in 'patches'
  (#245)
- Avoid reusing the same abi_pkg_entry_t struct in read_abi()
- Allow a set of excluded path prefixes in 'pathmigration'
- Fix the YAML parsing for the pathmigration block
- Document the BRANCHES variable for 'make koji'
- Include the .asc file when submitting new Koji builds (#191)
- Include the .asc file in the spec file

* Mon Oct 26 2020 David Cantrell <dcantrell@redhat.com> - 1.2-1
- For BUILDTYPE=release, generate the correct type of changelog
- Minor logic error in submit-koji-builds.sh
- Fix reading existing spec file in submit-koji-builds.sh
- Bump development build version to 1.2
- Use is_rebase() in the 'upstream' inspection
- Use rpmtdSetIndex() and rpmtdGetString() in get_header_value()
- Add get_rpmtag_fileflags() to files.c and call from extract_rpm()
- Use correct Version and Release values in download_build()
- #include <rpm/rpmfiles.h> -> #include <rpm/rpmfi.h>
- Add the 'config' inspection to librpminspect
- Rephrase reporting messages in the 'config' inspection
- Add the 'doc' inspection to librpminspect
- Update TODO list
- Minor updates to try and make gate.sh more reliable
- Add config and doc to the inspections list in generic.yaml
- Rename the '%%files' inspection to 'files' (#194)
- Modify baseclass.py to allow 'before' and 'after' NVR tuples
- Use the after tuple to override the NVR in test_abidiff.py
- Use the after tuple to override the NVR in test_upstream.py
- Write rpminspect output to a file in the test suite
- Add 28 test cases for the 'config' inspection
- Fix the errors in the 'config' inspection found by the test suite
- Fix Python problems in the test suite reported by black and flake8
- Add Makefile targets for black and flake8
- One more formatting issue reporting by Python black in test_config.py
- More 'python black' formatting errors reported for test_config.py
- https://mandoc.bsd.lv -> http://mandoc.bsd.lv
- Add a -D/--dump-config option to rpminspect(1)
- Use global reported variable in 'config' inspection
- Fix reporting errors in the 'doc' inspection
- Add test_doc.py with 'doc' inspection test cases
- Ignore flake8 W291 in test_doc.py where we explicitly want whitepsace.
- Add init_rebaseable() to librpminspect
- Check the rebaseable list in is_rebase() in librpminspect
- Update TODO list
- Define a new GitHub Action using utils/gate.sh
- Update the README.md file
- shellcheck fixes for utils/gate.sh
- Use utils/find-ninja.sh to determine what ninja-build command to use
- Install fedora-packager for the gate.yml GitHub Action
- Remove before and after variables from gate.sh; unused
- Remove unnecessary basename() calls in inspect_upstream.c
- Do not assume an or bn contain strings in is_rebase() (#196)
- Adjust what things run during with GitHub Actions
- Add get_rpm_header_string_array() to librpminspect
- Replace init_source() with get_rpm_header_string_array() in
  inspect_upstream.c
- free() allocated output string in inspect_changelog.c on errors
- s/10240/16384/ in archive_read_open_filename() call in unpack.c
- Add the 'patches' inspection to librpminspect
- Add uncompress_file() to librpminspect
- Add filecmp() and use that in place of zcmp/bzcmp/xzcmp
- README.md updates
- Restrict some GitHub Actions to source code and test suite changes.
- Only enable lz4 compression if ARCHIVE_FILTER_LZ4 is defined
- Go ahead and wrap the rest of the libarchive compression filters
- s/class Test/class /g
- Make sure uncompress_file() supports xz compression
- Handle more compressed file MIME types.
- Add test_changedfiles.py to the test suite.
- Add test_patches.py with test cases for the 'patches' inspection
- flake8 fixes in the test suite
- Python format fixes for test_changedfiles.py
- Python format fixes in test_patches.py
- More Python format fixes for test_patches.py
- Remove unnecessary 'a' in DESC_PATCHES
- Better explanation as to why the EmptyLicenseTag tests are skipped.
- Test suite cleanup; add rebase= and same= to TestCompareSRPM
- Black formatting fixes for the test suite.
- Remove unused imports in test_upstream.py
- Revert black fixes for test_config.py
- Fix my email address in test suite source files.
- Support single package URLs for before and after builds (#190)
- Handle invalid/missing RPMs in get_product_release()
- Use warnx(), errx(), and err() in src/rpminspect.c
- Modify submit-koji-builds.sh to pick up all pkg-git branches.
- Update the rpminspect.1 man page to reflect current status.
- Update translation template files in po/
- Support relative directory paths for the -w option (#188)
- Implement the 'virus' inspection and add test cases for it.
- Update po/ template files
- Python formatting fixes for test_virus.py
- Update the osdeps/*/reqs.txt files.
- More osdeps updates for the clamav needs
- Install 'xz' for the 'style' GitHub Action
- Fix a variety of small memory leaks in librpminspect
- Stop the freshclam service for the Ubuntu gate job
- Support slightly older versions of libclamav in inspect_virus.c
- Add the 'politics' inspection to librpminspect.
- In tearDown() in the test suite, call rpmfluff clean() methods
- Add test_politics.py with 'politics' inspection test cases
- Python black format fixes for test_politics.py
- 'it should added' -> 'it should be added'
- Increase the runtime timeout for test_virus.py
- Install the timeout decorator on all OSes in our GitHub Actions
- Install timeout-decorator with pip, not timeout
- Expand librpminspect with support for SHA-224, SHA-384, and SHA-512
- Define DEFAULT_MESSAGE_DIGEST in constants.h and use that.
- Replace some fprintf()/fflush() calls with warn()/warnx() calls
- Rename the 'DT_NEEDED' inspection to 'dsodeps'
- Rename 'LTO' inspection to 'lto'
- Update translation template and fix two incorrect error strings.
- Note all valid message digests in data/politics/GENERIC
- Improve reporting in the patches inspection
- Only fail 'changedfiles' for VERIFY and higher results
- If 'removedfiles' only reports INFO messages, pass the inspection
- If 'addedfiles' only reports INFO results, pass the inspection
- If 'patches' only reports INFO results, pass the inspection
- No need to check value of allowed in permissions_driver()
- Do not let INFO results fail the 'doc' inspection.
- Do not let all INFO results in 'upstream' fail the inspection
- Fix RPMFILE_FLAGS handling for %%config files (#221)
- Still report file changes in the 'config' inspection for rebases
- Correctly check RPMFILE_DOC flags in the 'doc' inspection
- Include rpm/rpmfi.h insted of rpm/rpmfiles.h
- Only check regular files and symlinks in the 'doc' inspection
- Remove unnecessary assert() statements in filecmp()
- Remove incorrect warnx() reportings based on filecmp() return value
- Exclude man pages from the 'doc' inspection
- Honor the -a command line option for downloads as well as runtime
  (#233)
- Allow optional 'commands' block in the config file
- Fix assorted non-critical memory leaks
- Remove unnecessary warn() after a failed stat()
- Additional memory fixes for the abidiff inspection (#244)
- Free ELF symbol names list in find_lto_symbols() before return
- Followup to the memory fixes for read_abi() and free_abi()
- Prevent invalid pointer dereferencing in invalid result in 'patches'
  (#245)
- Avoid reusing the same abi_pkg_entry_t struct in read_abi()
- Allow a set of excluded path prefixes in 'pathmigration'
- Fix the YAML parsing for the pathmigration block
- Document the BRANCHES variable for 'make koji'
- Include the .asc file when submitting new Koji builds (#191)
- Include the .asc file in the spec file

* Mon Oct 26 2020 David Cantrell <dcantrell@redhat.com> - 1.2-1
- For BUILDTYPE=release, generate the correct type of changelog
- Minor logic error in submit-koji-builds.sh
- Fix reading existing spec file in submit-koji-builds.sh
- Bump development build version to 1.2
- Use is_rebase() in the 'upstream' inspection
- Use rpmtdSetIndex() and rpmtdGetString() in get_header_value()
- Add get_rpmtag_fileflags() to files.c and call from extract_rpm()
- Use correct Version and Release values in download_build()
- #include <rpm/rpmfiles.h> -> #include <rpm/rpmfi.h>
- Add the 'config' inspection to librpminspect
- Rephrase reporting messages in the 'config' inspection
- Add the 'doc' inspection to librpminspect
- Update TODO list
- Minor updates to try and make gate.sh more reliable
- Add config and doc to the inspections list in generic.yaml
- Rename the '%%files' inspection to 'files' (#194)
- Modify baseclass.py to allow 'before' and 'after' NVR tuples
- Use the after tuple to override the NVR in test_abidiff.py
- Use the after tuple to override the NVR in test_upstream.py
- Write rpminspect output to a file in the test suite
- Add 28 test cases for the 'config' inspection
- Fix the errors in the 'config' inspection found by the test suite
- Fix Python problems in the test suite reported by black and flake8
- Add Makefile targets for black and flake8
- One more formatting issue reporting by Python black in test_config.py
- More 'python black' formatting errors reported for test_config.py
- https://mandoc.bsd.lv -> http://mandoc.bsd.lv
- Add a -D/--dump-config option to rpminspect(1)
- Use global reported variable in 'config' inspection
- Fix reporting errors in the 'doc' inspection
- Add test_doc.py with 'doc' inspection test cases
- Ignore flake8 W291 in test_doc.py where we explicitly want whitepsace.
- Add init_rebaseable() to librpminspect
- Check the rebaseable list in is_rebase() in librpminspect
- Update TODO list
- Define a new GitHub Action using utils/gate.sh
- Update the README.md file
- shellcheck fixes for utils/gate.sh
- Use utils/find-ninja.sh to determine what ninja-build command to use
- Install fedora-packager for the gate.yml GitHub Action
- Remove before and after variables from gate.sh; unused
- Remove unnecessary basename() calls in inspect_upstream.c
- Do not assume an or bn contain strings in is_rebase() (#196)
- Adjust what things run during with GitHub Actions
- Add get_rpm_header_string_array() to librpminspect
- Replace init_source() with get_rpm_header_string_array() in
  inspect_upstream.c
- free() allocated output string in inspect_changelog.c on errors
- s/10240/16384/ in archive_read_open_filename() call in unpack.c
- Add the 'patches' inspection to librpminspect
- Add uncompress_file() to librpminspect
- Add filecmp() and use that in place of zcmp/bzcmp/xzcmp
- README.md updates
- Restrict some GitHub Actions to source code and test suite changes.
- Only enable lz4 compression if ARCHIVE_FILTER_LZ4 is defined
- Go ahead and wrap the rest of the libarchive compression filters
- s/class Test/class /g
- Make sure uncompress_file() supports xz compression
- Handle more compressed file MIME types.
- Add test_changedfiles.py to the test suite.
- Add test_patches.py with test cases for the 'patches' inspection
- flake8 fixes in the test suite
- Python format fixes for test_changedfiles.py
- Python format fixes in test_patches.py
- More Python format fixes for test_patches.py
- Remove unnecessary 'a' in DESC_PATCHES
- Better explanation as to why the EmptyLicenseTag tests are skipped.
- Test suite cleanup; add rebase= and same= to TestCompareSRPM
- Black formatting fixes for the test suite.
- Remove unused imports in test_upstream.py
- Revert black fixes for test_config.py
- Fix my email address in test suite source files.
- Support single package URLs for before and after builds (#190)
- Handle invalid/missing RPMs in get_product_release()
- Use warnx(), errx(), and err() in src/rpminspect.c
- Modify submit-koji-builds.sh to pick up all pkg-git branches.
- Update the rpminspect.1 man page to reflect current status.
- Update translation template files in po/
- Support relative directory paths for the -w option (#188)
- Implement the 'virus' inspection and add test cases for it.
- Update po/ template files
- Python formatting fixes for test_virus.py
- Update the osdeps/*/reqs.txt files.
- More osdeps updates for the clamav needs
- Install 'xz' for the 'style' GitHub Action
- Fix a variety of small memory leaks in librpminspect
- Stop the freshclam service for the Ubuntu gate job
- Support slightly older versions of libclamav in inspect_virus.c
- Add the 'politics' inspection to librpminspect.
- In tearDown() in the test suite, call rpmfluff clean() methods
- Add test_politics.py with 'politics' inspection test cases
- Python black format fixes for test_politics.py
- 'it should added' -> 'it should be added'
- Increase the runtime timeout for test_virus.py
- Install the timeout decorator on all OSes in our GitHub Actions
- Install timeout-decorator with pip, not timeout
- Expand librpminspect with support for SHA-224, SHA-384, and SHA-512
- Define DEFAULT_MESSAGE_DIGEST in constants.h and use that.
- Replace some fprintf()/fflush() calls with warn()/warnx() calls
- Rename the 'DT_NEEDED' inspection to 'dsodeps'
- Rename 'LTO' inspection to 'lto'
- Update translation template and fix two incorrect error strings.
- Note all valid message digests in data/politics/GENERIC
- Improve reporting in the patches inspection
- Only fail 'changedfiles' for VERIFY and higher results
- If 'removedfiles' only reports INFO messages, pass the inspection
- If 'addedfiles' only reports INFO results, pass the inspection
- If 'patches' only reports INFO results, pass the inspection
- No need to check value of allowed in permissions_driver()
- Do not let INFO results fail the 'doc' inspection.
- Do not let all INFO results in 'upstream' fail the inspection
- Fix RPMFILE_FLAGS handling for %%config files (#221)
- Still report file changes in the 'config' inspection for rebases
- Correctly check RPMFILE_DOC flags in the 'doc' inspection
- Include rpm/rpmfi.h insted of rpm/rpmfiles.h
- Only check regular files and symlinks in the 'doc' inspection
- Remove unnecessary assert() statements in filecmp()
- Remove incorrect warnx() reportings based on filecmp() return value
- Exclude man pages from the 'doc' inspection
- Honor the -a command line option for downloads as well as runtime
  (#233)
- Allow optional 'commands' block in the config file
- Fix assorted non-critical memory leaks
- Remove unnecessary warn() after a failed stat()
- Additional memory fixes for the abidiff inspection (#244)
- Free ELF symbol names list in find_lto_symbols() before return
- Followup to the memory fixes for read_abi() and free_abi()
- Prevent invalid pointer dereferencing in invalid result in 'patches'
  (#245)
- Avoid reusing the same abi_pkg_entry_t struct in read_abi()
- Allow a set of excluded path prefixes in 'pathmigration'
- Fix the YAML parsing for the pathmigration block
- Document the BRANCHES variable for 'make koji'
- Include the .asc file when submitting new Koji builds (#191)
- Include the .asc file in the spec file

* Fri Sep 11 2020 David Cantrell <dcantrell@redhat.com> - 1.1-1
- Formatting fixes in Makefile help output
- Begin config file restructuring starting with rpminspect-data-generic
- Support multiple configuration files.
- Docs work in progress.
- Only fail the annocheck inspection for RESULT_VERIFY.
- Read debuginfo if available when running the 'annocheck' inspection.
- Add the '%%files' inspection to librpminspect
- Add __attribute__((__sentinel__)) to the run_cmd() prototype
- Add test suite cases for the '%%files' inspection.
- Added the 'types' inspection to compare MIME types between builds.
- Update TODO file
- Update the MISSING file
- s/rpminspect.yaml/generic.yaml/ in the Makefile and README
- Skip debuginfo and debugsource packages in the 'types' inspection
- Add test_types.py to the test suite
- Note the 'types' inspection generic.yaml
- Modify add_entry() in init.c to skip duplicate entries
- Start GitHub Action workflow files for rpminspect.
- Install meson in ci-ubuntu.yml
- Change 'nls' option in meson_options.txt to a boolean
- Install gettext for ci-ubuntu
- Add more build dependencies to ci-ubuntu.yml
- Drop the 'method' parameter from dependency() lines in meson.build
- Split xmlrpc libs to separate dependency() lines in meson.build
- More xmlrpc updates for meson.build and lib/meson.build
- Try to support systems with xmlrpc-c without the pkgconfig file.
- Changes to build on Ubuntu, specifically the GitHub Actions system
- Syntax error in ci-ubuntu.yml
- Add ci-fedora.yml for GitHub Action CI on Fedora
- Fix errors in ci-fedora.yml
- Put all of the ci-ubuntu.yml steps in ci-ubuntu.yml
- Remove install-libmandoc.sh and ubuntu-pkgs.sh helper scripts.
- Install python3-setuptools in ci-ubuntu.yml
- Install rpm-build in ci-fedora.yml
- Install libxmlrpc-core-c3-dev in ci-ubuntu.yml
- Disable ci-ubuntu.yml for now, enable code coverage in ci-fedora.yml
- Remove Travis-CI files.
- coverage fixes for ci-fedora.yml
- Install git in ci-fedora.yml
- Enable manual dispatching of the CI on Fedora tests
- Remove actionspanel thing for GitHub Actions, drop Coveralls block
- Comment the ci-fedora-yaml file
- Fix the 'elf' inspection and test_elf.py on Ubuntu
- Enable the ci-ubuntu GitHub Action again
- Check all return values of getcwd()
- Ignore installed Python modules with pip3 in ci-ubuntu.yml
- Build 'execstack' test program with -Wl,-z,lazy
- Add ci-centos8.yml to enable CI on CentOS 8 as a GitHub Action
- s/centos8:latest/centos8/g
- Trying 'container: centos:centos8'
- Drop 'sudo' from ci-centos8.yml
- Rename README to README.md
- Enable GitHub Action for CI on CentOS 7
- Drop -I from the pip install line in ci-centos7.yml
- Use the 'make instreqs' target for install test suite deps.
- Add back 'dnf -y install 'dnf-command(builddep)'' to ci-fedora.yml
- Nope, that doesn't do it.  Just install make in ci-fedora.yml first
- More 'make instreqs' fixes.
- s/scripts/utils/g in the Makefile
- s/TOPDIR/topdir/g in the Makefile
- Install make in ci-centos7.yml
- Move REQS and PIP lists out of the Makefile to files in osdep/
- '^$$' -> '^$'
- Slightly different sourcing of the osdep/ files
- Set OS using := in the Makefile
- Make the reqs.txt files in osdep/ contain all deps
- linux-headers -> linux-headers-$(uname -r) for Ubuntu
- Remove html401-dtds from osdep/centos8/reqs.txt
- Use `` instead of $() since this list goes through make(1)
- Does $(shell uname -r) work in this case?
- More osdep/ work and simplification.
- Rename 'osdep' to 'osdeps'
- meson patches for opensuse
- Move mandoc installation to post.sh in osdep/ubuntu
- Add GitHub Action for CI on OpenSUSE
- opensuse:latest -> opensuse/leap:latest
- Install tar in ci-opensuse.yml
- Install gzip in ci-opensuse.yml
- More fixes for ci-opensuse.yml
- Small fixes to determine-os.sh
- ci: Add Python linting jobs
- ShellCheck fixes for the regress/ scripts
- ci: Add ShellCheck to lint shell scripts
- Adjust how the Makefile reports unknown operating system.
- Just check $ID in determine-os.sh for opensuse
- Use pip for PIP_CMD on opensuse-leap
- Update the centos images before doing anything else.
- Install curl in opensuse-leap
- Get 'rc' from Fedora on opensuse and copy it to /usr/local
- Install kernel-default-devel for opensuse CI
- Move the 'uses' part of the centos CI jobs to the first step
- ShellCheck fixes for the utils/ scripts.
- Some flake8 fixes in test/, using yapf
- Combine all of the GitHub Actions CI runs in to ci.yml
- Manually install rpmfluff on CentOS 7; pip is failing here
- Use rpmfluff-0.5.7 explicitly for centos7
- Use rpmfluff-0.5.6 on centos7
- OK, let's try rpmfluff-0.5 for centos7
- Last try, rpmfluff-0.5.4.1 for centos7
- Back to trying to manually install rpmfluff for centos7
- Style the Python code with Black
- Add the Black formatting commit to blame revision ignore list
- OK, just copy rpmfluff.py in place
- Make sure to manually install rpmfluff-0.5.7.1 for centos7
- Don't assume we have a header or even a list of files (#161)
- python: flake8: drop * imports
- python: flake8: wrap long lines to less than 100 characters
- python: flake8: drop unused imports
- python: flake8: remove unused local variables
- python: flake8: add PEP8 whitespace
- python: flake8: mark in-line bash scripts as raw strings
- python: rename several duplicate test cases
- ci: merge style workflows
- Adjust rpminspect.spec.in for file moves and default changes.
- Return the reallybadword to the metadata tests
- Adjust test_metadata.LosingVendorCompareKojiBuild to expect VERIFY
- The shared libmandoc check should not look for a static libmandoc
- Update the AUTHORS file
- Rename ipv6_blacklist to forbidden_ipv6_functions
- Rename stat-whitelist to fileinfo
- Rename 'caps_whitelist' to 'caps' and drop the use of 'whitelist'
- Rename abi-checking-whitelist/ to abi/ in /usr/share/rpminspect
- Rename 'version-whitelist/' to 'rebaseable/' in /usr/share/rpminspect
- Rename "political-whitelist/" to "politics/" in /usr/share/rpminspect
- Drop unnecessary method re-definitions in base test classes
- Use super() rather than explicitly calling the parent class
- Call configFile() on object instance rather than using the parent
  class
- Upload coverage report to codecov
- Improve the error reporting for test result checking
- Convert to AUTHORS.md file, add Makefile target to generate it.
- Introduce the 'movedfiles' inspection and a lot of other fixes (#155)
- AUTHORS -> AUTHORS.md in rpminspect.spec.in
- Add basic tests for the filesize inspection
- Multiply the file size difference before dividing
- Update README.md
- Update README.md (more Markdown changes)
- Update POTFILES and rpminspect.pot
- chmod 0755 test_filesize.py
- tests: optionally check the result message
- tests: add further filesize tests for shrinking files
- inspect_filesize: drop extra - from the message about file shrinkage
- Enable 'permissions' inspect for single build analysis.
- Add 24 new test cases to cover the 'permissions' inspection.
- chmod 0755 test_permissions.py
- Make sure all RESULT_INFO results are set to NOT_WAIVABLE
- Fix some specific problems with the 'permissions' inspection.
- Pass "-r GENERIC" to rpminspect in the TestCompareKoji class
- Add 12 more permissions test cases for setuid file checks
- Update TODO list
- Update test_symlink.py tests for new waiver_auth values
- Add a fedora-rawhide job and renamed 'fedora' to fedora-stable
- Update the rpminspect.pot translation template
- Relicense librpminspect (lib/ and include/) as LGPL-3.0-or-later
- Ignore .tox/ subdirectory
- License the rpminspect-data-generic subpackage as CC-BY-4.0
- Add a copy of the Apache 2.0 license for the 5 files in librpminspect
- Update the License tag in the spec file and the %%license lines
- Add debian-testing as a CI workflow; add missing osdeps files.
- Update determine-os.sh to handle Fedora stable and rawhide
- Drop the use of 'sudo' in ci.yml
- sudo required for Ubuntu CI job, install make for debian-testing
- See what $ID is set to in determine-os.sh
- Workaround a bug in meson 0.55.0 for Fedora CI jobs
- Add 'debian' catch to utils/determine-os.sh
- Rename 'osdeps/debian-testing/' to 'osdeps/debian/'
- Add opensuse-tumbleweed to the CI job list
- Add libmagic-dev to osdeps/debian/reqs.txt
- Fix memory corruption in init_rpminspect
- Add comment clarifying the License tag in the spec file.
- If check_results() raises AssertionError, dump the JSON output
- Fix test_changelog.py test cases that are failing.
- Fix UnbalancedChangeLogEditCompareKoji
- Handle rpm versions with x.y.z.w version numbers in test_symlinks.py
- Fix mandoc build problems in opensuse-tumbleweed CI job
- Install gcovr using pip on opensuse-tumbleweed
- Handle systems that lack pkg-config files for libelf and libcap
- Add archlinux CI job in GitHub Actions
- Forgot --noconfirm on the 'pacman -Syu' line.
- Add missing DESC_MOVEDFILES block to inspection_desc()
- More minor fixes to the Arch Linux CI job.
- Install gcovr with pip for the Arch Linux CI job.
- Support building on systems that lack <sys/queue.h>
- Add detection for <sys/queue.h> to meson.build
- Ensure an int is used for snprintf() in inspect_manpage_path()
- WIP: 'abidiff' inspection
- Only report permissions change if there is a mode_diff (#181)
- Fix -Werror failures in inspect_abidiff.c
- Add sl_run_cmd() to librpminspect.
- Add get_arches() to librpminspect
- WIP: abidiff inspection
- Some minor edits to the README.md file
- More minor updates to the README.md file
- Replace get_arches() with init_arches()
- Add test_addedfiles.py to the integration test suite
- Expand find_one_peer() to soft match versioned ELF shared libraries
- Add the beginnings of the 'abidiff' inspection code.
- Report out findings in the abidiff inspection.
- Update the test suite to cover rpmfluff 0.6
- libmandoc configure workaround needed on Debian too
- shellcheck fixes for the scripts in utils/
- Add abi.c, the code that reads in the ABI compat level files (#144)
- Be sure to close the open file before exiting init_fileinfo()
- Python formatting cleanups
- Add --diff to the Python format checker
- Add new setting to abidiff section of the config file
- Add -n/--no-rebase command line option to disable rebase detection
- Store size_threshold as a long int rather than a char *
- Check abidiff(1) results against the ABI compat level definitions
  (#144)
- Add 'apt-get -y install libgcc-s1:i386' to pre.sh for Debian
- Add integration test cases for the abidiff inspection (#144)
- Add 'dpkg --configure -a' to pre.sh for debian
- Install libterm-readline-perl-perl for debian CI
- Install libabigail for Fedora and CentOS CI jobs
- libgcc-s1:i386 -> lib32gcc-s1 for debian CI
- Install libabigail for opensuse-leap, opensuse-tumbleweed, and arch CI
- Install libabigail for debian and ubuntu CI
- Install libabigail-dev for debian and ubuntu, not libabigail
- Install libabigail-tools on opensuse-leap and opensuse-tumbleweed
- Install libabigail-git for arch linux CI
- Move free_argv_table() to runcmd.c
- Install 'abigail-tools' for debian-testing and ubuntu CI
- Install libabigail using the Arch User Repo on arch CI
- Explain the osdeps/ subdirectory.
- No, just clone libabigail from git and build it manually on arch
- Add beginning of kmidiff inspection, put ABI functions in abi.c
- Read list of possible kernel executable filenames from the config
  file.
- Drop abidiff_ and kmidiff_ from extra_args; add kernel_filenames
- Just call the abidiff and kmidiff extra args settings "extra_args"
- Define 'kmi_ignore_pattern' in the config file.
- Handle builds that lack all debuginfo packages (#186)
- Do not assume peer->after_hdr exists (#187)
- Store copy of original pointer in strsplit() to free at the end.
- Use mmap() and strsplit() in read_file() rather than a getline() loop
- Fix memory leaks in abi.c functions
- open() failure in readfile() is not fatal, just return NULL
- Add utils/gate.sh
- Have check_abi() pass back the ABI compat level found
- Update descriptions for abidiff and kmidiff inspections
- Hook up the kmidiff inspection.
- Use read_file() in init_fileinfo() and init_caps()
- Use read_file() in validate_desktop_contents()
- Use read_file() in disttag_driver()
- Adjust how init_fileinfo() and init_caps() iterate over file contents
- Fix 'tox -e format' style problems found.
- Avoid comparing elf files that are not shared libraries
- Support --kmi-whitelist in the kmidiff inspection
- Trim worksubdir from paths in reported abidiff and kmidiff commands
- Remove the kmi_ignore_pattern setting for the config file.
- Create include/queue.h to replace the _COMPAT_QUEUE blocks everywhere
- Update AUTHORS.md
- Report metadata changes for rebased packages as INFO
- Do not fail the specname inspection when given a non-SRPM
- For passing upstream inspections, do not report a remedy string.
- Do not fail the lostpayload inspections if it only gives INFO messages
- Clarify unapproved license message in the license inspection
- Use FOPEN_MAX for nopenfd parameter in nftw() calls
- Make sure to close open file descriptors from get_elf() calls.
- Include 'src' architecture in the rpminspect runs in gate.sh
- Make sure kmidiff is listed in the spec file
- TODO updates
- Update rpminspect.pot and POTFILES for translations
