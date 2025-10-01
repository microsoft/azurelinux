# Retrieved from 'deps/npm/package.json' inside the sources tarball.
%define npm_version 10.2.3

Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs20
# WARNINGS: MUST check and update the 'npm_version' macro for every version update of this package.
#           The version of NPM can be found inside the sources under 'deps/npm/package.json'.
Version:        20.10.0
Release:        2%{?dist}
License:        BSD and MIT and Public Domain and NAIST-2003 and Artistic-2.0
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/nodejs/node
# !!!! Nodejs code has a vendored version of OpenSSL code that must be removed from source tarball 
# !!!! because it contains patented algorithms.
# !!!  => use clean-source-tarball.sh script to create a clean and reproducible source tarball.
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
Patch0:         disable-tlsv1-tlsv1-1.patch

BuildRequires:  brotli-devel
BuildRequires:  coreutils >= 8.22
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ninja-build
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  python3
BuildRequires:  which
BuildRequires:  zlib-devel
BuildRequires:  c-ares-devel

Requires:       brotli
Requires:       coreutils >= 8.22
Requires:       openssl >= 1.1.1

Provides:       npm = %{npm_version}.%{version}-%{release}

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
  --without-dtrace \
  --openssl-use-def-ca-store \
  --shared-cares

JOBS=4 make %{?_smp_mflags} V=0

%install

make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
install -m 755 -d %{buildroot}%{_libdir}/node_modules/
install -m 755 -d %{buildroot}%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

%check
make cctest

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/node_modules/*
%{_mandir}/man*/*
%doc CHANGELOG.md LICENSE README.md

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/*
%{_datadir}/systemtap/tapset/node.stp

%changelog
* Mon Dec 18 2023 Christopher Miller <chrmiller@microsoft.com> - 20.10.0
- Upgrade to 20.10.0

* Thu Oct 19 2023 Dan Streetman <ddstreet@ieee.org> - 18.18.2-2
- Re-enable building debuginfo. We can just ignore the dirs conflict failure in the pipelines! :)

* Wed Oct 18 2023 Dan Streetman <ddstreet@ieee.org> - 18.18.2-1
- Update to 18.18.2 to fix CVE-2023-44487

* Wed Sep 06 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 18.17.1-2
- Patch CVE-2023-35945

* Wed Sep 06 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 18.17.1-1
- Patch CVE-2023-32002 CVE-2023-32006 CVE-2023-32559
- Refresh patch CVE-2022-25883-v18

* Tue Jul 11 2023 Muhammad Falak <mwani@microsoft.com> - 18.16.0-3
- Patch CVE-2022-25883

* Tue May 30 2023 Dallas Delaney <dadelan@microsoft.com> - 18.16.0-2
- Fix CVE-2023-32067, CVE-2023-31130, CVE-2023-31147 by using system c-ares

* Wed Apr 12 2023 Riken Maharjan <rmaharjan@microsoft.com> - 18.16.0-1
- Upgrade to 18.16.0

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
