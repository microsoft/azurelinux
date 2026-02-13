# Retrieved from 'deps/npm/package.json' inside the sources tarball.
%define npm_version 11.6.2

%global nodejs_datadir %{_datarootdir}/nodejs

# ICU - from tools/icu/current_ver.dep
%global icu_major 77
%global icu_minor 1
%global icu_version %{icu_major}.%{icu_minor}

%global icudatadir %{nodejs_datadir}/icudata
%{!?little_endian: %global little_endian %(%{python3} -c "import sys;print (0 if sys.byteorder=='big' else 1)")}

Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs24
# WARNINGS: MUST check and update the 'npm_version' macro for every version update of this package.
#           The version of NPM can be found inside the sources under 'deps/npm/package.json'.
Version:        24.13.0
Release:        3%{?dist}
License:        BSD AND MIT AND Public Domain AND NAIST-2003 AND Artistic-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/nodejs/node
# !!!! Nodejs code has a vendored version of OpenSSL code that must be removed from source tarball
# !!!! because it contains patented algorithms.
# !!!  => use generate_source_tarball.sh script to create a clean and reproducible source tarball.
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
Source1:        https://github.com/unicode-org/icu/releases/download/release-%{icu_major}-%{icu_minor}/icu4c-%{icu_major}_%{icu_minor}-data-bin-b.zip
Source2:        https://github.com/unicode-org/icu/releases/download/release-%{icu_major}-%{icu_minor}/icu4c-%{icu_major}_%{icu_minor}-data-bin-l.zip
Source3:        btest402.js
Patch0:         disable-tlsv1-tlsv1-1.patch
Patch1:         CVE-2019-10906.patch
Patch2:         CVE-2024-22195.patch
Patch3:         CVE-2020-28493.patch
Patch4:         CVE-2024-34064.patch
Patch5:         CVE-2025-27516.patch
Patch6:         CVE-2025-69418.patch
BuildRequires:  brotli-devel
BuildRequires:  c-ares-devel
BuildRequires:  coreutils >= 8.22
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ninja-build
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  python3
BuildRequires:  which
BuildRequires:  zlib-devel
Requires:       brotli
Requires:       c-ares
Requires:       coreutils >= 8.22
Requires:       openssl >= 1.1.1
Provides:       nodejs24
# Until we make this as formal nodejs release, lets make it conflicting with nodejs20 
# This will uninstall nodejs20 during installation of nodejs24
Conflicts:      nodejs

Recommends: nodejs-full-i18n = %{version}-%{release}
Provides: bundled(icu) = %{icu_version}

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.
Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient.
The Node.js package ecosystem, npm, is the largest ecosystem of open source libraries in the world.

%package        devel
Summary:        Development files node
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
Requires:       brotli-devel
Requires:       openssl-devel >= 1.1.1
Requires:       zlib-devel

%description    devel
The nodejs-devel package contains libraries, header files and documentation
for developing applications that use nodejs.

%package full-i18n
Summary: Non-English locale data for Node.js
Requires: %{name} = %{version}-%{release}

%description full-i18n
Optional data files to provide full-icu support for Node.js. Remove this
package to save space if non-English locales are not needed.

%package        npm
Summary:        Node.js Package Manager
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
Provides:       nodejs24-npm = %{version}-%{release}
Obsoletes:      nodejs24-npm < %{version}-%{release}
Conflicts:      npm

%description npm
npm is a package manager for node.js. You can use it to install and publish
your node programs. It manages dependencies and does other cool stuff.

%prep
%autosetup -p1 -n node-v%{version}

%build
# remove unsupported TLSv1.3 cipher:
#    Mariner's OpenSSL configuration does not allow for this TLSv1.3
#    cipher. OpenSSL does not like being asked to use TLSv1.3 ciphers
#    it doesn't support (despite being fine processing similar cipher
#    requests for TLS < 1.3). This cipher's presence in the default
#    cipher list causes failures when initializing secure contexts
#    in the context of Node's TLS library.
sed -i '/TLS_CHACHA20_POLY1305_SHA256/d' ./src/node_constants.h

