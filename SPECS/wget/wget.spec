%global somajor 2

Summary:        An advanced file and recursive website downloader
Name:           wget
Version:        2.1.0
Release:        1%{?dist}
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://gitlab.com/gnuwget/wget2
Group:          System Environment/NetworkingPrograms
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://ftp.gnu.org/gnu/wget/%{name}2-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0001:      0001-src-log.c-log_init-Redirect-INFO-logs-to-stderr-with.patch

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
make DESTDIR=%{buildroot} install
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

ln -sr %{buildroot}%{_bindir}/%{name}2 %{buildroot}%{_bindir}/wget
# Link wget(1) to wget2(1)
echo ".so man1/%{name}.1" > %{buildroot}%{_mandir}/man1/wget.1

%{_fixperms} %{buildroot}/*

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan HTTP::Daemon
make  %{?_smp_mflags} check

%files -f %{name}2.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

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
* Wed Feb 28 2024 Muhammad Falak <mwani@microsoft.com> - 2.1.0-1
- Switch wget from 1.x to 2.x
- Add a provides for wget
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
