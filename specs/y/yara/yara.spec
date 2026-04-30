## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           yara
Version:        4.5.4
Summary:        Pattern matching Swiss knife for malware researchers
URL:            https://VirusTotal.github.io/yara/
VCS:            git:https://github.com/VirusTotal/yara/
#               https://github.com/VirusTotal/yara/releases

# yara package itself is licensed with BSD 3 clause license
# bison grammar parsers in libyara/* are licensed with  GPLv3+ license with exception from FSF alloving usage in larger work
# resulting binary package licensed as BSD
License:        BSD-3-Clause

%global         common_description %{expand:
YARA is a tool aimed at (but not limited to) helping malware researchers to
identify and classify malware samples. With YARA you can create descriptions
of malware families (or whatever you want to describe) based on textual or
binary patterns. Each description, a.k.a rule, consists of a set of strings
and a Boolean expression which determine its logic.}


%global         gituser         VirusTotal
%global         gitname         yara
# Commit of version 4.5.4
%global         gitdate         20250527
%global         commit          7ff39042be5c63682a037e13a75221d59393cf8b
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  release


# Build from git release version
%if %{with release}
Release:       %autorelease
# Source0:     https://github.com/%%{gituser}/%%{gitname}/archive/v%%{upversion}.tar.gz#/%%{name}-%%{upversion}.tar.gz
Source0:       https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       %autorelease -s %{gitdate}git%{shortcommit}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif

# Use default sphix theme to generate documentation rather than sphinx_rtd_theme
# to avoid static installation of font files on fedora >= 24
Patch1:         yara-docs-theme.patch


BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  m4
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  sharutils
BuildRequires:  file
BuildRequires:  sed
BuildRequires:  gawk
BuildRequires:  gzip
BuildRequires:  xz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  file-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  protobuf-c-devel
BuildRequires:  protobuf-compiler

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  openssl11-devel
%else
BuildRequires:  openssl-devel
%endif

# html doc generation
BuildRequires:  /usr/bin/sphinx-build

%description
%{common_description}

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
This package contains documentation for %{name}.
%{common_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}

%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1 -S git
%else
    %autosetup -n %{gitname}-%{commit} -p 1 -S git
%endif
autoreconf --force --install

%build

# Add missing protobuf definition on RHEL7, and also configure for the libcrypto11/openssl11 from EPEL
%if 0%{?rhel} && 0%{?rhel} == 7
export CFLAGS="%{optflags} -D PROTOBUF_C_FIELD_FLAG_ONEOF=4 $(pkg-config --cflags libcrypto11)"
export LDFLAGS="$LDFLAGS $(pkg-config --libs libcrypto11)"
%endif

# macro %%configure already does use CFLAGS="%%{optflags}" and yara build
# scripts configure/make already honors that CFLAGS
%configure --enable-magic --enable-cuckoo --enable-debug --enable-dotnet \
        --enable-macho --enable-dex --enable-pb-tests \
        --with-crypto \
        --htmldir=%{_datadir}/doc/%{name}/html
%make_build

# build the HTML documentation
pushd docs
make html
popd


%install
%make_install

# Remove static libraries
rm %{buildroot}%{_libdir}/lib%{name}.la
rm %{buildroot}%{_libdir}/lib%{name}.a

# Remove the rebuild-needed tag so it is not installed in doc pkg
rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo


%if 0%{?rhel} && 0%{?rhel} <= 7
%ldconfig_scriptlets
%endif

%check
# reenable the validation of SHA1 certificates in OPENSSL (RHEL9 disabled that by default)
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes
make check || (
    # print more verbose info in case the test(s) fail
    echo "===== ./test-suite.log"
    [ -f ./test-suite.log ] && cat ./test-suite.log
    # Build in COPR lacking the hwinfo.log
    echo "===== /proc/cpu"
    head -n 35 /proc/cpuinfo
    echo "===== /etc/os-release"
    cat /etc/os-release
    echo "===== uname -a"
    uname -a

%ifarch s390x
    # test-pe and test-dotnet fails for x390x at this point - ignored for rc1
    true
%else
    false
%endif
)

