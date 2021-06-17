Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        14.17.0
Release:        1%{?dist}
License:        BSD and MIT and Public Domain and naist-2003
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
Patch0:         patch_tls_nodejs14.patch

BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python3
BuildRequires:  which
Requires:       coreutils >= 8.22
Requires:       openssl >= 1.0.1
Requires:       python3

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient. The Node.js package ecosystem, npm, is the largest ecosystem of open source libraries in the world.

%package        devel
Summary:        Development files node
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The nodejs-devel package contains libraries, header files and documentation
for developing applications that use nodejs.

%prep
%setup -q -n node-v%{version}
%patch0 -p1

%build
sh configure --prefix=%{_prefix} \
           --shared-openssl \
           --shared-zlib

make %{?_smp_mflags}

%install

make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
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
*   Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 14.17.0-1
-   Update to nodejs version 14.17.0
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.11.2-7
-   Added %%license line automatically
*   Mon May 04 2020 Paul Monson <paulmon@microsoft.com> 9.11.2-6
-   Add patch that enables building openssl without TLS versions less 1.2
*   Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 9.11.2-5
-   Remove toybox and only use coreutils for requires.
*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 9.11.2-4
-   License verified.
-   Removed "%%define sha1".
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 9.11.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 9.11.2-2
-   Added BuildRequires python2, which
*   Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.11.2-1
-   Updated to version 9.11.2
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.9.0-1
-   Updated to version 9.9.0
*   Wed Feb 14 2018 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
-   Updated to version 8.3.0
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-4
-   Remove BuildArch
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-3
-   Requires coreutils or toybox
*   Fri Jul 14 2017 Chang Lee <changlee@vmware.com> 7.7.4-2
-   Updated %check
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
-   Initial packaging for Photon
