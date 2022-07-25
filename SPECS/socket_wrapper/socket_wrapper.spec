Name:           socket_wrapper
Version:        1.2.4
Release:        2%{?dist}

License:        BSD
Summary:        A library passing all socket communications through Unix sockets
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz
Source1:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz.asc
Source2:        socket_wrapper.keyring

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libcmocka-devel >= 1.1.0

Recommends:     cmake
Recommends:     pkgconfig

%description
socket_wrapper aims to help client/server software development teams willing to
gain full functional test coverage. It makes it possible to run several
instances of the full software stack on the same machine and perform locally
functional testing of complex network configurations.

To use it set the following environment variables:

LD_PRELOAD=libsocket_wrapper.so
SOCKET_WRAPPER_DIR=/path/to/swrap_dir

This package doesn't have a devel package because this project is for
development/testing.

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1

%build
if test ! -e "obj"; then
mkdir obj
fi
pushd obj
%cmake \
-DUNIT_TESTING=ON \
%{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd

%ldconfig_scriptlets

%check
pushd obj
ctest --output-on-failure

LD_PRELOAD=src/libsocket_wrapper.so bash -c '>/dev/null'

popd

%files
%doc AUTHORS README.md CHANGELOG
%license LICENSE
%{_libdir}/libsocket_wrapper.so*
%dir %{_libdir}/cmake/socket_wrapper
%{_libdir}/cmake/socket_wrapper/socket_wrapper-config-version.cmake
%{_libdir}/cmake/socket_wrapper/socket_wrapper-config.cmake
%{_libdir}/pkgconfig/socket_wrapper.pc
%{_mandir}/man1/socket_wrapper.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 24 2020 Andreas Schneider <asn@redhat.com> - 1.2.4-1
- Update to version 1.2.4
  * https://gitlab.com/cwrap/socket_wrapper/-/blob/master/CHANGELOG

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Andreas Schneider <asn@redhat.com> - 1.2.3-1
- Update to version 1.2.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Andreas Schneider <asn@redhat.com> - 1.2.1-1
- Update to version 1.2.1
  * Removed error message to fix applications doing stupid things

* Tue Nov 13 2018 Andreas Schneider <asn@redhat.com> - 1.2.0-1
- Update to vesrion 1.2.0
  * Added threading support
  * Moved to modern cmake
  * Several smaller bugfixes

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Andreas Schneider <asn@redhat.com> - 1.1.9-1
- Update to version 1.1.9
  * Fix thread deadlock with due to a signal interrupt

* Fri Oct 13 2017 Andreas Schneider <asn@redhat.com> - 1.1.8-1
- Update to version 1.1.8
  * Added support for openat()
  * Added support for open64() and fopen64()
  * Always enabled logging support
  * Increased maximum for wrapped interfaces to 64
  * Improved fd duplication code
  * Fixed strict-aliasing issues
  * Fixed some use after free issues
  * Fixed issues on ppc64le

* Wed Aug 02 2017 Andreas Schneider <asn@redhat.com> - 1.1.7-4
- resolves: #1465147 - Fix socket_wrapper on ppc64le

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 02 2016 Andreas Schneider <asn@redhat.com> - 1.1.7-1
- Update to version 1.1.7
  * Added support for accept4()
  * Added support for OpenBSD
  * Fixed sendto() with UDP and a connected socket
  * Fixed AF_RAWLINK sockets

* Wed Mar 23 2016 Andreas Schneider <asn@redhat.com> - 1.1.6-1
- Update to version 1.1.6
  * Added a wrapper for write()
  * Added support for automatic binding of ephemeral ports
  * Fixed recvmsg() with UDP
  * Fixed AF_NETLINK sockets

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Andreas Schneider <asn@redhat.com> - 1.1.5-1
- Update to version 1.1.5
  o Added support for TCP_NODELAY in setsockopt/getsockopt
  o Fixed cmsg space calculation

* Thu Sep 03 2015 Andreas Schneider <asn@redhat.com> - 1.1.4-1
- Update to version 1.1.4
  o Fixed handling of msg_name in recvmsg()
  o Fixed sendmsg()/recvmsg() TCP support
  o Fixed several compile warnings
  o Added environment variable to change MTU

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3.
  o Added support for address sanitizer.
  o Fixed leaking of memory and fds of stale sockets.
  o Fixed the library loading code.

* Mon Dec 15 2014 Michael Adam <madam@redhat.com> - 1.1.2-2
- Fix format of changelog entries.
- Require cmake.
- Require pkgconfig instead of owning {_libdir}/pkgconfig

* Fri Dec 12 2014 Michael Adam <madam@redhat.com> - 1.1.2-2
- Fix typos.

* Wed Oct 01 2014 Andreas Schneider <asn@redhat.com> - 1.1.2-1
- Update to version 1.1.2.

* Wed Oct 01 2014 Andreas Schneider <asn@redhat.com> - 1.1.1-2
- resolves: #1146409 - Do not own /usr/lib64/cmake

* Tue Sep 09 2014 Andreas Schneider <asn@redhat.com> - 1.1.1-1
- Update to version 1.1.1.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Andreas Schneider <asn@redhat.com> - 1.1.0-1
- Update to version 1.1.0.

* Tue May 06 2014 Andreas Schneider <asn@redhat.com> - 1.0.2-1
- Update to version 1.0.2.

* Tue Feb 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-3
- Remove Group
- Remove glibc-devel build requirement
- Do not create a subpackage.

* Tue Feb 04 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-2
- Fixed a typo.

* Tue Feb 04 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-1
- Update to version 1.0.1
  * Added --libs to pkg-config.
  * Added socket_wrapper-config.cmake
  * Fixed a bug packaging the obj directory.

* Mon Feb 03 2014 Andreas Schneider <asn@redhat.com> - 1.0.0-1
- Initial version 1.0.0
