Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        8.17.0
Release:        1%{?dist}
License:        BSD and MIT and Public Domain and naist-2003
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
Patch0:         patch_tls_nodejs8.patch

BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python2
BuildRequires:  which
Requires:       coreutils >= 8.22
Requires:       openssl >= 1.0.1
Requires:       python2

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
%{_docdir}/node/lldb_commands.py
%{_docdir}/node/lldbinit
%{_docdir}/node/gdbinit
%{_datadir}/systemtap/tapset/node.stp

%changelog
*   Mon Jun 07 2021 Henry Beberman <henry.beberman@microsoft.com> - 8.17.0-1
-   Update to version 8.17.0
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.11.4-7
-   Added %%license line automatically
*   Mon May 04 2020 Paul Monson <paulmon@microsoft.com> 8.11.4-6
-   Add patch that enables building openssl without TLS versions less 1.2
*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 8.11.4-5
-   License verified.
-   Fixed "Source0" tag.
-   Removed "%%define sha1".
*   Wed Apr 08 2020 Nicolas Ontiveros <niontive@microsoft.com> 8.11.4-4
-   Remove toybox and only use core-utils in requires. 
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.11.4-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 8.11.4-2
-   Added BuildRequires python2, which
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 8.11.4-1
-   Updated to version 8.11.4 to fix CVE-2018-7161 and CVE-2018-7167.
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
