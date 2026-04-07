# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# build order matters and multiple threads break it
%global _smp_mflags -j1

Name:           xmlrpc-c
Version:        1.60.04
Release:        4%{?dist}
Summary:        Lightweight RPC library based on XML and HTTP
# See doc/COPYING for details.
# The Python 1.5.2 license used by a few files is just BSD.
# Automatically converted from old format: BSD and MIT - review is highly recommended.
License:        LicenseRef-Callaway-BSD AND LicenseRef-Callaway-MIT
URL:            http://xmlrpc-c.sourceforge.net/
Source:         http://dl.sourceforge.net/sourceforge/xmlrpc-c/xmlrpc-c-%version.tgz

# Upstreamable patches
Patch102:       0002-Use-proper-datatypes-for-long-long.patch
Patch103:       0003-allow-30x-redirections.patch

BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel

%package c++
Summary:        C++ libraries for xmlrpc-c
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package client
Summary:        C client libraries for xmlrpc-c
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package client++
Summary:        C++ client libraries for xmlrpc-c
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-c++%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-client%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package devel
Summary:        Development files for xmlrpc-c based programs
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-c++%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-client%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-client++%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package apps
Summary:        Sample XML-RPC applications
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-c++%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-client%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-client++%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C.


%description c++
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C++.


%description client
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C
clients.

%description client++
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C++
clients.


%description devel
Static libraries and header files for writing XML-RPC applications in
C and C++.


%description apps
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.

This package contains some handy XML-RPC demo applications.


%prep
%autosetup -Sgit


%build
%configure
%make_build CFLAGS="%{optflags} -std=gnu17"
%make_build CFLAGS="%{optflags} -std=gnu17" -C tools


%install
%make_install
%make_install -C tools


%check
#%%make_test


%files
%license doc/COPYING lib/abyss/license.txt
%doc doc/CREDITS doc/HISTORY
%{_libdir}/libxmlrpc_xml*.so.*
%{_libdir}/libxmlrpc.so.*
%{_libdir}/libxmlrpc_openssl.so.*
%{_libdir}/libxmlrpc_util.so.*
%{_libdir}/libxmlrpc_abyss.so.*
%{_libdir}/libxmlrpc_server.so.*
%{_libdir}/libxmlrpc_server_abyss.so.*
%{_libdir}/libxmlrpc_server_cgi.so.*
%exclude %{_libdir}/libxmlrpc*.a


%files client
%{_libdir}/libxmlrpc_client.so.*

%files c++
%{_libdir}/libxmlrpc_cpp.so.*
%{_libdir}/libxmlrpc++.so.*
%{_libdir}/libxmlrpc_util++.so.*
%{_libdir}/libxmlrpc_abyss++.so.*
%{_libdir}/libxmlrpc_server++.so.*
%{_libdir}/libxmlrpc_server_abyss++.so.*
%{_libdir}/libxmlrpc_server_cgi++.so.*
%{_libdir}/libxmlrpc_packetsocket.so.*
%{_libdir}/libxmlrpc_server_pstream++.so.*

%files client++
%{_libdir}/libxmlrpc_client++.so.*

