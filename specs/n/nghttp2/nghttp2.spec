# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_mingw 0

%if 0%{?fedora}
%global with_mingw 0
%endif

Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.66.0
Release: 3%{?dist}

# Parts of ruby bindings are additionally under GPL-2.0-or-later, MIT and
# HPND-Kevlin-Henney but they are NOT shipped.
License: MIT

URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
Source1: https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz.asc
Source2: tatsuhiro-t.pgp

BuildRequires: CUnit-devel
BuildRequires: c-ares-devel
BuildRequires: gcc-c++
BuildRequires: libev-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: systemd-rpm-macros
BuildRequires: zlib-devel

# For gpg verification of source tarball
BuildRequires: gnupg2

Requires: libnghttp2%{?_isa} = %{version}-%{release}
%{?systemd_requires}

%if %{with_mingw}
BuildRequires: mingw32-filesystem >= 107
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-c-ares
BuildRequires: mingw32-libxml2
BuildRequires: mingw32-openssl
BuildRequires: mingw32-python3
BuildRequires: mingw32-zlib

BuildRequires: mingw64-filesystem >= 107
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-binutils
BuildRequires: mingw64-c-ares
BuildRequires: mingw64-libxml2
BuildRequires: mingw64-openssl
BuildRequires: mingw64-python3
BuildRequires: mingw64-zlib
%endif

%description
This package contains the HTTP/2 client, server and proxy programs.


%package -n libnghttp2
Summary: A library implementing the HTTP/2 protocol

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Requires: libnghttp2%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.

%if %{with_mingw}
%package -n mingw32-libnghttp2
Summary: A library implementing the HTTP/2 protocol

%description -n mingw32-libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.

This is the MinGW cross-compiled Windows library.

%package -n mingw64-libnghttp2
Summary: A library implementing the HTTP/2 protocol

%description -n mingw64-libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.

This is the MinGW cross-compiled Windows library.

%{?mingw_debug_package}
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
mkdir build
pushd build
%define _configure ../configure
%configure PYTHON=%{__python3}              \
    --disable-hpack-tools                   \
    --disable-python-bindings               \
    --disable-static                        \
    --with-libxml2

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

%make_build
popd

%if %{with_mingw}
%mingw_configure --disable-hpack-tools --disable-static
%mingw_make_build
%endif


%install
pushd build
%make_install
install -D -m0444 -p contrib/nghttpx.service \
    "$RPM_BUILD_ROOT%{_unitdir}/nghttpx.service"
popd

# not needed on Fedora/RHEL
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

%ldconfig_scriptlets -n libnghttp2

%if %{with_mingw}
%mingw_make_install
%mingw_debug_install_post

rm -f "${buildroot}%{mingw32_libdir}/libnghttp2.la"
rm -f "${buildroot}%{mingw64_libdir}/libnghttp2.la"
rm -f "%{buildroot}%{mingw32_datadir}/doc/nghttp2/README.rst"
rm -f "%{buildroot}%{mingw64_datadir}/doc/nghttp2/README.rst"
rm -r "%{buildroot}%{mingw32_mandir}/man1"
rm -r "%{buildroot}%{mingw64_mandir}/man1"
%endif

%post
%systemd_post nghttpx.service

%postun
%systemd_postun nghttpx.service


%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH"
pushd build
%make_build check
popd

%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*
%{_unitdir}/nghttpx.service

%files -n libnghttp2
%{_libdir}/libnghttp2.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING

%files -n libnghttp2-devel
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/libnghttp2.pc
%{_libdir}/libnghttp2.so
%doc README.rst

%if %{with_mingw}
%files -n mingw32-libnghttp2
%license COPYING
%doc README.rst
%{mingw32_bindir}/libnghttp2-14.dll
%{mingw32_libdir}/libnghttp2.dll.a
%{mingw32_libdir}/pkgconfig/libnghttp2.pc
%{mingw32_includedir}/nghttp2/

%files -n mingw64-libnghttp2
%license COPYING
%doc README.rst
%{mingw64_bindir}/libnghttp2-14.dll
%{mingw64_libdir}/libnghttp2.dll.a
%{mingw64_libdir}/pkgconfig/libnghttp2.pc
%{mingw64_includedir}/nghttp2/
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.66.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Jan Macku <jamacku@redhat.com> - 1.66.0-1
- update to the latest upstream release

