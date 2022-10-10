Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        14.20.1
Release:        2%{?dist}
License:        BSD and MIT and Public Domain and naist-2003
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/nodejs/node
# !!!! Nodejs code has a vendored version of OpenSSL code that must be removed from source tarball 
# !!!! because it contains patented algorithms.
# !!!  => use clean-source-tarball.sh script to create a clean and reproducible source tarball.
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
Patch0:         patch_tls_nodejs14.patch
Patch1:         remove_unsupported_tlsv13_ciphers.patch
BuildRequires:  coreutils >= 8.22
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  python3
BuildRequires:  which
Requires:       coreutils >= 8.22
Requires:       openssl >= 1.1.1
Requires:       python3

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.
Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient.
The Node.js package ecosystem, npm, is the largest ecosystem of open source libraries in the world.

%package        devel
Summary:        Development files node
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The nodejs-devel package contains libraries, header files and documentation
for developing applications that use nodejs.

%prep
%autosetup -p1 -n node-v%{version}

%build
python3 configure.py \
  --prefix=%{_prefix} \
  --shared-openssl \
  --shared-zlib \
  --openssl-use-def-ca-store
%make_build

%install
%make_install
rm -fr %{buildroot}%{_libdir}/dtrace/  # No systemtap support.
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
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/*
%{_libdir}/node_modules/*
%{_mandir}/man*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/*
%{_datadir}/systemtap/tapset/node.stp

%changelog
* Mon Oct 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 14.20.1-2
- Change src tarball generation mechanism so it is usable by autoupgrade tools

* Thu Oct 06 2022 Jon Slobodzian <joslobo@microsoft.com> - 14.20.1-1
- Upgrade to 14.20.1 to fix CVE-2022-32213, CVE-2022-32214, and CVE-2022-35256
- Note the previous version was believed to be fixed for 32213 and 32214 but the
- v14.20.1 nodejs release notes suggest that those two were resolved in this update
- (See https://nodejs.org/en/blog/release/v14.20.1/)

* Wed Jul 27 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 14.20.0-1
- Update to v14.20.0 to fix CVE-2022-32213, CVE-2022-32214, CVE-2022-32215.

* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 14.18.3-1
- Update to version 14.18.3 to fix CVE-2021-44531.

* Thu Nov 18 2021 Thomas Crain <thcrain@microsoft.com> - 14.18.1-1
- Update to version 14.18.1 to fix CVE-2021-22959, CVE-2021-22960, CVE-2021-37701,
  CVE-2021-37712, CVE-2021-37713, CVE-2021-39134, CVE-2021-39135
- Add patch to remove problematic cipher from default list
- Add config flag to use OpenSSL cert store instead of built-in Mozilla certs
- Add script to remove vendored OpenSSL tree from source tarball
- Update required OpenSSL version to 1.1.1
- Use python configure script directly
- Lint spec

* Mon Aug 30 2021 Andrew Phelps <anphel@microsoft.com> - 14.17.5-1
- Update to version 14.17.5 to fix CVE-2021-22931

* Mon Jul 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 14.17.2-1
- Update to version 14.17.2 to fix CVE-2021-22918

* Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 14.17.0-1
- Update to nodejs version 14.17.0

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.11.2-7
- Added %%license line automatically

* Mon May 04 2020 Paul Monson <paulmon@microsoft.com> - 9.11.2-6
- Add patch that enables building openssl without TLS versions less 1.2

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 9.11.2-5
- Remove toybox and only use coreutils for requires.

* Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.11.2-4
- License verified.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 9.11.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 9.11.2-2
- Added BuildRequires python2, which

* Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 9.11.2-1
- Updated to version 9.11.2

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 9.9.0-1
- Updated to version 9.9.0

* Wed Feb 14 2018 Xiaolin Li <xiaolinl@vmware.com> - 8.3.0-1
- Updated to version 8.3.0

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.7.4-4
- Remove BuildArch

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 7.7.4-3
- Requires coreutils or toybox

* Fri Jul 14 2017 Chang Lee <changlee@vmware.com> - 7.7.4-2
- Updated %check

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 7.7.4-1
- Initial packaging for Photon
