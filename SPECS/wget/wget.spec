%global somajor 2

Summary:        An advanced file and recursive website downloader
Name:           wget
Version:        2.1.0
Release:        7%{?dist}
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://gitlab.com/gnuwget/wget2
Group:          System Environment/NetworkingPrograms
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://ftp.gnu.org/gnu/wget/%{name}2-%{version}.tar.gz#/%{name}-%{version}.tar.gz
## Fix behavior for downloading to stdin (rhbz#2257700, gl#gnuwget/wget2#651)
Patch0001:      0001-src-log.c-log_init-Redirect-INFO-logs-to-stderr-with.patch
## Fix normalization of path part of URL (rhbz#2271362)
Patch0002:      0002-normalize-path-in-url.patch
# https://github.com/rockdaboot/wget2/pull/316
# Allow option --no-tcp-fastopen to work on Linux kernels >= 4.11
Patch0003:      0003-Allow-option-no-tcp-fastopen-to-work-on-Linux-kernel.patch
# https://gitlab.com/gnuwget/wget2/-/issues/664
# Disable explicit OCSP requests by default for privacy reasons.
Patch0004:      0004-Disable-OCSP-by-default.patch
# https://gitlab.com/gnuwget/wget2/-/issues/661
# Accept --progress=dot:... for backwards compatibility
Patch0005:      0005-Accept-progress-dot-.-for-backwards-compatibility.patch
# https://gitlab.com/gnuwget/wget2/-/commit/7a945d31aeb34fc73cf86a494673ae97e069d84d
# Disable TCP Fast Open by default
# rhbz#2291017
Patch0006:      0006-Disable-TCP-Fast-Open-by-default.patch
# https://github.com/rockdaboot/wget2/issues/342
Patch0007:      fix-ssl-read-and-write-error-check.patch
# https://github.com/rockdaboot/wget2/issues/344
Patch0008:      set-debug_skip_body-for-OCSP-requests-in-openssl-tls-provider.patch
Patch9:      CVE-2025-69194.patch
Patch10:     CVE-2025-69195.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  doxygen
BuildRequires:  flex-devel >= 2.5.35
BuildRequires:  gcc
BuildRequires:  gettext >= 0.18.2
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gpgme)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3
BuildRequires:  tar
BuildRequires:  texinfo
%if 0%{?with_check}
BuildRequires:  perl
# wget test fails to find libwget.so.2, this BuildRequires fixes the issue
# Due to azl using hydrated builds for testing, the circular dependency is OK
# for testing
BuildRequires:  %{name}-libs%{?_isa} = %{version}-%{release}
%endif

Provides:       webclient
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       openssl


%description
GNU Wget2 is the successor of GNU Wget, a file and recursive website
downloader.

Designed and written from scratch it wraps around libwget, that provides the
basic functions needed by a web client.

Wget2 works multi-threaded and uses many features to allow fast operation.
In many cases Wget2 downloads much faster than Wget1.x due to HTTP2, HTTP
compression, parallel connections and use of If-Modified-Since HTTP header.

%package libs
Summary:        Runtime libraries for GNU Wget2
# There's some gnulib in there :)
Provides:       bundled(gnulib)

%description libs
This package contains the libraries for applications to use
Wget2 functionality.

%package devel
Summary:        Libraries and header files needed for using wget2 libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers needed for building applications to
use functionality from GNU Wget2.

%prep
%autosetup -p1 -n %{name}2-%{version}

%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --with-ssl=openssl \
    --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build



%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
%make_install
install -vdm 755 %{buildroot}/etc
cat >> %{buildroot}/etc/wgetrc <<-EOF
#   default root certs location
    ca_certificate=/etc/pki/tls/certs/ca-bundle.trust.crt
    ca_directory = /etc/ssl/certs
EOF
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}2
install -D -m0644 -t %{buildroot}%{_mandir}/man1/ docs/man/man1/wget2.1

find %{buildroot} -type f -name "*.la" -delete -print

# Delete useless noinstall binary
rm -v %{buildroot}%{_bindir}/%{name}2_noinstall

ln -sr %{buildroot}%{_bindir}/%{name}2 %{buildroot}%{_bindir}/wget
# Link wget(1) to wget2(1)
echo ".so man1/%{name}.1" > %{buildroot}%{_mandir}/man1/wget.1

%{_fixperms} %{buildroot}/*

%check
%make_build check

%files -f %{name}2.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%license COPYING*
%{_libdir}/libwget*.so.%{somajor}{,.*}

%files devel
%{_includedir}/wget.h
%{_includedir}/wgetver.h
%{_libdir}/libwget*.so
%{_libdir}/pkgconfig/libwget.pc
%{_mandir}/man3/libwget*.3*

%changelog
* Mon Jan 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.1.0-7
- Patch for CVE-2025-69194, CVE-2025-69195

* Mon Feb 24 2025 Sam Meluch <sammeluch@microsoft.com> - 2.1.0-6
- Add %check section from Fedora upstream.

* Mon Sep 23 2024 Tobias Brick <tobiasb@microsoft.com> - 2.1.0-5
- Align fix for SSL read and write error check with upstream.

* Wed Sep 18 2024 Tobias Brick <tobiasb@microsoft.com> - 2.1.0-4
- Add patch to prevent debug output from printing binary request bodies.

* Fri Sep 13 2024 Tobias Brick <tobiasb@microsoft.com> - 2.1.0-3
- Add patch to fix SSL read and write error check.

* Thu Sep 12 2024 Tobias Brick <tobiasb@microsoft.com> - 2.1.0-2
- Add patches from Fedora upstream. Important ones include disabling OCSP and TCP Fast Open by default.
- Don't install wget2_noinstall binary, which is specifically for testing.
- Fix rpmbuild warnings.

* Wed Feb 28 2024 Muhammad Falak <mwani@microsoft.com> - 2.1.0-1
- Switch wget from 1.x to 2.x
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License Verified

* Wed Jan 26 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.21.2-1
- Update to version 1.21.2.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.3-4
- Removing the explicit %%clean stage.

* Fri Nov 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.3-3
- Adding 'local::lib' perl5 library to fix test dependencies.

* Wed Oct 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.20.3-2
- Updating certificate bundle path to include full set of trust information.

* Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> 1.20.3-1
- Update to version 1.20.3 to resolve CVE-2019-5953.
- Use https for URL.
- License verified.
- Remove sha1 macro.
- Fix macro in changelog.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.19.5-4
- Added %%license line automatically

* Fri May 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.19.5-3
- Removing *Requires for "ca-certificates".
- Adding "ca_directory" to wget's configuration.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.19.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.19.5-1
- Updated to latest version

* Tue Dec 19 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-4
- Fix CVE-2017-6508

* Mon Nov 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-3
- Fix CVE-2017-13089 and CVE-2017-13090

* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.19.1-2
- Install HTTP::Daemon perl module for the tests to pass.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-1
- Updated to version 1.19.1.

* Tue Nov 29 2016 Anish Swaminathan <anishs@vmware.com>  1.18-1
- Upgrade wget versions - fixes CVE-2016-7098

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.17.1-3
- Modified %%check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.17.1-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.17.1-1
- Upgrade version

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
- Initial build.  First version