* Mon Mar 03 2025 Jan Macku <jamacku@redhat.com> - 1.65.0-1
- update to the latest upstream release

* Thu Jan 23 2025 Jan Macku <jamacku@redhat.com> - 1.64.0-3
- Fix FTBFS - munit: Remove-ATOMIC_UINT32_INIT

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.64.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Jan Macku <jamacku@redhat.com> 1.64.0-1
- update to the latest upstream release

* Tue Aug 27 2024 Jan Macku <jamacku@redhat.com> 1.63.0-1
- update to the latest upstream release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.62.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun May 19 2024 Packit <hello@packit.dev> - 1.62.1-1
- update to the latest upstream release

* Tue May 14 2024 Jan Macku <jamacku@redhat.com> 1.62.0-1
- update to the latest upstream release

* Thu Apr 04 2024 Jan Macku <jamacku@redhat.com> 1.61.0-1
- update to the latest upstream release
- fixes CVE-2024-28182 - HTTP/2 CONTINUATION frames can be utilized for DoS attacks

* Wed Mar 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.60.0-2
- Fix shebang of fetch-ocsp-response

* Mon Mar 04 2024 Jan Macku <jamacku@redhat.com> 1.60.0-1
- update to the latest upstream release
- update PGP key from https://keyserver.ubuntu.com/pks/lookup?op=vindex&search=0x7e8403d5d673c366

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.59.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Jan Macku <jamacku@redhat.com> 1.59.0-1
- update to the latest upstream release

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.58.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Jan Macku <jamacku@redhat.com> 1.58.0-1
- update to the latest upstream release

* Wed Oct 11 2023 Jan Macku <jamacku@redhat.com> 1.57.0-2
- fix mingw build

* Wed Oct 11 2023 Jan Macku <jamacku@redhat.com> 1.57.0-1
- update to the latest upstream release
- fixes CVE-2023-44487 - HTTP/2 Rapid Reset

* Fri Sep 15 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.56.0-2
- Add MinGW packages. rhbz#2102067

* Mon Sep 11 2023 Jan Macku <jamacku@redhat.com> 1.56.0-1
- update to the latest upstream release

* Mon Aug 07 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1.55.1-3
- migrate to SPDX license format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.55.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Jan Macku <jamacku@redhat.com> 1.55.1-1
- update to the latest upstream release
- fixes CVE-2023-35945 - memmory leak

* Thu Jul 13 2023 Jan Macku <jamacku@redhat.com> 1.55.0-1
- update to the latest upstream release

* Thu Jun 08 2023 Jan Macku <jamacku@redhat.com> 1.54.0-1
- update to the latest upstream release

* Thu May 11 2023 Kamil Dudka <kdudka@redhat.com> 1.53.0-1
- verify GPG signature of upstream tarball
- update to the latest upstream release

* Tue Feb 14 2023 Kamil Dudka <kdudka@redhat.com> 1.52.0-1
- update to the latest upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 15 2022 Kamil Dudka <kdudka@redhat.com> 1.51.0-1
- update to the latest upstream release

* Thu Sep 22 2022 Kamil Dudka <kdudka@redhat.com> 1.50.0-1
- update to the latest upstream release

* Tue Aug 23 2022 Kamil Dudka <kdudka@redhat.com> 1.49.0-1
- update to the latest upstream release

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Kamil Dudka <kdudka@redhat.com> 1.48.0-1
- update to the latest upstream release

* Fri Feb 25 2022 Kamil Dudka <kdudka@redhat.com> 1.47.0-1
- update to the latest upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 19 2021 Kamil Dudka <kdudka@redhat.com> 1.46.0-1
- update to the latest upstream release

* Tue Sep 21 2021 Kamil Dudka <kdudka@redhat.com> 1.45.1-1
- update to the latest upstream release

* Mon Sep 20 2021 Kamil Dudka <kdudka@redhat.com> 1.45.0-1
- update to the latest upstream release

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.44.0-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.44.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Kamil Dudka <kdudka@redhat.com> 1.44.0-1
- update to the latest upstream release

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.43.0-2
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Feb 02 2021 Kamil Dudka <kdudka@redhat.com> 1.43.0-1
- update to the latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Kamil Dudka <kdudka@redhat.com> 1.42.0-1
- update to the latest upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.41.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1.41.0-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 02 2020 Kamil Dudka <kdudka@redhat.com> 1.41.0-1
- update to the latest upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Kamil Dudka <kdudka@redhat.com> 1.40.0-1
- update to the latest upstream release

