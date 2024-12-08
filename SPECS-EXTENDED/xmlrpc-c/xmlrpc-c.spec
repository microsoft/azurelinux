# Upstream libxml2 backend is completely broken since 2015 https://sourceforge.net/p/xmlrpc-c/patches/49/
%bcond_with libxml2
 
Name:           xmlrpc-c
Version:        1.59.03
Release:        1%{?dist}
Summary:        Lightweight RPC library based on XML and HTTP
# See doc/COPYING for details.
# The Python 1.5.2 license used by a few files is just BSD.
# Automatically converted from old format: BSD and MIT - review is highly recommended.
License:        LicenseRef-Callaway-BSD AND LicenseRef-Callaway-MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://xmlrpc-c.sourceforge.net/
Source: https://sourceforge.net/projects/xmlrpc-c/files/Xmlrpc-c%20Super%20Stable/%{version}/xmlrpc-c-%{version}.tgz
# Upstreamable patches
Patch102:       0002-Use-proper-datatypes-for-long-long.patch
Patch103:       0003-allow-30x-redirections.patch
 
BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if %{with libxml2}
BuildRequires:  pkgconfig(libxml-2.0)
%else
# upstream has its own fork of expat
Provides:       bundled(expat)
%endif
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
%make_build
# build order matters and multiple threads break it
%make_build -j1 -C tools
 
 
%install
%make_install
%make_install -C tools
 
 
%check
#%%make_test
 
 
%files
%license doc/COPYING lib/abyss/license.txt
%doc doc/CREDITS doc/HISTORY
%if ! %{with libxml2}
%{_libdir}/libxmlrpc_xml*.so.*
%endif
%{_libdir}/libxmlrpc.so.*
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
* Tue Nov 12 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.59.03-1
- Update to version 1.59.03

* Wed Nov 16 2022 Suresh Thelkar <sthelkar@microsoft.com> - 1.54.06-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Added upstream patch to use va_args properly
- Removed build dependency for makeinfo
- Added main package as the spec taken was directly starting from devel
- License verified

* Sat Oct 29 2022 Dirk Müller <dmueller@suse.com>
- update to 1.54.06:
  * Abyss HTTP server: Fix memory corruption in processing of "authorization"
    header field. Broken in Xmlrpc-c 1.41

* Mon Aug  8 2022 Dirk Müller <dmueller@suse.com>
- update to 1.54.05:
  * Fix handling of error on pipe used to interrupt the wait for a client connection.
  * Build of client libraries: fix failure to find Curl stuff
  * fix bug: wild memory reference when server times out waiting for request header
  * fix bug: won't compile with --enable-libxml2
  * fix bug: ignores LDFLAGS_FOR_BUILD, LDFLAGS_PERSONAL, and LDFLAGS_PTHREAD
    when building the build tool Gennmtab
  * Fix bug: 'toValue' won't compile for vector of vectors or map of vectors. Thanks Yang Bo .
  * Fix tiny memory leak in virtually impossible low memory situation.
  * Build: fix missing xmlrpc-c/config.h include file in separate build tree build

* Mon May 31 2021 Dirk Müller <dmueller@suse.com>
- update to 1.51.07:
  * fix bug: wild memory reference when server times out waiting for request header.

