Vendor:         Microsoft Corporation
Distribution:   Azure Linux
###############################################################################
###############################################################################
##
##  Copyright (C) 2012-2019 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2 or higher
##
###############################################################################
###############################################################################

# set defaults from ./configure invocation
%bcond_without sctp
%bcond_without nss
%bcond_without openssl
%bcond_without zlib
%bcond_without lz4
%bcond_without lzo2
%bcond_without lzma
%bcond_without bzip2
%bcond_without zstd
%bcond_without libnozzle
%bcond_with runautogen
%bcond_with rpmdebuginfo
%bcond_with overriderpmdebuginfo
%bcond_without buildman
%bcond_with installtests

%if %{with overriderpmdebuginfo}
%undefine _enable_debug_packages
%endif

# main (empty) package
# https://www.rpm.org/max-rpm/s1-rpm-subpack-spec-file-changes.html

Name: kronosnet
Summary: Multipoint-to-Multipoint VPN daemon
Version: 1.20
Release: 2%{?dist}
License: GPLv2+ and LGPLv2+
URL: https://kronosnet.org
Source0: https://kronosnet.org/releases/%{name}-%{version}.tar.xz

# Build dependencies
BuildRequires: gcc libqb-devel
# required to build man pages
%if %{with buildman}
BuildRequires: libxml2-devel doxygen
%endif
%if %{with sctp}
BuildRequires: lksctp-tools-devel
%endif
%if %{with nss}
BuildRequires: nss-devel
%endif
%if %{with openssl}
BuildRequires: openssl-devel
%endif
%if %{with zlib}
BuildRequires: zlib-devel
%endif
%if %{with lz4}
BuildRequires: lz4-devel
%endif
%if %{with lzo2}
BuildRequires: lzo-devel
%endif
%if %{with lzma}
BuildRequires: xz-devel
%endif
%if %{with bzip2}
BuildRequires: bzip2-devel
%endif
%if %{with zstd}
BuildRequires: libzstd-devel
%endif
%if %{with libnozzle}
BuildRequires: libnl3-devel
%endif
%if %{with runautogen}
BuildRequires: autoconf automake libtool
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%if %{with runautogen}
./autogen.sh
%endif

%{configure} \
%if %{with installtests}
	--enable-install-tests \
%else
	--disable-install-tests \
%endif
%if %{with buildman}
	--enable-man \
%else
	--disable-man \
%endif
%if %{with sctp}
	--enable-libknet-sctp \
%else
	--disable-libknet-sctp \
%endif
%if %{with nss}
	--enable-crypto-nss \
%else
	--disable-crypto-nss \
%endif
%if %{with openssl}
	--enable-crypto-openssl \
%else
	--disable-crypto-openssl \
%endif
%if %{with zlib}
	--enable-compress-zlib \
%else
	--disable-compress-zlib \
%endif
%if %{with lz4}
	--enable-compress-lz4 \
%else
	--disable-compress-lz4 \
%endif
%if %{with lzo2}
	--enable-compress-lzo2 \
%else
	--disable-compress-lzo2 \
%endif
%if %{with lzma}
	--enable-compress-lzma \
%else
	--disable-compress-lzma \
%endif
%if %{with bzip2}
	--enable-compress-bzip2 \
%else
	--disable-compress-bzip2 \
%endif
%if %{with zstd}
	--enable-compress-zstd \
%else
	--disable-compress-zstd \
%endif
%if %{with libnozzle}
	--enable-libnozzle \
%else
	--disable-libnozzle \
%endif
	--with-initdefaultdir=%{_sysconfdir}/sysconfig/ \
	--with-systemddir=%{_unitdir}