# remove brotli and zlib source code from deps folder
# keep the .gyp and .gypi files that are still used during configuration
find deps/zlib -name *.[ch] -delete
find deps/brotli -name *.[ch] -delete

python3 configure.py \
  --prefix=%{_prefix} \
  --ninja \
  --shared-openssl \
  --shared-zlib \
  --shared-brotli \
  --with-intl=small-icu \
  --with-icu-source=deps/icu-small \
  --with-icu-default-data-dir=%{icudatadir} \
  --openssl-use-def-ca-store \
  --shared-cares

JOBS=%{_smp_build_ncpus} make %{?_smp_mflags} V=0

%install

make %{?_smp_mflags} install DESTDIR=%{buildroot}
install -m 755 -d %{buildroot}%{_libdir}/node_modules/
install -m 755 -d %{buildroot}%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

# Install the full-icu data files
mkdir -p %{buildroot}%{icudatadir}
%if 0%{?little_endian}
unzip -d %{buildroot}%{icudatadir} %{SOURCE2} icudt%{icu_major}l.dat
%else
unzip -d %{buildroot}%{icudatadir} %{SOURCE1} icudt%{icu_major}b.dat
%endif

%check
# Make sure i18n support is working
NODE_PATH=%{buildroot}%{_prefix}/lib/node_modules:%{buildroot}%{_prefix}/lib/node_modules/npm/node_modules LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node --icu-data-dir=%{buildroot}%{icudatadir} %{SOURCE3}