%files devel
%{_bindir}/xmlrpc-c-config
%{_includedir}/xmlrpc-c/
%{_includedir}/*.h
%{_libdir}/pkgconfig/xmlrpc*.pc
%{_libdir}/libxmlrpc*.so

%files apps
%{_bindir}/xmlrpc_parsecall
%{_bindir}/xmlrpc
%{_bindir}/xmlrpc_transport
%doc tools/xmlrpc_transport/xmlrpc_transport.html
%{_bindir}/xml-rpc-api2cpp
%{_mandir}/man1/xml-rpc-api2cpp.1*
%{_bindir}/xml-rpc-api2txt
%{_mandir}/man1/xml-rpc-api2txt.1*
%{_bindir}/xmlrpc_cpp_proxy
%{_bindir}/xmlrpc_pstream
%{_bindir}/xmlrpc_dumpserver

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.60.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 Jonathan Wright <jonathan@almalinux.org> - 1.60.04-3
- fix ftbfs on gcc15 rhbz#2341577

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.60.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Jonathan Wright <jonathan@almalinux.org> - 1.60.4-2
- Use global macro to override make smp_flags

* Thu Jan 02 2025 Jonathan Wright <jonathan@almalinux.org> - 1.60.4-1
- update to 1.60.4 rhbz#2334236
- re-enable builds against libxml2, no more bundled libexpat
- fixes rhbz#2310136
- fixes rhbz#2310146
- fixes rhbz#2310152

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.59.03-3
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.59.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 26 2024 Jonathan Wright <jonathan@almalinux.org> - 1.59.03-1
- update to 1.59.03 rhbz#2271506

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.59.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Jonathan Wright <jonathan@almalinux.org> - 1.59.02-1
- Update to 1.59.02 rhbz#1694044

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 06 2022 Jonathan Wright <jonathan@almalinux.org> - 1.51.08-1
- update to 1.51.08
- Remove meson build code, follow upstream build methods
- rhbz#2009098
- rhbz#2010890

* Tue Dec 06 2022 Jonathan Wright <jonathan@almalinux.org> - 1.51.0-17
- Merge PR from yselkowitz to fix meson builds

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.51.0-14
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.51.0-8
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Adam Williamson <awilliam@redhat.com> - 1.51.0-5
- Backport upstream fix for console spam with debug messages (#1541868)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.51.0-3
- Switch to %%ldconfig_scriptlets

* Wed Jan 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.51.0-2
- BuildRequire openssl by pkgconfig()

* Mon Jan 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.51.0-1
- Update to 1.51.0

* Sun Oct 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.49.02-2
- Fix Requires.private in xmlrpc_server++.pc

* Fri Sep 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.49.02-1
- Update to 1.49.02

* Fri Sep 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.48.0-8
- Add xmlrpc_client++.pc

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.48.0-5
- Fix underlinking issue causing FTBFS

* Mon Mar 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.48.0-4
- Build with openssl 1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 21 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.48.0-2
- Apply patches via git to preserve permissions

* Sun Dec 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.48.0-1
- Update to 1.48.0

* Tue Feb 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.32.5-1909.svn2451
- Add patch for conversion from int to usnigned char
- Resolves: rhbz#1308254

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.5-1909.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.5-1908.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.32.5-1907.svn2451
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.5-1906.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.5-1905.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.32.5-1904.svn2451
- Add patch to silence format-security compiler warning
- Resolves: rhbz#1037399

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.5-1903.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.32.5-1902.svn2451
- Add missing inter-package dependencies
- Rename fedora directory to build

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32.5-1901.svn2451
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec  9 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.32.5-1900.svn2451
- updated to 1.32.5

* Sun Oct 21 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.32.2-1900.svn2434
- updated to 1.32.2

* Sat Oct  6 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.32.1-1900.svn2413
- updated to 1.32.1

* Sun Aug 26 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.31.4-1900.svn2386
- updated to 1.31.4

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31.0-1801.svn2365
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  1 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.31.0-1800.svn2365
- updated to 1.31.0

* Wed Jun  6 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.30.6-1800.svn2328
- updated to 1.30.6

* Sat May 26 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.30.5-1800.svn2324
- updated to 1.30.5 (IPv6 server fixes)

* Sat May 12 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.30.4-1800.svn2318
- updated to 1.30.4

* Thu Apr  5 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.30.1-1800.svn2298
- updated to 1.30.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.0-1701.svn2233
- Rebuilt for c++ ABI breakage

* Wed Jan  4 2012 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.29.0-1700.svn2233
- updated to 1.29.0

* Mon Oct  3 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.28.1-1700.svn2203
- updated to 1.28.1

* Mon Oct  3 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.27.5-1701.svn2185
- fixed error handling when transfering too large files (#741980)

* Sat Aug 27 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.27.5-1700.svn2185
- updated to 1.27.5

* Sun Aug  7 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.27.4-1700.svn2171
- updated to 1.27.4

* Sun Aug  7 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.27.3-1700.svn2145
- updated to 1.27.3

* Mon Jun 27 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.27.0-1600.svn2145
- updated to 1.27.0
- made it build with recent curl

* Mon Jun 13 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.26.3-1600.svn2134
- updated to 1.26.3
- removed default-constructor patch; issue is solved upstream

* Sat Apr  2 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.26.0-1600.svn2188
- updated to 1.26.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.1-1501.svn2077
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.25.1-1500.svn2077
- updated to 1.25.1

* Thu Dec 30 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.25.0-1500.svn2074
- updated to 1.25.0

* Sun Nov  7 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.24.4-1500.svn2042
- updated to 1.24.4

* Sat Oct  9 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.24.1-1500.svn1987
- updated to 1.24.1
- set -Wno-uninitialized CFLAGS; code contains lot of constructs
  triggering this warning and the 'int a=a' defeaters have been
  removed in this version

* Fri Aug 27 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.23.02-1500.svn1968
- updated to 1.23.02 (note: this breaks C++ ABI)
- added vasprintf patch

* Thu Jul 29 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.23.01-1400.svn1958
- updated to 1.23.01
- added patch to make curl follow HTTP POST 301 redirects (#618504)

* Sun Apr 18 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.22.01-1400.svn1907
- updated to 1.22.01 (svn 1907)

* Tue Feb 23 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.21.00-1401.1851
- require the various subpackages explicitly for -devel; the ld linker
  scripts broke rpm's autodetection (#567400)
- removed -devel Requires: which are covered by pkgconfig autodeps
- added %%{?_isa} annotations

* Sun Feb 21 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.21.00-1400.1851
- made linker scripts more 'ldconfig' friendly

* Mon Feb 15 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.21.00-1301.1851
- replaced .so symlinks by linker scripts which add all implicit
  dependencies in AS_NEEDED() commands (#564607, #565577)

* Thu Jan 14 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.21.00-1300.1851
- updated to 1.21.00 (rev 1851)
- removed curl-trace patch as applied upstream
- rediffed patches

* Sat Nov 21 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.20.3-1.1841
- updated to rev1841
- rediffed patches
- added patch to fix handling of wrong certificates (Nikola Pajkovsky)
- added support for $XMLRPC_TRACE_CURL env (John Dennis)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.6-3.1582
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.6-2.1582
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.16.6-1.1582
- updated to 1.16.6; rediffed patches
- fixed client headers (bug #475887)

* Sat Nov 15 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.16.4.1567-2
- updated to 1.16.4
- rediffed/updated patches
- splitted some subpackages (c++, client) out of main package as they
  introduce additional dependencies (c++, curl)

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14.8-2
- fix license tag

* Sat Jun 21 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.14.8-1
- updated to 1.14.8

* Sun May 25 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.14.6-1
- updated to 1.14.6

* Sat Apr 12 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.14.2-1
- updated to 1.14.2
- rediffed patches
- added patch to fix broken usage of 'long long' datatype

* Mon Mar 17 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.13.8-2
- fixed cmake quoting so that pkgconfig files get correct version number
- fixed handling of 'server-util' and '--cflags' within xmlrpc-c-config

* Sun Mar 16 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.13.8-1
- updated to 1.13.8
- removed some patches which were applied upstream

* Tue Feb 26 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.13.07-2
- moved to advanced branched; rediffed/updated existing cmake patch
  and fixed other compilation issues (#369841)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.06.23-2
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.23-1
- use correct pkg-config script for 'xmlrpc-config abyss-server'
  output (#355411)
- updated to 1.06.23 (#355411)

* Tue Sep  4 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.18-1
- updated to 1.06.18

* Thu Aug 16 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.17-1
- updated to 1.06.17

* Sun Jul 22 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.16-1
- updated to 1.06.16

* Thu Jun 14 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.14-1
- updated to 1.06.14

* Sun Apr  1 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.11-2
- rediffed cmake patch against current version
- made the xmlrpc-c-config compatible to the upstream version
- added compatibility symlinks for some header files (thx to Robert de
  Vries for reporting these two issues)

* Sat Mar 17 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.11-1
- updated to 1.06.11

* Sat Feb  3 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.09-1
- updated to 1.06.09
- removed -typo patch since applied upstream

* Mon Nov  6 2006 Jindrich Novy <jnovy@redhat.com> - 1.06.05-3
- rebuild against the new curl

* Mon Oct  2 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.05-2
- updated cmake patch
- strip installed libraries

* Wed Sep 20 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.05-1
- updated to 1.06.05
- merged + updated patches

* Sat Sep 16 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.06.04-1
- updated to 1.06.04
- patched the broken buildsystem
- disabled libwww backend explicitely

* Sun Jun  4 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.05-1
- updated to 1.05
- updated patches

* Sat Feb 18 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.04-2
- rebuilt for FC5

* Sun Dec 18 2005 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.04-1
- added libxml2-devel and openssl-devel Requires: for the -devel
  subpackage
- ship doc/* instead of doc
- initial Fedora Extras package (review 175840)

* Thu Dec 15 2005 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.04-0.1
- disabled w3c-libwww because it does not exist anymore in FC5 and
  seems to be unmaintained upstream
- added missing libxml2-devel
- cleaned up list of %%doc files
- fixed gcc4.1 build issues
- removed static libraries when there exists a corresponding dynamic one

* Tue Aug  2 2005 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 1.03.02-1
- Initial build.