make %{_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# tree cleanup
# remove static libraries
find %{buildroot} -name "*.a" -exec rm {} \;
# remove libtools leftovers
find %{buildroot} -name "*.la" -exec rm {} \;

# remove init scripts
rm -rf %{buildroot}/etc/init.d

# remove docs
rm -rf %{buildroot}/usr/share/doc/kronosnet

# main empty package
%description
 The kronosnet source

%if %{with libnozzle}
%package -n libnozzle1
Summary: Simple userland wrapper around kernel tap devices
License: LGPLv2+

%description -n libnozzle1
 This is an over-engineered commodity library to manage a pool
 of tap devices and provides the basic
 pre-up.d/up.d/down.d/post-down.d infrastructure.

%files -n libnozzle1
%license COPYING.* COPYRIGHT
%{_libdir}/libnozzle.so.*

%if 0%{?ldconfig_scriptlets}
%ldconfig_scriptlets -n libnozzle1
%else
%post -n libnozzle1 -p /sbin/ldconfig
%postun -n libnozzle1 -p /sbin/ldconfig
%endif

%package -n libnozzle1-devel
Summary: Simple userland wrapper around kernel tap devices (developer files)
License: LGPLv2+
Requires: libnozzle1%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libnozzle1-devel
 This is an over-engineered commodity library to manage a pool
 of tap devices and provides the basic
 pre-up.d/up.d/down.d/post-down.d infrastructure.

%files -n libnozzle1-devel
%license COPYING.* COPYRIGHT
%{_libdir}/libnozzle.so
%{_includedir}/libnozzle.h
%{_libdir}/pkgconfig/libnozzle.pc
%if %{with buildman}
%{_mandir}/man3/nozzle*.3.gz
%endif
%endif

%package -n libknet1
Summary: Kronosnet core switching implementation
License: LGPLv2+

%description -n libknet1
 The whole kronosnet core is implemented in this library.
 Please refer to the not-yet-existing documentation for further
 information.

%files -n libknet1
%license COPYING.* COPYRIGHT
%{_libdir}/libknet.so.*
%dir %{_libdir}/kronosnet

%if 0%{?ldconfig_scriptlets}
%ldconfig_scriptlets -n libknet1
%else
%post -n libknet1 -p /sbin/ldconfig
%postun -n libknet1 -p /sbin/ldconfig
%endif

%package -n libknet1-devel
Summary: Kronosnet core switching implementation (developer files)
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libknet1-devel
 The whole kronosnet core is implemented in this library.
 Please refer to the not-yet-existing documentation for further
 information. 

%files -n libknet1-devel
%license COPYING.* COPYRIGHT
%{_libdir}/libknet.so
%{_includedir}/libknet.h
%{_libdir}/pkgconfig/libknet.pc
%if %{with buildman}
%{_mandir}/man3/knet*.3.gz
%endif

%if %{with nss}
%package -n libknet1-crypto-nss-plugin
Summary: Provides libknet1 nss support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-crypto-nss-plugin
 Provides NSS crypto support for libknet1.

%files -n libknet1-crypto-nss-plugin
%{_libdir}/kronosnet/crypto_nss.so
%endif

%if %{with openssl}
%package -n libknet1-crypto-openssl-plugin
Summary: Provides libknet1 openssl support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-crypto-openssl-plugin
 Provides OpenSSL crypto support for libknet1.

%files -n libknet1-crypto-openssl-plugin
%{_libdir}/kronosnet/crypto_openssl.so
%endif

%if %{with zlib}
%package -n libknet1-compress-zlib-plugin
Summary: Provides libknet1 zlib support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-zlib-plugin
 Provides zlib compression support for libknet1.

%files -n libknet1-compress-zlib-plugin
%{_libdir}/kronosnet/compress_zlib.so
%endif

%if %{with lz4}
%package -n libknet1-compress-lz4-plugin
Summary: Provides libknet1 lz4 and lz4hc support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-lz4-plugin
 Provides lz4 and lz4hc compression support for libknet1.

%files -n libknet1-compress-lz4-plugin
%{_libdir}/kronosnet/compress_lz4.so
%{_libdir}/kronosnet/compress_lz4hc.so
%endif

%if %{with lzo2}
%package -n libknet1-compress-lzo2-plugin
Summary: Provides libknet1 lzo2 support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-lzo2-plugin
 Provides lzo2 compression support for libknet1.

%files -n libknet1-compress-lzo2-plugin
%{_libdir}/kronosnet/compress_lzo2.so
%endif

%if %{with lzma}
%package -n libknet1-compress-lzma-plugin
Summary: Provides libknet1 lzma support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-lzma-plugin
 Provides lzma compression support for libknet1.

%files -n libknet1-compress-lzma-plugin
%{_libdir}/kronosnet/compress_lzma.so
%endif

%if %{with bzip2}
%package -n libknet1-compress-bzip2-plugin
Summary: Provides libknet1 bzip2 support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-bzip2-plugin
 Provides bzip2 compression support for libknet1.

%files -n libknet1-compress-bzip2-plugin
%{_libdir}/kronosnet/compress_bzip2.so
%endif

%if %{with zstd}
%package -n libknet1-compress-zstd-plugin
Summary: Provides libknet1 zstd support
License: LGPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n libknet1-compress-zstd-plugin
 Provides zstd compression support for libknet1.

%files -n libknet1-compress-zstd-plugin
%{_libdir}/kronosnet/compress_zstd.so
%endif

%package -n libknet1-crypto-plugins-all
Summary: Provides libknet1 crypto plugins meta package
License: LGPLv2+
%if %{with nss}
Requires: libknet1-crypto-nss-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with openssl}
Requires: libknet1-crypto-openssl-plugin%{_isa} = %{version}-%{release}
%endif

