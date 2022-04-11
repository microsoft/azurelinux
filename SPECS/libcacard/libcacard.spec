Summary:        CAC (Common Access Card) library
Name:           libcacard
Version:        2.7.0
Release:        11%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.freedesktop.org/spice/libcacard
Source0:        https://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz
# https://gitlab.freedesktop.org/spice/libcacard/merge_requests/5
Patch0:         %{name}-2.7.0-caching-keys.patch

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  gnupg2
BuildRequires:  gnutls-utils
BuildRequires:  pkgconfig(nss)
BuildRequires:  openssl
%if %{with_check}
BuildRequires:  nss-tools
BuildRequires:  softhsm
BuildRequires:  opensc
%endif

%description
This library provides emulation of smart cards to a virtual card
reader running in a guest virtual machine.

It implements DoD CAC standard with separate pki containers
(compatible coolkey), using certificates read from NSS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%check
sed -i "s!%{_lib64dir}/!%{_libdir}/!" tests/setup-softhsm2.sh
%make_build check

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libcacard.so.0
%{_libdir}/libcacard.so.0.*

%files devel
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc

%changelog
* Mon Mar 07 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.7.0-11
- Reverting removal of nss-tools BR for ptests.

* Tue Mar 01 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.7.0-10
- Switching to pkgconfig(nss) BR.

* Mon Feb 21 2022 Muhammad Falak <mwani@microsoft.com> - 2.7.0-9
- Add an explicit BR on `softhsm` & `opensc` to enable ptest

* Wed Dec 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.0-8
- Using CBL-Mariner RPM macros for "make".
- Removing unnecessary in-spec signature check.
- Removing unused BRs: 'lcov', 'opensc', and 'softhsm'.
- Using HTTPS for the source URL.
- License verified.

* Wed Dec 01 2021 Muhammad Falak <mwani@microsoft.com> - 2.7.0-7
- Remove conflicts with qemu

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.7.0-6
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3:2.7.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 29 2019 Jakub Jelen <jjelen@redhat.com> - 2.7.0-3
- Backport an upstream patch to unbreak testing

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Christophe Fergeau <cfergeau@redhat.com> - 2.6.1-1
- Update to new upstream release

* Wed Aug 08 2018 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.6.0-1
- Update to release v2.6.0
- remove vscclient, drop libcacard-tools

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.3-1
- new upstream release 2.5.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 08 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.2-1
- Update to latest libcacard's release (2.5.2)

* Wed Nov 25 2015 Fabiano Fidêncio <fidencio@redhat.com> - 3:2.5.1-1
- Update to latest libcacard's release (2.5.1)

* Wed Sep 23 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.0-1
- Initial standalone libcacard package.
