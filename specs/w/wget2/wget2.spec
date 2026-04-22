# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/wget2.azl.macros}

%if (0%{?fedora} && 0%{?fedora} < 40) || (0%{?rhel} && 0%{?rhel} < 11)
%bcond as_wget 0
%else
%bcond as_wget 1
%endif

%global somajor 4

Name:           wget2
Version:        2.2.1
Release: 2%{?dist}
Summary:        An advanced file and recursive website downloader

# Documentation is GFDL
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://gitlab.com/gnuwget/wget2
Source0:        https://ftp.gnu.org/gnu/wget/%{name}-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/wget/%{name}-%{version}.tar.gz.sig
# key 08302DB6A2670428
Source2:        tim.ruehsen-keyring.asc
Source9999: wget2.azl.macros

# Buildsystem build requirements
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  flex-devel >= 2.5.35
BuildRequires:  gettext >= 0.18.2
BuildRequires:  gcc
BuildRequires:  make

# Documentation build requirements
BuildRequires:  doxygen
BuildRequires:  git-core
%if ! 0%{?rhel}
BuildRequires:  pandoc
%endif

# Wget2 build requirements
BuildRequires:  bzip2-devel
BuildRequires:  python3
BuildRequires:  rsync
BuildRequires:  tar
BuildRequires:  texinfo
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gpgme)
BuildRequires:  pkgconfig(libbrotlidec)
## Not available yet
#BuildRequires:  pkgconfig(libhsts)
BuildRequires:  pkgconfig(libidn2) >= 0.14.0
## Not available yet
#BuildRequires:  pkgconfig(liblz)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libmicrohttpd)
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libpsl)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(zlib)

%if ! 0%{?rhel}
# Test suite
BuildRequires:  lcov
BuildRequires:  lzip
%endif

# For gpg signature verification
BuildRequires:  gnupg2

Provides:       webclient
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

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

%if %{with as_wget}
%package wget
Summary:        %{name} shim to provide wget
Requires:       wget2%{?_isa} = %{version}-%{release}
# Replace wget1
Conflicts:      wget < 2
Provides:       wget = %{version}-%{release}
Provides:       wget%{?_isa} = %{version}-%{release}
# From original wget package
Provides:       webclient

%description wget
This package provides the shim links for %{name} to be automatically
used in place of wget. This ensures that %{name} is used as
the system provider of wget.
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git_am


%build
%configure --disable-static
%if ! 0%{?rhel}
# Remove RPATH, rely on default -Wl,--enable-new-dtags in Fedora.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif
%make_build


%install
%make_install
%find_lang %{name}

%if 0%{?rhel}
# tarball includes a pre-built manpage
install -D -m0644 -t %{buildroot}%{_mandir}/man1/ docs/man/man1/wget2.1
%endif

# Purge all libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

# Delete useless noinstall binary
rm -v %{buildroot}%{_bindir}/%{name}_noinstall

%if %{with as_wget}
ln -sr %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/wget
# Link wget(1) to wget2(1)
echo ".so man1/%{name}.1" > %{buildroot}%{_mandir}/man1/wget.1
%endif

%check
%make_build check


%files -f %{name}.lang
%license COPYING*
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%license COPYING*
%{_libdir}/libwget*.so.%{somajor}{,.*}

%files devel
%{_includedir}/wget.h
%{_includedir}/wgetver.h
%{_libdir}/libwget*.so
%{_libdir}/pkgconfig/libwget.pc
%{_mandir}/man3/libwget*.3*

%if %{with as_wget}
%files wget
%{_bindir}/wget
%{_mandir}/man1/wget.1*
%endif


%changelog
* Thu Jan 01 2026 LuK1337 <priv.luk@gmail.com> - 2.2.1-1
- New version 2.2.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 14 2025 Michal Ruprich <mruprich@redhat.com> - 2.2.0-5
- Removing Obsoletes so that wget2 can be replaced by wget1

* Fri Feb 28 2025 Neal Gompa <ngompa@fedoraproject.org> - 2.2.0-3
- Backport support for --show-progress flag
  Resolves: rhbz#2348997

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 02 2024 Michal Ruprich <mruprich@redhat.com> - 2.2.0-1
- New version 2.2.0
- Resolves: rhbz#2298879 - Using options -nc and -O simultaneously causes existing files to be clobbered/truncated
- Resolves: rhbz#2327788 - wget starts using non-working IPv6 addresses on dual stack
- Resolves: rhbz#2327728 - Crash: "free(): double free detected in tcache 2" when using --load-cookies
- Resolves: rhbz#2280151 - wget2 always re-downdloads when using custom output filename

* Fri Aug 09 2024 Jonathan Wright <jonathan@almalinux.org> - 2.1.0-13
- do not replace wget on el10

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Romain Geissler <romain.geissler@amadeus.com> - 2.1.0-11
- Disable TCP Fast Open by default

* Mon May 20 2024 Romain Geissler <romain.geissler@amadeus.com> - 2.1.0-10
- Disable explicit OCSP requests by default for privacy reasons.
- Accept --progress=dot:... for backwards compatibility.

* Sat May 11 2024 Romain Geissler <romain.geissler@amadeus.com> - 2.1.0-9
- Allow option --no-tcp-fastopen to work on Linux kernels >= 4.11.

* Tue Apr 02 2024 Michal Ruprich <mruprich@redhat.com> - 2.1.0-8
- Resolves: #2271362 - wget2 blacklists files intended for download

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 2.1.0-6
- Backport fix for wget to stdin
  Resolves: rhbz#2257700

* Thu Jan 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.0-5
- Drop unused autogen build dependency

* Thu Dec 21 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.0-4
- Avoid pandoc dependency on RHEL
- Fix tests on RHEL

* Sat Dec 16 2023 Neal Gompa <ngompa@fedoraproject.org> - 2.1.0-3
- Enable wget2-wget for F40+ / RHEL10+

* Fri Sep 01 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2.1.0-2
- Add gpg signature check

* Fri Sep 01 2023 Neal Gompa <ngompa@fedoraproject.org> - 2.1.0-1
- New upstream version
- Add conditional for using wget2 as wget

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Michal Ruprich <mruprich@redhat.com> - 2.0.0-5
- SPDX migration

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Sep 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.0.0-1
- Rebase to 2.0.0 final
- Split out libraries into libs subpackage
- Delete unwanted static subpackage

* Wed Apr  1 2020 Anna Khaitovich <akhaitov@redhat.com> - 1.99.2-1
- Initial package