%description -n libknet1-crypto-plugins-all
 Provides meta package to install all of libknet1 crypto plugins

%files -n libknet1-crypto-plugins-all

%package -n libknet1-compress-plugins-all
Summary: Provides libknet1 compress plugins meta package
License: LGPLv2+
%if %{with zlib}
Requires: libknet1-compress-zlib-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with lz4}
Requires: libknet1-compress-lz4-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with lzo2}
Requires: libknet1-compress-lzo2-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with lzma}
Requires: libknet1-compress-lzma-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with bzip2}
Requires: libknet1-compress-bzip2-plugin%{_isa} = %{version}-%{release}
%endif
%if %{with zstd}
Requires: libknet1-compress-zstd-plugin%{_isa} = %{version}-%{release}
%endif

%description -n libknet1-compress-plugins-all
 Meta package to install all of libknet1 compress plugins

%files -n libknet1-compress-plugins-all

%package -n libknet1-plugins-all
Summary: Provides libknet1 plugins meta package
License: LGPLv2+
Requires: libknet1-compress-plugins-all%{_isa} = %{version}-%{release}
Requires: libknet1-crypto-plugins-all%{_isa} = %{version}-%{release}

%description -n libknet1-plugins-all
 Meta package to install all of libknet1 plugins

%files -n libknet1-plugins-all

%if %{with installtests}
%package -n kronosnet-tests
Summary: Provides kronosnet test suite
License: GPLv2+
Requires: libknet1%{_isa} = %{version}-%{release}

%description -n kronosnet-tests
 This package contains all the libknet and libnozzle test suite.

%files -n kronosnet-tests
%{_libdir}/kronosnet/tests/*
%endif

%if %{with rpmdebuginfo}
%debug_package
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Oct 19 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.20-1
- New upstream release
- Fix TX/RX stats collections
- Minor test suite improvements
- Minor build fixes

* Mon Aug 17 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.19-1
- New upstream release
- Add native support for openssl 3.0 (drop API COMPAT macros).
- Code cleanup of public APIs. Lots of lines of code moved around, no
  functional changes.
- Removed kronosnetd unsupported code completely
- Removed unused poc-code from the source tree
- Make sure to initialize epoll events structures

* Tue Jul 14 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.18-1
- New upstream release
- Add ability to change crypto configuration at runtime without
  restarting knet and without packet drop
- Add compatibility support for openssl 3.0
- Add functional testing framework and new test cases
- Minor build fixes

* Thu Apr 23 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.16-1
- New upstream release
- Fix major issues with SCTP transport
- Fix build with recent gcc
- Minor bug fixes
- Update BuildRequires now that libqb is used unconditionally

* Wed Mar 04 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.15-1
- New upstream release
- Fix major interaction issues between stats gathering and PMTUd
- Fix UDP socket options that could lead to knet not being properly
  functional
- Man pages updates
- Minor bug fixes

* Fri Jan 31 2020 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.14-1
- New upstream release
- Fixes several major issues with newer kernels
- Fix build with gcc10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.13-1
- New upstream release
- Fixes more memory corruption problems on unstable networks.

* Fri Sep 20 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.12-1
- New upstream release
- Fixes memory corruption problem on unstable networks.

* Wed Aug 21 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.11-1
- New upstream release
- Fixes major issues with PMTUd implementation when used in combination with
  crypto.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.10-1
- New upstream release
- fix URL in spec file (rhbz#1708616)

* Thu May 09 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.9-1
- New upstream release

* Wed May 08 2019 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.8-2
- Fix ldconfig scriptlet (Resolves rhbz#1699074)
- Cleanup .gitignore (Resolves rhbz#1699093)

* Wed Apr 03 2019 Madison Kelly <mkelly@alteeve.ca> - 1.8-1
- Updated to upstream release v1.8.