* Thu Aug 20 2020 Dirk Mueller <dmueller@suse.com>
- update to 1.51.06:
  * Build: fix bug: won't compile with --enable-libxml2, introduced with Release 1.44 (December 2015).
  * Remove trace statements accidentally added in Release 1.51.00. (Released December 2017, promoted to Super Stable March 2019).
  * Build: fix bug: ignores LDFLAGS_FOR_BUILD, LDFLAGS_PERSONAL, and LDFLAGS_PTHREAD when building the build tool Gennmtab.
  * Fix tiny memory leak in virtually impossible low memory situation.
  * Fix bug: 'toValue' won't compile for vector of vectors or map of vectors. Thanks Yang Bo .
  * Build: fix missing xmlrpc-c/config.h include file in separate build tree build. Thanks Philip Belemezov <philip@belemezov.net>.
  * Build: Add --disable-abyss-openssl for build environments that appear to have Openssl but don't really. (A Pkg-config design flaw makes that happen sometimes - you can't control what directories it searches for .pc files).
  * Windows build: add Visual Studio 2017 project files, fix various things broken for Windows in recent updates. Thanks to Maksym Veremeyenko .
  * Disable 10M restriction on document size in Libxml2 XML parser.
  * Build: Recognize additional Linux "host OS" environments. E.g. "linux-uclibc".
  * Build: replace BUILDTOOL_CC and BUILDTOOL_CCLD with more conventional CC_FOR_BUILD. Add CFLAGS_FOR_BUILD, LDFLAGS_FOR_BUILD.
  * Build: Don't attempt to build C++ internal utility module cmdline_parser_cpp if we aren't building the C++ libraries. In that case, 1) it isn't needed, and 2) the environment probably is incapable of compiling C++.
  * Build: Use AC_CHECK_TOOL to determine 'ar' command and AC_PROG_RANLIB to determine 'ranlib' command to use.
  * Build: fix compile failure in build for a system that does not have Unicode wide characters (wchar_t).
  * Packet stream client: Add option to throw a BrokenConnEx exception when transport fails because the server hung up or network broke, instead of throwing error.
  * Add ServerAbyss::getListenName method, ChanSwitchUnixGetListeName: ability to find out on what port your server is listening.
  * Packet stream server ('serverPstreamConn'): fix bug: runOnce() fails with indication that it was interrupted when the server hangs up. Always broken (interruptible RunOnce() was new in Xmlrpc-c 1.14 (March 2008).
  * Fix compile failure with old OpenSSL that doesn't have SSL_ERROR_WANT_ACCEPT. Introduced in Xmlrpc-c 1.45.
  * Add SSL/TLS capability via OpenSSL to Abyss server.
  * Fix xmlrpc_mem_block accidentally made private in 1.44.
  * Build: Remove example and test program usage of XML parser facility (<xmlrpc-c/xmlparser.h>), which was made private in 1.44, so the examples and tools no longer build.
  * C++: Add 'toValue' and 'fromValue' for 64-bit integer (xmlrpc_c::value_i8).
  * Memory block utility: Remove xmlrpc_mem_block_init and xmlrpc_mem_block_clean. These complicate forward compatibility and probably were never used. xmlrpc_mem_block_new and xmlrpc_mem_block_free remain to fulfill the same purpose.
  * Remove XML parser (<xmlrpc-c/xmlparser.h>) from external API. This is not specific to XML-RPC, so has no business being a service of Xmlrpc-c. It is just an abstraction to allow us to use various XML parsing libraries (to wit, Expat and Libxml2). We don't think it was ever used externally.
  * Add xmlrpc_value_new(): deep copy of xmlrpc_value.
  * Abyss C++: Add 'terminate' and 'resetTerminate' methods, analogous to C Abyss 'ServerTerminate' and 'ServerResetTerminate'.
  * Fix bug: infinite recursion if you try to format a floating point value that was created from something other than a finite number. Creation of a floating point XML-RPC value from something other than a number now fails. Introduced in Xmlrpc-c 1.15 (June 2008).
  * Curl client: fix garbage in message where explanation from Curl library belongs. Always there, with some Curl libraries.
  * Curl client: fix instantaneous timeout with some Curl libraries. Introduced in Xmlrpc-c 1.41 (March 2015).
  * Curl client: fix 'connect_timeout' transport parameter interpreted as 'timeout'. Always broken ('connect_timeout' was new in Xmlrpc-c 1.41 (March 2015)).
  * AbysssServer: add 'Session::headerValue' and 'Session::getHeaderValue'.
  * Fix crash in 'xmlrpc' program under most circumstances. Broken in Xmlrpc-c 1.40 (December 2014).
  * Packet socket: fix missing parenthesis in error message. Broken in Xmlrpc-c 1.25 (December 2010).
  * Fix crash: multithreaded client program that uses the Curl XML transport and does not specify a Curl timeout transport parameter crashes because of signal use inside the Curl library, unless the Curl library is one that does DNS lookups with the ARES library.
  * Make a client that uses the Curl XML transport and does not specify a Curl timeout transport parameter wait indefinitely for a DNS lookup, or at least until the OS DNS lookup service gives up, unless the Curl library is one that does DNS lookups with the ARES library. In previous releases, the RPC failed after waiting 5 minutes. This was not intended as an enhancement, but rather is a side effect of fixing the crash described above. But it also adds consistency, since the wait for the DNS lookup was always indefinite, ironically, in the case that the program specified timeout.
  * Add connect_timeout curl transport parameter.
  * Packet stream socket: fix: sends corrupted packet when the packet contains an ESC character. Always broken. (packet stream sockets were new in Xmlrpc-c 1.11 - June 2007).
  * Add XMLRPC_TRACE_PACKETSOCKET environment variable: a means of tracing communication at the packet socket level.
  * Fix AbyssServer::readRequestBody for chunked bodies. Always broken (AbyssServer was new in Netpbm 1.39 (September 2014).
- remove xmlrpc-c-no_return_nonvoid.patch (upstream)

* Fri Mar 24 2017 mpluskal@suse.com
- Update to version 1.39.12:
  * For full list of changes see:
    http://xmlrpc-c.sourceforge.net/change_super_stable.html
- Drop upstreamed narrowing.patch
- Add xmlrpc-c-no_return_nonvoid.patch

* Wed Jul 27 2016 schwab@suse.de
- narrowing.patch: fix invalid narrowing conversion

* Tue Nov 17 2015 mpluskal@suse.com
- Update to 1.33.18
  * Fix bug: infinite recursion if you try to format a floating
  point value that was created from something other than a
  finite number. Creation of a floating point XML-RPC value from
  something other than a number now fails.

* Mon Apr 20 2015 mpluskal@suse.com
- Update to 1.33.17
  * Build: fix a "recompile with -fPIC" failure in parallel make.

* Mon Mar  9 2015 mpluskal@suse.com
- Update dependencies
- Enable checks

* Sun Mar  8 2015 mpluskal@suse.com
- Cleanup spec file with spec-cleaner
- Use url for source
- Update to 1.33.16
  * Packet stream socket: fix: sends corrupted packet when the
    packet contains an ESC character. Always broken. (packet
    stream sockets were new in Xmlrpc-c 1.11 - June 2007).
  * Build: fix 'make distclean' so it doesn't leave src/cpp/srcdir
    and src/cpp/blddir.
- Changes for 1.33.15
  * Build: fix 'make distclean' so it doesn't leave src/cpp/srcdir
    and src/cpp/blddir.

* Mon Nov 25 2013 jengelh@inai.de
- Update to new upstream release 1.33
  * Abyss XML-RPC server: Implement HTTP access control and the
  OPTIONS method
  * Change strategy for overallocating memory - grow blocks no more
  than a megabyte at a time

* Sat Jun  1 2013 asterios.dramis@gmail.com
- Update to 1.25.23:
  * Test program build: include <unistd.h> instead of <sys/unistd.h>.
  1.25.22:
  * Abyss server: don't reject a request with colons in the host name (e.g. IPv6
  address form "[::1]") as invalid. This appears to be all that is required
  for Abyss to work on an IPv6 network, as long as the user binds the
  listening socket himself.
  1.25.21:
  * libxml2: fix memory leaks.
  * Server: fix method add failure when signature string contains "I" (for 64
    bit integer).
  1.25.20:
  * Client with Curl transport: fix bug which disables interruption unless you
    register a progress function for the transport. Introduced in 1.24.
  1.25.19:
  * Server: Fix crash when string value in parameter list contains invalid
    UTF-8. Broken in 1.18 (March 2006).
  1.25.18:
  * Build: fix build tree != source tree bug: no transport_config.mk. Broken in
    1.10 (March 2007).
  1.25.17:
  * Fix crash due to bogus memory free when xmlrpc_parse_value() fails. Broken
    in 1.07 (October 2006).
  1.25.16:
  * Install: fix install of man pages to wrong directory. Broken in 1.18 (March
    2009).
  * Build: Add a user-defined default constructor for class callInfo to avoid
    compilation failure with recent GNU compilers.
  1.25.15:
  * Abyss XML-RPC server: Fix bug in access control expiration.
  * xmlrpc, xmlrpc_pstream client programs: fix bug in display of unprintable
    ASCII as \xHH: shows \xff where it should be something else.
  1.25.14:
  * Windows Abyss: fix 16 byte per thread memory leak. Thanks Angelo Masci.
  1.25.13:
  * xmlrpc client program: fix bug: doesn't accept b/f to mean boolean false.
    Broken since 1.07.
  1.25.12:
  * Fix crash when sending structure with a member value too large. Introduced
    in 1.21.
  1.25.11:
  * Build with --disable-abyss-threads: include <sys/wait.h> instead of
    <wait.h> in Abyss thread_fork.c.
  1.25.10:
  * Fix bug: infinite loop parsing XML when a string or character data is
    longer than 1K in UTF-8. Introduced in 1.12.
  * Client curl transport: fix bug: multiple authentication methods doesn't
    work; only one of them takes effect. Always broken.
  1.25.09:
  * Curl client: fix libcurl version in user-agent header. Always broken
    (user-agent function added in Release 1.03).
  * C++ Curl client: fix bug: ignores proxy Curl transport options. Always
    broken.
  1.25.08:
  * Accomodate newer libcurl, which does not have <curl/types.h>.
  * Build of test programs: Fix "struct sockaddr_in" not defined in
    server_pstream.cpp.
  * Fix per-connection memory leak in libwww client XML transport. Present
    since the beginning.
- Removed xmlrpc-c-default-constructor.patch (fixed upstream).
- Removed xmlrpc-c-no-curltypes-incl.patch (fixed upstream).
- Updated license to "BSD-3-Clause and MIT".
- Removed autoconf, automake, file, libtool and libstdc++-devel build
  requirements (not needed).
- Added ncurses-devel and readline-devel build requirements.
- Removed support for openSUSE < 10.4.
- Renamed libxmlrpc-c-devel package to xmlrpc-c-devel. Added the necessary
  Provides/Obsoletes entries for libxmlrpc-c-devel.
- Remove static libraries.

* Tue Nov 22 2011 pascal.bleser@opensuse.org
- fix requires in -devel package
- remove Authors block from description

* Mon Nov 21 2011 jengelh@medozas.de
- Remove redundant/unwanted tags/section (cf. specfile guidelines)

* Mon Nov 21 2011 rschweikert@suse.com
- remove include of curl/types.h; file no longer exists and has been
  empty for a while

* Tue Jun 28 2011 appleonkel@opensuse.org
- update to 1.25.07
  * soname for cpp libs to 7
  * 3 new libraries (server_cgi++, server_pstream++, packetsocket)
- deleted old patches, looks like upstream had fixed it
- added fix for default constructor

* Sat Oct 30 2010 pascal.bleser@opensuse.org
- update to 1.06.41:
  * CGI XML-RPC server accepts (ignores) parameters after "text/xml" in Content-type header from client
- moved changelog entries from spec file to .changes file
- added patches to fix wrong usage of printf format for size_t (upstream uses llu instead of zu)

* Tue Aug 31 2010 chris@computersalat.de
- merge with hamradio/xmlrpc-c
  o there shouldn't be 2 maintained packages :(
- used Source from sourceforge.net
  o correct named: xmlrpc-c-1.06.40.tgz

* Thu Jul  8 2010 dl8fcl@darc.de
- imported fixes from pascal@links2linux.de
  * C++ bytesFromBase64(): fix bug: high two bits always zero.
    Broken since created (2005)
  * Abyss: terminate after current request, not current connection.
    (Matters with keepalive)
  * fix xmlrpc_inetd_server C++ example. It has never worked.
  * fix error message about invalid <int> XML

* Sun Dec 20 2009 dl8fcl@darc.de
- update to 1.06.38

* Mon Sep 28 2009 pascal.bleser@opensuse.org
- update to 1.06.37

* Sat May  9 2009 bitshuffler #suse@irc.freenode.org
- Updated to 1.06.33
  * Mon Aug  4 00:00:00 UTC 2008 - Peter Nixon
- Add xmlrpc-c-gcc43.patch from Gentoo project to placate newer GCC
  version on openSUSE 11.0
- Add Packager tag
- Update group for -devel package
- replace %%%%%%%%run_ldconfig with %%%%post(un) -p /sbin/ldconfig
  * Tue Jun 12 00:00:00 UTC 2007 - Peter Nixon
- Updated to 1.06.14
- Enabled all options
- Fixed 64bit build problems
  Tue Mar 14 00:00:00 UTC 2006 - Peter Nixon
- enabled abyss-server

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Thu Mar 18 2004 hvogel@suse.de
- fix files list

* Tue Mar 16 2004 kkaempf@suse.de
- initial package version 0.9.10