* Thu Nov 14 2019 Kamil Dudka <kdudka@redhat.com> 1.39.2-2
- enable use of libxml2 to make `nghttp --get-assets` work (#1772462)

* Wed Aug 14 2019 Kamil Dudka <kdudka@redhat.com> 1.39.2-1
- update to the latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Kamil Dudka <kdudka@redhat.com> 1.39.1-1
- update to the latest upstream release

* Tue Jun 11 2019 Kamil Dudka <kdudka@redhat.com> 1.39.0-1
- update to the latest upstream release

* Thu Apr 18 2019 Kamil Dudka <kdudka@redhat.com> 1.38.0-1
- update to the latest upstream release

* Fri Mar 08 2019 Kamil Dudka <kdudka@redhat.com> 1.37.0-1
- update to the latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Kamil Dudka <kdudka@redhat.com> 1.36.0-1
- update to the latest upstream release

* Mon Dec 10 2018 Kamil Dudka <kdudka@redhat.com> 1.35.1-1
- update to the latest upstream release

* Fri Nov 23 2018 Kamil Dudka <kdudka@redhat.com> 1.35.0-1
- update to the latest upstream release

* Thu Oct 04 2018 Kamil Dudka <kdudka@redhat.com> 1.34.0-1
- update to the latest upstream release

* Mon Sep 03 2018 Kamil Dudka <kdudka@redhat.com> 1.33.0-1
- use python3 for build
- update to the latest upstream release

* Mon Aug 27 2018 Kamil Dudka <kdudka@redhat.com> 1.32.1-1
- update to the latest upstream bugfix release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Kamil Dudka <kdudka@redhat.com> 1.32.0-1
- update to the latest upstream release

* Fri Apr 13 2018 Kamil Dudka <kdudka@redhat.com> 1.31.1-1
- update to the latest upstream release (fixes CVE-2018-1000168)

* Thu Mar 15 2018 Kamil Dudka <kdudka@redhat.com> 1.31.0-2
- make fetch-ocsp-response use Python 3

* Tue Feb 27 2018 Kamil Dudka <kdudka@redhat.com> 1.31.0-1
- update to the latest upstream release

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> 1.30.0-3
- add explicit BR for the gcc-c++ compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kamil Dudka <kdudka@redhat.com> 1.30.0-1
- update to the latest upstream release

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.29.0-2
- Switch to %%ldconfig_scriptlets

* Tue Dec 19 2017 Kamil Dudka <kdudka@redhat.com> 1.29.0-1
- update to the latest upstream release

* Sun Nov 26 2017 Kamil Dudka <kdudka@redhat.com> 1.28.0-1
- update to the latest upstream release

* Wed Oct 25 2017 Kamil Dudka <kdudka@redhat.com> 1.27.0-1
- update to the latest upstream release

* Wed Sep 20 2017 Kamil Dudka <kdudka@redhat.com> 1.26.0-1
- update to the latest upstream release

* Fri Aug 18 2017 Kamil Dudka <kdudka@redhat.com> 1.25.0-1
- update to the latest upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 1.24.0-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Kamil Dudka <kdudka@redhat.com> 1.24.0-2
- drop workaround for a GCC bug that has been fixed (#1358845)

* Sun Jul 02 2017 Kamil Dudka <kdudka@redhat.com> 1.24.0-1
- update to the latest upstream release

* Tue May 30 2017 Kamil Dudka <kdudka@redhat.com> 1.23.1-1
- update to the latest upstream release

* Sat May 27 2017 Kamil Dudka <kdudka@redhat.com> 1.23.0-1
- update to the latest upstream release

* Mon Apr 24 2017 Kamil Dudka <kdudka@redhat.com> 1.22.0-1
- update to the latest upstream release

* Mon Apr 10 2017 Kamil Dudka <kdudka@redhat.com> 1.21.1-1
- update to the latest upstream release

* Mon Mar 27 2017 Kamil Dudka <kdudka@redhat.com> 1.21.0-1
- update to the latest upstream release

* Sun Feb 26 2017 Tomasz Torcz <ttorcz@fedoraproject.org> - 1.20.0-1
- package systemd unit file (#1426929)
- update to latest upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Kamil Dudka <kdudka@redhat.com> 1.19.0-1
- update to the latest upstream release

* Thu Jan 05 2017 Kamil Dudka <kdudka@redhat.com> 1.18.1-1
- update to the latest upstream release

* Tue Dec 27 2016 Kamil Dudka <kdudka@redhat.com> 1.18.0-1
- update to the latest upstream release (requires c-ares for apps)

* Mon Nov 28 2016 Kamil Dudka <kdudka@redhat.com> 1.17.0-1
- update to the latest upstream release

* Tue Nov 15 2016 Kamil Dudka <kdudka@redhat.com> 1.16.1-1
- update to the latest upstream release

* Mon Oct 24 2016 Kamil Dudka <kdudka@redhat.com> 1.16.0-1
- update to the latest upstream release

* Mon Sep 26 2016 Kamil Dudka <kdudka@redhat.com> 1.15.0-1
- update to the latest upstream release

* Mon Sep 12 2016 Kamil Dudka <kdudka@redhat.com> 1.14.1-1
- update to the latest upstream release

* Thu Aug 25 2016 Kamil Dudka <kdudka@redhat.com> 1.14.0-1
- update to the latest upstream release

* Tue Jul 26 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-2
- prevent nghttpx from crashing on armv7hl (#1358845)

* Thu Jul 21 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-1
- update to the latest upstream release

* Mon Jun 27 2016 Kamil Dudka <kdudka@redhat.com> 1.12.0-1
- update to the latest upstream release

* Sun May 29 2016 Kamil Dudka <kdudka@redhat.com> 1.11.1-1
- update to the latest upstream release

* Thu May 26 2016 Kamil Dudka <kdudka@redhat.com> 1.11.0-1
- update to the latest upstream release

* Mon Apr 25 2016 Kamil Dudka <kdudka@redhat.com> 1.10.0-1
- update to the latest upstream release

* Sun Apr 03 2016 Kamil Dudka <kdudka@redhat.com> 1.9.2-1
- update to the latest upstream release

* Tue Mar 29 2016 Kamil Dudka <kdudka@redhat.com> 1.9.1-1
- update to the latest upstream release

* Thu Feb 25 2016 Kamil Dudka <kdudka@redhat.com> 1.8.0-1
- update to the latest upstream release

* Thu Feb 11 2016 Kamil Dudka <kdudka@redhat.com> 1.7.1-1
- update to the latest upstream release (fixes CVE-2016-1544)

* Fri Feb 05 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-3
- make the package compile with gcc-6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-1
- update to the latest upstream release

* Fri Dec 25 2015 Kamil Dudka <kdudka@redhat.com> 1.6.0-1
- update to the latest upstream release (fixes CVE-2015-8659)

* Thu Nov 26 2015 Kamil Dudka <kdudka@redhat.com> 1.5.0-1
- update to the latest upstream release

* Mon Oct 26 2015 Kamil Dudka <kdudka@redhat.com> 1.4.0-1
- update to the latest upstream release

* Thu Sep 24 2015 Kamil Dudka <kdudka@redhat.com> 1.3.4-1
- update to the latest upstream release

* Wed Sep 23 2015 Kamil Dudka <kdudka@redhat.com> 1.3.3-1
- update to the latest upstream release

* Wed Sep 16 2015 Kamil Dudka <kdudka@redhat.com> 1.3.2-1
- update to the latest upstream release

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> 1.3.1-1
- update to the latest upstream release

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> 1.3.0-1
- update to the latest upstream release

* Mon Aug 17 2015 Kamil Dudka <kdudka@redhat.com> 1.2.1-1
- update to the latest upstream release

* Sun Aug 09 2015 Kamil Dudka <kdudka@redhat.com> 1.2.0-1
- update to the latest upstream release

* Wed Jul 15 2015 Kamil Dudka <kdudka@redhat.com> 1.1.1-1
- update to the latest upstream release

* Tue Jun 30 2015 Kamil Dudka <kdudka@redhat.com> 1.0.5-1
- packaged for Fedora (#1237247)