%files
%license COPYING
%doc AUTHORS CONTRIBUTORS README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}c.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%files doc
%license COPYING
%doc docs/_build/html


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4.5.4-4
- test: add initial lock files

* Fri Sep 05 2025 Zephyr Lykos <git@mochaa.ws> - 4.5.4-3
- Update sources file

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Michal Ambroz <rebus@seznam.cz> - 4.5.4-1
- bump to yara 4.5.4

* Fri May 23 2025 Michal Ambroz <rebus@seznam.cz> - 4.5.3-1
- bump to 4.5.3

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 4.5.2-5
- Rebuild for Jansson 2.14 (https://lists.fedoraproject.org/archives/list/d
  evel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Tue Oct 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.5.2-4
- Remove unused pcre dependency

* Sat Sep 28 2024 Michal Ambroz <rebus@seznam.cz> - 4.5.2-3
- switch to autochangelog

* Mon Sep 16 2024 Michal Ambroz <rebus _AT seznam.cz> - 4.5.2-1
- bump to 4.5.2

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 27 2024 Michal Ambroz <rebus _AT seznam.cz> - 4.5.1-1
- bump to 4.5.1

* Wed Feb 14 2024 Michal Ambroz <rebus _AT seznam.cz> - 4.5.0-1
- bump to 4.5.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 17 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 4.4.0-1
- bump to 4.4.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.2-1
- bump to 4.3.2

* Wed Apr 26 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.1-1
- bump to 4.3.1

* Thu Mar 30 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.0-1
- bump to 4.3.0

* Tue Jan 24 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.0-0.rc1.3
- fix EPEL9 build = reenable the SHA1 certificate validation in OpenSSL for make check

* Sat Jan 21 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.0-0.rc1.2
- fix EPEL7 build

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Michal Ambroz <rebus _AT seznam.cz> - 4.3.0-0.rc1.1
- bump to 4.3.0 rc1
- remove the androguard module which is no longer available from github

* Tue Aug 09 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 4.2.3-1
- Update to 4.2.3 (#2116594)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 4.2.2-1
- Update to 4.2.2 (#2103444)
- BUGFIX: Fix buffer overrun in "dex" module (#1728).
- BUGFIX: Wrong offset used when checking Version string of .net metadata (#1708).
- BUGFIX: YARA doesn't compile if --with-debug-verbose flag is enabled (#1719).
- BUGFIX: Null-pointer dereferences while loading corrupted compiled rules (#1727).

* Mon May 23 2022 Michal Ambroz <rebus _AT seznam.cz> - 4.2.1-1
- bump to 4.2.1
- adding changes based on proposal of Mikel Olasagasti Uranga:
- change to BSD license as yara was relicensed in 2016
- minor changes to spec, like using https for URL
- remove old patches
- enable checks

* Sat Mar 12 2022 Michal Ambroz <rebus _AT seznam.cz> - 4.2.0-1
- bump to 4.2.0

* Thu Feb 17 2022 Michal Ambroz <rebus _AT seznam.cz> - 4.2.0-0.rc1.1
- bump to 4.2.0-rc1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.1.3-1
- bump to 4.1.3

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 4.1.1-5
- Rebuilt for protobuf 3.19.0

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 4.1.1-4
- Rebuilt for protobuf 3.18.1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.1.1-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.1.1-1
- bump to 4.1.1

* Mon Apr 26 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.1.0-1
- bump to 4.1.0

* Sun Apr 25 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.0.5-2
- rebuild for epel

* Fri Feb 5 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.0.5-1
- bump to yara bugfix 4.0.5 release

* Wed Feb 3 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.0.4-1
- bump to yara bugfix 4.0.4 release

* Thu Jul 16 2020 Michal Ambroz <rebus _AT seznam.cz> - 4.0.2-1
- bump to yara bugfix 4.0.2 release
- fix build on epel7

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 4.0.1-2
- Rebuilt for protobuf 3.12

* Tue Jun 2 2020 Michal Ambroz <rebus _AT seznam.cz> - 4.0.1-1
- bump to yara bugfix 4.0.1 release

* Tue Apr 28 2020 Michal Ambroz <rebus _AT seznam.cz> - 4.0.0-1
- bump to yara 4.0.0 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Michal Ambroz <rebus _AT seznam.cz> - 3.11.0-1
- bump to 3.11.0 release (#1760678)
- BUGFIX: Some regexp character classes not matching correctly when used with “nocase” modifier (upstream #1117)
- BUGFIX: Reduce the number of ERROR_TOO_MANY_RE_FIBERS errors for certain hex pattern containing large jumps (upstream #1107)
- BUGFIX: Buffer overrun in “dotnet” module (upstream #1108)
- BUGFIX: Memory leak while attaching to a process fails (upstream #1070)

* Sat Sep 28 2019 Michal Ambroz <rebus _AT seznam.cz> - 3.10.0-3
- change the sphinx build dependency

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 03 2019 Michal Ambroz <rebus _AT seznam.cz> - 3.10.0-1
- bump to 3.10.0 release (#1680204)
- Harden virtual machine against malicious code.
- BUGFIX: Regression bug in hex strings containing wildcards (upstream #1025).
- BUGFIX: Buffer overrun in “elf” module.
- BUGFIX: Buffer overrun in “dotnet” module.

* Sat Mar 16 2019 Michal Ambroz <rebus _AT seznam.cz> - 3.9.0-1
- bump to 3.9.0 release (#1680203)
- switch from python-sphinx to python3-sphinx for generating the documentation for fc31+
- should fix also #1660398 (CVE-2018-19974 CVE-2018-19975 CVE-2018-19976),
  but by design it might be always dangerous to run yara signatures compiled by 3rd party,
  so it is advised to re-compile yara rules instead
- BUGFIX: Denial of service when using "dex" module. Found by the Cisco Talos team. (upstream #1023, CVE-2019-5020)
- BUGFIX: Buffer overflow in "dotnet" module.
- BUGFIX: Regexp regression when using nested quantifiers {x,y} for certain values of x and y. (#1018)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Michal Ambroz <rebus _AT seznam.cz> - 3.8.1-1
- bump to 3.8.1 release (#1613093)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Michal Ambroz <rebus _AT seznam.cz> - 3.7.1-1
- bump to 3.7.1 release (#1534993)

* Wed Nov 15 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.7.0-1
- bump to 3.7.0 release (#1511921)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.6.3-1
- bump to 3.6.3 release - bugfix CVE-2017-11328

* Mon Jul 03 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.6.2-1
- bump to 3.6.2 release - bugfix CVE-2017-9304, CVE-2017-9465

* Wed May 24 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.6.0-1
- bump to 3.6.0 release
- update the androguard-yara with bugfixes

* Thu Apr 13 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-7
- Adding patch from pull request 627 until 3.5.1 is released
- https://patch-diff.githubusercontent.com/raw/VirusTotal/yara/pull/627.patch
- Fixes CVE-2016-10210 CVE-2016-10211 CVE-2017-5923 CVE-2017-5924

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-5
- import package to Fedora
- remove unnecessary .buildinfo tag from doc package

* Fri Aug 05 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-4
- package review - bugzilla #1362265
- cosmetics of the changelog
- using default spinx theme to remove the static fonts

* Fri Aug 05 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-3
- package review - bugzilla #1362265
- dropped Buildroot, pkgconfig, zlib-devel, defattr
- added buildrequires gcc
- change license back to ASL 2.0 only

* Thu Aug 04 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-2
- package review - bugzilla #1362265
- changed packaging of doc sub-package

* Thu Aug 04 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.5.0-1
- bump to new 3.5.0

* Wed Aug 03 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.4.0-6
- package review - bugzilla #1362265
- dropped dependency of python-tools

* Mon Aug 01 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.4.0-4
- compile with the androguard module

* Wed Jun 08 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.4.0-2
- jansson dependency >= 2.5

* Wed Jun 08 2016 Michal Ambroz <rebus _AT seznam.cz> - 3.4.0-1
- python3 stuff

* Mon Jun 22 2015 Michal Ambroz <rebus _AT seznam.cz> - 3.4.0-0.git20150618
- initial build for Fedora Project

## END: Generated by rpmautospec