make cctest

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/node
%dir %{_prefix}/lib/node_modules
%{_mandir}/man*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/*

%files full-i18n
%dir %{icudatadir}
%{icudatadir}/icudt%{icu_major}*.dat

%files npm
%defattr(-,root,root)
%{_bindir}/npm
%{_bindir}/npx
%{_bindir}/corepack
%{_prefix}/lib/node_modules/*

%changelog
* Tue Feb 10 2026 Sandeep Karambelkar <skarambelkar@microsoft.com> - 24.13.0-2
- Add conflicts for legacy npm package
- Update provided capability from npm to nodejs24-npm
* Fri Feb 13 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 24.13.0-3
- Patch for CVE-2025-69418
* Tue Dec 23 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 24.13.0-1
- Upgrade to 24.13.0
- Add support for passing runtime internationalization data

* Fri Nov 07 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 20.14.0-10
- Patch for CVE-2025-5222

* Tue May 27 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 20.14.0-9
- Patch CVE-2025-23165, CVE-2025-23166

* Wed May 21 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 20.14.0-8
- Patch CVE-2025-47279

* Mon Mar 10 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 20.14.0-7
- Patch CVE-2025-27516

* Wed Feb 12 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 20.14.0-6
- Patch CVE-2020-28493
- Patch CVE-2024-34064

* Tue Feb 11 2025 Kanishk Bansal <kanbansal@microsoft.com> - 20.14.0-5
- Patch CVE-2025-22150, CVE-2025-23085, CVE-2024-22020, CVE-2024-22195

* Mon Jan 27 2025 Sumedh Sharma <sumsharma@microsoft.com> - 20.14.0-4
- Patch CVE-2025-23083

* Tue Nov 19 2024 Bala <balakumaran.kannan@microsoft.com> - 20.14.0-3
- Patch CVE-2024-21538

* Thu Sep 19 2024 Suresh Thelkar <sthelkar@microsoft.com> - 20.14.0-2
- Patch CVE-2019-10906

* Fri Jun 07 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 20.14.0-1
- Upgrade to 20.14.0 to address CVEs

* Thu Jun 06 2024 Riken Maharjan <rmaharjan@microsoft.com> - 20.10.0-3
- Separate npm from node using Fedora 50 (LICENSE: MIT)

* Tue May 21 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 20.10.0-2
- Bump release to build with new libuv to fix CVE-2024-24806

* Wed Jan 31 2024 Saul Paredes <saulparedes@microsoft.com> - 20.10.0-1
- Upgrade to nodejs to 20.10.0 and npm to 10.2.3

* Wed Sep 06 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 16.20.2-2
- Patch CVE-2023-35945

* Wed Sep 06 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 16.20.2-1
- Patch CVE-2023-32002 CVE-2023-32006 CVE-2023-32559

* Wed Jul 12 2023 Olivia Crain <oliviacrain@microsoft.com> - 16.20.1-2
- Backport upstream patches to fix CVE-2022-25883

* Wed Jun 28 2023 David Steele <davidsteele@microsoft.com> - 16.20.1-1
- Upgrade to nodejs to 16.20.1 and npm to 8.19.4

* Tue May 30 2023 Dallas Delaney <dadelan@microsoft.com> - 16.19.1-2
- Fix CVE-2023-32067, CVE-2023-31130, CVE-2023-31147 by using system c-ares

* Wed Mar 01 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 16.19.1-1
- Auto-upgrade to 16.19.1 - to fix CVE-2023-23936
- Update npm version to 8.19.3 to reflect the actual version of npm bundled with v16.19.1

* Tue Dec 13 2022 Andrew Phelps <anphel@microsoft.com> - 16.18.1-2
- Update license to reference Artistic 2.0

* Fri Dec 09 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 16.18.1-1
- Auto-upgrade to 16.18.1 - CVE-2022-43548

* Tue Oct 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 16.17.1-2
- Change npm_version to 8.15.0 to reflect the actual version of npm bundled with v16.17.1

* Mon Oct 24 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 16.17.1-1
- Upgrade to 16.17.1

* Thu Aug 18 2022 Cameron Baird <cameronbaird@microsoft.com> - 16.16.0-2
- Change npm_version to 8.11.0 to reflect the actual version of npm bundled with v16.16.0

* Tue Aug 02 2022 Cameron Baird <cameronbaird@microsoft.com> - 16.16.0-1
- Update to v16.16.0 (security update) to resolve CVE-2022-32213, CVE-2022-32214, CVE-2022-32215

* Mon May 16 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 16.14.2-2
- Remove python3 as a runtime dependency as it is not needed during runtime.

* Tue Apr 19 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 16.14.2-1
- Update to 16.14.2.

* Thu Feb 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 16.14.0-1
- Upgrade to 16.14.0.

* Thu Nov 18 2021 Thomas Crain <thcrain@microsoft.com> - 14.18.1-1
- Update to version 14.18.1 to fix CVE-2021-22959, CVE-2021-22960, CVE-2021-37701,
    CVE-2021-37712, CVE-2021-37713, CVE-2021-39134, CVE-2021-39135
- Add patch to remove problematic cipher from default list
- Add config flag to use OpenSSL cert store instead of built-in Mozilla certs
- Add script to remove vendored OpenSSL tree from source tarball
- Update required OpenSSL version to 1.1.1
- Use python configure script directly
- Lint spec

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 14.17.2-2
- Adding 'Provides' for 'npm'.

* Mon Jul 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 14.17.2-1
- Update to version 14.17.2 to fix CVE-2021-22918

* Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 14.17.0-1
- Update to nodejs version 14.17.0

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.11.2-7
- Added %%license line automatically

* Mon May 04 2020 Paul Monson <paulmon@microsoft.com> 9.11.2-6
- Add patch that enables building openssl without TLS versions less 1.2

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 9.11.2-5
- Remove toybox and only use coreutils for requires.

* Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 9.11.2-4
- License verified.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 9.11.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 9.11.2-2
- Added BuildRequires python2, which

* Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.11.2-1
- Updated to version 9.11.2

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.9.0-1
- Updated to version 9.9.0

* Wed Feb 14 2018 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
- Updated to version 8.3.0

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-4
- Remove BuildArch

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-3
- Requires coreutils or toybox

* Fri Jul 14 2017 Chang Lee <changlee@vmware.com> 7.7.4-2
- Updated %check

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
- Initial packaging for Photon
